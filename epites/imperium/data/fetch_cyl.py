# Junta de Castilla y León – Patrimonio Cultural CyL: yacimientos arqueológicos (IDECyL WFS, réteg pacu_cyl_yac_arqu_vw).
# Felhasználási feltétel (metaadat): „Uso libre y gratuito. Cita obligada a la propiedad de la fuente: Junta de Castilla y León”;
# a regionális nyílt adatportál licence CC BY 4.0. Csak a római kori (köztársasági, korai császárkori, késő római) lelőhelyek,
# lassan, 1000 rekord/kérés, 5 mp szünettel. A hely a befoglaló téglalap közepe (EPSG:25830 → WGS84).
import json, time, urllib.request, urllib.parse, os
from pyproj import Transformer
tr = Transformer.from_crs('EPSG:25830', 'EPSG:4326', always_xy=True)
OUT = '/home/claude/dl/cyl/cyl_romano.json'
H = {'User-Agent': 'roman-empire-map/1.0 (https://eidmar-roma.netlify.app; personal non-commercial research map)'}
PROPS = ['c_bien_id', 'd_bien_denom', 'd_categ_prot', 'n_prov', 'n_mun', 'l_url_pweb', 'romano_republicano', 'romano_altoimperial', 'tardorromano',
         'hierro_ii', 'visigodo']
CQL = 'romano_republicano=true OR romano_altoimperial=true OR tardorromano=true'
R = []; n = 0
while True:
    q = {'service': 'WFS', 'version': '2.0.0', 'request': 'GetFeature', 'typeNames': 'patrimoniocultural:pacu_cyl_yac_arqu_vw', 'count': '1000',
         'startIndex': str(n), 'outputFormat': 'application/json', 'CQL_FILTER': CQL, 'sortBy': 'fid'}
    url = 'https://idecyl.jcyl.es/geoserver/patrimoniocultural/wfs?' + urllib.parse.urlencode(q)
    for att in range(5):
        try: d = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=240).read()); break
        except Exception as e: print('hiba', e, flush=True); time.sleep(20 * (att + 1))
    else: raise SystemExit('feladom')
    F = d.get('features', [])
    for f in F:
        p = f['properties']; b = f.get('bbox')
        if not b:
            xs = [c[0] for ring in (f['geometry']['coordinates'] if f['geometry']['type'] == 'Polygon' else [r for poly in f['geometry']['coordinates'] for r in poly]) for c in ring]
            ys = [c[1] for ring in (f['geometry']['coordinates'] if f['geometry']['type'] == 'Polygon' else [r for poly in f['geometry']['coordinates'] for r in poly]) for c in ring]
            b = [min(xs), min(ys), max(xs), max(ys)]
        lon, lat = tr.transform((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
        o = {k: p.get(k) for k in PROPS}; o['lon'] = round(lon, 6); o['lat'] = round(lat, 6); o['ha'] = round((b[2] - b[0]) * (b[3] - b[1]) / 1e4, 1)
        R.append(o)
    n += len(F); print(n, flush=True)
    if len(F) < 1000: break
    time.sleep(5)
json.dump(R, open(OUT, 'w'), ensure_ascii=False)
print('kész', len(R))
