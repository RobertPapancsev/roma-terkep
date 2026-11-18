# v197: ORBIS (Scheidel–Meeks, Stanford; MIT licenc) vízi útvonalai: parti, nyílt tengeri, komp, hajózható folyó.
# A vonalak az ORBIS hálózati modelljének élei (sematikus hajóutak két csomópont között), nem régészetileg igazolt nyomvonalak.
import json, warnings; warnings.filterwarnings('ignore')
from shapely.geometry import shape
from pyproj import Transformer
R='/home/claude/imperium/'
P4=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km +ellps=WGS84',always_xy=True)
F=json.load(open('/home/claude/dl/orbis/orbis_v2/base_routes.geojson'))['features']
out={'c':[],'o':[],'f':[],'r':[]};K={'coastal':'c','overseas':'o','ferry':'f','upstream':'r','downstream':'r'};seen=set();km={k:0 for k in out}
for f in F:
    p=f['properties'];k=K.get(p['t'])
    if not k: continue
    key=(k,)+tuple(sorted((p['sid'],p['tid'])))
    if key in seen: continue
    seen.add(key)
    g=shape(f['geometry']).simplify(0.01)
    gs=[g] if g.geom_type=='LineString' else list(g.geoms)
    for q in gs:
        pts=[P4.transform(x,y) for x,y,*_ in q.coords]
        km[k]+=sum(((a[0]-b[0])**2+(a[1]-b[1])**2)**.5 for a,b in zip(pts,pts[1:]))
        out[k].append(' '.join('%.1f,%.1f'%t for t in pts))
json.dump(out,open(R+'imp_sea.json','w'),separators=(',',':'))
print({k:len(v) for k,v in out.items()},{k:round(v) for k,v in km.items()})
