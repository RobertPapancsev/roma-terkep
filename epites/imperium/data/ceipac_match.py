# CEIPAC – Roman Open Data (romanopendata.eu, SPARQL-lekérdezés 2026. november 12-én; a Róma-térképhez letöltött állomány).
# Kifejezett adatlicencet nem találtam, ezért csak saját összesítés kerül a térképre (darabszámok, típusok), mint a Róma-térképen.
# A feliratos amforák lelőhelye a CEIPAC helyhierarchiájában az első koordinátás szint (település); minden település a legközelebbi
# városhoz / civitas-központhoz / légiós táborhoz / erődhöz kerül 8 km-en belül, ennek hiányában bármely helyhez 3 km-en belül,
# így egy amfora csak egy térképhelynél számít. Kimenet: data/agg/ceipac_match.json {id: {n, st, tp, ty:[[típus,db]]}}
import json, glob, collections
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
exec(open('/home/claude/dl/ceipac/load.py').read())
R = '/home/claude/imperium/'
tr = Transformer.from_crs('EPSG:4326', '+proj=laea +lat_0=40 +lon_0=15 +units=km', always_xy=True)
def coord(p, seen=None):
    seen = seen or set()
    if p in PLL: return PLL[p], p
    for w in PW.get(p, ()):
        if w in seen or 'Country' in PC.get(w, set()): continue
        seen.add(w); r = coord(w, seen)
        if r: return r
    return None
# típusok: csak a közismert, egyértelmű típusok kapnak nevet; a többi „egyéb”
TY = {'dressel_20': 'd20', 'AmphoricType-DR20': 'd20', 'brindisian_amphora': 'brin', 'dressel_2-4_catalan': 'd24c', 'AmphoricType-DR2-4': 'd24',
      'pascual_1': 'pas1', 'AmphoricType-DR1': 'd1', 'AmphoricType-DR1+ITA': 'd1', 'AmphoricType-DR1B': 'd1', 'dressel_6a': 'd6a', 'dressel_6b': 'd6b',
      'AmphoricType-DR6B+HST': 'd6b', 'AmphoricType-LA2': 'la2', 'AmphoricType-LA2+ITA': 'la2', 'gauloise_4': 'g4'}
P = {}
for p in json.load(open(R + 'imp_base.json'))['pts']: P[p[7]] = p
for f in glob.glob(R + 'tiles/*.json'):
    for p in json.load(open(f)).get('s', []): P[p[7]] = p
ids = list(P); XY = np.array([[P[i][1], P[i][2]] for i in ids]); BIG = np.array([P[i][0] in ('city', 'civ', 'leg', 'fort') for i in ids])
TB = cKDTree(XY[BIG]); TA = cKDTree(XY); idB = [i for i, b in zip(ids, BIG) if b]
agg = collections.defaultdict(lambda: {'n': 0, 'st': 0, 'tp': 0, 'ty': collections.Counter()}); st = collections.Counter(); cache = {}
for a, r in AM.items():
    if not r['fp']: st['nincs_lelohely'] += 1; continue
    c = coord(r['fp'])
    if not c: st['nincs_koordinata'] += 1; continue
    (la, lo), pl = c
    if pl not in cache:
        x, y = tr.transform(lo, la); d, k = TB.query([x, y])
        if d <= 8: cache[pl] = idB[k]
        else:
            d2, k2 = TA.query([x, y]); cache[pl] = ids[k2] if d2 <= 3 else None
    pid = cache[pl]
    if not pid: st['nincs_terkephely'] += 1; continue
    o = agg[pid]; o['n'] += 1; st['ok'] += 1
    kinds = {IN[i]['kind'] for i in r['insc'] if i in IN}
    if 'Stamp' in kinds: o['st'] += 1
    if 'Titulus pictus' in kinds: o['tp'] += 1
    t = {TY.get(x.split('/')[-1]) for x in r['type']} - {None}
    o['ty'][next(iter(t)) if len(t) == 1 else 'oth'] += 1
out = {}
for pid, o in agg.items():
    out[str(pid)] = {'n': o['n'], 'st': o['st'], 'tp': o['tp'], 'ty': [[k, v] for k, v in o['ty'].most_common() if k != 'oth'][:6] + ([['oth', o['ty']['oth']]] if o['ty']['oth'] else [])}
json.dump(out, open(R + 'data/agg/ceipac_match.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print(dict(st), 'helyek', len(out))
for k, v in sorted(out.items(), key=lambda kv: -kv[1]['n'])[:12]: print(P[k][3], P[k][4], v)
