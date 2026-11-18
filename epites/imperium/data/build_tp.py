# v204: a Tabula Peutingeriana helyei és útkapcsolatai. Forrás: OmnesViae (R. Voorburg, MIT licenc; alapja: R. J. A. Talbert, Rome's World, 2010),
# a cyberhirsch/peutinger-map GitHub-tároló places.json állományán keresztül (ez Pleiades-azonosítókkal és helyminősítéssel egészíti ki; MIT).
# Kimenet: imp_st/tp.json {p:[[x,y,TP-írásmód,Pleiades-név,mai név,helyminősítés 1-3,Pleiades-azonosító|0]], r:"M..L.." útkapcsolatok egyenes vonalai}
import json, collections
from pyproj import Transformer
R='/home/claude/imperium/'
tg=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km',always_xy=True)
d=json.load(open('/home/claude/dl/omnesviae/pm/places.json'));P=d['places'];E=d['roads']
idx={};pts=[]
for i,p in enumerate(P):
    if 'll' not in p: continue
    x,y=tg.transform(p['ll'][1],p['ll'][0])
    if not(-2600<x<3600 and -2200<y<2200): continue   # a térkép kivágásán kívüli (pl. indiai, perzsiai) helyek kimaradnak
    idx[i]=len(pts);pts.append([round(x),round(y),p['n'],p.get('pt',''),p.get('m',''),p['lq'],int((p.get('ids') or {}).get('p',0) or 0)])
seg=[];long=0
for a,b,dist in E:
    if a in idx and b in idx:
        A,B=pts[idx[a]],pts[idx[b]];L=((A[0]-B[0])**2+(A[1]-B[1])**2)**.5
        if L>400: long+=1;continue   # nyilvánvalóan hibás párosítás vagy tengeri átkelés
        seg.append(f"M{A[0]} {-A[1]}L{B[0]} {-B[1]}")
json.dump({'p':pts,'r':''.join(seg)},open(R+'imp_st/tp.json','w'),ensure_ascii=False,separators=(',',':'))
sm={'ntot':len(P),'n':len(pts),'noll':sum(1 for p in P if 'll' not in p),'lq':[sum(1 for p in pts if p[5]==i) for i in (1,2,3)],'edges':len(E),'seg':len(seg),'long':long,'npl':sum(1 for p in pts if p[6])}
json.dump(sm,open(R+'data/stats/tp_summary.json','w'));import os;print(sm,os.path.getsize(R+'imp_st/tp.json'))
