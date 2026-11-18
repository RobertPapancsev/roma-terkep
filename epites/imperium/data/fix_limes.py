# v193: a DARE/Klokan fortifications.geojson egyes vonalai (Hadrianus- és Antoninus-fal, felső-germaniai és raetiai limes, Main)
# kb. 0,15–0,19 fokkal északabbra vannak: a koordinátákat Web Mercatorból (EPSG:3857) úgy alakították át, mintha
# ellipszoidi Mercator (EPSG:3395) lett volna. Javítás: lat_ok = inv3857(fwd3395(lat_hibás)).
# Vonalanként döntünk: akkor javítjuk, ha a javított vonal mediántávolsága a DARE erődpontjaitól legalább 40%-kal kisebb.
import json, numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
R='/home/claude/imperium/'; D='/home/claude/klokan/roman-empire/data/'
P4=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km +ellps=WGS84',always_xy=True)
to3395=Transformer.from_crs('EPSG:4326','EPSG:3395',always_xy=True); from3857=Transformer.from_crs('EPSG:3857','EPSG:4326',always_xy=True)
fix=lambda lo,la: from3857.transform(*to3395.transform(lo,la))
b=json.load(open(R+'data/imp_base_before_v193.json'))
F=np.array([(p[1],p[2]) for p in b['pts'] if p[0] in('fort','fortlet','leg','camp')]);T=cKDTree(F)
fo=json.load(open(D+'fortifications.geojson'))['features']
out=[];log=[]
for f in fo:
    g=f['geometry'];ls=[g['coordinates']] if g['type']=='LineString' else g['coordinates']
    allraw=np.array([P4.transform(c[0],c[1]) for l in ls for c in l]);allcor=np.array([P4.transform(*fix(c[0],c[1])) for l in ls for c in l])
    mr=float(np.median(T.query(allraw)[0]));mc=float(np.median(T.query(allcor)[0]))
    nm=str(f['properties'].get('Name'))
    use=mc<mr*0.6 or nm.startswith(('VALLVM','Wall Mil','Limes Germania','Limes Raetia','FL. NICER','FL. MOENVS'))   # ugyanazon digitalizálás részei: egységesen
    log.append([f['properties'].get('Name'),len(allraw),round(mr,1),round(mc,1),use])
    for l in ls:
        if len(l)<2: continue
        cs=[P4.transform(*fix(c[0],c[1])) if use else P4.transform(c[0],c[1]) for c in l]
        out.append(' '.join('%.2f,%.2f'%(x,y) for x,y in cs))
assert len(out)==len(b['limes']), (len(out),len(b['limes']))
b['limes']=out
json.dump(b,open(R+'imp_base.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump(log,open(R+'data/stats/limes_fix_log.json','w'),ensure_ascii=False,indent=0)
print(sum(1 for x in log if x[4]),'/',len(log),'vonal javítva')
for x in log:
    if x[4]: print(x)
