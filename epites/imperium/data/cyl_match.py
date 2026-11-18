# Kasztília és León római kori lelőhelyei (data/fetch_cyl.py) a térkép helyeihez: városoknál 3 km, máshol 1,5 km-en belül
# (a lelőhely befoglaló téglalapjának közepe, a lelőhely fél kiterjedésével megnövelt körzetben; a védett régészeti zónák elöl). Kimenet: data/agg/cyl_match.json {id: {n, r, per:[köztársasági, korai császárkori, késő római], nm:[[név, url, km]]}}
import json, glob, re
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
R = '/home/claude/imperium/'
tr = Transformer.from_crs('EPSG:4326', '+proj=laea +lat_0=40 +lon_0=15 +units=km', always_xy=True)
S = json.load(open('/home/claude/dl/cyl/cyl_romano.json'))
XY = np.array([tr.transform(s['lon'], s['lat']) for s in S]); T = cKDTree(XY)
SR = np.array([min(3.0, (s['ha'] * 1e4) ** 0.5 / 2000) for s in S])  # a lelőhely fél kiterjedése km-ben (befoglaló téglalapból, legfeljebb 3 km)
LOW = {'de', 'del', 'la', 'las', 'el', 'los', 'y', 'e', 'en', 'a'}
def nice(n):
    n = re.sub(r'\s+', ' ', n.strip()); m = re.match(r'^(.*), (EL|LA|LOS|LAS)$', n)
    if m: n = m.group(2) + ' ' + m.group(1)
    w = n.lower().split(' ')
    return ' '.join(x if (i and x in LOW) else re.sub(r'^(\W*)(\w)', lambda m: m.group(1) + m.group(2).upper(), x) for i, x in enumerate(w))
P = {}
for p in json.load(open(R + 'imp_base.json'))['pts']: P[p[7]] = p
for f in glob.glob(R + 'tiles/*.json'):
    for p in json.load(open(f)).get('s', []): P[p[7]] = p
out = {}
for pid, p in P.items():
    r = 3.0 if p[0] in ('city', 'civ') else 1.5
    ix = [k for k in T.query_ball_point([p[1], p[2]], r + 3.0) if np.hypot(*(XY[k] - [p[1], p[2]])) <= r + SR[k]]  # a lelőhely kiterjedését is figyelembe véve
    if not ix: continue
    ix.sort(key=lambda k: (S[k]['d_categ_prot'] != 'ZONA ARQUEOLÓGICA', np.hypot(*(XY[k] - [p[1], p[2]]))))
    per = [sum(1 for k in ix if S[k][f]) for f in ('romano_republicano', 'romano_altoimperial', 'tardorromano')]
    out[str(pid)] = {'n': len(ix), 'r': r, 'per': per,
                     'nm': [[nice(S[k]['d_bien_denom']), S[k]['l_url_pweb'], round(float(np.hypot(*(XY[k] - [p[1], p[2]]))), 1)] for k in ix[:6]]}
json.dump(out, open(R + 'data/agg/cyl_match.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('lelőhelyek', len(S), '| térképhelyek', len(out))
for pid, p in P.items():
    if p[3] in ('Clunia', 'Numantia', 'Asturica Augusta', 'Legio') and str(pid) in out: print(p[3], out[str(pid)])
