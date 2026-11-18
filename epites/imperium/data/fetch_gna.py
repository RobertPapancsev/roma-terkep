# Geoportale Nazionale per l'Archeologia (MiC – ICA), WFS https://gna.cultura.gov.it/ogc/wfs, CC BY 4.0.
# MOSI rétegek (pont, terület, vonal) lassan, 2000 rekord/kérés, kérések között 5 mp. Csak a szükséges mezők;
# a hely a rekord befoglaló téglalapjának közepe. Kimenet: /home/claude/dl/gna/<réteg>.jsonl (folytatható).
import os, re, time, json, urllib.request, urllib.parse, html
D = '/home/claude/dl/gna/'; os.makedirs(D, exist_ok=True)
F = ['msGeometry', 'gid', 'OGD_MACRO_value', 'OGD', 'OGT', 'OGN', 'LCR', 'LCP', 'LCC', 'DTR', 'DTT', 'DTSI', 'DTSF', 'GPM', 'OGM', 'URL', 'DES']
H = {'User-Agent': 'roman-empire-map/1.0 (personal non-commercial research map; slow paged requests)'}
for L in ('MOSI_multipoint', 'MOSI_multipolygon', 'MOSI_multilinea'):
    out = D + L + '.jsonl'; n = sum(1 for _ in open(out)) if os.path.exists(out) else 0
    while True:
        q = {'service': 'WFS', 'version': '2.0.0', 'request': 'GetFeature', 'typeNames': 'ms:' + L, 'count': '2000', 'startIndex': str(n),
             'propertyName': ','.join(F), 'sortBy': 'gid'}
        url = 'https://gna.cultura.gov.it/ogc/wfs?' + urllib.parse.urlencode(q)
        wait = 20
        for att in range(6):
            try:
                t = urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=180).read().decode('utf-8', 'replace'); break
            except Exception as e:
                print('hiba', e, 'várok', wait, flush=True); time.sleep(wait); wait *= 2
        else: raise SystemExit('feladom')
        mem = re.findall(r'<wfs:member>(.*?)</wfs:member>', t, re.S)
        with open(out, 'a') as fo:
            for m in mem:
                r = {k: html.unescape(v.strip()) for k, v in re.findall(r'<ms:(\w+)>(.*?)</ms:\1>', m, re.S) if v.strip()}
                r.pop('msGeometry', None)
                nums = [float(x) for g in re.findall(r'<gml:(?:pos|posList)[^>]*>([^<]+)<', m) for x in g.split()]
                if nums:
                    la, lo = nums[0::2], nums[1::2]  # EPSG:4326 urn: szélesség, hosszúság sorrend
                    r['lat'] = round((min(la) + max(la)) / 2, 6); r['lon'] = round((min(lo) + max(lo)) / 2, 6); r['ext'] = round(max(max(la) - min(la), max(lo) - min(lo)), 5)
                fo.write(json.dumps(r, ensure_ascii=False) + '\n')
        n += len(mem); print(L, n, flush=True)
        if len(mem) < 2000: break
        time.sleep(5)
print('kész', flush=True)
