# Légiómozgás-kalkulátor hálózata (v146): imp_net.json
# Szárazföld: Itiner-e (Kr. u. 150 körül) 14 769 útszakasza; csomópontok a szakaszvégeken, 0,5 km-en belül összevonva;
#   hossz a teljes geometriából (LAEA km), átlagos lejtő (Avg_Slope, fok), úttípus (fő/mellékút), bizonyosság (biztos/feltételezett/hipotetikus).
#   Hézagjavítás: 1,5 km-en belüli, egymással nem összekötött csomópontok között rövid összekötő él (kind 1).
# Víz: ORBIS v2 (Scheidel–Meeks, base_routes.geojson, MIT) part menti, nyílt tengeri, folyami (le/fel, irányított) és komp élei;
#   minden ORBIS-hely a legközelebbi útcsomóponthoz kapcsolva (kind 2, kikötői átszállás), ha 25 km-en belül van.
# Kimenet: n: [[x,y]] csomópontok (km, 2 tizedes); e: [a, b, km, kind, ref, lejtő, bizonyosság, úttípus, (úton: v147) sebességarány a→b, b→a, emelkedés a→b m, emelkedés b→a m, legnagyobb magasság m]
#   kind: 0 út (ref = Itiner-e index, imp_roads1 geometria), 1 összekötő, 2 kikötő, 3 part menti, 4 nyílt tenger, 5 folyón le, 6 folyón fel, 7 komp
#   (a 3–7 ref = w index), w: vízi élek egyszerűsített geometriája "x,y x,y …"
import json, math, collections
import numpy as np
from pyproj import Transformer
from scipy.spatial import cKDTree
R = '/home/claude/imperium/'
tm = Transformer.from_crs('EPSG:3395', '+proj=laea +lat_0=40 +lon_0=15 +units=km', always_xy=True)
tg = Transformer.from_crs('EPSG:4326', '+proj=laea +lat_0=40 +lon_0=15 +units=km', always_xy=True)
RD = json.load(open('/home/claude/dl/itinere/roads.geojson'))['features']
CERT = {'Certain': 0, 'Conjectured': 1, 'Hypothetical': 2}
# v147: domborzat a geometria Z-értékeiből (m). A csúcspontokat legalább 250 m-es darabokká vonjuk össze (DEM-zaj),
# darabonként lejtő (±0,4-re vágva), irányonként Tobler-sebességarány (sík = 1), összes emelkedés 10 m-es hiszterézissel, legnagyobb magasság.
def tob(s): return math.exp(-3.5 * abs(s + 0.05)) / math.exp(-3.5 * 0.05)
def relief(parts_xyz, zcap=None, bcap=None):
    Lt = 0; tf = 0; tb = 0; up = 0; dn = 0; zmax = -1e9
    for xyz in parts_xyz:
        if len(xyz) < 2: continue
        d = np.r_[0, np.cumsum(np.hypot(*np.diff(xyz[:, :2], axis=0).T))]; z = xyz[:, 2]
        if not np.isfinite(z).all(): z = np.nan_to_num(z, nan=float(np.nanmean(z)) if np.isfinite(z).any() else 0)
        if zcap is not None:  # felső korlát: a 15 km-en belüli ismert hágók legmagasabbika + 100 m
            near_ = set(k for lst in PST.query_ball_point(xyz[:, :2], 15.0) for k in lst)
            if near_:
                cap_ = max(PS[j][1] for j in near_) + 100
                if z.max() > cap_: z = np.minimum(z, cap_); zcap.append(max((PS[j] for j in near_), key=lambda q: q[1])[2])
        if bcap is not None and z.max() > bcap: z = np.minimum(z, bcap)  # v151: a folyosó legalacsonyabb átjárója + 50 m
        zmax = max(zmax, float(z.max()))
        idx = [0]
        for j in range(1, len(d)):
            if d[j] - d[idx[-1]] >= 0.25 or j == len(d) - 1: idx.append(j)
        ref = z[0]
        for a_, b_ in zip(idx, idx[1:]):
            h = d[b_] - d[a_]
            if h <= 0: continue
            s = max(-0.4, min(0.4, (z[b_] - z[a_]) / (h * 1000)))
            Lt += h; tf += h / tob(s); tb += h / tob(-s)
            if z[b_] - ref >= 10: up += z[b_] - ref; ref = z[b_]
            elif ref - z[b_] >= 10: dn += ref - z[b_]; ref = z[b_]
    if Lt <= 0: return 1.0, 1.0, 0, 0, 0
    return round(Lt / tf, 3), round(Lt / tb, 3), int(up), int(dn), int(zmax)
# v147: ahol az Itiner-e geometriában nincs magasság (Z = 0: főleg Hispania, Gallia, Britannia, Itália, Alpok), ott a
# Terrain Tiles (Mapzen/AWS, terrarium, z9 ≈ 200–300 m-es rács) domborzatából vett, ~200 m-enként mintavételezett magasság.
from PIL import Image
t4326 = Transformer.from_crs('EPSG:3395', 'EPSG:4326', always_xy=True)
DEMC = {}
def dem_at(lon, lat):
    n = 512; fx = (lon + 180) / 360 * n
    fy = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    x, y = int(fx), int(fy); key = (x, y)
    if key not in DEMC:
        fn = '/home/claude/dl/dem9/%d_%d.png' % key
        if not __import__('os').path.exists(fn): DEMC[key] = None
        else:
            a = np.asarray(Image.open(fn).convert('RGB'), dtype=float); DEMC[key] = a[:, :, 0] * 256 + a[:, :, 1] + a[:, :, 2] / 256 - 32768
    A = DEMC[key]
    if A is None: return float('nan')
    px = (fx - x) * 256 - 0.5; py = (fy - y) * 256 - 0.5; i = int(min(254, max(0, math.floor(py)))); j = int(min(254, max(0, math.floor(px))))
    dy = min(1, max(0, py - i)); dx = min(1, max(0, px - j))
    return float(A[i, j] * (1 - dx) * (1 - dy) + A[i, j + 1] * dx * (1 - dy) + A[i + 1, j] * (1 - dx) * dy + A[i + 1, j + 1] * dx * dy)
def densify_dem(part):
    a = np.array([q[:2] for q in part], dtype=float); out = []
    for k in range(len(a)):
        if k:
            seg = math.dist(a[k - 1], a[k]); nstep = max(1, int(seg / 300))   # Mercator-méter; ~200 m valós
            for j in range(1, nstep): out.append(a[k - 1] + (a[k] - a[k - 1]) * j / nstep)
        out.append(a[k])
    out = np.array(out); lo, la = t4326.transform(out[:, 0], out[:, 1])
    z = np.array([dem_at(lo[k], la[k]) for k in range(len(out))])
    if np.isfinite(z).any(): z = np.where(np.isfinite(z), z, np.nanmean(z))
    if len(z) >= 5:  # ~1 km-es mozgóátlag: a pontatlan nyomvonal gerinceken átvágó csúcsait simítja
        zp = np.r_[z[0], z[0], z, z[-1], z[-1]]; z = np.convolve(zp, np.ones(5) / 5, mode='valid')
    return [[out[k, 0], out[k, 1], z[k]] for k in range(len(out))]
# v148: valós hágómagasságok (Wikidata, P31 = hegyi hágó, P2044 magasság; QLever-lekérdezés 2026-11-13): ha egy útszakasz
# nyomvonala 3 km-en belül halad el egy ismert hágó mellett, és a számított legnagyobb magassága több mint 100 m-rel meghaladja
# a hágó magasságát: az ókorban használt főbb hágók válogatott listája alapján a nyomvonal magassági profilját a 15 km-en belüli
# ismert hágók legmagasabbika + 100 m szintjén levágjuk (az út a legalacsonyabb átkelőt használja, nem a gerinceket; a közelítő
# nyomvonal gerinceken átvágó csúcsait így kiszűrjük).
import re as _re
# csak az ókorban is használt (vagy az Itiner-e úthálózatban szereplő átkelőkhöz tartozó) főbb hágók – válogatott lista:
ROMPASS = {'Great St Bernard Pass', 'Little St Bernard Pass', 'Col de Montgenèvre', 'Mont Cenis Pass', 'Col du Petit Mont-Cenis', 'Brenner Pass',
    'Reschen Pass', 'Julier Pass', 'Septimer Pass', 'Splügen Pass', 'Maloja Pass', 'Plöcken Pass', 'Radstädter Tauern Pass', 'Somport',
    'Shipka Pass', 'Simplon Pass', 'Col du Lautaret', 'Hochtor', 'Loibl Pass', 'Pyhrn Pass', 'Fern Pass', 'Arlberg Pass', 'Cilician Gates',
    'Belen Pass', 'Col de Tende', 'Seefeld Saddle', 'Katschberg Pass', 'Wurzen Pass', 'Predil Pass', 'Col du Perthus', 'Port de Larrau',
    'Roncevaux Pass', 'Puerto de Guadarrama', 'Colle di Cadibona', 'Bocca Trabaria', 'Kerenzerberg Pass', 'Zigana Pass'}
PS = []
for x in json.load(open('/home/claude/dl/passes/passes.json'))['results']['bindings']:
    mm = _re.match(r'POINT\(([-\d.]+) ([-\d.]+)\)', x['c']['value'], _re.I)
    if not mm: continue
    lo, la = float(mm.group(1)), float(mm.group(2))
    lb = x.get('lab', {}).get('value', '')
    if lb in ROMPASS and -11 < lo < 46 and 24 < la < 58: PS.append((tg.transform(lo, la), float(x['z']['value']), lb))
PST = cKDTree(np.array([p[0] for p in PS])); NCLIP = []
# ---- v151: folyosó-átjáró, keltezés, folyóátkelések ----
from scipy import ndimage
import shapely
from shapely.geometry import LineString, MultiLineString
INV = Transformer.from_crs('+proj=laea +lat_0=40 +lon_0=15 +units=km', 'EPSG:4326', always_xy=True)
def dem_v(lon, lat):  # vektorizált Terrain Tiles-mintavétel (z9, terrarium), bilineáris
    lon = np.asarray(lon, dtype=float); lat = np.asarray(lat, dtype=float)
    n = 512; fx = (lon + 180) / 360 * n; la = np.radians(lat)
    fy = (1 - np.log(np.tan(la) + 1 / np.cos(la)) / np.pi) / 2 * n
    tx = np.floor(fx).astype(int); ty = np.floor(fy).astype(int); out = np.full(lon.shape, np.nan)
    for key in set(zip(tx.ravel().tolist(), ty.ravel().tolist())):
        dem_at(*INV.transform(0, 0)) if False else None
        if key not in DEMC:
            fn = '/home/claude/dl/dem9/%d_%d.png' % key
            if not __import__('os').path.exists(fn): DEMC[key] = None
            else:
                a_ = np.asarray(Image.open(fn).convert('RGB'), dtype=float); DEMC[key] = a_[:, :, 0] * 256 + a_[:, :, 1] + a_[:, :, 2] / 256 - 32768
        A = DEMC[key]
        if A is None: continue
        m = (tx == key[0]) & (ty == key[1])
        px = (fx[m] - key[0]) * 256 - .5; py = (fy[m] - key[1]) * 256 - .5
        i = np.clip(np.floor(py), 0, 254).astype(int); j = np.clip(np.floor(px), 0, 254).astype(int)
        dy = np.clip(py - i, 0, 1); dx = np.clip(px - j, 0, 1)
        out[m] = A[i, j] * (1 - dx) * (1 - dy) + A[i, j + 1] * dx * (1 - dy) + A[i + 1, j] * (1 - dx) * dy + A[i + 1, j + 1] * dx * dy
    return out
def bottleneck(xy, W=4.0, st=0.25):
    # a nyomvonal ±W km-es folyosójában a két végpontot összekötő legalacsonyabb átjáró magassága (minimax út, DEM-rácson)
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(xy, axis=0).T))]; L = d[-1]
    if L < 0.5: return float('nan')
    s_ = np.arange(0, L + st / 2, st); px = np.interp(s_, d, xy[:, 0]); py = np.interp(s_, d, xy[:, 1])
    tx = np.gradient(px); ty = np.gradient(py); nn = np.hypot(tx, ty) + 1e-9; nx = -ty / nn; ny = tx / nn
    k = 9; ker = np.ones(2 * k + 1) / (2 * k + 1)
    nx = np.convolve(np.r_[[nx[0]] * k, nx, [nx[-1]] * k], ker, 'valid'); ny = np.convolve(np.r_[[ny[0]] * k, ny, [ny[-1]] * k], ker, 'valid')
    t = np.arange(-W, W + st / 2, st)
    GX = px[:, None] + nx[:, None] * t[None, :]; GY = py[:, None] + ny[:, None] * t[None, :]
    lo, la = INV.transform(GX, GY); Z = dem_v(lo, la)
    if not np.isfinite(Z).any(): return float('nan')
    Z = np.where(np.isfinite(Z), Z, np.nanmax(Z))
    c = len(t) // 2; lo_ = max(Z[0, c], Z[-1, c]); hi_ = Z[:, c].max()
    if hi_ - lo_ < 20: return float(hi_)
    for _ in range(14):
        mid = (lo_ + hi_) / 2; lab, _n = ndimage.label(Z <= mid, structure=np.ones((3, 3)))
        if lab[0, c] and lab[0, c] == lab[-1, c]: hi_ = mid
        else: lo_ = mid
    return float(hi_)
_CP = _re.compile(r'\((\d+)(?:\s*[-–]\s*(\d+))?\s*(BCE|CE|BC|AD)\)')
def date_of(p):
    def ok(v): return v is not None and v not in (0, 9999, 9999.0)
    lo = hi = None
    if ok(p.get('Lower_Date')): lo = int(p['Lower_Date'] - (p['Low_Date_E'] if ok(p.get('Low_Date_E')) else 0))
    # a Cons_per_e (építtető) mező a mérföldkövek keltezését követi (pl. Vienna–Brigantio: Nagy Konstantin), ezért nem használjuk
    if ok(p.get('Upper_Date')): hi = int(p['Upper_Date'] + (p['Up_Date_E'] if ok(p.get('Up_Date_E')) else 0))
    return (lo, hi)
# folyók: Natural Earth 10m folyók (a Klokan-féle római birodalom-térkép változata, latin névvel); csak 'River'
RIV = []; RIVG = []
for f_ in json.load(open('/home/claude/klokan/roman-empire/data/10m_rivers_lake_centerlines.geojson'))['features']:
    pp = f_['properties']
    if pp.get('FeatureCla') != 'River': continue
    g_ = f_['geometry']; parts_ = g_['coordinates'] if g_['type'] == 'MultiLineString' else [g_['coordinates']]
    ls_ = []
    for part_ in parts_:
        a_ = np.array(part_); x_, y_ = tg.transform(a_[:, 0], a_[:, 1]); ls_.append(np.c_[x_, y_])
    RIV.append((pp.get('latin') or '', pp.get('modern') or '')); RIVG.append(MultiLineString([q.tolist() for q in ls_]))
RTREE = shapely.STRtree(RIVG)
# ismert római hidak: Wikidata (CC0; QLever 2026-11-14: 'római híd' Q1223230 példányai, ókori időszakhoz/építészethez kötött hidak, római nevű hidak)
BRL = []
for q_, v_ in json.load(open('/home/claude/dl/bridges/bridges.json')).items():
    x_, y_ = tg.transform(v_[0], v_[1]); BRL.append((x_, y_, v_[2], q_))
BRT = cKDTree(np.array([[b[0], b[1]] for b in BRL]))
def crossings(xy):
    if len(xy) < 2: return []
    ln = LineString(xy.tolist()); res = []
    for ri in RTREE.query(ln, predicate='intersects'):
        it = ln.intersection(RIVG[ri])
        pts = [g for g in getattr(it, 'geoms', [it]) if g.geom_type == 'Point']
        if len(pts) % 2 == 0: continue  # páros számú metszés: a pontatlan nyomvonal a folyó mentén cikázik, nem kel át
        bd, bi = BRT.query([[p_.x, p_.y] for p_ in pts])
        j = int(np.argmin(bd)); res.append((int(ri), int(bi[j]) if bd[j] <= 2.0 else -1))
    return res
NBOT = []; DT = []; XC = []; DTE = []; XCE = []; ZE = []

NDEM = 0
segs = []
for i, f in enumerate(RD):
    p = f['properties']; parts = f['geometry']['coordinates']
    L = 0; first = last = None; pxyz = []
    if all(len(q) < 3 or abs(q[2]) < 0.5 for part in parts for q in part):
        parts = [densify_dem(part) for part in parts]; NDEM += 1
    for part in parts:
        a = np.array([q[:3] if len(q) > 2 else q[:2] + [float('nan')] for q in part], dtype=float); x, y = tm.transform(a[:, 0], a[:, 1]); xy = np.c_[x, y]
        L += float(np.hypot(*np.diff(xy, axis=0).T).sum()); pxyz.append(np.c_[xy, a[:, 2]])
        if first is None: first = xy[0]
        last = xy[-1]
    ty = 0 if 'Main' in (p.get('Type') or '') else 1
    rl = relief(pxyz); hit = []
    rl2 = relief(pxyz, hit)
    if hit: NCLIP.append((p.get('Name'), rl[4], rl2[4], sorted(set(hit))[:3], rl[2] + rl[3], rl2[2] + rl2[3])); rl = rl2
    allxy = np.vstack([q[:, :2] for q in pxyz])
    if rl[4] >= 500:  # v151: legalacsonyabb átjáró a nyomvonal ±4 km-es folyosójában
        bz = bottleneck(allxy)
        if np.isfinite(bz) and bz + 50 < rl[4]:
            rl3 = relief(pxyz, [], bz + 50); NBOT.append((p.get('Name'), rl[4], rl3[4], rl[2] + rl[3], rl3[2] + rl3[3])); rl = rl3
    DT.append(date_of(p)); XC.append(crossings(allxy)); ZE.append((float(pxyz[0][0, 2]), float(pxyz[-1][-1, 2])))
    segs.append((i, first, last, L, float(p.get('Avg_Slope') or 0), CERT.get(p.get('Segment_s'), 1), ty, rl))
E = np.array([s[1] for s in segs] + [s[2] for s in segs])
T = cKDTree(E); par = list(range(len(E)))
def fd(a):
    while par[a] != a: par[a] = par[par[a]]; a = par[a]
    return a
for a, b in T.query_pairs(0.5): par[fd(a)] = fd(b)
roots = {}; nid = [0] * len(E); N = []
for k in range(len(E)):
    r = fd(k)
    if r not in roots: roots[r] = len(N); N.append(E[k])
    nid[k] = roots[r]
N = [list(map(float, v)) for v in N]
edges = []; m = len(segs); adj = collections.defaultdict(set)
for k, (i, f0, l0, L, sl, ce, ty, rl) in enumerate(segs):
    a, b = nid[k], nid[k + m]
    if a == b and L < 0.3: continue
    edges.append([a, b, round(L, 2), 0, i, round(sl, 1), ce, ty, *rl]); adj[a].add(b); adj[b].add(a)
    ei = len(edges) - 1
    if DT[k][0] is not None or DT[k][1] is not None: DTE.append([ei, DT[k][0], DT[k][1]])
    for rv_, br_ in XC[k]: XCE.append([ei, rv_, br_])
# komponensek és hézagjavítás
def comps():
    seen = {}; c = 0
    for s in range(len(N)):
        if s in seen: continue
        st = [s]; seen[s] = c
        while st:
            u = st.pop()
            for v in adj[u]:
                if v not in seen: seen[v] = c; st.append(v)
        c += 1
    return seen, c
seen, c0 = comps()
NT = cKDTree(np.array(N)); nconn = 0
for a, b in NT.query_pairs(1.5):
    if seen[a] != seen[b]:
        d = math.dist(N[a], N[b]); edges.append([a, b, round(d, 2), 1, -1, 0, 1, 1]); adj[a].add(b); adj[b].add(a); nconn += 1
seen, c1 = comps()
sz = collections.Counter(seen.values())
print('DEM-ből vett magasság', NDEM, 'szakaszon; hágómagassághoz igazítva', len(NCLIP));json.dump(NCLIP, open('/home/claude/dl/passes/clipped.json', 'w'), ensure_ascii=False);print('út-csomópontok', len(N), '| élek', len(edges), '| komponensek', c0, '->', c1, '| összekötők', nconn, '| legnagyobb komponens', sz.most_common(3))
# ORBIS vízi élek
OB = json.load(open('/home/claude/dl/orbis/orbis_v2/base_routes.geojson'))['features']
SITES = {}
import csv
for r in csv.DictReader(open('/home/claude/dl/orbis/orbis_v2/sites.csv')):
    SITES[int(r['id'])] = tg.transform(float(r['x']), float(r['y']))
KIND = {'coastal': 3, 'overseas': 4, 'downstream': 5, 'upstream': 6, 'ferry': 7}
W = []; onode = {}
def onode_of(sid, pt):
    if sid not in onode: onode[sid] = len(N); N.append([float(pt[0]), float(pt[1])])
    return onode[sid]
for f in OB:
    p = f['properties']
    if p['t'] not in KIND: continue
    g = f['geometry']; cs = g['coordinates'] if g['type'] == 'LineString' else [q for part in g['coordinates'] for q in part]
    a = np.array(cs); x, y = tg.transform(a[:, 0], a[:, 1]); xy = np.c_[x, y]
    L = float(np.hypot(*np.diff(xy, axis=0).T).sum())
    # egyszerűsítés: kb. 2 km-enként
    keep = [0]; acc = 0
    for j in range(1, len(xy)):
        acc += math.dist(xy[j], xy[keep[-1]])
        if acc >= 2 or j == len(xy) - 1: keep.append(j); acc = 0
    s0 = SITES.get(p['sid'], xy[0]); s1 = SITES.get(p['tid'], xy[-1])
    a_, b_ = onode_of(p['sid'], s0), onode_of(p['tid'], s1)
    W.append(' '.join('%.1f,%.1f' % (xy[j][0], xy[j][1]) for j in keep))
    edges.append([a_, b_, round(L, 1), KIND[p['t']], len(W) - 1, 0, 0, 0])
# kikötők az úthálózathoz
RN = np.array(N[:NT.n]); RT = cKDTree(RN); np_ = 0
for sid, k in onode.items():
    d, j = RT.query(N[k])
    if d <= 25: edges.append([k, int(j), round(float(d), 2), 2, -1, 0, 0, 0]); np_ += 1
print('ORBIS vízi élek', len(W), '| ORBIS-helyek', len(onode), '| úthálózathoz kötve', np_)
# v151: csomópont-magasság (Terrain Tiles) a magassági profilhoz
# a szakaszvégek magasságának átlaga (Itiner-e Z vagy Terrain Tiles); ha nincs, a csomópont helyén vett DEM-érték
_zs = collections.defaultdict(list)
for k_ in range(m):
    for side_, zz in ((0, ZE[k_][0]), (1, ZE[k_][1])):
        if np.isfinite(zz) and abs(zz) > 0.5: _zs[nid[k_ + side_ * m]].append(zz)
_lo, _la = INV.transform(np.array([q[0] for q in N[:NT.n]]), np.array([q[1] for q in N[:NT.n]]))
_dz = dem_v(_lo, _la)
NZ = [int(round(float(np.mean(_zs[i])))) if _zs.get(i) else (int(round(float(_dz[i]))) if np.isfinite(_dz[i]) else None) for i in range(NT.n)]
print('csomópont-magasság', sum(1 for v in NZ if v is not None), '/', NT.n)
print('folyosó-átjáróval csökkentett csúcsmagasság', len(NBOT), 'szakaszon; datált út', len(DTE), '; folyóátkelés', len(XCE), 'ebből ismert római híd', sum(1 for q in XCE if q[2] >= 0))
json.dump(NBOT, open('/home/claude/dl/passes/bottleneck.json', 'w'), ensure_ascii=False)
out = {'n': [[round(a, 2), round(b, 2)] for a, b in N], 'e': edges, 'w': W, 'nr': NT.n, 'z': NZ, 'dt': DTE, 'xc': XCE,
       'rv': [[r[0], r[1]] for r in RIV], 'br': [[b[2], b[3]] for b in BRL]}
json.dump(out, open(R + 'imp_net.json', 'w'), separators=(',', ':'))
import os; print('imp_net.json', round(os.path.getsize(R + 'imp_net.json') / 1e6, 2), 'MB')
