# Bajorország: a Bayerisches Landesamt für Denkmalpflege (BLfD) Bodendenkmal-listája (D-x-xxxx-xxxx azonosítók)
# a Wikidatán keresztül (P4244 + P625 koordináta + német leírás; Wikidata CC0). Lekérés: 2026-11-13.
# Csak a római kori tételek: a leírásban „römisch / Kaiserzeit / Spätantike / Villa rustica / Kastell / Burgus / Limes / Vicus”.
# A BLfD leírásai CC BY-ND alatt vannak (keine Bearbeitung), ezért a térképre csak saját besorolás és darabszám kerül,
# a tételekhez Wikidata-link; a leírásokat nem vesszük át.
# Besorolás: a leírásban a római korszakmegjelölés előtti utolsó típusszó (Siedlung, Villa, Kastell, Straße, Gräber …);
# ha nincs ilyen, a közvetlenül utána álló szó (pl. „römische Inntalstraße”).
# Időszak: korai (frühe/ältere/mittlere römische Kaiserzeit), késő (späte/jüngere, spätrömisch, Spätantike), egyébként általános.
# Körzet (vidéki lelőhelyek, mint az RRSP-nél): városoknál 8 km, máshol 5 km.
# Kimenet: data/agg/by_match.json {id: {n, r, t:[[kat, db]], per:[korai, általános, késő], nm:[[kat, település, wikidata-Q, km, BLfD-azonosító]]}}
import json, glob, re, sys, collections
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
R = '/home/claude/imperium/'; F = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/dl/de/wd/by_rom2.json'
tr = Transformer.from_crs('EPSG:4326', '+proj=laea +lat_0=40 +lon_0=15 +units=km', always_xy=True)
CAT = [('mil', r'kastell|burgus|lager|wachtt?urm|wachtposten|limes|militär|befestigung|schanze'),
       ('vil', r'villa|gutshof|landgut'), ('vic', r'vicus|zivilsiedlung|stadt\b|städt|ortschaft|municipium'),
       ('kult', r'heiligtum|tempel|kult(?!ur)|mithr|weihe'), ('gr', r'grab|gräber|bestattung|nekropole|friedhof'),
       ('ind', r'töpfer|ofen|öfen|ziegel|werkstatt|handwerk|steinbruch|bergbau|schmiede|kalkbrenn|verhüttung|materialentnahme|tongrube'),
       ('str', r'straße|strasse|brücke|meilenstein'), ('sie', r'siedlung|gebäude|hof\b|höfe|bauten|ansiedlung'),
       ('fu', r'fund|depot|hort|münz')]
ROM = r'römisch|villa rustica|kastell|burgus|limes|vicus|spätantik|kaiserzeit'
ALL = '|'.join('(?P<%s>%s)' % (k, r) for k, r in CAT)
def classify(t):
    tl = t.lower(); cats = set()
    for s in re.split(r'(?<=[a-zäöüß)]{3}[.;])\s+(?=[A-ZÄÖÜa-z])', tl):
        for m in re.finditer(ROM, s):
            last = None
            for mm in re.finditer(ALL, s[:m.end()]): last = mm
            if last is None:
                mm = re.search(ALL, s[m.start():m.end() + 40])
                last = mm
            if last: cats.add(last.lastgroup)
    return cats or {'oth'}
def period(t):
    tl = t.lower()
    late = re.search(r'(späte[nrs]?|jüngere[nrs]?)\s+(und\s+späten\s+)?(römisch|kaiserzeit)|spätrömisch|spätantik', tl)
    early = re.search(r'(frühe[nrs]?|ältere[nrs]?|mittlere[nrs]?)\s+(römisch|kaiserzeit)|frührömisch', tl)
    if late and not early: return 2
    if early and not late: return 0
    return 1
it = {}
for x in json.load(open(F))['results']['bindings']:
    q = x['i']['value'].rsplit('/', 1)[1]
    if q in it:
        if 'gl' in x and not it[q]['g']: it[q]['g'] = x['gl']['value']
        continue
    lon, lat = map(float, x['c']['value'][6:-1].split())
    it[q] = {'q': q, 'id': x['id']['value'], 'd': x['d']['value'], 'g': x.get('gl', {}).get('value', ''), 'xy': tr.transform(lon, lat)}
S = [v for v in it.values() if re.search(ROM, v['d'], re.I)]
for v in S: v['c'] = sorted(classify(v['d'])); v['p'] = period(v['d'])
cc = collections.Counter(k for v in S for k in v['c'])
print('tétel', len(it), '| római kori', len(S), dict(cc), '| időszak', collections.Counter(v['p'] for v in S))
P = {}
for p in json.load(open(R + 'imp_base.json'))['pts']: P[str(p[7])] = p
for f in glob.glob(R + 'tiles/*.json'):
    for p in json.load(open(f)).get('s', []): P[str(p[7])] = p
XY = np.array([v['xy'] for v in S]); T = cKDTree(XY)
ORD = ['mil', 'vic', 'vil', 'kult', 'sie', 'gr', 'ind', 'str', 'fu', 'oth']
out = {}; used = set()
for pid, p in P.items():
    r = 8.0 if p[0] in ('city', 'civ') else 5.0
    ks = T.query_ball_point([p[1], p[2]], r)
    if not ks: continue
    used.update(ks)
    h = sorted(((S[k], float(np.hypot(*(XY[k] - [p[1], p[2]])))) for k in ks), key=lambda t: (ORD.index(t[0]['c'][0]) if t[0]['c'][0] in ORD else 9, t[1]))
    tc = collections.Counter(k for v, _ in h for k in v['c'])
    show = sorted(h, key=lambda t: (min(ORD.index(c) for c in t[0]['c']), t[1]))[:6]
    out[pid] = {'n': len(h), 'r': r, 't': [[k, tc[k]] for k in ORD if tc[k]], 'per': [sum(v['p'] == b for v, _ in h) for b in range(3)],
                'nm': [[min(v['c'], key=ORD.index), v['g'], v['q'], round(d, 1), v['id']] for v, d in show]}
json.dump(out, open(R + 'data/agg/by_match.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('térképhelyek', len(out), '| párosított tételek', len(used))
for pid in out:
    if P[pid][3] in ('Augusta Vindelicum', 'Castra Regina', 'Cambodunum', 'Abusina', 'Guntia', 'Batavis', 'Biriciana'):
        print(P[pid][3], json.dumps(out[pid], ensure_ascii=False)[:400])
