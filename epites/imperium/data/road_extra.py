# Itiner-e: útszakaszok geodéziai hossza (saját számítás) és átlagos emelkedése (az Itiner-e mezője, fokban)
import json
from pyproj import Transformer,Geod
from shapely.geometry import shape
T=Transformer.from_crs('EPSG:3395','EPSG:4326',always_xy=True);G=Geod(ellps='WGS84')
R=json.load(open('/home/claude/dl/itinere/r.json'))['features']
out=[]
for f in R:
    g=shape(f['geometry']);L=0
    for ls in getattr(g,'geoms',[g]):
        xs,ys=zip(*[(c[0],c[1]) for c in ls.coords]);lo,la=T.transform(xs,ys);L+=G.line_length(lo,la)
    sl=f['properties'].get('Avg_Slope');out.append([round(L/1000,1),round(sl,1) if sl is not None else None])
json.dump(out,open('/home/claude/imperium/data/agg/road_extra.json','w'),separators=(',',':'))
import statistics as S
print(len(out),'median km',S.median(o[0] for o in out),'total km',round(sum(o[0] for o in out)),'slope max',max(o[1] or 0 for o in out))
print('example Tingi-Tamuda',out[0],R[0]['properties']['Shape_Leng'])
