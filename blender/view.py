import sys
from PIL import Image
fs=sys.argv[2:]; ims=[Image.open(f) for f in fs]
sc=float(sys.argv[1])
ims=[i.resize((int(i.width*sc),int(i.height*sc))) for i in ims]
W=sum(i.width for i in ims)+20*(len(ims)+1); H=max(i.height for i in ims)+40
bg=Image.new('RGBA',(W,H),(20,110,160,255)); x=20
for i in ims: bg.alpha_composite(i,(x,20)); x+=i.width+20
bg.convert('RGB').save('/tmp/view.png')
