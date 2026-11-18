# Brit-szigetek: a védett régészeti emlékek (scheduled monuments) hivatalos listái, Open Government Licence v3.0.
# Anglia: Historic England (planning.data.gov.uk scheduled-monument.csv) – korszakmező nincs, a név alapján: Roman (nem Roman Catholic),
#   Romano(-British), Hadrian, Antonine, vicus, castra, Saxon Shore. Skócia: Historic Environment Scotland (sam_scotland.zip) – a név
#   vagy a kategória alapján (Roman, Romano, Antonine, Agricola, Gask, fortlet, temporary camp). Wales: Cadw (DataMapWales WFS, Cadw_SAM) – Period = Roman.
# Városoknál 3 km, máshol 1,5 km. Kimenet: data/agg/uk_match.json {id: {n, nm:[[név, url, km]]}}
import csv, json, glob, re, sys
import numpy as np, shapefile
from pyproj import Transformer
from scipy.spatial import cKDTree
R = '/home/claude/imperium/'; D = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/dl/uk/'
csv.field_size_limit(10**9)
tr = Transformer.from_crs('EPSG:4326', '+proj=laea +lat_0=40 +lon_0=15 +units=km', always_xy=True)
bng = Transformer.from_crs('EPSG:27700', 'EPSG:4326', always_xy=True)
S = []; cnt = {}
RX = re.compile(r'\bRoman\b(?! Catholic)|Romano|Hadrian|Antonine|\bvicus\b|\bcastra\b|Saxon Shore', re.I)
for r in csv.DictReader(open(D + 'sm_eng.csv', encoding='utf-8')):
    if not RX.search(r['name']) or not r['point'].strip(): continue
    lon, lat = map(float, r['point'].strip()[7:-1].split())
    S.append({'xy': tr.transform(lon, lat), 'nm': r['name'].strip(), 'u': r['documentation-url'] or f"https://historicengland.org.uk/listing/the-list/list-entry/{r['reference']}"})
cnt['eng'] = len(S)
sh = shapefile.Reader(D + 'hes/Scheduled_Monuments')
F = [f[0] for f in sh.fields[1:]]
RXS = re.compile(r'\bRoman\b(?! Catholic)|Romano|Antonine|Agricol|\bGask\b|fortlet|temporary camp', re.I)
for rec in sh.records():
    x = dict(zip(F, rec))
    if not RXS.search(f"{x['DES_TITLE']} {x['CATEGORY']}"): continue
    S.append({'xy': tr.transform(*bng.transform(x['X'], x['Y'])), 'nm': x['DES_TITLE'].strip(), 'u': x['LINK'].strip()})
cnt['sco'] = len(S) - cnt['eng']
for f in json.load(open(D + 'cadw.json'))['features']:
    p = f['properties']
    if p['Period'] != 'Roman': continue
    if p['easting'] is not None: ll = bng.transform(p['easting'], p['northing'])
    else:  # néhány tételnél nincs megadva a középpont: a körvonal pontjainak átlaga (a WFS-ből EPSG:4326, hossz–szél sorrendben)
        cs = np.array(re.findall(r'-?\d+\.\d+', json.dumps(f['geometry']['coordinates'])), float).reshape(-1, 2); ll = tuple(cs.mean(0))
    S.append({'xy': tr.transform(*ll), 'nm': f"{p['Name'].strip()} ({p['SiteType'].strip()})",
              'u': f"https://cadwpublic-api.azurewebsites.net/reports/sam/FullReport?lang=en&id={p['RecordNumber']}"})
cnt['wal'] = len(S) - cnt['eng'] - cnt['sco']
print('római védett emlékek', cnt)
P = {}
for p in json.load(open(R + 'imp_base.json'))['pts']: P[str(p[7])] = p
for f in glob.glob(R + 'tiles/*.json'):
    for p in json.load(open(f)).get('s', []): P[str(p[7])] = p
XY = np.array([s['xy'] for s in S]); T = cKDTree(XY); out = {}; used = set()
for pid, p in P.items():
    r = 3.0 if p[0] in ('city', 'civ') else 1.5
    ix = T.query_ball_point([p[1], p[2]], r)
    if not ix: continue
    used.update(ix)
    h = sorted(((S[k], float(np.hypot(*(XY[k] - [p[1], p[2]])))) for k in ix), key=lambda t: t[1])
    out[pid] = {'n': len(h), 'nm': [[s['nm'], s['u'], round(d, 1)] for s, d in h[:6]]}
json.dump(out, open(R + 'data/agg/uk_match.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('térképhelyek', len(out), '| megjelenő emlékek', len(used), 'a', len(S), '-ből')
for pid in out:
    if P[pid][3] in ('Londinium', 'Eboracum', 'Deva', 'Isca', 'Camulodunum', 'Verulamium', 'Vindolanda', 'Calleva'): print(P[pid][3], json.dumps(out[pid], ensure_ascii=False)[:300])
