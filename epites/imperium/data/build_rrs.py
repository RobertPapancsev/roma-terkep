# v188: The Rural Settlement of Roman Britain (Allen et al. 2018, ADS doi:10.5284/1030449) -> imp_st/rrs.json
import json, pandas as pd, numpy as np
from pyproj import Transformer
R='/home/claude/imperium/'; D=R+'data/rrs/'
t27=Transformer.from_crs('EPSG:27700','EPSG:4326',always_xy=True)
tg=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km',always_xy=True)
c=pd.read_csv(D+'rrs_core_data.csv',encoding='latin-1',dtype=str); s=pd.read_csv(D+'rrs_site_data.csv',encoding='latin-1',dtype=str); t=pd.read_csv(D+'rrs_site_t_major.csv',encoding='latin-1',dtype=str)
m=c.merge(s,on='ID',how='left')
TY=t.groupby('ID').SITE_TYPE_MAJOR.apply(lambda v:sorted(set(v.dropna())))
ORD=['Military','Nucleated settlement','Religious ritual and funerary','Industry','Rural settlement','Rural landscape','Communications']
# fő kategória: 0 villa, 1 katonai, 2 csoportos (nucleated) település, 3 vallási/temetkezési, 4 ipari, 5 vidéki település (és egyéb)
def main(r,ty):
    if r.VILLA_BUILDING=='Yes': return 0
    for k,v in [('Military',1),('Nucleated settlement',2),('Rural settlement',5),('Religious ritual and funerary',3),('Industry',4)]:
        if k in ty: return v
    return 5
num=lambda v: None if pd.isna(v) or str(v).strip()=='' else float(v)
SZ={'small (<1 - 3 ha)':1,'medium (4 - 8 ha)':2,'large (9+ ha)':3}
FM={'enclosed':1,'unenclosed':2,'complex':3,'linear':4}
RG=['Central Belt','South','North-East','East','Central West','North','South-West','Upland Wales and the Marches']
out=[];bad=0
for _,r in m.iterrows():
    e,n=num(r.X_REF_MAP),num(r.Y_REF_MAP)
    if e is None or n is None or e<=0 or n<=0: bad+=1; continue
    lon,lat=t27.transform(e,n); x,y=tg.transform(lon,lat)
    ty=TY.get(r.ID,[])
    d0,d1=num(r.DATE_START),num(r.DATE_END)
    fl=(r.VILLA_BUILDING=='Yes')*1|(r.MASONRY_BUILDING=='Yes')*2|(r.AISLED_BUILDING=='Yes')*4|(r.EARLY_SAXON_ACTIVITY=='Yes')*8
    out.append([int(round(x)),int(round(y)),str(r.SITE_NAME)[:60],str(r.COUNTY),main(r,ty),None if d0 is None else int(d0),None if d1 is None else int(d1),
                SZ.get(r.SETTLEMENT_SIZE,0),FM.get(r.RURAL_SETTLEMENT_FORM,0),fl,[ORD.index(k) for k in ty if k in ORD],RG.index(str(r.REGION)) if str(r.REGION) in RG else -1])
json.dump(out,open(R+'imp_st/rrs.json','w'),ensure_ascii=False,separators=(',',':'))
# idősor: lakott lelőhelyek száma 25 évenként, főkategóriánként (csak keltezettek)
Y=list(range(-100,525,25)); ser={k:[0]*len(Y) for k in range(6)}
for o in out:
    if o[5] is None or o[6] is None: continue
    for i,y in enumerate(Y):
        if o[5]<=y<o[6]: ser[o[4]][i]+=1
from collections import Counter
S={'n':len(m),'nmap':len(out),'bad':bad,'cat':[sum(1 for o in out if o[4]==k) for k in range(6)],'Y':Y,'ser':ser,
   'RG':RG,'reg':[sum(1 for o in out if o[11]==i) for i in range(len(RG))],'villa_reg':[sum(1 for o in out if o[11]==i and o[4]==0) for i in range(len(RG))],
   'dated':sum(1 for o in out if o[5] is not None and o[6] is not None),'end400':sum(1 for o in out if o[6]==400),'saxon':sum(1 for o in out if o[9]&8),
   'peak':{k:[Y[int(np.argmax(v))],max(v)] for k,v in ser.items()},'masonry':sum(1 for o in out if o[9]&2)}
json.dump(S,open(R+'data/stats/rrs_summary.json','w'),ensure_ascii=False,indent=1)
print({k:v for k,v in S.items() if k not in('ser',)}); print({k:v for k,v in ser.items()})
