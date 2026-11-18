# Wikimedia Commons: a Wikidata P18 képek szerzője, licence és bélyegkép-URL-je (lassan, 50 cím/kérés, kérések között 15 mp,
# 429/maxlag esetén a Retry-After szerinti vagy növekvő várakozás). Folytatható: a már lekért címeket kihagyja.
import json, os, time, urllib.request, urllib.parse
A = '/home/claude/imperium/data/agg/'
T = json.load(open(A + 'img_titles.json'))
OUT = A + 'commons_meta.json'
R = json.load(open(OUT)) if os.path.exists(OUT) else {}
H = {'User-Agent': 'roman-empire-map/1.0 (https://eidmar-roma.netlify.app; personal non-commercial research map; slow batched requests)'}
todo = [t for t in T if t not in R]
print('hátra', len(todo), flush=True)
for k in range(0, len(todo), 50):
    batch = todo[k:k + 50]
    q = {'action': 'query', 'format': 'json', 'formatversion': '2', 'prop': 'imageinfo', 'iiprop': 'url|extmetadata|size',
         'iiurlwidth': '480', 'iiextmetadatafilter': 'Artist|Credit|LicenseShortName|LicenseUrl|AttributionRequired|UsageTerms|Copyrighted',
         'maxlag': '5', 'titles': '|'.join('File:' + t for t in batch)}
    url = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(q)
    wait = 30
    for att in range(8):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=60)
            d = json.loads(r.read())
            if 'error' in d:  # maxlag
                print('api-hiba', d['error'].get('code'), 'várok', wait, flush=True); time.sleep(wait); wait *= 2; continue
            break
        except urllib.error.HTTPError as e:
            ra = e.headers.get('Retry-After')
            s = int(ra) if ra and ra.isdigit() else wait
            print('HTTP', e.code, 'várok', s, flush=True); time.sleep(s); wait *= 2
        except Exception as e:
            print('hiba', e, 'várok', wait, flush=True); time.sleep(wait); wait *= 2
    else:
        raise SystemExit('feladom ennél a csomagnál: %d' % k)
    norm = {n['to']: n['from'] for n in d['query'].get('normalized', [])}
    got = set()
    for p in d['query']['pages']:
        title = norm.get(p['title'], p['title'])
        t = title[5:] if title.startswith('File:') else title
        if p.get('missing') or 'imageinfo' not in p:
            R[t] = {'missing': 1}; got.add(t); continue
        ii = p['imageinfo'][0]; m = ii.get('extmetadata', {})
        R[t] = {'th': ii.get('thumburl'), 'tw': ii.get('thumbwidth'), 'thh': ii.get('thumbheight'), 'desc': ii.get('descriptionurl'),
                **{x: m[x]['value'] for x in ('Artist', 'Credit', 'LicenseShortName', 'LicenseUrl', 'AttributionRequired', 'UsageTerms', 'Copyrighted') if x in m}}
        got.add(t)
    for t in batch:
        if t not in got: R[t] = {'missing': 1}
    json.dump(R, open(OUT, 'w'), ensure_ascii=False)
    print(k + len(batch), '/', len(todo), flush=True)
    time.sleep(15)
print('kész', len(R), 'hiányzó', sum(1 for v in R.values() if v.get('missing')), flush=True)
