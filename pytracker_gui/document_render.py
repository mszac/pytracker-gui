"""Small native-Tk documentation formatter, for local Markdown and reStructuredText.

Intentionally *not* a full CommonMark/Sphinx renderer. No HTML engine, asset loads,
network, external packages or background work. Work happens only when a user
selects a local file; the caller limits file size beforehand.
"""
import re

from .theme import COLORS

_RST_RULES = frozenset('=-~^"`:+*#')
_MARKDOWN_HEADER = re.compile(r'^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$')
_BULLET = re.compile(r'^\s*(?:[-*+]\s+|\d+[.)]\s+)')
_INLINE = re.compile(r'(`[^`\n]+`|\*\*[^*\n]+\*\*|\*[^*\n]+\*)')


def configure_document_tags(widget):
    """One-time style declaration; reuse one native Text widget for all files."""
    widget.tag_configure('doc_h1', font=('TkDefaultFont', 15, 'bold'),
                         foreground=COLORS['accent'], spacing1=12, spacing3=7)
    widget.tag_configure('doc_h2', font=('TkDefaultFont', 12, 'bold'),
                         foreground=COLORS['text'], spacing1=10, spacing3=5)
    widget.tag_configure('doc_h3', font=('TkDefaultFont', 11, 'bold'),
                         foreground=COLORS['muted'], spacing1=8, spacing3=3)
    widget.tag_configure('doc_body', font=('TkDefaultFont', 10), spacing3=3)
    widget.tag_configure('doc_bullet', lmargin1=15, lmargin2=30, spacing3=4)
    widget.tag_configure('doc_quote', foreground=COLORS['muted'], lmargin1=22, lmargin2=22)
    widget.tag_configure('doc_code', font=('TkFixedFont', 10),
                         foreground=COLORS['success'], lmargin1=18, lmargin2=18)
    widget.tag_configure('doc_bold', font=('TkDefaultFont', 10, 'bold'))
    widget.tag_configure('doc_emph', font=('TkDefaultFont', 10, 'italic'))
    widget.tag_configure('doc_rule', foreground=COLORS['border'])


def _inline_text(widget, raw, base='doc_body'):
    """Highlight a few inline conventions without parsing links or running code."""
    pos = 0
    for match in _INLINE.finditer(raw):
        if match.start() > pos:
            widget.insert('end', raw[pos:match.start()], base)
        item = match.group()
        if item.startswith('`'):
            widget.insert('end', item[1:-1], 'doc_code')
        elif item.startswith('**'):
            widget.insert('end', item[2:-2], 'doc_bold')
        else:
            widget.insert('end', item[1:-1], 'doc_emph')
        pos = match.end()
    if pos < len(raw):
        widget.insert('end', raw[pos:], base)


def render_document(widget, source, kind):
    """Render safe plain-text styles for one selected .md or .rst file.

    The renderer deliberately does not resolve relative images/links, use Sphinx,
    launch a browser, or interpret directives/HTML.
    """
    widget.configure(state='normal')
    widget.delete('1.0', 'end')
    # Very large documents deliberately bypass per-line styling to keep Tk responsive.
    if len(source) > 256 * 1024:
        widget.insert('end', source)
        widget.configure(state='disabled')
        widget.yview_moveto(0)
        return
    lines = source.splitlines()
    fenced = False
    rst_code = False
    idx = 0
    while idx < len(lines):
        raw = lines[idx]
        trimmed = raw.strip()
        if kind == 'md':
            if trimmed.startswith('```') or trimmed.startswith('~~~'):
                fenced = not fenced
                idx += 1
                continue
            if fenced:
                widget.insert('end', raw + '\n', 'doc_code')
                idx += 1
                continue
            header = _MARKDOWN_HEADER.match(raw)
            if header:
                level = len(header.group(1))
                widget.insert('end', header.group(2) + '\n',
                              'doc_h1' if level == 1 else ('doc_h2' if level == 2 else 'doc_h3'))
            elif trimmed in ('---', '***', '___'):
                widget.insert('end', '────────────────────────\n', 'doc_rule')
            elif raw.lstrip().startswith('>'):
                _inline_text(widget, raw.lstrip()[1:].lstrip(), 'doc_quote')
                widget.insert('end', '\n', 'doc_quote')
            elif _BULLET.match(raw):
                _inline_text(widget, raw.strip(), 'doc_bullet')
                widget.insert('end', '\n', 'doc_bullet')
            else:
                _inline_text(widget, raw, 'doc_body')
                widget.insert('end', '\n', 'doc_body')
        else:
            # RST setext headings: the underline is represented by heading style.
            if trimmed and idx + 1 < len(lines):
                rule = lines[idx + 1].strip()
                if rule and len(rule) >= len(trimmed) and len(set(rule)) == 1 and rule[0] in _RST_RULES:
                    style = 'doc_h1' if rule[0] in '=\u0023' else 'doc_h2'
                    widget.insert('end', trimmed + '\n', style)
                    idx += 2
                    continue
            if raw.startswith('    ') and rst_code:
                widget.insert('end', raw.strip('\n') + '\n', 'doc_code')
            elif trimmed.startswith('.. ') or trimmed.startswith(':'):
                widget.insert('end', raw + '\n', 'doc_code')
            elif _BULLET.match(raw):
                _inline_text(widget, raw, 'doc_bullet')
                widget.insert('end', '\n', 'doc_bullet')
            else:
                _inline_text(widget, raw, 'doc_body')
                widget.insert('end', '\n', 'doc_body')
            if trimmed.endswith('::'):
                rst_code = True
            elif trimmed and not raw.startswith('    '):
                rst_code = False
        idx += 1
    widget.configure(state='disabled')
    widget.yview_moveto(0)
