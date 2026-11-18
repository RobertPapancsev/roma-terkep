# v186: IsoArcH emberi csontkollagén δ13C/δ15N, római kor (a keltezés közepe Kr. e. 30 – Kr. u. 476) -> imp_st/iso.json
import json, re, math, pandas as pd, numpy as np
from pyproj import Transformer
from shapely.geometry import Polygon, Point
R='/home/claude/imperium/'
tg=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km',always_xy=True)
B=json.load(open(R+'imp_base.json'))
PP=[]
for p in B['prov']:
    for g in p['g']:
        pts=[tuple(map(float,q.split(','))) for q in g.lstrip('p').split(' ') if ',' in q]
        if len(pts)>=3: PP.append((p['n'],Polygon(pts).buffer(0)))
def prov(x,y):
    pt=Point(x,y)
    for n,pg in PP:
        if pg.contains(pt): return n
    best=min(PP,key=lambda t:t[1].distance(pt))
    return best[0] if best[1].distance(pt)<15 else None   # partközeli pontok
REG={'Italia':['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','Sicilia','Sardinia et Corsica'],
 'Britannia':['Britannia'],'Gallia, Germania':['Lugdunensis','Belgica','Germania Inferior','Aquitania','Germania Superior','Narbonensis','Alpes Graiae et Poeninae','Alpes Cottiae','Alpes Maritimae'],
 'Hispania':['Tarraconensis','Baetica','Lusitania'],'Duna-vidék':['Raetia','Noricum','Pannonia Superior','Pannonia Inferior','Moesia Superior','Moesia Inferior','Dacia','Dalmatia'],
 'Balkán, Görögország':['Thracia','Macedonia','Achaia','Creta et Cyrene'],'Kis-Ázsia':['Bithynia et Pontus','Cilicia','Galatia et Cappadocia','Lycia et Pamphylia','Asia','Cyprus'],
 'Kelet, Egyiptom':['Aegyptus','Arabia','Iudaea','Syria','Armenia Mesopotamia'],'Africa':['Africa Proconsularis','Numidia','Mauretania Caesariensis','Mauretania Tingitana']}
P2R={p:r for r,ps in REG.items() for p in ps}
x=pd.ExcelFile(R+'data/isoarch/isoarch-export-2026-11-15.xlsx')
o=pd.read_excel(x,'Organic measures'); ds=pd.read_excel(x,'Datasets')
h=o[(o['Material type']=='hominin')&(o['Relative dating timescale']=='BCE/CE')&(o['Sample type']=='bone')].copy()
h['mid']=(h['Relative dating - lower limit']+h['Relative dating - upper limit'])/2
h=h[(h.mid>=-30)&(h.mid<=476)&h['δ13C (‰vpdb)'].notna()&h['δ15N (‰air)'].notna()]
# minőségi szűrés: C:N 2,9–3,6 (DeNiro 1985), ahol meg van adva
cn=h['C:N']; nq=int(((cn<2.9)|(cn>3.6)).sum()); h=h[cn.isna()|((cn>=2.9)&(cn<=3.6))]
ind=h.groupby(['Location name','Material identifier']).agg(lat=('Latitude','first'),lon=('Longitude','first'),c=('δ13C (‰vpdb)','mean'),n=('δ15N (‰air)','mean'),mid=('mid','first'),ref=('Short references','first'),doi=('Dataset DOI','first')).reset_index()
locs=[]; RR={}
ind=ind[(ind.lon>-12)&(ind.lon<50)&(ind.lat>22)&(ind.lat<60)]   # csak Európa és a Mediterráneum (a térkép kiterjedése)
for (nm,),g in ind.groupby(['Location name']):
    lon,lat=g.lon.iloc[0],g.lat.iloc[0]; X,Y=tg.transform(lon,lat); pv={'Kellis 2':'Aegyptus','Zabayir Zahir ed-Diyab - Queen Alia International Airport':'Arabia'}.get(nm) or prov(X,Y); rg=P2R.get(pv,'kívül') if pv else 'kívül'
    refs=sorted({r for r in g.ref.dropna()})
    locs.append([int(round(X)),int(round(Y)),nm,pv or '',len(g),round(g.c.mean(),2),round(g.n.mean(),2),round(g.c.std(),2) if len(g)>1 else None,round(g.n.std(),2) if len(g)>1 else None,
                 [int(g.mid.min()),int(g.mid.max())],'; '.join(refs)[:160]])
    RR.setdefault(rg,[]).append(g)
json.dump(locs,open(R+'imp_st/iso.json','w'),ensure_ascii=False,separators=(',',':'))
reg={}
for rg,gs in RR.items():
    a=pd.concat(gs); reg[rg]={'ind':len(a),'loc':len(gs),'c':round(a.c.mean(),2),'csd':round(a.c.std(),2),'n':round(a.n.mean(),2),'nsd':round(a.n.std(),2)}
S={'ind':len(ind),'loc':len(locs),'nq':nq,'reg':reg,'ds':len(ds),'lic':ds['Dataset license'].value_counts().to_dict(),
   'pann':[l for l in locs if l[3] in ('Pannonia Superior','Pannonia Inferior')],
   'c_hi':int((ind.c>-18).sum()),'refs':int(ind.ref.nunique())}
json.dump(S,open(R+'data/stats/iso_summary.json','w'),ensure_ascii=False,indent=1)
print(json.dumps({k:v for k,v in S.items() if k!='pann'},ensure_ascii=False,indent=0)); print([ (l[2],l[4],l[5],l[6],l[9]) for l in S['pann']])
print([ (l[2],l[3]) for l in locs if not l[3]][:30])
