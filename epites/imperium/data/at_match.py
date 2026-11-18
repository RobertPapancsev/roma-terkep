# Ausztria: a Bundesdenkmalamt (BDA) műemléklistájának tételei a Wikidatán keresztül (P2951 Austrian cultural heritage ID,
# P625 koordináta, német név; Wikidata CC0). Lekérés: 2026-11-13. A Wikidatában nincs korszakmező, ezért a hivatalos név alapján
# válogatunk: römisch / Römer- / röm. / Kaiserzeit / spätantik / Kastell / villa rustica / Burgus / Limes / Legionslager / Vicus /
# Mithras / Auxiliarlager; kizárva az álpárok (röm.-kath., »Zum römischen Kaiser«, Römerstraße-címek, kastélyok »Kastell« néven,
# hagyományosan »sog. Römerbrücke« hidak, Römermuseum stb.).
# Körzet: városoknál 8, máshol 5 km. Kimenet: data/agg/at_match.json {id: {n, r, nm:[[név, Q, km, község]]}}
import json, glob, re, sys
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
R = '/home/claude/imperium/'; F = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/dl/at/at_all.json'
tr = Transformer.from_crs('EPSG:4326', '+proj=laea +lat_0=40 +lon_0=15 +units=km', always_xy=True)
ROM = r'römisch|römer|röm\.|kaiserzeit|spätantik|kastell|villa rustica|burgus|limes|legionslager|vicus|mithr|auxiliarlager'
BAD = (r'röm\.?-? ?kath|römischen? (kaiser|papst)|römerstraße \d|römerhof|römermuseum|römerbergschule|kulturhaus römerfeld|'
       r'römerstein\b(?!bruch)|römer-marterl|römerhand|römerwand|sog\.? (alte )?römerbrücke|alte römerbrücke|straßenbrücke, römerbrücke|'
       r'teufels-, römerbrücke|^römerbrücke$|kastell (batthy|festetics|loipersdorf)|esterhazysches kastell|sogen\. kastell|ehem\. kastell|'
       r'neues kastell|kastellan|bergkastell|römerturm|römisches handelshaus|römertor, heute|krankenhaus/römertor|^römerweg$|laufbrunnen|'
       r'gasthaus zum römerstein')
it = {}
for x in json.load(open(F))['results']['bindings']:
    q = x['i']['value'].rsplit('/', 1)[1]
    if q in it: continue
    l = x['l']['value']
    if not re.search(ROM, l, re.I) or re.search(BAD, l, re.I): continue
    lon, lat = map(float, x['c']['value'][6:-1].split())
    it[q] = {'q': q, 'l': l, 'g': x.get('gl', {}).get('value', ''), 'xy': tr.transform(lon, lat)}
S = list(it.values()); print('római nevű műemlék', len(S))
P = {}
for p in json.load(open(R + 'imp_base.json'))['pts']: P[str(p[7])] = p
for f in glob.glob(R + 'tiles/*.json'):
    for p in json.load(open(f)).get('s', []): P[str(p[7])] = p
XY = np.array([v['xy'] for v in S]); T = cKDTree(XY)
out = {}; used = set()
for pid, p in P.items():
    r = 8.0 if p[0] in ('city', 'civ') else 5.0
    ks = T.query_ball_point([p[1], p[2]], r)
    if not ks: continue
    used.update(ks)
    h = sorted(((S[k], float(np.hypot(*(XY[k] - [p[1], p[2]])))) for k in ks), key=lambda t: t[1])
    out[pid] = {'n': len(h), 'r': r, 'nm': [[v['l'], v['q'], round(d, 1), v['g']] for v, d in h[:6]]}
json.dump(out, open(R + 'data/agg/at_match.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('térképhelyek', len(out), '| párosított tételek', len(used))
for pid in out:
    if P[pid][3] in ('Flavia Solva', 'Lauriacum', 'Virunum', 'Carnuntum', 'Ovilava'): print(P[pid][3], json.dumps(out[pid], ensure_ascii=False)[:300])
