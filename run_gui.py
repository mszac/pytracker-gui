"""GUI entry point; layout preflight can run without Tk, PsychoPy or YAML."""
import argparse
import sys
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description='pytracker-gui, konfigurator istniejących dem')
    parser.add_argument('--check-layout', action='store_true', help='sprawdź zagnieżdżone repozytoria bez GUI')
    args = parser.parse_args(argv)
    if args.check_layout:
        from pytracker_gui.layout import format_layout_report
        report, ok = format_layout_report(Path(__file__).resolve().parent)
        print(report)
        return 0 if ok else 2
    from pytracker_gui.app import main as gui_main
    gui_main()
    return 0


if __name__ == '__main__':
    sys.exit(main())
