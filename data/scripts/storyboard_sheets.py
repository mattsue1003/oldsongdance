import email,io,json,os,sys
from PIL import Image,ImageDraw,ImageFont
d=json.load(open('/Users/matt/Claude/教案/oldsongdance/data/final.json'))
if len(sys.argv)>2: d=json.load(open(sys.argv[2]))  # optional alternate list
F=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',26)
meta={}
for l in open('hi/meta.txt'):
    p=l.split()
    if len(p)==5 and p[1]!='NA': meta[p[0]]=tuple(int(float(v)) for v in p[1:])
N=8;TW,TH=240,135
def frames(u):
    p=f'hi/{u}.mhtml'
    if not os.path.exists(p) or u not in meta: return None
    w,h,rows,cols=meta[u]
    tiles=[]
    m=email.message_from_bytes(open(p,'rb').read())
    for part in m.walk():
        if not part.get_content_type().startswith('image'): continue
        im=Image.open(io.BytesIO(part.get_payload(decode=True))).convert('RGB')
        for r in range(im.height//h):
            for c in range(im.width//w):
                t=im.crop((c*w,r*h,c*w+w,r*h+h))
                if t.convert('L').resize((1,1)).getpixel((0,0))>8: tiles.append(t)
    if not tiles: return None
    n=len(tiles); return [tiles[min(int((i+0.5)*n/N),n-1)] for i in range(N)]
def fit(t):
    t=t.copy(); t.thumbnail((TW,TH)); bg=Image.new('RGB',(TW,TH),'black'); bg.paste(t,((TW-t.width)//2,(TH-t.height)//2)); return bg
out=sys.argv[1]; os.makedirs(out,exist_ok=True)
ok=[(i,x,f) for i,x in enumerate(d) for f in [frames(x['u'])] if f]
print('ok',len(ok),'of',len(d))
PER=6;LW=80
for s in range(0,len(ok),PER):
    g=ok[s:s+PER]; sh=Image.new('RGB',(LW+N*TW,len(g)*(TH+6)),'white'); dr=ImageDraw.Draw(sh)
    for k,(i,x,fr) in enumerate(g):
        y=k*(TH+6); dr.text((8,y+50),str(i),fill='black',font=F)
        for j,t in enumerate(fr): sh.paste(fit(t),(LW+j*TW,y))
    sh.save(f'{out}/s{s//PER:02d}.jpg',quality=82)
