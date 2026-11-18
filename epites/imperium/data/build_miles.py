# v201: mérföldkő-kártya. Forrás: LIST v1.2 (Kaše–Heřmánková–Sobotková, Zenodo, CC BY 4.0) – az EDCS „miliaria” feliratfajtájú tételei.
# Kimenet: imp_st/miles.json sorok: [x,y,hely,provincia,darab,keltezett darab,legkorábbi év|null,legkésőbbi év|null]; lelőhelyenként összevonva.
import pandas as pd, json, collections
from pyproj import Transformer
R='/home/claude/imperium/'
tg=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km',always_xy=True)
m=pd.read_pickle('/home/claude/dl/list/all_meta.pkl')
ms=m[m['inscr_type'].astype(str).str.contains('miliari',case=False,na=False)].copy()
ntot=len(ms); g=ms[ms['Latitude'].notna()&ms['Longitude'].notna()].copy()
g['d']=g['not_before'].notna()&g['not_after'].notna()&((g['not_after']-g['not_before'])<=100)
g['mid']=(g['not_before']+g['not_after'])/2
xy=[tg.transform(lo,la) for lo,la in zip(g['Longitude'],g['Latitude'])]
g['X']=[round(v[0]) for v in xy];g['Y']=[round(v[1]) for v in xy]
def per(v): return 0 if v<193 else 1 if v<285 else 2
rows=[]
for (x,y),q in g.groupby(['X','Y']):
    d=q[q['d']];c=[0,0,0]
    for v in d['mid']: c[per(v)]+=1
    pl=q['place'].dropna().astype(str);pv=q['province'].dropna().astype(str)
    rows.append([int(x),int(y),pl.mode().iat[0] if len(pl) else '',pv.mode().iat[0] if len(pv) else '',len(q),len(d),int(d['not_before'].min()) if len(d) else None,int(d['not_after'].max()) if len(d) else None,c])
rows.sort(key=lambda r:-r[4])
d=g[g['d']];b=collections.Counter((int(v)//25)*25 for v in d['mid'])
tl=[[a,b.get(a,0)] for a in range(-150,426,25)]
json.dump(rows,open(R+'imp_st/miles.json','w'),ensure_ascii=False,separators=(',',':'))
pv=g['province'].value_counts()
sm={'ntot':ntot,'n':len(g),'nplace':len(rows),'ndated':len(d),'tl':tl,'prov':[[k,int(v)] for k,v in pv.head(12).items()],'per':[int(sum(r[8][i] for r in rows)) for i in range(3)],
    'pann':int(pv.get('Pannonia inferior',0)+pv.get('Pannonia superior',0)),'top':[[r[2],r[3],r[4]] for r in rows[:8]]}
json.dump(sm,open(R+'data/stats/miles_summary.json','w'),ensure_ascii=False)
print(sm)
import os;print(os.path.getsize(R+'imp_st/miles.json'))
