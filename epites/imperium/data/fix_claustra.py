# v207: a Claustra Alpium Iuliarum falszakaszai. A DARE/Barrington-féle vonalak sematikusak (hosszuk többszöröse a felmértnek).
# A claustra.org szakaszlistája (https://claustra.org/facts/, 2026-11-16) szerinti felmért hosszra rövidítjük azokat, amelyek egy megnevezett szakaszhoz köthetők;
# a rövidített szakasz a régi vonal mentén marad (a hely tehát közelítő). A nem köthető vonalak megmaradnak, „sematikus” jelöléssel.
# b['limt'] = {vonalindex: [név, felmért hossz m | 0, sematikus 0/1]}
import json, shutil, os
from shapely.geometry import LineString, Point
from shapely.ops import substring
from pyproj import Transformer
R='/home/claude/imperium/'
if not os.path.exists(R+'data/imp_base_before_v207.json'): shutil.copy(R+'imp_base.json',R+'data/imp_base_before_v207.json')
b=json.load(open(R+'data/imp_base_before_v207.json'));L=b['limes']
tg=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km',always_xy=True)
ls=lambda i:LineString([tuple(map(float,q.split(','))) for q in L[i].split()])
fmt=lambda g:' '.join('%.2f,%.2f'%p for p in g.coords)
def mid(g,km):   # km hosszú darab a vonal közepe körül
    c=g.length/2;return substring(g,max(0,c-km/2),min(g.length,c+km/2))
def around(g,pt,km):   # km hosszú darab a vonalnak a megadott ponthoz legközelebbi része körül
    c=g.project(pt);a=max(0,min(g.length-km,c-km/2));return substring(g,a,a+km)
T={};log=[]
def setl(i,g,name,m,sch=0):
    old=ls(i).length if i<len(L) else 0
    if i<len(L): L[i]=fmt(g)
    else: L.append(fmt(g))
    T[str(i)]=[name,m,sch];log.append((i,name,round(old,2),round(g.length,2),sch))
# 52: Rijekától északra, a Grobniki-mező felé -> Jelenje (2981 m)
setl(52,mid(ls(52),2.981),'Jelenje (Grobničko polje)',2981)
# 53+54: Studena (4958 m) – a két vonal arányosan rövidítve
t=ls(53).length+ls(54).length
setl(53,mid(ls(53),4.958*ls(53).length/t),'Studena',4958);setl(54,mid(ls(54),4.958*ls(54).length/t),'Studena',4958)
# 55: 18,7 km-es folyamatos vonal a Babno poljéig; a felmért prezidi fal (2754 m) az északi végén van, a többi sematikus
g=ls(55);setl(55,substring(g,g.length-2.754,g.length),'Prezid – Babno polje',2754)
setl(len(L),substring(g,0,g.length-2.754),'',0,1)
# 56: Bloke-fennsík -> Benete (583) + Novi Pot (240) + Tabršče (15)
setl(56,mid(ls(56),0.838),'Benete – Novi Pot – Tabršče',838)
# 57: Rob környéke -> Selo pri Robu (396) + Gradišče pri Robu (1308)
setl(57,mid(ls(57),1.704),'Selo pri Robu – Gradišče pri Robu',1704)
# 60: Pokojišče (577 m)
setl(60,mid(ls(60),0.577),'Pokojišče',577)
# 62: Logatec környéke -> Lanišče (315) + Brst pri Martinjem hribu (605)
setl(62,mid(ls(62),0.920),'Lanišče – Brst pri Martinjem hribu',920)
# 63: Hrušica (Ad Pirum; 1882 m) – az erőd (45.86361 É, 14.11167 K) körüli rész
setl(63,around(ls(63),Point(*tg.transform(14.11167,45.86361)),1.882),'Hrušica (Ad Pirum)',1882)
# 64: Ajdovski zid Vrhnika fölött – a rajzolt 6,1 km közel a felmért 6742 m-hez, változatlan
setl(64,ls(64),'Ajdovski zid (Vrhnika)',6742)
# nem köthető vonalak: sematikus jelöléssel maradnak
for i in (58,59,61,65,66): setl(i,ls(i),'',0,1)
b['limes']=L;b['limt']=T
json.dump(b,open(R+'imp_base.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump(log,open(R+'data/stats/claustra_fix_log.json','w'),ensure_ascii=False)
for r in log: print(r)
print('fal össz. előtte/utána km:',round(sum(r[2] for r in log),1),round(sum(r[3] for r in log),1),'ebből sematikus:',round(sum(r[3] for r in log if r[4]),1), len(L))
