# EDR (Epigraphic Database Roma, EpiDoc-fájlok 12. változat, Zenodo 2026, doi:10.5281/zenodo.18468635, CC BY 4.0)
# hozzárendelése a térkép itáliai helyeihez az EDR ókori helynévmezője (origPlace 2. eleme, pl. „Ostia”, „Aquileia”) alapján.
# Az EDR nyílt állományában nincsenek szerkezett személyadatok: a jelöléseket és az életkort a feliratok szövegéből számolom,
# ugyanazzal a módszerrel, mint a Róma-térképen (roma/nm/calc.py, roma/age/calc.py). Kimenet: data/agg/edr_social.json
import json, re, collections, glob, unicodedata, difflib
from pyproj import Transformer
R = '/home/claude/imperium/'
REC = json.load(open('/home/claude/dl/edr/recs.json')); T = json.load(open('/home/claude/dl/edr/text.json'))
inv = Transformer.from_crs('+proj=laea +lat_0=40 +lon_0=15 +units=km', 'EPSG:4326', always_xy=True)
def clean(t):  # azonos a roma/nm/calc.py clean() függvényével
    t = re.sub(r'=\s*/\s*', '', t); t = re.sub(r'(?<=[^\s\-])-\s*/\s*(\[?)', r'\1', t)
    t = re.sub(r'(?<=[A-Za-z\)])\[[\s\-–?]*\]', ' ¤t ', t); t = re.sub(r'\[[\s\-–?]*\]', ' ¤ ', t); t = re.sub(r'(?:-\s){2,}-', ' ¤ ', t)
    t = unicodedata.normalize('NFD', t.lower()); t = ''.join(ch for ch in t if unicodedata.category(ch) != 'Mn')
    t = re.sub(r'\(:[^)]*\)', '', t); t = re.sub(r'\(\((?:mulieris|gaiae)\)\)', 'mulieris', t); t = re.sub(r'\(\([^)]*\)\)', ' ', t)
    t = re.sub(r'[\[\]\(\)<>{}`´?!+〚〛《》⌜⌝"]', '', t)
    t = re.sub(r'〈:?\s*(vacat|verso|recto)\s*〉', ' § ', t); t = re.sub(r'〈:\s*([a-z]{3,}(?: diem)?)\s*〉', r' \1 ', t); t = re.sub(r'〈([a-z])〉', r'\1', t)
    t = re.sub(r'〈[^〉]*〉', ' § ', t); t = re.sub(r'[/,.;:·\-=]+', ' ', t); return re.sub(r'\s+', ' ', t).strip()
tlen = lambda c: len(re.sub(r'\s*¤t?\s*', ' ', c).strip())
PRAE = r'(?:marci|luci|gai|cai|quinti|publi|titi|gnaei|cnaei|auli|sexti|decimi|tiberi|mani|numeri|spuri|servi|appi)'
IW = r'(?:august[io]|augustae|augustorum|augg?|caesaris|caesarum|imperatoris)(?: nostri| nostrorum| n)?'
RX = {'lib': re.compile(r'\blibert(?:us|a|o|ae|um|am|i)\b'), 'ilib': re.compile(IW + r' libert'),
      'ser': re.compile(r'\b(?:con)?serv(?:us|a|o|ae|um|am|i)\b(?! (?:dei|christi|domini))|\bvern(?:a|ae|am)\b'), 'iser': re.compile(IW + r' (?:serv|vern)'),
      'fil': re.compile(PRAE + r' (?:filius|filia|filio|filiae|fili)\b'),
      'mil': re.compile(r'\b(?:miles|militi|militis|militavit|veteran(?:us|o|i)|legion(?:is|e)|cohort(?:is|e)|centurio(?:ni|nis)?|classis praetoriae)\b'),
      'aug': re.compile(r'\b(?:sevir|seviro|seviri)\b(?: august)|\baugustal(?:is|i|es|ibus)\b')}
V = {'i': 1, 'v': 5, 'x': 10, 'l': 50, 'c': 100}
def rom(s):
    t = 0; mx = 0
    for ch in reversed(s):
        v = V[ch]
        if v < mx: t -= v
        else: t += v; mx = v
    return t
NUM = r'([ivxlc]+)\b'
AGE = re.compile(r'\b(?:vix(?:it|sit|et|xit)?|bix(?:it|et)|visit) (?:in pace )?(?:annis|annos|annum|anno|annus|annu|ann|anos|anis|anni) (?:plus minus |p m |pm |plus m )?' + NUM)
AGE2 = re.compile(r'\bannorum ' + NUM)
MAR = re.compile(r'\bcum (?:quo|qua|quem|que|eo|ea|quibus)\b|\bmecum\b|\bsecum\b|\bin coniugio\b')
# ismétlődő szövegek (ugyanaz a felirat több EDR-számon) egyszer számítanak
seen = set()
# térképhelyek: Itália (Szicília, Szardínia, Isztria) területén lévő DARE-helyek latin és egyéb ókori nevei
P = {}
for p in json.load(open(R + 'imp_base.json'))['pts']: P[p[7]] = p
for f in glob.glob(R + 'tiles/*.json'):
    for p in json.load(open(f)).get('s', []): P[p[7]] = p
INFO = {}
for f in glob.glob(R + 'imp_info/ii_*.json'): INFO.update(json.load(open(f)))
norm = lambda s: re.sub(r'[^a-z]', '', unicodedata.normalize('NFD', (s or '').lower()).encode('ascii', 'ignore').decode())
BYN = collections.defaultdict(set); MOD = {}
for pid, p in P.items():
    lon, lat = inv.transform(p[1], p[2])
    if not (6.3 <= lon <= 18.8 and 36.4 <= lat <= 47.2): continue
    if lon > 13.9 and lat > 44.6: continue  # Isztrián túl (Dalmácia) nem EDR-terület
    if lon > 16.5 and lat > 41.9: continue  # az Adria keleti partja
    if lon < 12.0 and lat < 38.0 and not (lon > 11.8 and lat > 36.7): continue  # Észak-Afrika (Pantelleria marad)
    if 8.5 <= lon <= 9.65 and 41.35 <= lat <= 43.05: continue  # Korzika
    ns = {norm(p[3])}
    for n, l, tp in (INFO.get(str(pid), {}).get('p', {}) or {}).get('n', []): ns.add(norm(n))
    for n in ns:
        if len(n) >= 3: BYN[n].add(pid)
    MOD[pid] = norm(p[4])
NAMES = sorted(BYN); FZ = {}; GEN = {'ager', 'agri', 'mons', 'forum', 'pagus', 'vicus', 'vallis', 'insula', 'statio', 'superior', 'inferior', 'ignoratur', 'karalibus', 'caralibus', 'via'}
st = collections.Counter(); MISS = collections.Counter(); out = {}; agg = collections.defaultdict(lambda: {'n': 0, 'c': collections.Counter(), 'ages': []})
for r in REC:
    if len(r['op']) < 2: continue
    an = r['op'][1].strip()
    if an.lower() in ('roma?', 'unknown location', '') or an.endswith('?'): st['kihagy_roma_ismeretlen'] += 1; continue
    keys = [norm(an)] + [norm(x) for x in re.split(r'\s*[-–(),/]\s*', an) if len(norm(x)) >= 4]
    cand = set()
    for k in keys + [norm(x) for x in an.split() if len(norm(x)) >= 5 and norm(x) not in GEN]:
        k2 = k.replace('k', 'c')
        if BYN.get(k): cand = BYN[k]; break
        if BYN.get(k2): cand = BYN[k2]; break
        f = FZ.get(k)
        if f is None:  # közeli írásváltozat (Mediolanum ~ Mediolanium, Lipara ~ Liparae): egyetlen legjobb, legalább 0,9-es egyezés
            m = difflib.get_close_matches(k2, NAMES, n=2, cutoff=0.9); f = FZ[k] = m[0] if len(m) == 1 or (len(m) == 2 and difflib.SequenceMatcher(None, k2, m[0]).ratio() > difflib.SequenceMatcher(None, k2, m[1]).ratio()) else ''
        if f and len(k) >= 5:
            mod = norm((r['pf'] or [''])[0].split('(')[0].split(',')[0])
            c2 = {c for c in BYN[f] if MOD.get(c) and mod and (MOD[c][:5] == mod[:5])}
            if c2: cand = c2; st['kozeli_nev'] += 1
            break  # közeli írásváltozat csak akkor, ha a mai helynév is egyezik
    if not cand: st['nincs_par'] += 1; MISS[an] += 1; continue
    if len(cand) > 1:
        mod = norm((r['pf'] or [''])[0].split('(')[0])
        c2 = {c for c in cand if MOD.get(c) and (MOD[c].startswith(mod[:6]) or mod.startswith(MOD[c][:6]))}
        if len(c2) != 1: st['tobb_jelolt'] += 1; continue
        cand = c2
    pid = next(iter(cand)); c = clean(T.get(r['id'], ''))
    if tlen(c) < 8: st['rovid_szoveg'] += 1; continue
    if len(c) >= 40 and '¤' not in c:
        if c in seen: st['ismetlodo'] += 1; continue
        seen.add(c)
    a = agg[pid]; a['n'] += 1; st['ok'] += 1
    for k, rx in RX.items():
        if rx.search(c): a['c'][k] += 1
    for m in list(AGE.finditer(c)) + list(AGE2.finditer(c)):
        pre = c[max(0, m.start() - 40):m.start()].split(); post = c[m.end():m.end() + 14]
        if post.lstrip().startswith('¤t'): continue
        if MAR.search(' '.join(pre[-5:])) or re.match(r' (?:cum|mecum|secum|in coniugio)', post): continue  # házasság hossza, nem életkor
        v = rom(m.group(1))
        if 0 < v <= 110: a['ages'].append(v)
for pid, a in agg.items():
    o = {'n': a['n'], 'c': [[k, a['c'][k]] for k in ('fil', 'lib', 'ilib', 'ser', 'iser', 'mil', 'aug') if a['c'][k]]}
    if a['ages']:
        g = sorted(a['ages']); b = collections.Counter(min(x // 10, 7) for x in g); o['age'] = [len(g), g[len(g) // 2], [b.get(i, 0) for i in range(8)]]
    out[str(pid)] = o
json.dump(out, open(R + 'data/agg/edr_social.json', 'w'), ensure_ascii=False)
print(MISS.most_common(40)); print(dict(st), 'helyek', len(out), 'életkorral', sum(1 for v in out.values() if 'age' in v))
for nm in ('Ostia', 'Pompeii', 'Aquileia', 'Puteoli', 'Capua'):
    for pid in BYN.get(norm(nm), []):
        if str(pid) in out: print(nm, pid, P[pid][3], out[str(pid)])
