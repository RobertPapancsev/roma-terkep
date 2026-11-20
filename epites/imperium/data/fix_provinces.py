# v225: a többi provincia átnézése (a fix_pannonia.py után fut).
# 1) DARE-pontok, amelyek a Pleiades és a Wikidata (egymástól független) adataitól, illetve a lelőhely ismert helyétől
#    több km-re estek, és a hiba egyértelmű (más lelőhelyre / a mai városra / más régióba került a pont).
# 2) Tartomány-megjegyzések: ismert, Kr. u. 117-ben biztosan egy adott tartományhoz tartozó városok ellenőrzése a DARE-poligonokkal
#    (cities117.py); ahol a térkép mást mutat, a tartománykártyán megjegyzés magyarázza (a határvonalat nem rajzoljuk át).
# 3) Két légiós tábor keltezése (en.wikipedia).
import json, shutil, os
from pyproj import Transformer
R = '/home/claude/imperium/'
BK = R + 'data/imp_base_before_v225.json'
if not os.path.exists(BK): shutil.copy(R + 'imp_base.json', BK)
SBK = R + 'data/imp_search_before_v225.json'
if not os.path.exists(SBK): shutil.copy(R + 'imp_search.json', SBK)
b = json.load(open(BK)); S = json.load(open(SBK))
f4 = Transformer.from_crs('EPSG:4326', '+proj=laea +lat_0=40 +lon_0=15 +units=km +ellps=WGS84', always_xy=True)

POS = {  # id: (lat, lon, új mai név vagy None, megjegyzés hu, en)
 '22333': (31.2832, 45.8524, 'Tell as-Senkereh',
           'Helye javítva: Larsa a Tell as-Senkereh-dombon feküdt; a DARE-pont Tell Abu Shahrainra, vagyis Eridura esett (kb. 54 km-rel délebbre). Hely: Pleiades és Wikidata.',
           'Location corrected: Larsa lay at Tell as-Senkereh; the DARE point fell on Tell Abu Shahrain, i.e. Eridu (c. 54 km further south). Location: Pleiades and Wikidata.'),
 '21801': (39.8819, 44.5752, 'Artashat (Khor Virap)',
           'Helye javítva: az ókori Artaxata romjai a Khor Virap-i dombokon vannak; a DARE-pont a mai Artashat városra, kb. 9 km-rel északabbra esett. Hely: Pleiades és Wikidata.',
           'Location corrected: the ruins of ancient Artaxata are on the hills of Khor Virap; the DARE point fell on the modern town of Artashat, c. 9 km further north. Location: Pleiades and Wikidata.'),
 '21643': (35.4042, 8.1223, None,
           'Helye javítva: Theveste a mai Tébessa alatt fekszik (Caracalla íve, városfal); a DARE-pont kb. 3 km-rel délnyugatabbra, a városon kívül volt. Hely: Pleiades és Wikidata.',
           'Location corrected: Theveste lies beneath modern Tébessa (Arch of Caracalla, city wall); the DARE point lay c. 3 km to the south-west, outside the town. Location: Pleiades and Wikidata.'),
 '21948': (38.1678, 20.5167, None,
           'Helye javítva: az ókori Krane Argostolitól délkeletre, a Koutavos-öböl mögötti dombon feküdt; a DARE-pont Argostoli városára esett. Hely: Pleiades és Wikidata.',
           'Location corrected: ancient Krane lay on the hill south-east of Argostoli, behind the Koutavos lagoon; the DARE point fell on the town of Argostoli. Location: Pleiades and Wikidata.'),
 '25239': (25.5220, 55.6260, None,
           'Helye javítva: ed-Dur az Egyesült Arab Emírségekben (Umm al-Kaivain) van; a DARE-pont tévesen Bahreinbe, kb. 516 km-rel arrébb esett. Hely: Pleiades.',
           'Location corrected: ed-Dur is in the United Arab Emirates (Umm al-Quwain); the DARE point wrongly fell in Bahrain, c. 516 km away. Location: Pleiades.'),
 '34689': (34.8610, 4.9250, None,
           'Helye javítva: Ausum (Sadouri) a Zab vidékén, Biskra környékén volt; a DARE-pont tévesen a tengerparti Kabíliába, kb. 180 km-rel északabbra esett. Hely: Pleiades.',
           'Location corrected: Ausum (Sadouri) lay in the Zab region near Biskra; the DARE point wrongly fell in coastal Kabylia, c. 180 km further north. Location: Pleiades.'),
 '27307': (16.1280, 44.8140, None,
           'Helye javítva: Karna (Qarnawu), a minaiak fővárosa, Ma’in romjainál, a jemeni al-Dzsauf vidékén volt; a DARE-pont kb. 85 km-rel északkeletebbre esett. Hely: Pleiades.',
           'Location corrected: Karna (Qarnawu), capital of the Minaeans, lay at the ruins of Ma’in in the al-Jawf region of Yemen; the DARE point fell c. 85 km to the north-east. Location: Pleiades.'),
}
DT = {  # id: (kezdet, vég, hu, en)
 '22989': (82, 87, 'Időszak: Kr. u. 82/83-ban épült, 86 nyarán, legkésőbb 87 elején kiürítették (en.wikipedia, „Inchtuthil”).',
           'Period: built in AD 82 or 83, evacuated in the summer of 86, at the latest early in 87 (en.wikipedia, “Inchtuthil”).'),
 '20684': (75, None, 'Időszak: a légiós tábort a legio II Adiutrix kezdte építeni a 70-es évek közepén (en.wikipedia, „Deva Victrix”); a vég a DARE általános időszaka.',
           'Period: the legionary fortress was begun by legio II Adiutrix in the mid-70s AD (en.wikipedia, “Deva Victrix”); the end is DARE’s general period.'),
}
pn = b.get('pnote', {}); log = []
for p in b['pts']:
    i = p[7]
    if i in POS:
        la, lo, mo, h, e = POS[i]; x, y = f4.transform(lo, la)
        log.append(('hely', i, p[3] or p[4], p[1], p[2], round(x, 2), round(y, 2))); p[1], p[2] = round(x, 2), round(y, 2)
        if mo: p[4] = mo
        pn[i] = [h, e]
    if i in DT:
        s0, s1, h, e = DT[i]; old = (p[5], p[6])
        if s0 is not None: p[5] = s0
        if s1 is not None: p[6] = s1
        log.append(('kor', i, p[3], old, (p[5], p[6]))); pn[i] = [h, e]
b['pnote'] = pn
for r in S:
    if r[6] in POS:
        la, lo, mo = POS[r[6]][:3]; x, y = f4.transform(lo, la); r[4], r[5] = round(x, 1), round(y, 1)
        if mo: r[1] = mo
for i in POS:   # a DARE pontossági sora a javított helyeknél nem érvényes
    fn = R + 'imp_info/ii_%d.json' % (int(i) % 64); d = json.load(open(fn))
    if i in d and d[i].get('d', {}).pop('prec', None) is not None:
        json.dump(d, open(fn, 'w'), ensure_ascii=False, separators=(',', ':')); log.append(('prec törölve', i, fn.split('/')[-1]))

V = b.get('pvn', {})
PAN = (' Sopianae (Pécs) a térképen Felső-Pannoniába esik, holott Alsó-Pannonia része volt.',
       ' Sopianae (Pécs) falls into Upper Pannonia on the map, although it belonged to Lower Pannonia.')
for k in ('Pannonia Superior', 'Pannonia Inferior'):
    if PAN[0] not in V[k][0]: V[k] = (V[k][0] + PAN[0], V[k][1] + PAN[1])
NUM = ('Megjegyzés: Kr. u. 117-ben Numidia még nem volt önálló tartomány; formálisan Africa Proconsularis része volt, bár a III. Augusta légió parancsnoka (legatus) igazgatta. Önálló provinciává Septimius Severus alatt, kb. 198–200 körül vált. A térkép itt a későbbi állapotot mutatja: Cirta, Lambaesis, Thamugadi és Theveste 117-ben Africához tartozott.',
       'Note: in AD 117 Numidia was not yet a separate province; formally it was part of Africa Proconsularis, although it was governed by the legate of legio III Augusta. It became a province in its own right under Septimius Severus, c. 198–200. Here the map shows the later situation: Cirta, Lambaesis, Thamugadi and Theveste belonged to Africa in 117.')
V['Numidia'] = NUM; V['Africa Proconsularis'] = NUM
V['Galatia et Cappadocia'] = ('Megjegyzés: Kr. u. 117-ben Galatia és Cappadocia két külön tartomány volt: Vespasianus kb. 72-ben egyesítette őket, Traianus uralkodása alatt (kb. 113) újra szétváltak. A térkép közös területként mutatja őket. Satala légiós tábora a térképen éppen a határ túloldalára esik, de Cappadociához tartozott.',
                              'Note: in AD 117 Galatia and Cappadocia were two separate provinces: Vespasian united them c. 72, and they were separated again under Trajan (c. 113). The map shows them as one area. The legionary fortress of Satala falls just across the boundary on the map, but it belonged to Cappadocia.')
V['Armenia Mesopotamia'] = ('Megjegyzés: Satala légiós tábora a térképen ide esik, de Cappadociához tartozott.',
                            'Note: the legionary fortress of Satala falls here on the map, but it belonged to Cappadocia.')
PR = ('Megjegyzés: Prusa (Bursa) a térképen Asia provinciába esik, holott Bithynia része volt (Bithynia et Pontus).',
      'Note: Prusa (Bursa) falls into the province of Asia on the map, although it was part of Bithynia (Bithynia et Pontus).')
V['Bithynia et Pontus'] = PR; V['Asia'] = PR
V['Syria'] = ('Megjegyzés: Palmyra a térképen a tartomány határán kívül esik, de Kr. u. 117-ben Syria provincia része volt (az 1. század óta római fennhatóság alatt állt).',
              'Note: Palmyra falls outside the province on the map, but in AD 117 it was part of the province of Syria (under Roman control since the 1st century).')
SEG = ('Megjegyzés: Alpes Cottiae székhelye, Segusio (Susa) a térképen néhány km-rel a szomszédos Alpes Graiae et Poeninae területére esik.',
       'Note: the capital of Alpes Cottiae, Segusio (Susa), falls a few km into neighbouring Alpes Graiae et Poeninae on the map.')
V['Alpes Cottiae'] = SEG; V['Alpes Graiae et Poeninae'] = SEG
b['pvn'] = V
json.dump(b, open(R + 'imp_base.json', 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump(S, open(R + 'imp_search.json', 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump(log, open(R + 'data/stats/provinces_fix_log.json', 'w'), ensure_ascii=False, indent=0)
for l in log: print(l)
print('pvn', len(V), 'pnote', len(pn))
