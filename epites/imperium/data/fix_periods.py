# v226/v227: erődök időszaka a német Wikipédia erődcikkeinek adatlapja („Infobox Limeskastell”, „Belegung von bis”) alapján.
# Előállítás: a de.wikipedia „Kastell/Kleinkastell/Legionslager/Burgus/Römerlager…” című, koordinátás cikkei (Wikidata/QLever) a 2 km-en belüli
# legközelebbi DARE-erődponthoz rendelve (névegyezés vagy 300 m-en belüli távolság), a cikkek szövege Special:Export-tal (2026-11-20);
# a „Belegung” mező értelmezése: /home/claude/per/parse.py -> data/periods_dewiki.json (minden sor tartalmazza a forrásszöveget).
# Szabályok: évszám -> az évszám; uralkodóhoz kötött („trajanisch”) -> az uralkodás kezdete (kezdetnél) ill. vége (végnél), „früh/spät” esetén negyeddel beljebb;
# évszázad-rész („Mitte 2. Jh.”, „spätes 4. Jh.”) -> kerekített év; csupasz évszázad („3. Jh.”) -> nem adható meg, a DARE értéke marad.
# Több szakasznál az első kezdete és az utolsó vége (a közbeeső szünetek nem látszanak). A v224/v225-ben már kézzel javított pontokat nem érinti.
import json, shutil, os
R = '/home/claude/imperium/'
BK = R + 'data/imp_base_before_v226.json'
if not os.path.exists(BK): shutil.copy(R + 'imp_base.json', BK)
b = json.load(open(BK)); D = {}
for o in json.load(open(R + 'data/periods_all.json')): D.setdefault(o['id'], o)   # v227: de + en, csak ahol a DARE-keltezés általános
pn = b.get('pnote', {}); n = 0; log = []
for p in b['pts']:
    o = D.get(p[7])
    if not o or p[7] in pn: continue
    a, e = o['new']; old = (p[5], p[6])
    if a is not None and e is None and p[6] and a > p[6]: continue   # ellentmond a DARE végpontjának (pl. Untereggingen): változatlan
    if a is not None: p[5] = a
    if e is not None: p[6] = e
    if (p[5], p[6]) == old: continue
    n += 1; log.append((p[7], p[3] or p[4], old, (p[5], p[6]), o['art']))
    src = o['src'] if len(o['src']) <= 180 else o['src'][:177] + '…'
    L = o.get('lang', 'de'); fld = 'Belegung' if L == 'de' else 'infobox'
    pn[p[7]] = ['Időszak: a %s.wikipedia „%s” cikkének adatlapja szerint (%s: „%s”). Uralkodóhoz kötött keltezésnél az uralkodás kezdő vagy záró éve, évszázad-résznél kerekített év áll; ahol a forrás csak évszázadot ad, ott a DARE értéke maradt.' % (L, o['art'], fld, src),
                'Period: after the infobox of the %s.wikipedia article “%s” (%s: “%s”). For datings tied to a reign the first or last year of the reign is used, for parts of a century a rounded year; where the source gives only a century, the DARE value remains.' % (L, o['art'], fld, src)]
b['pnote'] = pn
json.dump(b, open(R + 'imp_base.json', 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump(log, open(R + 'data/stats/periods_fix_log.json', 'w'), ensure_ascii=False, indent=0)
print(n, 'pont időszaka változott')
