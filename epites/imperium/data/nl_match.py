# Hollandia: a Rijksdienst voor het Cultureel Erfgoed (RCE) linked open data (CC BY 4.0) régészeti rijksmonumentjai
# (heeftMonumentAard = archeologisch; 1496 tétel koordinátával), SPARQL 2026-11-13 (dl/nl/nl_arch.json).
# Római: a hivatal leírásában »Romein…« / castellum / limes, a »voor-Romeinse (IJzertijd)« és »na-Romeins« említések nélkül.
# Megjelenítés: a leírás első mondata (a »Datering« előtt, legfeljebb 120 karakter) + a keltezés; link a műemlékregiszterre.
# Körzet: városoknál 8, máshol 5 km. Kimenet: data/agg/nl_match.json {id: {n, r, nm:[[rövid leírás, keltezés, nr, km]]}}
import json, glob, re, sys
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
R = '/home/claude/imperium/'; F = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/dl/nl/nl_arch.json'
tr = Transformer.from_crs('EPSG:4326', '+proj=laea +lat_0=40 +lon_0=15 +units=km', always_xy=True)
def roman(o):
    o2 = re.sub(r'(voor|na)[- ]romeins\w*', '', o, flags=re.I)
    return re.search(r'romein|castell|limes', o2, re.I)
def short(o):
    o = re.sub(r'\s+', ' ', o.split('|||')[0]).strip()
    s = re.split(r'\.\s|\s*Datering:', o)[0].strip().rstrip('.')
    s = re.sub(r'\b([A-Z]{3,})\b', lambda m: m.group(1).capitalize(), s)
    return s if len(s) <= 120 else s[:117].rsplit(' ', 1)[0] + '…'
def dat(o):
    o = re.sub(r'\b([vn])\. ?Chr\.?', r'\1. Chr', o); o = re.sub(r'\b(plm|ca|c)\.', r'\1', o)
    o = o.replace('. Chr', '\u2009Chr')
    m = re.search(r'Datering:\s*(.*?)(?:\.\s+[A-Z(]|\.?\s*\(|\.?\s*$|\s*\|\|\|)', o); return re.sub(r'Chr(?=\w)', 'Chr. ', m.group(1).strip(' -.').replace('\u2009', '. ')) if m else ''
S = []
for x in json.load(open(F))['results']['bindings']:
    o = x['om']['value']
    if not roman(o) or 'w' not in x: continue
    nums = [float(v) for v in re.findall(r'-?\d+\.\d+', x['w']['value'])]
    lon = np.mean(nums[0::2]); lat = np.mean(nums[1::2])
    S.append({'nr': x['nr']['value'], 's': short(o), 'd': dat(o), 'xy': tr.transform(lon, lat)})
print('római régészeti rijksmonument', len(S))
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
    h = sorted(((S[k], float(np.hypot(*(XY[k] - [p[1], p[2]])))) for k in ks), key=lambda t: t[1])
    out[pid] = {'n': len(h), 'r': r, 'nm': [[s['s'], s['d'], s['nr'], round(d, 1)] for s, d in h[:6]]}
json.dump(out, open(R + 'data/agg/nl_match.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('térképhelyek', len(out), '| párosított tételek', len(used))
for pid in out:
    if P[pid][3] in ('Noviomagus', 'Ulpia Noviomagus', 'Traiectum', 'Fectio', 'Forum Hadriani', 'Albaniana', 'Praetorium Agrippinae', 'Coriovallum'):
        print(P[pid][3], json.dumps(out[pid], ensure_ascii=False)[:400])
