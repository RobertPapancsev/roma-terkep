# Commons-bélyegképek csomagolása a helyadatlapokhoz: imp_img/im_<id%64>.json = {id: [webp base64, szél, mag, szerző, licenc, licenc-URL, Commons-oldal]}
# Csak az a kép kerül be, amelynek van letöltött bélyegképe ÉS ismert licence (LicenseShortName); a szerző a Commons 'Artist' mezője
# (HTML nélkül), ha nincs, a 'Credit' mező. Szabad licencű (CC, közkincs) képek; a nem azonosítható licencűek kimaradnak.
import json, glob, os, re, base64, hashlib, html
from PIL import Image
B = '/home/claude/imperium/'; A = B + 'data/agg/'
M = json.load(open(A + 'commons_meta.json'))
def txt(s):
    s = html.unescape(re.sub(r'<[^>]+>', ' ', s or '')); s = re.sub(r'\s+', ' ', s).strip()
    return s if len(s) <= 90 else s[:87].rsplit(' ', 1)[0] + '…'
FREE = re.compile(r'^(cc[ -]?by|cc[ -]?sa|cc[ -]?0|cc0|public domain|pd|attribution|gfdl|fal|free art|copyrighted free use|no restrictions|mit|odbl)', re.I)
out = {}; st = {'kep': 0, 'nincs_bk': 0, 'nincs_lic': 0, 'nem_szabad': 0}; seen_lic = {}
for f in glob.glob(B + 'imp_info/ii_*.json'):
    for pid, v in json.load(open(f)).items():
        w = v.get('w') or {}; t = w.get('img')
        if not t: continue
        p = B + 'data/thumbs/' + hashlib.md5(t.encode()).hexdigest() + '.webp'
        m = M.get(t) or {}
        if not os.path.exists(p): st['nincs_bk'] += 1; continue
        lic = txt(m.get('LicenseShortName'))
        if not lic: st['nincs_lic'] += 1; continue
        if not FREE.match(lic): st['nem_szabad'] += 1; seen_lic[lic] = seen_lic.get(lic, 0) + 1; continue
        au = txt(m.get('Artist')) or txt(m.get('Credit')) or '?'
        au = re.sub(r'\s*\(\s*talk\s*·\s*contribs\s*\)', '', au).strip()   # v224: a Commons-felhasználói hivatkozások maradéka
        g = re.search(r'\bas author (.+?) under\b', au, re.I)
        if g: au = g.group(1).strip(' "“”')
        im = Image.open(p)
        out.setdefault(int(pid) % 64, {})[pid] = [base64.b64encode(open(p, 'rb').read()).decode(), im.width, im.height, au, lic,
                                                  m.get('LicenseUrl', ''), m.get('desc') or 'https://commons.wikimedia.org/wiki/File:' + t.replace(' ', '_')]
        st['kep'] += 1
# v219: kézi képcserék (data/img_override.json) – ahol a Wikidata-elem képe nem a helyet mutatja
OV = json.load(open(B + 'data/img_override.json')) if os.path.exists(B + 'data/img_override.json') else {}
for pid, o in OV.items():
    im = Image.open(B + o['file'])
    out.setdefault(int(pid) % 64, {})[pid] = [base64.b64encode(open(B + o['file'], 'rb').read()).decode(), im.width, im.height, o['author'], o['lic'], o['licurl'], o['desc']]
# v225: kézi törlések (data/img_remove.json) – a kép más helyet mutat, és nincs helyette megfelelő
RM = json.load(open(B + 'data/img_remove.json')) if os.path.exists(B + 'data/img_remove.json') else {}
for pid in RM: out.get(int(pid) % 64, {}).pop(pid, None)
os.makedirs(B + 'imp_img', exist_ok=True)
for c in range(64):
    json.dump(out.get(c, {}), open(B + 'imp_img/im_%d.json' % c, 'w'), ensure_ascii=False, separators=(',', ':'))
print(st, 'nem szabad licencek:', seen_lic)
print('méret MB', round(sum(os.path.getsize(x) for x in glob.glob(B + 'imp_img/*.json')) / 1e6, 1))
