"""Build-only icon rasterizer. Optional Pillow is NOT needed to run the GUI."""
from PIL import Image, ImageDraw
from pathlib import Path
out=Path(__file__).resolve().parents[1] / 'pytracker_gui' / 'assets'
out.mkdir(exist_ok=True)
DARK='#a9b6c4';ORANGE='#ff9d45'

def art(d,n,c):
  w=2.6
  def line(points):d.line(points, fill=c,width=3,joint='curve')
  def box(coords):d.rounded_rectangle(coords, radius=3,outline=c,width=3)
  if n=='experiment':
    line([(23,6),(23,20),(15,35),(15,40),(33,40),(33,35),(25,20),(25,6)])
    line([(18,6),(30,6)]);line([(18,33),(30,33)])
  elif n=='logs': box((13,7,34,40));line([(18,17),(29,17)]);line([(18,24),(29,24)]);line([(18,31),(27,31)])
  elif n=='diagnostics':line([(6,25),(15,25),(20,14),(27,34),(33,20),(38,25),(43,25)])
  elif n=='statistics':
    for x,y in [(10,29),(21,19),(32,10)]:d.rounded_rectangle((x,y,x+7,40),radius=1,fill=c)
  elif n=='data':
    for yy in [14,23,32]:d.ellipse((10,yy-6,38,yy+3),outline=c,width=3)
  elif n=='monitor':box((7,9,41,34));line([(24,35),(24,42)]);line([(16,42),(32,42)])
  elif n=='appearance':
    d.ellipse((7,7,41,41),outline=c,width=3)
    for x,y in [(16,19),(24,13),(33,20)]:d.ellipse((x-2,y-2,x+2,y+2),fill=c)
    d.ellipse((24,30,30,36),outline=c,width=2)
  elif n=='instructions':box((13,7,35,41));line([(18,18),(29,18)]);line([(18,25),(29,25)]);line([(18,32),(28,32)])
  elif n=='yaml':line([(20,12),(10,24),(20,36)]);line([(28,12),(38,24),(28,36)])
  elif n=='launch':d.polygon([(16,9),(39,24),(16,39)],outline=c);line([(16,9),(39,24),(16,39),(16,9)])
  elif n=='save':box((9,8,39,40));d.rectangle((16,8,34,19),fill=c);d.rectangle((15,29,33,40),outline=c,width=3)
  elif n=='check':line([(8,24),(19,35),(40,12)])
  elif n=='folder':
    d.rounded_rectangle((6,15,42,37),radius=3,outline=c,width=3);line([(8,16),(8,11),(19,11),(23,15)])
  elif n=='stop':d.rounded_rectangle((12,12,36,36),radius=3,fill=c)
  elif n=='reset':d.arc((10,10,39,39),20,320,fill=c,width=3);line([(9,12),(9,24),(21,20)])
  elif n=='export':line([(24,8),(24,31)]);line([(14,21),(24,31),(34,21)]);line([(9,35),(9,41),(39,41),(39,35)])
  else: raise ValueError(n)
for name in ['experiment','logs','diagnostics','statistics','data','monitor','appearance','instructions','yaml','launch','save','check','folder','stop','reset','export']:
  for suffix,color in [('muted',DARK),('orange',ORANGE),('ink','#131820')]:
    im=Image.new('RGBA',(48,48),(0,0,0,0));d=ImageDraw.Draw(im);art(d,name,color)
    im.resize((28,28),Image.Resampling.LANCZOS).save(out/f'{name}-{suffix}.png',optimize=True)
print(len(list(out.glob('*.png'))), 'PNG',sum(f.stat().st_size for f in out.glob('*.png')),'bytes')
