# Domborzati árnyékolás (v176): Terrain Tiles (Mapzen/AWS, terrarium, z8) → LAEA-rács (1,5 km/px) → árnyékolt átlátszó WebP
# + kisebb felbontású magassági rács (5 km) későbbi menetszámításhoz (data/agg/elev5km.npz).
import numpy as np, math, os, glob
from PIL import Image
from pyproj import Transformer
from scipy.ndimage import map_coordinates, zoom
D='/home/claude/dl/dem8/'; R='/home/claude/imperium/'
x0,x1,y0,y1=map(int,open(D+'bbox.txt').read().split()); Z=8; S=128
H=np.zeros(((y1-y0+1)*S,(x1-x0+1)*S),np.float32)
for f in glob.glob(D+'*.png'):
    tx,ty=map(int,os.path.basename(f)[:-4].split('_'))
    a=np.asarray(Image.open(f).convert('RGB'),np.float32)
    e=a[...,0]*256+a[...,1]+a[...,2]/256-32768
    e=e.reshape(S,2,S,2).mean(axis=(1,3))
    H[(ty-y0)*S:(ty-y0+1)*S,(tx-x0)*S:(tx-x0+1)*S]=e
print('mozaik',H.shape,H.min(),H.max())
FULL=[-2600,-2300,6100,4600]; RES=1.5
W=int(FULL[2]/RES); Hh=int(FULL[3]/RES)
xs=FULL[0]+(np.arange(W)+.5)*RES; ys=-(FULL[1]+(np.arange(Hh)+.5)*RES)
X,Y=np.meshgrid(xs,ys)
t=Transformer.from_crs('+proj=laea +lat_0=40 +lon_0=15 +units=km','EPSG:4326',always_xy=True)
lon,lat=t.transform(X,Y)
n=2**Z
px=((lon+180)/360*n - x0)*S - .5
py=((1-np.arcsinh(np.tan(np.radians(lat)))/math.pi)/2*n - y0)*S - .5
E=map_coordinates(H,[py,px],order=1,mode='nearest').astype(np.float32)
del X,Y,lon,lat,px,py
np.save(R+'data/agg/elev1500.npy',np.clip(E,-32000,32000).astype(np.int16))
land=E>0
# árnyékolás: fény ÉNy-ról (315°, 45°), függőleges túlzás 2×
cs=RES*1000; ex=5.0
gy,gx=np.gradient(E*ex,cs)   # gy: lefelé (dél) növekvő sor
slope=np.arctan(np.hypot(gx,gy)); aspect=np.arctan2(-gy,gx)
az=math.radians(360-315+90); alt=math.radians(45)
hs=np.sin(alt)*np.cos(slope)+np.cos(alt)*np.sin(slope)*np.cos(az-aspect)
flat=math.sin(alt)
shade=np.clip((flat-hs)/flat,0,1)      # 0 = sík vagy napos, 1 = mély árnyék
light=np.clip((hs-flat)/(1-flat),0,1)
from scipy.ndimage import gaussian_filter
dark=gaussian_filter(np.clip(shade*1.4,0,1)**0.7,0.6)
alpha=np.round(dark*200/6)*6
alpha[~land]=0
A=np.zeros((Hh,W,4),np.uint8); A[...,0]=45; A[...,1]=35; A[...,2]=25; A[...,3]=alpha.astype(np.uint8)
im=Image.fromarray(A,'RGBA')
for name,scale in (('imp_relief.webp',1.0),('imp_relief_s.webp',0.5)):
    o=im if scale==1 else im.resize((int(W*scale),int(Hh*scale)),Image.LANCZOS)
    o.save(R+name,'WEBP',quality=55,method=6,alpha_quality=60)
    print(name,o.size,os.path.getsize(R+name)//1024,'KB')
# 5 km-es magassági rács későbbre
step=int(5/RES)
np.savez_compressed(R+'data/agg/elev5km.npz',e=E[::step,::step].astype(np.int16),x0=FULL[0],ytop=-FULL[1],res=RES*step)
print('elev5km',E[::step,::step].shape)
