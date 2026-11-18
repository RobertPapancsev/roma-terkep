# ICAC bor- és olajtermelő lelőhelyek (data/icac_geo.py, községi szintű hely) a térkép helyeihez: minden lelőhely a legközelebbi
# térképhelyhez kerül 15 km-en belül (egy lelőhely egyszer számít). Kimenet: data/agg/icac_match.json {id: [[név, község, termék, település-jelleg], ...]}
import json, glob, re
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
R = '/home/claude/imperium/'
tr = Transformer.from_crs('EPSG:4326', '+proj=laea +lat_0=40 +lon_0=15 +units=km', always_xy=True)
S = json.load(open('/home/claude/dl/icac/icac_geo.json'))
P = {}
for p in json.load(open(R + 'imp_base.json'))['pts']: P[p[7]] = p
for f in glob.glob(R + 'tiles/*.json'):
    for p in json.load(open(f)).get('s', []): P[p[7]] = p
ids = list(P); T = cKDTree(np.array([[P[i][1], P[i][2]] for i in ids]))
def prod(s):
    s = (s or '').strip(); a = 'aceite' in s.lower(); v = 'vino' in s.lower(); q = '¿' in s or '?' in s
    if a and v: return 'ov?' if q else 'ov'
    if a: return 'o?' if q else 'o'
    if v: return 'v?' if q else 'v'
    return 'x'
SET = {'Rural': 'r', 'Urbano': 'u', 'Suburbano': 's', 'Villa suburbana': 's', 'Villa': 'r', 'Castro': 'c'}
out = {}; n = 0
for s in S:
    x, y = tr.transform(s['lon'], s['lat']); d, k = T.query([x, y])
    if d > 15: continue
    out.setdefault(str(ids[k]), []).append([s['Yacimiento'].strip(), s['Municipio'].strip(), prod(s['Producto']), SET.get(s['Asentamiento'].strip(), '')]); n += 1
json.dump(out, open(R + 'data/agg/icac_match.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('lelőhely', len(S), 'hozzárendelve', n, '| térképhelyek', len(out))
for k, v in sorted(out.items(), key=lambda kv: -len(kv[1]))[:6]: print(P[k][3], P[k][4], len(v), v[:3])
