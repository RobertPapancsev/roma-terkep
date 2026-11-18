# Románia: a Lista monumentelor istorice 2015 (Monitorul Oficial 113 bis/15.II.2016; hivatalos közigazgatási szöveg,
# a román szerzői jogi törvény 9. cikk b) pontja szerint nem áll szerzői jogi védelem alatt) régészeti (I. kategóriás) tételei közül
# a római kori keltezésűek („roman” a keltezésben: Epoca romană, daco-romană, romano-bizantină stb.), valamint a Kr. u.-i
# keltezésű dák (Latène / geto-dák) tételek. 31 megye (Dácia, Moesia Inferior és a Duna menti területek), data/lmi_parse.py.
# Hely: (1) a tétel Wikidata-koordinátája az LMI-kód (P1770) alapján, (2) ennek híján a fölérendelt lelőhely (kód .NN nélkül) koordinátája,
# (3) különben a falu/község Wikidata-koordinátája (SIRUTA-elemek, P843) – ez csak településnyi pontosságú.
# Párosítás: (1)-(2) városoknál 3 km, máshol 1,5 km; (3) a legközelebbi térképhely 5 km-en belül.
# Kimenet: data/agg/lmi_match.json {id: {n, r, per:[római, késő római/római–bizánci, dák (Kr. u.)], v:[településnyi pontosságú db],
#   nm:[[név, wikidata-url vagy '', km, 'e'|'v']]}}
import json, glob, re, sys, unicodedata, collections
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
R = '/home/claude/imperium/'; D = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/dl/lmi/'
tr = Transformer.from_crs('EPSG:4326', '+proj=laea +lat_0=40 +lon_0=15 +units=km', always_xy=True)
JUD = {'AB': 'Alba', 'AG': 'Argeș', 'AR': 'Arad', 'BH': 'Bihor', 'BN': 'Bistrița-Năsăud', 'BR': 'Brăila', 'BV': 'Brașov', 'BZ': 'Buzău', 'CJ': 'Cluj',
       'CL': 'Călărași', 'CS': 'Caraș-Severin', 'CT': 'Constanța', 'CV': 'Covasna', 'DB': 'Dâmbovița', 'DJ': 'Dolj', 'GJ': 'Gorj', 'GL': 'Galați', 'GR': 'Giurgiu',
       'HD': 'Hunedoara', 'HR': 'Harghita', 'IL': 'Ialomița', 'MH': 'Mehedinți', 'MS': 'Mureș', 'OT': 'Olt', 'PH': 'Prahova', 'SB': 'Sibiu', 'SJ': 'Sălaj',
       'TL': 'Tulcea', 'TM': 'Timiș', 'TR': 'Teleorman', 'VL': 'Vâlcea'}
def nz(s):
    s = s.replace('ş', 'ș').replace('Ş', 'Ș').replace('ţ', 'ț').replace('Ţ', 'Ț')
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s = re.sub(r'^(comuna|orașul|oras|municipiul|judetul)\s+', '', s.strip(), flags=re.I)
    return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()
L = json.load(open(D + 'lmi.json'))
I = [r for r in L if '-I-' in r['cod']]
def bucket(r):
    t = (r['dat'] + ' ' + r['den']).lower()
    if 'roman' in r['dat'].lower() or re.search(r'\broman[aăe]?\b|castru|villa rustica', r['den'].lower()):
        return 1 if re.search(r'bizantin|târzi|tarzi|sec\. ?(iv|v|vi)\b', t) and not re.search(r'sec\. ?(i|ii|iii) ', t) else 0
    if re.search(r'lat[eè]ne|dacic|geto', t) and 'p. chr' in t: return 2
    return None
S = [dict(r, b=bucket(r)) for r in I]; S = [r for r in S if r['b'] is not None]
WD = {}
for x in json.load(open(D + 'wd_lmi_I.json'))['results']['bindings']:
    c = x['code']['value'].strip()
    if 'c' in x and c not in WD: WD[c] = (x['i']['value'].rsplit('/', 1)[1], tuple(map(float, x['c']['value'][6:-1].split())))
SI = collections.defaultdict(list)
for x in json.load(open(D + 'wd_siruta.json'))['results']['bindings']:
    nm = nz(x['l']['value'].split(',')[0]); pa = nz(x.get('al', {}).get('value', '').split(',')[0])
    SI[nm].append((pa, tuple(map(float, x['c']['value'][6:-1].split()))))
def village(r):
    parts = [p.strip() for p in r['loc'].split(';') if p.strip()]
    m0 = re.match(r'^(sat|localitatea|oraș|oraş|municipiul|comuna|com\.)\s+(.+)$', parts[0], re.I) if parts else None
    if not m0: return None
    name = nz(m0.group(2)); parent = None
    if len(parts) > 1:
        m1 = re.match(r'^(comuna|com\.|oraș|oraş|municipiul)\s+(.+)$', parts[1], re.I); parent = nz(m1.group(2)) if m1 else None
    cand = SI.get(name, [])
    jud = nz(JUD[r['cod'].split('-')[0]])
    for want in ([parent] if parent else []) + [jud]:
        c = [ll for pa, ll in cand if pa == want]
        if len(set(c)) == 1: return c[0]
    if len({ll for _, ll in cand}) == 1: return cand[0][1]
    return None
pts = []; stat = collections.Counter()
for r in S:
    q, ll = WD.get(r['cod'], (None, None)); prec = 'e'; vl = village(r)
    def far(a): return a is not None and vl is not None and np.hypot(*np.subtract(tr.transform(*a), tr.transform(*vl))) > 15
    if far(ll): stat['wikidata-koordináta >15 km-re a településtől, elvetve'] += 1; ll = None
    if ll is None:
        par = re.sub(r'(\.\d+)+$', '', r['cod']); par = re.sub(r'-m-', '-s-', par)
        for k in (par, re.sub(r'-s-', '-m-', par)):
            if k in WD and not far(WD[k][1]): q2, ll = WD[k]; break
    if ll is None:
        ll = vl; prec = 'v'
    if ll is None: stat['nincs hely'] += 1; continue
    stat[prec] += 1
    vil = re.sub(r'^(sat|localitatea|oraș|oraş|municipiul)\s+', '', r['loc'].split(';')[0].strip(), flags=re.I).title()
    pts.append({'xy': tr.transform(*ll), 'b': r['b'], 'p': prec, 'nm': f"{r['den']} ({vil})", 'u': f'https://www.wikidata.org/wiki/{q}' if q else ''})
print('régészeti tétel', len(I), '| római/dák', len(S), collections.Counter(r['b'] for r in S), '| hely', dict(stat))
P = {}
for p in json.load(open(R + 'imp_base.json'))['pts']: P[str(p[7])] = p
for f in glob.glob(R + 'tiles/*.json'):
    for p in json.load(open(f)).get('s', []): P[str(p[7])] = p
PID = list(P); PXY = np.array([[P[k][1], P[k][2]] for k in PID]); PT = cKDTree(PXY)
E = [x for x in pts if x['p'] == 'e']; V = [x for x in pts if x['p'] == 'v']
EXY = np.array([x['xy'] for x in E]); ET = cKDTree(EXY)
hits = collections.defaultdict(list)
for pid in PID:
    p = P[pid]; r = 3.0 if p[0] in ('city', 'civ') else 1.5
    for k in ET.query_ball_point([p[1], p[2]], r): hits[pid].append((E[k], float(np.hypot(*(EXY[k] - [p[1], p[2]])))))
nv = 0
for x in V:
    d, k = PT.query(x['xy'])
    if d <= 5.0: hits[PID[k]].append((x, float(d))); nv += 1
out = {}
for pid, h in hits.items():
    p = P[pid]; h.sort(key=lambda t: (t[0]['p'] != 'e', t[0]['b'] == 2, t[1]))
    out[pid] = {'n': len(h), 'r': 3.0 if p[0] in ('city', 'civ') else 1.5, 'per': [sum(t[0]['b'] == b for t in h) for b in range(3)],
                'v': sum(t[0]['p'] == 'v' for t in h), 'nm': [[t[0]['nm'], t[0]['u'], round(t[1], 1), t[0]['p']] for t in h[:6]]}
json.dump(out, open(R + 'data/agg/lmi_match.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('térképhelyek', len(out), '| pontos helyű tételek párosítva', len({id(t[0]) for h in hits.values() for t in h if t[0]['p'] == 'e'}), 'a', len(E), '-ből | településnyi', nv, 'a', len(V), '-ből')
for pid in out:
    if P[pid][3] in ('Apulum', 'Porolissum', 'Sarmizegetusa', 'Ulpia Traiana Sarmizegetusa', 'Drobeta', 'Romula', 'Tomis', 'Histria', 'Troesmis', 'Potaissa', 'Napoca', 'Sucidava'):
        print(P[pid][3], json.dumps(out[pid], ensure_ascii=False)[:300])
