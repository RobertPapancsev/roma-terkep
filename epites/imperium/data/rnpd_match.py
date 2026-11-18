# Szlovénia: a kulturális örökség nyilvántartásának (RNPD, podatki.gov.si, CC BY 4.0) római keltezésű tételei a térkép helyeihez.
# Római tétel: a DATACIJA mezőben szerepel a „rimska doba” (zgodnja / pozna / általános). Városoknál 3 km, máshol 1,5 km-en belül.
# Kategória: a GESLA (kulcsszavak) első besorolható eleme, a GNA-kártya kategóriáival azonos kulcsokkal.
# Kimenet: data/agg/rnpd_match.json {id: {n, r, per:[korai, római (közelebbről nem keltezett), késő], c:[[kat,n]], nm:[[név, url, km]]}}
import csv, json, glob, re, sys, collections
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
R = '/home/claude/imperium/'
csv.field_size_limit(10**9)
tr = Transformer.from_crs('EPSG:4326', '+proj=laea +lat_0=40 +lon_0=15 +units=km', always_xy=True)
rows = [r for r in csv.DictReader(open(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/dl/si/rnpd.csv', encoding='utf-8-sig'))
        if 'rimsk' in r['DATACIJA'].lower() and r['X'] and r['Y']]
CAT = [('villa', r'villa'), ('fort', r'^(kastel|castra|utrdba|zaporni zid|dolinska zapora|vojaški tabor|tabor|postojanka|refugij|obrambn|obzidje|mestno obzidje|stolp)'),
       ('public', r'^(terme|insula|forum|amfiteater|mozaik|hipokavst|mestno jedro|ulica|trg)'),
       ('cult', r'^(svetišče|mitrej|tempelj|krstilnica)'), ('water', r'^(vodovod|vodnjak|cisterna|kanal|vodni)'),
       ('harbour', r'^(pristanišče|ladja|deblak)'), ('craft', r'^(talilnica|talilna peč|opekarna|kamnolom|lončarska peč|steklarska peč|rudnik|železokop|apnenica|kovačija|peč)'),
       ('road', r'^(cesta|obcestna postaja|most|miljnik|pot|vlečna pot|tovorniška pot|mitnica|postaja)$'),
       ('coin', r'^(depo|zakladna najdba)'), ('inscr', r'^(napis|spolija|lapidarij)'),
       ('burial', r'(grob|gomila|žara|pokop|nagrobnik|sarkofag|nekropola|pepelnica|pokopališče|grobnica)'),
       ('settl', r'^(naselbina|vicus|gradišče|kaštelir|gradec|stavba|zemljanka|jamska postojanka|jamsko najdišče|vas|zaselek)'),
       ('finds', r'^(posamična najdba)')]
def cat(g):
    for t in g.split(','):
        t = t.strip().lower()
        for k, rx in CAT:
            if re.search(rx, t): return k
    return 'other'
XY = np.array([tr.transform(float(r['X']), float(r['Y'])) for r in rows]); T = cKDTree(XY)
CA = [cat(r['GESLA']) for r in rows]
PE = [(('zgodnja rimska' in r['DATACIJA']), bool(re.search(r'(^|,\s*)rimska doba', r['DATACIJA'])), ('pozna rimska' in r['DATACIJA'])) for r in rows]
P = {}
for p in json.load(open(R + 'imp_base.json'))['pts']: P[p[7]] = p
for f in glob.glob(R + 'tiles/*.json'):
    for p in json.load(open(f)).get('s', []): P[p[7]] = p
out = {}
for pid, p in P.items():
    r = 3.0 if p[0] in ('city', 'civ') else 1.5
    ix = T.query_ball_point([p[1], p[2]], r)
    if not ix: continue
    d = {k: float(np.hypot(*(XY[k] - [p[1], p[2]]))) for k in ix}
    ix.sort(key=lambda k: (CA[k] in ('other', 'finds'), d[k]))  # a besorolható (építmény jellegű) tételek elöl
    c = collections.Counter(CA[k] for k in ix)
    out[str(pid)] = {'n': len(ix), 'r': r, 'per': [sum(PE[k][j] for k in ix) for j in range(3)],
                     'c': [[k, v] for k, v in c.most_common()],
                     'nm': [[rows[k]['IME'].strip(), rows[k]['QR'] or 'https://eid.gov.si/S/' + rows[k]['ESD'], round(d[k], 1)] for k in ix[:6]]}
json.dump(out, open(R + 'data/agg/rnpd_match.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('római tételek', len(rows), '| kategóriák', collections.Counter(CA).most_common(), '| térképhelyek', len(out), '| párosított tételek', len({k for p in P.values() for k in T.query_ball_point([p[1], p[2]], 3.0 if p[0] in ('city','civ') else 1.5)}))
for pid, p in P.items():
    if p[3] in ('Emona', 'Celeia', 'Poetovio', 'Neviodunum', 'Nauportus') and str(pid) in out: print(p[3], json.dumps(out[str(pid)], ensure_ascii=False)[:400])
