# Franciaország, három nyílt forrás a térkép helyeihez (városoknál 3 km, máshol 1,5 km):
# (1) Mérimée – a műemlékként védett épületek listája (Ministère de la Culture, data.gouv.fr, Licence Ouverte 2.0), azok a tételek,
#     amelyek fő építési korszaka gallo-római, antik vagy Kr. u. 1–5. század; link: POP-adatlap.
# (2) Inrap – a megelőző feltárások válogatott helylistája (data.gouv.fr, Licence Ouverte), az „Antiquité” korszakot érintők; Lambert-93.
# (3) Párizs – Référentiel archéologique de Paris (R&CAP, Ville de Paris, ODbL), az antik leletek / beavatkozások.
# Kimenet: data/agg/fr_match.json {id: {mh: {n, nm:[[név, url, km]]}, ir: {n, nm:[[név, község, év, km]]}, pa: {n, old, nm:[[cím, jelleg, év, km]]}}}
import csv, json, glob, re, sys
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
R = '/home/claude/imperium/'; D = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/dl/fr/'
csv.field_size_limit(10**9)
tr = Transformer.from_crs('EPSG:4326', '+proj=laea +lat_0=40 +lon_0=15 +units=km', always_xy=True)
l93 = Transformer.from_crs('EPSG:2154', 'EPSG:4326', always_xy=True)
def anc(s):
    for t in s.split(';'):
        t = t.strip()
        if t in ('Gallo-romain', 'Antiquité', 'Haut-Empire', 'Bas-Empire'): return True
        m = re.search(r'(\d+)(?:er|e) siècle(.*)$', t)
        if m and int(m.group(1)) <= 5 and 'av' not in m.group(2): return True
    return False
MH = []
for r in csv.DictReader(open(D + 'merimee.csv', encoding='utf-8'), delimiter='|'):
    c = r['coordonnees_au_format_WGS84'].strip()
    if not anc(r['Siecle_de_la_campagne_principale_de_construction']) or not c: continue
    lat, lon = map(float, c.split(','))
    MH.append({'xy': tr.transform(lon, lat), 'nm': f"{r['Titre_editorial_de_la_notice'].strip()} ({r['Commune_forme_editoriale'].strip()})",
               'u': f"https://pop.culture.gouv.fr/notice/merimee/{r['Reference'].strip()}"})
IR = []
for r in csv.DictReader(open(D + 'inrap.csv', encoding='latin-1'), delimiter=';'):
    if 'Antiquit' not in r['Période(s)']: continue
    x, y = (float(re.sub(r'\s', '', r[k]).replace(',', '.')) for k in ('Coordonnée Lambert X', 'Coordonnée Lambert Y'))
    IR.append({'xy': tr.transform(*l93.transform(x, y)), 'nm': r['Nom du site'].strip(), 'c': r['Commune'].strip(), 'y': (r['Date début'] or r['Date fin'])[:4]})
PA = []
for r in csv.DictReader(open(D + 'paris.csv', encoding='utf-8-sig'), delimiter=';'):
    if r['Antiquité'] != 'Oui' or not r['geo_point_2d'].strip(): continue
    lat, lon = map(float, r['geo_point_2d'].split(','))
    PA.append({'xy': tr.transform(lon, lat), 'nm': r['Adresse'].strip(), 't': r["Nature de l'opération"].strip(), 'y': r["Date de l'opération"].strip()[:4],
               'old': r["Nature de l'opération"].strip() == 'Découverte ancienne'})
print('Mérimée ókori, koordinátával', len(MH), '| Inrap antik', len(IR), '| Párizs antik', len(PA))
P = {}
for p in json.load(open(R + 'imp_base.json'))['pts']: P[str(p[7])] = p
for f in glob.glob(R + 'tiles/*.json'):
    for p in json.load(open(f)).get('s', []): P[str(p[7])] = p
def near(S):
    if not S: return {}
    XY = np.array([s['xy'] for s in S]); T = cKDTree(XY); res = {}
    for pid, p in P.items():
        r = 3.0 if p[0] in ('city', 'civ') else 1.5
        ix = T.query_ball_point([p[1], p[2]], r)
        if ix: res[pid] = sorted(((S[k], float(np.hypot(*(XY[k] - [p[1], p[2]])))) for k in ix), key=lambda t: t[1])
    return res
out = {}
for pid, h in near(MH).items(): out.setdefault(pid, {})['mh'] = {'n': len(h), 'nm': [[s['nm'], s['u'], round(d, 1)] for s, d in h[:6]]}
for pid, h in near(IR).items(): out.setdefault(pid, {})['ir'] = {'n': len(h), 'nm': [[s['nm'], s['c'], s['y'], round(d, 1)] for s, d in h[:6]]}
for pid, h in near(PA).items():
    h2 = sorted(h, key=lambda t: (t[0]['old'], t[1]))  # a modern feltárások elöl
    out.setdefault(pid, {})['pa'] = {'n': len(h), 'old': sum(s['old'] for s, _ in h), 'nm': [[s['nm'], s['t'], s['y'], round(d, 1)] for s, d in h2[:6]]}
json.dump(out, open(R + 'data/agg/fr_match.json', 'w'), ensure_ascii=False, separators=(',', ':'))
for k in ('mh', 'ir', 'pa'): print(k, 'helyek', sum(k in v for v in out.values()))
for pid, v in out.items():
    if P[pid][3] in ('Lutetia', 'Nemausus', 'Arelate', 'Lugdunum', 'Augustodunum', 'Caesarodunum'): print(P[pid][3], json.dumps(v, ensure_ascii=False)[:420])
