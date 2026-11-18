# Úton kívüli menetrács (v177): 9 km-es cellák a térkép teljes területén.
#  e: átlagos magasság/25 m + 1 (0 = tenger vagy tó, járhatatlan); t: a cellán belüli terep tényezője (Tobler-függvény
#  átlaga az 1,5 km-es rács lejtőin, 255 = sík); r: folyóátkelés a szomszéd cella felé (bit0 K, bit1 D, bit2 DK, bit3 DNy),
#  Natural Earth 10m folyóvonalak alapján.
import numpy as np, json, base64, math, shapefile
from shapely.geometry import shape, LineString
from shapely.ops import transform, unary_union
from shapely import STRtree, contains_xy, prepare
from pyproj import Transformer
R='/home/claude/imperium/'
E=np.load(R+'data/agg/elev1500.npy').astype(np.float32)   # 3066 x 4066, 1,5 km
FULL=[-2600,-2300,6100,4600]; RES0=1.5; K=6; RES=RES0*K
H0,W0=E.shape; H,W=H0//K,W0//K
f4=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km +ellps=WGS84',always_xy=True)
t4=lambda x,y,z=None:f4.transform(x,y)
# víz: AWMC nyílt víz (Kr. u. 200) + Natural Earth tavak
r=shapefile.Reader('/home/claude/awmc/geodata/Physical Data/open_water_awmc_work/200_ce_open_water/openwater_c_200_ce')
WAT=[transform(t4,shape(s.__geo_interface__)).buffer(0) for s in r.shapes()]
D='/home/claude/klokan/roman-empire/data/'
for f in json.load(open(D+'10m_lakes.geojson'))['features']: WAT.append(transform(t4,shape(f['geometry'])).buffer(0))
water=unary_union(WAT); prepare(water)
xs=FULL[0]+(np.arange(W0)+.5)*RES0; ys=-(FULL[1]+(np.arange(H0)+.5)*RES0)
wm=np.zeros((H0,W0),bool)
for i in range(H0): wm[i]=contains_xy(water,xs,np.full(W0,ys[i]))
print('víz kész',wm.mean())
# tereptényező az 1,5 km-es lejtőkből
gy,gx=np.gradient(E,RES0*1000); s=np.hypot(gx,gy)
tob=lambda v: np.exp(-3.5*np.abs(v+.05))
T0=(tob(s)+tob(-s))/2/math.exp(-.175)
land=(~wm)&(E>-100)
B=lambda a: a[:H*K,:W*K].reshape(H,K,W,K)
landc=B(land).mean(axis=(1,3))
Tc=np.where(B(land).sum(axis=(1,3))>0,(B(T0*land)).sum(axis=(1,3))/np.maximum(1,B(land).sum(axis=(1,3))),0)
Ec=np.where(B(land).sum(axis=(1,3))>0,(B(np.maximum(E,0)*land)).sum(axis=(1,3))/np.maximum(1,B(land).sum(axis=(1,3))),0)
pas=landc>=.5
e8=np.where(pas,np.clip(np.round(Ec/25)+1,1,255),0).astype(np.uint8)
t8=np.where(pas,np.clip(np.round(Tc*255),20,255),0).astype(np.uint8)
# folyóátkelések
RV=[]
for f in json.load(open(D+'10m_rivers_lake_centerlines.geojson'))['features']:
    g=transform(t4,shape(f['geometry']))
    for ls in getattr(g,'geoms',[g]): RV.append(ls)
tree=STRtree(RV)
cx=lambda j: FULL[0]+(j+.5)*RES; cy=lambda i: -(FULL[1]+(i+.5)*RES)
r8=np.zeros((H,W),np.uint8); DIRS=[(0,1,1),(1,0,2),(1,1,4),(1,-1,8)]
segs=[];idx=[]
for i in range(H):
    for j in range(W):
        if not pas[i,j]: continue
        for di,dj,bit in DIRS:
            i2,j2=i+di,j+dj
            if 0<=i2<H and 0<=j2<W and pas[i2,j2]: segs.append(LineString([(cx(j),cy(i)),(cx(j2),cy(i2))])); idx.append((i,j,bit))
res=tree.query(segs,predicate='intersects')
hit=set(res[0].tolist())
for k in hit:
    i,j,bit=idx[k]; r8[i,j]|=bit
print('cellák',W,H,'járható',int(pas.sum()),'folyós élek',len(hit))
from PIL import Image
Image.fromarray(np.dstack([e8,t8,r8*16]),'RGB').save(R+'imp_offroad.png',optimize=True)
json.dump({'res':RES,'x0':FULL[0],'ytop':-FULL[1],'w':W,'h':H},open(R+'imp_offroad_meta.json','w'))
import os; print(os.path.getsize(R+'imp_offroad.png')//1024,'KB')
