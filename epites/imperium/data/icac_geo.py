# ICAC „Archaeological sites of wine and olive oil production in Hispania” (Peña Cervantes 2025, CORA doi:10.34810/data2461, CC BY 4.0)
# A katalógusban nincs koordináta, csak mai ország, tartomány/kerület és község: a lelőhelyet a község Wikidata-koordinátájára
# teszem (CC0; spanyol községek INE-kód + tartomány szerint, portugál községek kerület szerint). Kimenet: /home/claude/dl/icac/icac_geo.json
import json, csv, re, unicodedata, difflib
D = '/home/claude/dl/icac/'
W = json.load(open(D + 'wd_municipios.json'))
nrm = lambda s: re.sub(r'[^a-z]', '', unicodedata.normalize('NFD', (s or '').lower()).encode('ascii', 'ignore').decode())
pt_ = lambda c: tuple(map(float, re.search(r'Point\(([-\d.eE]+) ([-\d.eE]+)\)', c).groups()))
PRV = {x['ine'][:2]: nrm(re.sub(r'^provincia de ', '', x['l'])) for x in W['esprov']}
PRV.update({'07': 'baleares', '26': 'larioja', '28': 'madrid', '30': 'murcia', '31': 'navarra'})  # egytartományos autonóm közösségek INE-kódjai
ALIAS = {'castellondelaplana': 'castellon', 'braganza': 'braganca', 'coimbra': 'coimbra', 'oporto': 'porto', 'guipuzcoa': 'guipuzcoa'}
ES = {}
for x in W['es'] + W.get('es2', []):  # es2: minden INE-kódos község (katalán, galiciai stb. is), spanyol, katalán és galiciai névvel
    p = PRV.get(x['ine'][:2]); ES.setdefault(p, {})
    for v in re.split(r'\s*/\s*', x['l']): ES[p][nrm(v)] = pt_(x['c'])
PT = {}
for x in W['pt']:
    PT.setdefault(nrm(x.get('dl', '')), {})[nrm(x['l'])] = pt_(x['c']); PT.setdefault('*', {})[nrm(x['l'])] = pt_(x['c'])
R = list(csv.DictReader(open(D + 'Torcularia/Datos/cataleg.csv', encoding='utf-8')))
out = []; miss = []
for r in R:
    pr = nrm(r['Provincia_Distrito']); pr = ALIAS.get(pr, pr); mu = nrm(r['Municipio'].split('/')[0]); c = None
    if r['Pais'] == 'España':
        T = ES.get(pr, {})
        c = T.get(mu)
        if not c:
            m = difflib.get_close_matches(mu, list(T), n=1, cutoff=0.88); c = T.get(m[0]) if m else None
        if not c and not pr:  # tartomány nélkül: csak egyértelmű országos névegyezés
            hits = [t[mu] for t in ES.values() if mu in t]; c = hits[0] if len(hits) == 1 else None
    elif r['Pais'] == 'Portugal':
        T = PT.get(pr) or PT['*']; c = T.get(mu)
        if not c:
            m = difflib.get_close_matches(mu, list(T), n=1, cutoff=0.88); c = T.get(m[0]) if m else None
    if c: out.append({**r, 'lon': c[0], 'lat': c[1]})
    else: miss.append((r['Pais'], r['Provincia_Distrito'], r['Municipio']))
# második kör: a községlistában nem szereplő helynevek (portugál freguesiák, spanyol helységek) célzott Wikidata-lekérdezéssel
# (data: wd_targeted.json); csak ha az azonos nevű találatok egymástól 15 km-en belül vannak (egyértelmű hely)
import math, collections
TG = collections.defaultdict(list)
for x in (json.load(open(D + 'wd_targeted.json')) if __import__('os').path.exists(D + 'wd_targeted.json') else []):
    if 'Point(' in x['c']: TG[(x['ctry'], nrm(x['l']))].append(pt_(x['c']))  # ismeretlen (genid) koordináta kihagyva
still = []
for r in [r for r in R if (r['Pais'], r['Provincia_Distrito'], r['Municipio']) in set(miss)]:
    C = TG.get((r['Pais'], nrm(re.sub(r'\s*\(.*\)', '', r['Municipio']))), [])
    C = list({c for c in C})
    if C and max(math.hypot((a[0] - b[0]) * 85, (a[1] - b[1]) * 111) for a in C for b in C) <= 15:
        out.append({**r, 'lon': C[0][0], 'lat': C[0][1], 'geo2': 1})
    else: still.append((r['Pais'], r['Provincia_Distrito'], r['Municipio']))
miss = still
json.dump(out, open(D + 'icac_geo.json', 'w'), ensure_ascii=False)
print('helymeghatározva', len(out), 'hiányzik', len(miss)); print(sorted(set(miss)))
