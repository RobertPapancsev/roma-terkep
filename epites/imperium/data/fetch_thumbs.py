# Commons bélyegképek letöltése lassan (egyszerre egy, kérések között 6 mp; 429-nél legalább 60 mp szünet).
# Szabványos 330 px-es méret; jpg/png/gif/webp fájloknál a cím md5-jéből képzett URL, egyébként a commons_meta 'th' URL-je.
# Mentés: data/thumbs/<md5>.webp (280 px széles, minőség 62). Folytatható.
import json, os, time, hashlib, io, urllib.request, urllib.parse
from PIL import Image
A = '/home/claude/imperium/data/'
T = json.load(open(A + 'agg/img_titles.json'))
D = A + 'thumbs/'; os.makedirs(D, exist_ok=True)
H = {'User-Agent': 'roman-empire-map/1.0 (https://eidmar-roma.netlify.app; personal non-commercial research map; slow sequential downloads)'}
FAIL = A + 'agg/thumb_fail.json'
F = json.load(open(FAIL)) if os.path.exists(FAIL) else {}
def url_for(t):
    n = t.replace(' ', '_'); h = hashlib.md5(n.encode()).hexdigest(); q = urllib.parse.quote(n)
    ext = n.rsplit('.', 1)[-1].lower()
    if ext in ('jpg', 'jpeg', 'png', 'gif', 'webp'):
        return 'https://upload.wikimedia.org/wikipedia/commons/thumb/%s/%s/%s/330px-%s' % (h[0], h[:2], q, q)
    M = json.load(open(A + 'agg/commons_meta.json')) if os.path.exists(A + 'agg/commons_meta.json') else {}
    return (M.get(t) or {}).get('th')
n_ok = 0
for i, t in enumerate(T):
    key = hashlib.md5(t.encode()).hexdigest()
    if os.path.exists(D + key + '.webp') or t in F: continue
    u = url_for(t)
    if not u: continue  # nem-raszteres fájl, a metaadat még nincs meg: következő futásnál
    wait = 20
    for att in range(4):
        try:
            b = urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60).read(); break
        except urllib.error.HTTPError as e:
            if e.code in (404, 400, 410):
                b = None; break
            ra = e.headers.get('Retry-After'); s = max(60, int(ra) if ra and ra.isdigit() else wait)
            print('HTTP', e.code, 'várok', s, flush=True); time.sleep(s); wait *= 2
        except Exception as e:
            print('hiba', e, 'várok', wait, flush=True); time.sleep(wait); wait *= 2
    else:
        print('feladom', t, flush=True); continue
    if b is None:
        F[t] = 'notfound'; json.dump(F, open(FAIL, 'w'), ensure_ascii=False); time.sleep(2); continue
    try:
        im = Image.open(io.BytesIO(b)); im = im.convert('RGB')
        if im.width > 280: im = im.resize((280, round(im.height * 280 / im.width)), Image.LANCZOS)
        im.save(D + key + '.webp', 'WEBP', quality=62, method=6); n_ok += 1
    except Exception as e:
        F[t] = 'decode:' + str(e)[:80]; json.dump(F, open(FAIL, 'w'), ensure_ascii=False)
    if n_ok % 100 == 0: print(i + 1, '/', len(T), 'kész', len(os.listdir(D)), flush=True)
    time.sleep(6)
print('vége', len(os.listdir(D)), 'hiba', len(F), flush=True)
