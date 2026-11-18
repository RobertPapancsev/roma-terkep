# Svájc: a BABS KGS-Inventar (nemzeti jelentőségű kulturális javak, 2021-es kiadás; adat 2026-09-28) INTERLIS-fájlja
# (data.geo.admin.ch, ch.babs.kulturgueter; szövetségi OGD: szabad felhasználás, forrásmegjelöléssel).
# Csak a »Römische Zeit« objektumtípusú tételek (167). Koordináta: LV95 (EPSG:2056) pontkoordináta.
# Körzet: városoknál 8, máshol 5 km. Kimenet: data/agg/ch_match.json {id: {n, r, nm:[[leírás, link vagy '', km, község, KGS-szám]]}}
import json, glob, re, sys, html
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
R = '/home/claude/imperium/'; D = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/dl/ch/x/'
tr = Transformer.from_crs('EPSG:2056', '+proj=laea +lat_0=40 +lon_0=15 +units=km', always_xy=True)
t = open(glob.glob(D + 'ID65*.xtf')[0], encoding='utf-8').read()
c = open(D + 'KGS_PBC_Catalogues_V2_2.xml', encoding='utf-8').read()
cat = {}
for m in re.finditer(r'TID="([^"]+)".*?</KGS_PBC_V2_2[^>]*>', c, re.S):
    cat[m.group(1)] = (re.findall(r'<Text>([^<]*)</Text>', m.group(0)) or [''])[0]
LK = {}
for m in re.finditer(r'<Weblink>([^<]*)</Weblink>.*?<R1_KGSobj REF="([^"]+)"', t):
    LK.setdefault(m.group(2), html.unescape(m.group(1)))
S = []
for m in re.finditer(r'<KGS_PBC_V2_2.KGS_Inventar.KGS_Objekt TID="([^"]+)">(.*?)</KGS_PBC_V2_2.KGS_Inventar.KGS_Objekt>', t, re.S):
    b = m.group(2); g = lambda k: html.unescape((re.search(r'<%s>([^<]*)</%s>' % (k, k), b) or [None, ''])[1])
    if 'Römische Zeit' not in [cat.get(r, '') for r in re.findall(r'Objektarten_CatRef><Reference REF="([^"]+)"', b)]: continue
    S.append({'id': g('Objekt_Nr'), 'd': g('Beschreibung'), 'g': g('Gemeinde'), 'u': LK.get(m.group(1), ''),
              'xy': tr.transform(float(g('C1')), float(g('C2')))})
print('római KGS-tétel', len(S), '| linkkel', sum(bool(s['u']) for s in S))
P = {}
for p in json.load(open(R + 'imp_base.json'))['pts']: P[str(p[7])] = p
for f in glob.glob(R + 'tiles/*.json'):
    for p in json.load(open(f)).get('s', []): P[str(p[7])] = p
XY = np.array([s['xy'] for s in S]); T = cKDTree(XY)
out = {}; used = set()
for pid, p in P.items():
    r = 8.0 if p[0] in ('city', 'civ') else 5.0
    ks = T.query_ball_point([p[1], p[2]], r)
    if not ks: continue
    used.update(ks)
    h = sorted(((S[k], float(np.hypot(*(XY[k] - [p[1], p[2]])))) for k in ks), key=lambda x: x[1])
    out[pid] = {'n': len(h), 'r': r, 'nm': [[s['d'], s['u'], round(d, 1), s['g'], s['id']] for s, d in h[:6]]}
json.dump(out, open(R + 'data/agg/ch_match.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('térképhelyek', len(out), '| párosított tételek', len(used))
for pid in out:
    if P[pid][3] in ('Vindonissa', 'Aventicum', 'Augusta Raurica', 'Noviodunum', 'Lousonna', 'Curia'): print(P[pid][3], json.dumps(out[pid], ensure_ascii=False)[:350])
