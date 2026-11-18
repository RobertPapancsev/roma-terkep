# Britannia vidéki települései: The Rural Settlement of Roman Britain (Allen, Blick, Brindle, Evans, Fulford, Holbrook, Lodwick, Richards, Smith 2015/2018,
# ADS doi:10.5284/1030449; ADS Terms of Use and Access). A licenc nem nyílt, ezért csak saját összesítés szerepel: helyenként a feltárt lelőhelyek
# száma altípus-csoportok szerint és az ott talált érmek száma; nevek, leírások nem. Koordináták: X_REF_MAP / Y_REF_MAP (OSGB, EPSG:27700).
# Vidéki településekről van szó, ezért nagyobb körzet: városoknál 8 km, máshol 5 km (egy lelőhely több helynél is számíthat). Kimenet: data/agg/rrsp_match.json {id: {n, r, t:[[csoport, n]], c, cn}}
import csv, json, glob, sys, collections
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
R = '/home/claude/imperium/'; D = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/dl/rrsp/'
csv.field_size_limit(10**9)
tr = Transformer.from_crs('EPSG:4326', '+proj=laea +lat_0=40 +lon_0=15 +units=km', always_xy=True)
bng = Transformer.from_crs('EPSG:27700', 'EPSG:4326', always_xy=True)
def rd(f):
    for enc in ('utf-8-sig', 'latin-1'):
        try: return list(csv.DictReader(open(D + f, encoding=enc)))
        except UnicodeDecodeError: pass
GRP = {'farm': 'farm', 'villa': 'villa', 'roadside settlement': 'nuc', 'village': 'nuc', 'vicus': 'nuc', "walled 'small town'": 'nuc', "unwalled 'small town'": 'nuc',
       'mansio': 'nuc', 'shrine': 'cult', 'RC temple': 'cult', 'funerary site': 'fun', 'fort': 'mil', 'other military': 'mil',
       'pottery production': 'ind', 'tile production': 'ind', 'iron production': 'ind', 'other metal production': 'ind', 'salt production': 'ind',
       'quarry': 'ind', 'other industry': 'ind', 'mill': 'ind', 'field system': 'agr', 'agricultural building': 'agr'}
core = {r['ID']: r for r in rd('rrs_core_data.csv')}
types = collections.defaultdict(set)
for r in rd('rrs_site_t_minor.csv'):
    g = GRP.get(r['SITE_TYPE_MINOR'].strip())
    if g: types[r['ID']].add(g)
coins = {}
for r in rd('rrs_coins_data.csv'):
    try: coins[r['ID']] = int(float(r.get('COINS_TOTAL') or 0))
    except ValueError: coins[r['ID']] = 0
S = []
for i, r in core.items():
    try: x, y = float(r['X_REF_MAP']), float(r['Y_REF_MAP'])
    except ValueError: continue
    S.append({'xy': tr.transform(*bng.transform(x, y)), 't': types.get(i, set()), 'c': coins.get(i, 0)})
print('lelőhely', len(core), '| koordinátával', len(S), '| éremmel', sum(1 for s in S if s['c'] > 0), '| érem összesen', sum(s['c'] for s in S))
P = {}
for p in json.load(open(R + 'imp_base.json'))['pts']: P[str(p[7])] = p
for f in glob.glob(R + 'tiles/*.json'):
    for p in json.load(open(f)).get('s', []): P[str(p[7])] = p
XY = np.array([s['xy'] for s in S]); T = cKDTree(XY); out = {}; used = set()
for pid, p in P.items():
    r = 8.0 if p[0] in ('city', 'civ') else 5.0
    ix = T.query_ball_point([p[1], p[2]], r)
    if not ix: continue
    used.update(ix)
    c = collections.Counter(g for k in ix for g in S[k]['t'])
    out[pid] = {'n': len(ix), 'r': r, 't': c.most_common(), 'c': sum(S[k]['c'] for k in ix), 'cn': sum(1 for k in ix if S[k]['c'] > 0)}
json.dump(out, open(R + 'data/agg/rrsp_match.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('térképhelyek', len(out), '| megjelenő lelőhelyek', len(used))
for pid in out:
    if P[pid][3] in ('Verulamium', 'Calleva', 'Corinium', 'Durovernum', 'Venta', 'Lindum', 'Durobrivae'): print(P[pid][3], out[pid])
