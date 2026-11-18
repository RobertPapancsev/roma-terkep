# MiC „Luoghi della cultura” (dati.cultura.gov.it, CIS-adatkészlet, CC BY 4.0): régészeti területek, régészeti parkok, sírépítmények
# és a nevük szerint régészeti múzeumok/antiquariumok, koordinátával. SPARQL-lekérdezés 2026. november 13-án → /home/claude/dl/mic_luoghi/luoghi.json
# Hozzárendelés: a térkép helyeitől 3 km-en belül (városoknál 4 km), helyenként legfeljebb 6, távolság szerint.
import json, glob, re, collections
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
R = '/home/claude/imperium/'
tr = Transformer.from_crs('EPSG:4326', '+proj=laea +lat_0=40 +lon_0=15 +units=km', always_xy=True)
B = json.load(open('/home/claude/dl/mic_luoghi/luoghi.json'))['results']['bindings']
L = {}
for b in B:
    s = b['s']['value']
    if 'lat' not in b: continue
    try: la, lo = float(b['lat']['value']), float(b['lon']['value'])
    except ValueError: continue
    if not (35 < la < 48 and 6 < lo < 19): continue  # hibás koordináták kiszűrése (Olaszországon kívül)
    t = {'Area Archeologica': 'a', 'Parco Archeologico': 'p', 'Monumento Funerario': 'f', 'Museo, Galleria e/o raccolta': 'm'}[b['t']['value']]
    o = L.setdefault(s, {'n': b['name']['value'].strip(), 't': t, 'x': tr.transform(lo, la), 'u': ''})
    u = b.get('url', {}).get('value', '').strip()
    if u and not u.startswith('http'): u = 'http://' + u
    if u and not o['u'] and '@' not in u and re.match(r'^https?://[a-z0-9.\-]+\.[a-z]{2,}(/\S*)?$', u, re.I): o['u'] = u  # hibás (pl. e-mail) címek nélkül
LL = list(L.values()); XY = np.array([o['x'] for o in LL]); T = cKDTree(XY)
P = {}
for p in json.load(open(R + 'imp_base.json'))['pts']: P[p[7]] = p
for f in glob.glob(R + 'tiles/*.json'):
    for p in json.load(open(f)).get('s', []): P[p[7]] = p
out = {}; used = collections.Counter()
for pid, p in P.items():
    r = 4.0 if p[0] in ('city', 'civ') else 3.0
    ix = T.query_ball_point([p[1], p[2]], r)
    if not ix: continue
    ix.sort(key=lambda k: np.hypot(*(XY[k] - [p[1], p[2]])))
    out[str(pid)] = [[LL[k]['n'], LL[k]['t'], LL[k]['u'], round(float(np.hypot(*(XY[k] - [p[1], p[2]]))), 1)] for k in ix[:6]]
    for k in ix: used[k] += 1
json.dump(out, open(R + 'data/agg/luoghi_match.json', 'w'), ensure_ascii=False)
print('MiC-helyek', len(LL), 'ebből térképhelyhez rendelve', len(used), '| térképhelyek MiC-hellyel', len(out))
for nm in ('Ostia', 'Pompeii', 'Aquileia', 'Paestum'):
    for pid, p in P.items():
        if p[3] == nm and str(pid) in out: print(nm, out[str(pid)])
