# A román műemléklista (LMI 2015, Monitorul Oficial 113 bis/15.II.2016) megyei PDF-jeinek táblázatát olvassa ki
# a szavak vízszintes helyzete alapján (a PDF-ben nincsenek cellavonalak). Kimenet: lmi.json [{cod, den, loc, adr, dat}]
import pdfplumber, re, json, sys, glob, os
CODE = re.compile(r'^[A-Z]{1,2}-(I|II|III|IV)-[ams]-[AB]-\d{5}(\.\d+)*$')
out = []
for f in sorted(glob.glob(os.path.join(sys.argv[1], 'LMI-*.pdf'))):
    with pdfplumber.open(f) as pdf:
        cols = None; cur = None; n0 = len(out)
        # oszlophatárok a fájl szóhelyeiből: az oszlop eleje az a vízszintes helyzet, ahol a legtöbb szó nagy köz után kezdődik,
        # az előző és a saját oszlopfej között (a fejlécek középre igazítottak, és megyénként eltolódnak)
        import collections
        H = None; GS = collections.Counter()
        for pg in pdf.pages[:12]:
            W = pg.extract_words()
            h = {w['text']: w['x0'] for w in W if w['text'] in ('Cod', 'Denumire', 'Localitate', 'Adresă', 'Adresa', 'Datare')}
            if H is None and {'Cod', 'Denumire', 'Localitate', 'Datare'} <= h.keys(): H = h
            ln = {}
            for w in W: ln.setdefault(round(w['top']), []).append(w)
            for ws in ln.values():
                ws.sort(key=lambda w: w['x0'])
                for a, b in zip(ws, ws[1:]):
                    if b['x0'] - a['x1'] > 7: GS[round(b['x0'])] += 1
        hx = [H['Cod'], H['Denumire'], H['Localitate'], H.get('Adresă', H.get('Adresa')), H['Datare']]
        COLS = [hx[0] - 45]
        for i in range(1, 5):
            cand = {x: n for x, n in GS.items() if hx[i - 1] + 20 < x <= hx[i] + 5}
            COLS.append(max(cand, key=cand.get) - 3)
        for pg in pdf.pages:
            W = pg.extract_words(keep_blank_chars=False, use_text_flow=False)
            hdr = {w['text']: w['x0'] for w in W if w['text'] in ('Cod', 'Denumire', 'Localitate', 'Adresă', 'Adresa', 'Datare')}
            if {'Cod', 'Denumire', 'Localitate', 'Datare'} <= hdr.keys():
                cols = COLS
                htop = max(w['bottom'] for w in W if w['text'] == 'Datare')
            if not cols: continue
            lines = {}
            for w in W:
                if w['top'] <= htop + 1 and hdr: continue
                lines.setdefault(round(w['top']), []).append(w)
            for y in sorted(lines):
                ws = sorted(lines[y], key=lambda w: w['x0'])
                if any(w['text'] in ('Datare', 'Denumire') for w in ws): continue
                cell = ['', '', '', '', '']
                for w in ws:
                    if w['x0'] < cols[0] or w['x0'] > cols[4] + 150: continue  # sorszám, illetve a lap szélén függőlegesen futó Monitorul Oficial-fejléc
                    k = max(i for i in range(5) if w['x0'] >= cols[i])
                    cell[k] += (' ' if cell[k] else '') + w['text']
                c0 = cell[0].replace(' ', '')  # a kód néha két szóra esik (pl. 'TL-I' + '-s-B-05764')
                if cur and c0 and not CODE.match(cur['cod']) and not re.match(r'^[A-Z]{1,2}-(I|II|III|IV)\b', c0):
                    cur['cod'] += c0  # a kód a cellában több sorra tördelődött
                    c0 = ''
                if re.match(r'^[A-Z]{1,2}-(I|II|III|IV)(-|$)', c0):
                    cur = {'cod': c0, 'den': cell[1], 'loc': cell[2], 'adr': cell[3], 'dat': cell[4], 'f': os.path.basename(f)}
                    out.append(cur)
                elif cur and not re.match(r'^(MINISTERUL|INSTITUTUL|MONITORUL|LISTA)', ' '.join(cell).strip()):
                    for i, k in enumerate(('cod', 'den', 'loc', 'adr', 'dat')):
                        if cell[i] and i > 0: cur[k] += ' ' + cell[i]
    print(os.path.basename(f), len(out) - n0, [round(c) for c in COLS])
for r in out:
    for k in ('den', 'loc', 'adr', 'dat'): r[k] = re.sub(r'\s+', ' ', r[k]).replace('- ', '-' if False else '- ').strip()
bad = [r['cod'] for r in out if not CODE.match(r['cod'])]; print('hibás kód', len(bad), bad[:5])
out = [r for r in out if CODE.match(r['cod'])]
json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False, indent=0)
print('összesen', len(out))
