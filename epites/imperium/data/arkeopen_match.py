# ArkeOpen (az ArkeoGIS nyílt része, arkeopen.org, nyilvános GraphQL-felület) kiválasztott adatkészletei a térkép helyeihez.
# Csak a római korral átfedő tételek: a keltezési tartomány (start_date1 – end_date2) legalább 25 évben átfed a Kr. e. 30 – Kr. u. 500 közötti szakasszal.
# Pontos helyű tételek: városoknál 3 km, máshol 1,5 km; a község közepére tett tételek (centroid=true): a legközelebbi térképhely 5 km-en belül (≈).
# A három villa-adatkészlet átfed: 300 m-en belüli villák közül csak egy számít.
# Kimenet: data/agg/arkeopen_match.json {id: {n, c:[[kat, n]], v, nm:[[név, község, kat, km, 'e'|'v']]}}
import json, glob, sys
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
R = '/home/claude/imperium/'; D = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/dl/arkeopen/'
tr = Transformer.from_crs('EPSG:4326', '+proj=laea +lat_0=40 +lon_0=15 +units=km', always_xy=True)
CAT = {840: 'villa', 548: 'villa', 517: 'villa', 518: 'urb', 113: 'water', 121: 'water', 630: 'water', 88: 'water', 159: 'water', 364: 'mine', 814: 'cult', 77: 'vis'}
S = []
for db in (840, 548, 517, 518, 113, 121, 630, 88, 159, 364, 814, 77):  # a pontosabb villa-adatkészletek elöl
    for x in json.load(open(f'{D}db_{db}.json'))['data']['ako_site']:
        a, b = x['start_date1'], x['end_date2']
        if a is None or b is None or min(b, 500) - max(a, -30) < 25 or not x.get('geom'): continue
        lon, lat = x['geom']['coordinates'][:2]
        S.append({'xy': tr.transform(lon, lat), 'nm': (x['name'] or '').strip(), 'c': (x['city_name'] or '').strip().strip("'").replace("''", "'"),
                  'k': CAT[db], 'p': 'v' if x['centroid'] else 'e', 'db': db})
keep = []; vt = None; vx = []
for s in S:
    if s['k'] == 'villa':
        if vx and min(np.hypot(*(np.array(vx) - s['xy']).T)) < 0.3: continue
        vx.append(s['xy'])
    keep.append(s)
print('római korral átfedő', len(S), '| villa-ismétlések nélkül', len(keep))
P = {}
for p in json.load(open(R + 'imp_base.json'))['pts']: P[str(p[7])] = p
for f in glob.glob(R + 'tiles/*.json'):
    for p in json.load(open(f)).get('s', []): P[str(p[7])] = p
PID = list(P); PXY = np.array([[P[k][1], P[k][2]] for k in PID]); PT = cKDTree(PXY)
E = [s for s in keep if s['p'] == 'e']; V = [s for s in keep if s['p'] == 'v']
EXY = np.array([s['xy'] for s in E]); ET = cKDTree(EXY)
hits = {}
for pid in PID:
    p = P[pid]; r = 3.0 if p[0] in ('city', 'civ') else 1.5
    for k in ET.query_ball_point([p[1], p[2]], r): hits.setdefault(pid, []).append((E[k], float(np.hypot(*(EXY[k] - [p[1], p[2]])))))
nv = 0
for s in V:
    d, k = PT.query(s['xy'])
    if d <= 5.0: hits.setdefault(PID[k], []).append((s, float(d))); nv += 1
out = {}
ORD = {'urb': 0, 'vis': 1, 'cult': 2, 'water': 3, 'villa': 4, 'mine': 5}
for pid, h in hits.items():
    h.sort(key=lambda t: (t[0]['p'] != 'e', ORD[t[0]['k']], t[1]))
    c = {}
    for s, _ in h: c[s['k']] = c.get(s['k'], 0) + 1
    out[pid] = {'n': len(h), 'c': sorted(c.items(), key=lambda kv: -kv[1]), 'v': sum(s['p'] == 'v' for s, _ in h),
                'nm': []}
    seen = {}
    for s, d in h:  # az azonos nevű tételek (pl. ugyanannak a lelőhelynek több vízépítménye) egy sorba, darabszámmal
        key = (s['nm'], s['k'])
        if key in seen: seen[key][5] += 1; continue
        if len(seen) < 6: seen[key] = [s['nm'], s['c'], s['k'], round(d, 1), s['p'], 1]
    out[pid]['nm'] = list(seen.values())
json.dump(out, open(R + 'data/agg/arkeopen_match.json', 'w'), ensure_ascii=False, separators=(',', ':'))
used = {id(s) for h in hits.values() for s, _ in h}
print('térképhelyek', len(out), '| megjelenő tételek', len(used), '| ebből községszintű', nv)
import collections; print(collections.Counter(s['k'] for s in keep if id(s) in used))
for pid in out:
    if P[pid][3] in ('Arelate', 'Nemausus', 'Aquae Sextiae', 'Forum Iulii', 'Narbo', 'Vasio', 'Augusta Raurica', 'Glanum'): print(P[pid][3], json.dumps(out[pid], ensure_ascii=False)[:350])
