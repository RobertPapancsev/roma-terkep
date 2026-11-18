# Geoportale Nazionale per l'Archeologia (MiC – Istituto Centrale per l'Archeologia), MOSI-rekordok (CC BY 4.0), WFS-letöltés 2026. november 13.
# Római kori rekordok: a „DTR” (keltezés) mezőben „Età Roman…” vagy „Età Tardoantica”. A „régészeti nyomok nélküli” rekordok kimaradnak.
# Hozzárendelés: a térkép helyeitől 3 km-en belül (városoknál, civitas-központoknál), máshol 1,5 km-en belül; a rekord helye a pont,
# illetve a terület/vonal befoglaló téglalapjának közepe. Kimenet: data/agg/gna_match.json {id: {n, c:[[kat,db]], nm:[[név,kat]]}}
import json, glob, re, collections
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
R = '/home/claude/imperium/'
tr = Transformer.from_crs('EPSG:4326', '+proj=laea +lat_0=40 +lon_0=15 +units=km', always_xy=True)
def cat(r):
    o = (r.get('OGT', '') + ' ' + r.get('OGN', '')).lower(); d = r.get('OGD', '').lower(); m = r.get('OGD_MACRO_value', '')
    if 'relitt' in o or 'giacimento subacqueo' in d: return 'wreck'
    if re.search(r'\bvill[ae]\b|azienda agricola|fattoria', o): return 'villa'
    if m == 'AREA FUNERARIA': return 'burial'
    if m == 'INFRASTRUTTURA VIARIA' or re.search(r'\bmansio|mutatio|stazione di sosta', o): return 'road'
    if m == 'INFRASTRUTTURA IDRICA': return 'harbour' if re.search(r'porto|banchina|molo', o) else 'water'
    if re.search(r'culto|santuario|tempio|sacello|mitreo', o) or 'culto' in d: return 'cult'
    if re.search(r'terme|termale|teatro|anfiteatro|foro\b|basilica|circo', o) or 'uso pubblico' in d: return 'public'
    if re.search(r'fornac|produtt|officin|cava\b|miniera|torchio', o) or 'attività produttiva' in d: return 'craft'
    if re.search(r'fortific|castr|cinta|mura\b|torre', o) or 'fortificazione' in d: return 'fort'
    if re.search(r'numismatic|ripostiglio|monet|tesoretto', o): return 'coin'
    if 'epigrafe' in o or 'iscrizion' in o: return 'inscr'
    if m == 'INSEDIAMENTO' or re.search(r'domus|abitazion|insediament|villaggio|edifici', o) or 'struttura abitativa' in d: return 'settl'
    if m == 'INFRASTRUTTURA AGRICOLA' or 'centuriazion' in o: return 'agri'
    if m == 'EVIDENZA DI FREQUENTAZIONE': return 'finds'
    return 'other'
ROM = re.compile(r'Età Roman|Età Tardoantica')
G = []; st = collections.Counter()
for f in ('MOSI_multipoint', 'MOSI_multipolygon', 'MOSI_multilinea'):
    fn = '/home/claude/dl/gna/%s.jsonl' % f
    if not __import__('os').path.exists(fn): print('HIÁNYZIK', f); continue
    for line in open(fn):
        r = json.loads(line); st['osszes'] += 1
        if 'lat' not in r or not ROM.search(r.get('DTR', '')): continue
        if r.get('OGD_MACRO_value') in ('AREA PRIVA DI TRACCE ARCHEOLOGICHE', 'GIACIMENTO PALEONTOLOGICO'): continue
        st['romai'] += 1; G.append((tr.transform(r['lon'], r['lat']), cat(r), (r.get('OGN') or '').strip(), r['gid']))
XY = np.array([g[0] for g in G]); T = cKDTree(XY)
P = {}
for p in json.load(open(R + 'imp_base.json'))['pts']: P[p[7]] = p
for f in glob.glob(R + 'tiles/*.json'):
    for p in json.load(open(f)).get('s', []): P[p[7]] = p
ORD = ['villa', 'settl', 'burial', 'road', 'water', 'harbour', 'cult', 'public', 'craft', 'fort', 'agri', 'wreck', 'coin', 'inscr', 'finds', 'other']
NAMED = {'villa', 'cult', 'public', 'fort', 'harbour', 'wreck', 'craft'}
GENERIC = re.compile(r'^(?:villa|tomba|tombe|necropoli|strada|ponte|cisterna|area di frammenti.*|tracce di insediamento|frammenti.*|[\d\s\-_.,/]+|punto.*|sito.*|ut\s*\d.*|us\s*\d.*|saggio.*|anomalia.*)$', re.I)
out = {}
for pid, p in P.items():
    r = 3.0 if p[0] in ('city', 'civ') else 1.5
    ix = T.query_ball_point([p[1], p[2]], r)
    if not ix: continue
    c = collections.Counter(G[k][1] for k in ix)
    nm = []; seen = set()
    for k in sorted(ix, key=lambda k: np.hypot(*(XY[k] - [p[1], p[2]]))):
        n, ct = G[k][2], G[k][1]
        if ct in NAMED and n and not GENERIC.match(n) and n.lower() not in seen and len(n) <= 70:
            seen.add(n.lower()); nm.append([n, ct])
        if len(nm) >= 8: break
    o = {'n': len(ix), 'c': [[k, c[k]] for k in ORD if c[k]], 'r': r}
    if nm: o['nm'] = nm
    out[str(pid)] = o
json.dump(out, open(R + 'data/agg/gna_match.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print(dict(st), 'római rekordok helye', len(G), '| térképhelyek GNA-adattal', len(out))
print(collections.Counter(g[1] for g in G).most_common())
for nm_ in ('Ostia', 'Aquileia', 'Luna', 'Paestum'):
    for pid, p in P.items():
        if p[3] == nm_ and str(pid) in out: print(nm_, out[str(pid)])
