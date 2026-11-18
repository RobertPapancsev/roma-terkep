# Közös párosító az országos műemlék-/lelőhelylistákhoz (v143-tól): nh_<ország>.json → build_info o['nh'] = [[ország, adat], …]
# Bemenet: tételek listája {'s': név, 'u': link vagy '', 'x': kiegészítő szöveg (típus, keltezés), 'g': település, 'xy': (LAEA km)}
# Körzet: városoknál 8, máshol 5 km. Kimenet: {pid: {n, r, nm:[[név, link, kiegészítés, település, km]]}}
import json, glob
import numpy as np
from scipy.spatial import cKDTree
from pyproj import Transformer
R = '/home/claude/imperium/'
def laea(src='EPSG:4326'):
    return Transformer.from_crs(src, '+proj=laea +lat_0=40 +lon_0=15 +units=km', always_xy=True)
def places():
    P = {}
    for p in json.load(open(R + 'imp_base.json'))['pts']: P[str(p[7])] = p
    for f in glob.glob(R + 'tiles/*.json'):
        for p in json.load(open(f)).get('s', []): P[str(p[7])] = p
    return P
def match(S, cc, names=()):
    P = places(); XY = np.array([s['xy'] for s in S]); T = cKDTree(XY)
    out = {}; used = set()
    for pid, p in P.items():
        r = 8.0 if p[0] in ('city', 'civ') else 5.0
        ks = T.query_ball_point([p[1], p[2]], r)
        if not ks: continue
        used.update(ks)
        h = sorted(((S[k], float(np.hypot(*(XY[k] - [p[1], p[2]])))) for k in ks), key=lambda t: t[1])
        out[pid] = {'n': len(h), 'r': r, 'nm': [[s['s'], s.get('u', ''), s.get('x', ''), s.get('g', ''), round(d, 1)] for s, d in h[:6]]}
    json.dump(out, open(R + f'data/agg/nh_{cc}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
    print(cc, 'tétel', len(S), '| térképhelyek', len(out), '| párosított tételek', len(used))
    for pid in out:
        if P[pid][3] in names: print(' ', P[pid][3], json.dumps(out[pid], ensure_ascii=False)[:300])
    return out
