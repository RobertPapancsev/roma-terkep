# Caesar hadjáratai – séták (v152): data/walks/w*.py → imp_walks_hu.json, imp_walks_en.json
# A helyek a térkép keresőindexéből (DARE/Pleiades-alapú pontok) vagy Pleiades-koordinátából (LAEA km-re vetítve).
import json, glob, os, importlib.util
from pyproj import Transformer
R = '/home/claude/imperium/'
tg = Transformer.from_crs('EPSG:4326', '+proj=laea +lat_0=40 +lon_0=15 +units=km', always_xy=True)
S = json.load(open(R + 'imp_search.json'))
PREF = {'city': 0, 'civ': 1, 'leg': 2, 'set': 3, 'fort': 4}
def place(pl, lab, li):
    if isinstance(pl, tuple) and len(pl) == 2 and all(isinstance(q, str) for q in pl):
        c = [s for s in S if s[0] == pl[0] and s[1] == pl[1]]
        if not c: raise SystemExit('nincs ilyen hely: %s' % (pl,))
        s = c[0]
        return {'x': s[4], 'y': s[5], 'pid': s[6], 'n': lab[li] if lab else s[0], 'e': [s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7]]}
    if isinstance(pl, str):
        c = [s for s in S if s[0] == pl]
        if not c: raise SystemExit('nincs ilyen hely: ' + pl)
        c.sort(key=lambda s: PREF.get(s[7], 9)); s = c[0]
        return {'x': s[4], 'y': s[5], 'pid': s[6], 'n': lab[li] if lab else s[0], 'e': [s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7]]}
    la, lo, nm = pl; x, y = tg.transform(lo, la)
    n = lab[li] if lab else nm
    return {'x': round(x, 2), 'y': round(y, 2), 'n': n, 'e': [nm, '', '', '', round(x, 2), round(y, 2), None, 'site']}
import hashlib, html as _h, re as _re, sys as _sys
_sys.path.insert(0, R + 'data'); from walk_img import WI
WM = json.load(open(R + 'data/agg/wimg_meta.json'))
from PIL import Image as _Im
def wimg(wid, i, li):
    v = WI.get(wid, {}).get(i)
    if not v: return None
    m = WM.get(v['f']); fn = 'imp_wimg/' + hashlib.md5(v['f'].encode()).hexdigest()[:12] + '.webp'
    if not m or not os.path.exists(R + fn): raise SystemExit('hiányzó kép: ' + v['f'])
    a = m['a']; g = _re.search(r'\bas author (.+?) under\b', a, _re.I); a = g.group(1) if g else a
    if len(a) > 70: a = a[:67].rsplit(' ', 1)[0] + '…'
    w_, h_ = _Im.open(R + fn).size
    return {'id': fn[9:21], 'w': w_, 'h': h_, 'c': v['c'][li], 'k': v['k'], 'a': a, 'l': m['lic'], 'lu': m['lu'], 'p': m['page']}
PACK = {}
WS = []
for fn in sorted(glob.glob(R + 'data/walks/w*.py')):
    sp = importlib.util.spec_from_file_location('w', fn); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); WS.append(m.W)
WS.sort(key=lambda w: w.get('ord', 0))
for li, lang in enumerate(('hu', 'en')):
    out = []
    for w in WS:
        o = {'id': w['id'], 'g': w.get('grp', 'caesar'), 'y': w['y'] if li == 0 else w['ye'], 't': w['t'][li], 'intro': w['intro'][li], 's': []}
        for st in w['s']:
            p = place(st['pl'], st.get('lab'), li)
            q = {'x': p['x'], 'y': p['y'], 'n': p['n'], 'pid': p.get('pid'), 'h': st['h'][li], 'd': st['d'][li], 't': st['x'][li], 'sea': st.get('sea', False)}
            if st.get('via'):
                q['via'] = [[place(v_, None, li)['x'], place(v_, None, li)['y']] for v_ in st['via']]
            if st.get('mp'):
                m_ = place(st['mp'][1], None, li); q['mp'] = {'n': st['mp'][0], 'f': [m_['x'], m_['y']], 'fn': m_['n']}
                if len(st['mp']) > 2 and st['mp'][2]: q['mp']['s'] = 1
            if st.get('ln'): q['ln'] = 1
            if st.get('rf'):
                r_ = place(st['rf'], None, li); q['rf'] = [r_['x'], r_['y']]
            c = st.get('calc')
            if c:
                f = place(c['from'], None, li)
                q['calc'] = {'f': f['e'], 'to': p['e'], 'J': list(c['J']), 'leg': c['leg'], 'src': c['src'][li], 'sea': c.get('sea', False)}
                for k_ in ('inf', 'cav', 'mules', 'pace', 'party', 'winter'):
                    if k_ in c: q['calc'][k_] = c[k_]
            im_ = wimg(w['id'], len(o['s']), li)
            if im_:
                im_['g'] = w.get('grp', 'caesar'); q['img'] = im_
                if li == 0: PACK.setdefault(im_['g'], {})[im_['id']] = R + 'imp_wimg/' + im_['id'] + '.webp'
            o['s'].append(q)
        out.append(o)
    json.dump(out, open(R + 'imp_walks_%s.json' % lang, 'w'), ensure_ascii=False, separators=(',', ':'))
    print(lang, len(out), 'séta', sum(len(w['s']) for w in out), 'megálló', os.path.getsize(R + 'imp_walks_%s.json' % lang), 'bájt')
import base64
for g_, d_ in PACK.items():
    out_ = {k: base64.b64encode(open(f, 'rb').read()).decode() for k, f in d_.items()}
    json.dump(out_, open(R + 'imp_wimg_%s.json' % g_, 'w'), separators=(',', ':'))
    print('képcsomag', g_, len(out_), os.path.getsize(R + 'imp_wimg_%s.json' % g_), 'bájt')
