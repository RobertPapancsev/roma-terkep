# Észak-Macedónia: a Wikidata (CC0) régészeti lelőhelyei, amelyeknek korszaka (P2348) klasszikus ókor, késő antikvitás,
# ókeresztény kor, a Nyugatrómai Birodalom bukása, ókori Róma vagy Római Birodalom (lekérdezés: 2026. november 13.).
# Városoknál 3 km, máshol 1,5 km. Név: az angol címke, ha van; különben a macedón címke latin betűs átírása (a cirill név zárójelben).
# Link: a macedón Wikipédia-szócikk, ha van; különben a Wikidata-elem.
# Kimenet: data/agg/nmk_match.json {id: {n, r, per:[klasszikus ókor, késő antik/ókeresztény, római], nm:[[név, url, km]]}}
import json, glob, sys, urllib.parse
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
R = '/home/claude/imperium/'; D = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/dl/nmk/'
tr = Transformer.from_crs('EPSG:4326', '+proj=laea +lat_0=40 +lon_0=15 +units=km', always_xy=True)
CL = {'Q486761'}; LA = {'Q217050', 'Q51644', 'Q608613'}; RO = {'Q1747689', 'Q2277'}
it = {}
for x in json.load(open(D + 'q1.json'))['results']['bindings']:
    q = x['i']['value'].rsplit('/', 1)[1]; lon, lat = map(float, x['c']['value'][6:-1].split())
    e = it.setdefault(q, {'ll': (lon, lat), 'per': set()}); e['per'].add(x['per']['value'].rsplit('/', 1)[1])
LAT = dict(zip('абвгдѓежзѕијклљмнњопрстќуфхцчџш', ['a','b','v','g','d','gj','e','zh','z','dz','i','j','k','l','lj','m','n','nj','o','p','r','s','t','kj','u','f','h','c','ch','dzh','sh']))
def tl(s): return ''.join((LAT[c.lower()].capitalize() if c.isupper() else LAT[c]) if c.lower() in LAT else c for c in s)
for x in json.load(open(D + 'q2.json'))['results']['bindings']:
    q = x['i']['value'].rsplit('/', 1)[1]
    if q not in it: continue
    mk = x.get('mk', {}).get('value', ''); en = x.get('en', {}).get('value', '')
    it[q]['nm'] = en or (f'{tl(mk)} ({mk})' if mk else q)
    it[q]['url'] = x['art']['value'] if 'art' in x else f'https://www.wikidata.org/wiki/{q}'
Q = [q for q in it if 'nm' in it[q]]
XY = np.array([tr.transform(*it[q]['ll']) for q in Q]); T = cKDTree(XY)
P = {}
for p in json.load(open(R + 'imp_base.json'))['pts']: P[p[7]] = p
for f in glob.glob(R + 'tiles/*.json'):
    for p in json.load(open(f)).get('s', []): P[p[7]] = p
out = {}; used = set()
for pid, p in P.items():
    r = 3.0 if p[0] in ('city', 'civ') else 1.5
    ix = T.query_ball_point([p[1], p[2]], r)
    if not ix: continue
    used.update(ix)
    d = {k: float(np.hypot(*(XY[k] - [p[1], p[2]]))) for k in ix}
    ix.sort(key=lambda k: (not (it[Q[k]]['per'] & RO), d[k]))  # a kifejezetten rómainak jelöltek elöl
    out[str(pid)] = {'n': len(ix), 'r': r, 'per': [sum(bool(it[Q[k]]['per'] & S) for k in ix) for S in (CL, LA, RO)],
                     'nm': [[it[Q[k]]['nm'], it[Q[k]]['url'], round(d[k], 1)] for k in ix[:6]]}
json.dump(out, open(R + 'data/agg/nmk_match.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('lelőhelyek', len(Q), '| térképhelyek', len(out), '| párosított lelőhelyek', len(used))
for pid, p in P.items():
    if p[3] in ('Scupi', 'Stobi', 'Heraclea Lyncestis', 'Lychnidus', 'Astibus', 'Bylazora') and str(pid) in out: print(p[3], json.dumps(out[str(pid)], ensure_ascii=False)[:330])
