# v129: keresőindex a birodalmi térkép helyeihez → imp_search.json
# Soronként: [latin név, mai név, görög név, további névváltozatok „|”-vel (Pleiades, legfeljebb 8), x, y, id, típus]
# A térkép összes helye (alap + csempék), hogy a csak nagyításkor betöltődő kisebb helyek is megtalálhatók legyenek.
import json, glob, re, unicodedata
R = '/home/claude/imperium/'
P = {}
for p in json.load(open(R + 'imp_base.json'))['pts']: P[p[7]] = p
for f in glob.glob(R + 'tiles/*.json'):
    for p in json.load(open(f)).get('s', []): P[p[7]] = p
INFO = {}
for f in glob.glob(R + 'imp_info/ii_*.json'): INFO.update(json.load(open(f)))
nrm = lambda s: ''.join(c for c in unicodedata.normalize('NFD', (s or '').lower()) if unicodedata.category(c) != 'Mn')
out = []
for pid, p in P.items():
    t, x, y, la, mo, s0, s1, _, gr = p[:9]
    seen = {nrm(la), nrm(mo), nrm(gr)}; al = []
    for n, l, tp in (INFO.get(str(pid), {}).get('p', {}) or {}).get('n', []):
        k = nrm(n)
        if not k or k in seen or len(n) > 40: continue
        seen.add(k); al.append(n)
        if len(al) >= 8: break
    out.append([la or '', mo or '', gr or '', '|'.join(al), round(x, 1), round(y, 1), pid, t])
json.dump(out, open(R + 'imp_search.json', 'w'), ensure_ascii=False, separators=(',', ':'))
import os; print(len(out), round(os.path.getsize(R + 'imp_search.json') / 1e6, 2), 'MB')
