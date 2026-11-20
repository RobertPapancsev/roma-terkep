# v224: Pannonia átnézése – helyjavítások, névjavítás, a limeserődök keltezése, megjegyzés a tartományhatárhoz.
# Források:
#  - de.wikipedia, „Liste der Limeskastelle in Ungarn” (Visy Zsolt: Der pannonische Limes in Ungarn, 1988 beosztása és keltezése szerint)
#    és „Liste der Limeskastelle in Kroatien und Serbien” (2026-11-20);
#  - az egyes erődcikkek koordinátái (de.wikipedia / Wikidata), a Pleiades helyadatai.
# Csak olyan keltezést írunk át, amelyet a forrás uralkodóhoz, évtizedhez vagy évszámhoz köt; az évszázad pontosságú („1. Jh.”) kezdeteket
# és a „5. Jh.” típusú végpontokat változatlanul hagyjuk (ott a DARE általános római/késő antik időszaka marad).
import json, shutil, os
from pyproj import Transformer
R = '/home/claude/imperium/'
BK = R + 'data/imp_base_before_v224.json'
if not os.path.exists(BK): shutil.copy(R + 'imp_base.json', BK)
SBK = R + 'data/imp_search_before_v224.json'
if not os.path.exists(SBK): shutil.copy(R + 'imp_search.json', SBK)
b = json.load(open(BK)); S = json.load(open(SBK))
f4 = Transformer.from_crs('EPSG:4326', '+proj=laea +lat_0=40 +lon_0=15 +units=km +ellps=WGS84', always_xy=True)

# 1) helyek (lat, lon)
POS = {
 '10905': (47.782658, 19.054964),   # Cirpi (Dunabogdány): a DARE-pont 1,9 km-re K-re, a falun kívül; de.wikipedia „Kastell Dunabogdány” = Pleiades 197208
 '10770': (45.558233, 18.711822),   # Mursa: a város Eszék Alsóvárosában (Donji grad) volt (de.wikipedia „Kastell Mursa”); a DARE-pont a Felsővárosban, kb. 2,8 km-re Ny-ra
 '10866': (45.500458, 19.004247),   # Teutoburgium (Dalj): az erőd közvetlenül a Duna partján (de.wikipedia „Kastell Teutoburgium”); a DARE-pont a falu közepén
 '19903': (47.689531, 19.083478),   # Burgus Szentendre-Hunka (de.wikipedia; a DARE-pont pontossága csak 200 m-es kategóriájú és 2,7 km-re D-re esett)
}
# 2) nevek
NAME = {'10771': 'Siscia'}          # a római város neve Siscia; Segestica a római előtti település (a keresőben megmarad)
# 3) keltezés (kezdet, vég) – None = változatlan
DT = {
 '10843': (90, 400),   # Ad Flexum: 1. sz. vége – 4. sz.
 '10900': (100, 430),  # Ad Statuas (Ács-Vaspuszta): kora Traianus-kor – 5. sz. eleje
 '10873': (100, 430),  # Ad Mures: kora Traianus-kor – 5. sz. eleje
 '10901': (170, 400),  # Iža-Leányvár (Kelamantia): a 2. sz. utolsó harmada – késő 4. sz.
 '10902': (101, 430),  # Odiavum (Almásfüzitő): valószínűleg 101/105 – legkésőbb 5. sz. eleje
 '10857': (None, 400), # Crumerum: 2. sz. – 4. sz. vége
 '10903': (364, 430),  # Tokod: Valentinianus-kori – 4./5. sz. fordulója
 '10904': (290, 433),  # Castra ad Herculem: 3. sz. vége – legkésőbb kb. 433
 '16083': (337, 430),  # Visegrád-Gizellamajor: II. Constantius – 5. sz. első harmadának vége
 '10855': (325, 433),  # Visegrád-Sibrik (Pone Navata): kb. 325/330 – a tartomány végéig (380 előtt erődként, utána őrtoronyként)
 '10905': (70, 433),   # Cirpi: Flavius-kor – legkésőbb kb. 433
 '10851': (90, 430),   # Ulcisia Castra (Szentendre): Domitianus–Traianus-kor – 5. sz. eleje
 '16087': (373, 374),  # Göd-Bócsaújtelep: 373 – 374 (befejezetlen erőd)
 '10906': (100, 430),  # Campona: 1./2. sz. fordulója – 4./5. sz. fordulója
 '10845': (110, 430),  # Matrica: Traianus/Hadrianus-kor – 5. sz. eleje
 '10848': (85, 425),   # Intercisa: Domitianus-kor (81–96)? – az 5. sz. 2./3. évtizede
 '10907': (70, None),  # Annamatia: Vespasianus-kor – legalább 374-ig
 '13793': (50, 430),   # Lussonium: kb. 50 – legkésőbb 5. sz. eleje
 '10909': (None, 430), # Alta Ripa (Tolna): 1. sz. – 4./5. sz. fordulója
 '13310': (100, None), # Alisca: kb. 100?
 '10910': (90, 400),   # Ad Statuas (Várdomb): Flavius/Traianus-kor – 4. sz.
 '10856': (70, 430),   # Lugio (Dunaszekcső): Vespasianus-kor – 5. sz. eleje
 '10912': (None, 430), # Ad Militare (Batina): 1. sz. – 4./5. sz. fordulója
 '10913': (None, 433), # Ad Novas (Zmajevac): legkésőbb 2. sz. – az 5. sz. első harmada
 '10866': (40, None),  # Teutoburgium: késő Tiberius / kora Claudius-kor – 5. sz.
 '10931': (100, None), # Cuccium (Ilok): 1./2. sz. fordulója – 5. sz.?
}
NOTE = ('Időszak: Visy Zsolt beosztása és keltezése szerint (de.wikipedia, „Liste der Limeskastelle in Ungarn”, ill. „… in Kroatien und Serbien”); az uralkodóhoz vagy évtizedhez kötött keltezés kerekített évszámmal; ahol a forrás csak évszázadot ad, ott a kezdő- vagy végpont a DARE általános időszaka maradt.',
        'Period: after Zsolt Visy’s dating (de.wikipedia, “Liste der Limeskastelle in Ungarn” / “… in Kroatien und Serbien”); datings tied to a reign or decade are given as a rounded year; where the source gives only a century, the start or end remains DARE’s general period.')
log = []; pn = b.get('pnote', {})
for p in b['pts']:
    i = p[7]
    if i in POS:
        la, lo = POS[i]; x, y = f4.transform(lo, la); log.append(('hely', i, p[3] or p[4], p[1], p[2], round(x, 2), round(y, 2))); p[1], p[2] = round(x, 2), round(y, 2)
    if i in NAME: log.append(('név', i, p[3], NAME[i])); p[3] = NAME[i]
    if i in DT:
        s0, s1 = DT[i]; old = (p[5], p[6])
        if s0 is not None: p[5] = s0
        if s1 is not None: p[6] = s1
        log.append(('kor', i, p[3] or p[4], old, (p[5], p[6]))); pn[i] = list(NOTE)
PN = {
 '10905': ('Helye javítva a de.wikipedia „Kastell Dunabogdány” cikke és a Pleiades szerint (a DARE-pont kb. 2 km-re keletre esett).','Location corrected after de.wikipedia “Kastell Dunabogdány” and Pleiades (the DARE point lay c. 2 km to the east).'),
 '10770': ('Helye javítva: Mursa Eszék Alsóvárosában (Donji grad) feküdt (de.wikipedia „Kastell Mursa”); a DARE-pont a Felsővárosra, kb. 3 km-rel nyugatabbra esett.','Location corrected: Mursa lay in the Lower Town (Donji grad) of Osijek (de.wikipedia “Kastell Mursa”); the DARE point fell on the Upper Town, c. 3 km further west.'),
 '10866': ('Helye javítva: az erőd közvetlenül a Duna partján állt (de.wikipedia „Kastell Teutoburgium”); a DARE-pont Dalj falu közepére esett.','Location corrected: the fort stood directly on the Danube bank (de.wikipedia “Kastell Teutoburgium”); the DARE point fell on the centre of Dalj village.'),
 '19903': ('Helye javítva a de.wikipedia „Burgus Szentendre-Hunka” cikke szerint (a DARE-pont kb. 2,7 km-rel délebbre esett).','Location corrected after de.wikipedia “Burgus Szentendre-Hunka” (the DARE point lay c. 2.7 km further south).'),
}
for i,(h,e) in PN.items():
    if i in pn: pn[i]=[h+' '+pn[i][0], e+' '+pn[i][1]]
    else: pn[i]=[h,e]
b['pnote'] = pn
# a pontosság-sor (DARE) a javított helyeknél már nem érvényes
import glob
for i in PN:
    fn = R + 'imp_info/ii_%d.json' % (int(i) % 64); d = json.load(open(fn))
    if i in d and d[i].get('d', {}).pop('prec', None) is not None:
        json.dump(d, open(fn, 'w'), ensure_ascii=False, separators=(',', ':')); log.append(('prec törölve', i))
# 4) tartományhatár-megjegyzés (a DARE-határ itt nem a 117-es állapotot mutatja)
b['pvn'] = {
 'Pannonia Superior': ('Megjegyzés: a térkép határvonala Pannoniában két helyen nem a Kr. u. 117-es állapotot mutatja. Poetovio (Ptuj) és környéke itt Noricumhoz esik, pedig Traianus korában Felső-Pannoniához tartozott (Noricumhoz csak a Diocletianus utáni tartományrendezésben került). Brigetio (Szőny) Alsó-Pannoniában látszik, de csak 214 körül, Caracalla alatt csatolták oda; 117-ben még Felső-Pannonia része volt.',
                       'Note: in Pannonia the boundary on the map does not show the situation of AD 117 in two places. Poetovio (Ptuj) and its surroundings fall into Noricum here, although under Trajan it belonged to Upper Pannonia (it passed to Noricum only in the post-Diocletianic reorganisation). Brigetio (Szőny) appears in Lower Pannonia, but it was transferred there only c. 214, under Caracalla; in 117 it was still part of Upper Pannonia.'),
}
b['pvn']['Pannonia Inferior'] = b['pvn']['Pannonia Superior']
b['pvn']['Noricum'] = ('Megjegyzés: a térképen Noricumhoz eső Poetovio (Ptuj) és környéke Traianus korában Felső-Pannoniához tartozott; Noricumhoz csak a Diocletianus utáni tartományrendezésben került.',
                       'Note: Poetovio (Ptuj) and its surroundings, shown here in Noricum, belonged to Upper Pannonia under Trajan; they passed to Noricum only in the post-Diocletianic reorganisation.')
# keresőindex
for r in S:
    i = r[6]
    if i in POS:
        la, lo = POS[i]; x, y = f4.transform(lo, la); r[4], r[5] = round(x, 1), round(y, 1)
    if i in NAME:
        r[3] = '|'.join([v for v in (r[3].split('|') if r[3] else []) if v != NAME[i]] + ([r[0]] if r[0] and r[0] != NAME[i] else [])); r[0] = NAME[i]
json.dump(b, open(R + 'imp_base.json', 'w'), ensure_ascii=False, separators=(',', ':'))
json.dump(S, open(R + 'imp_search.json', 'w'), ensure_ascii=False, separators=(',', ':'))
os.makedirs(R + 'data/stats', exist_ok=True)
json.dump(log, open(R + 'data/stats/pannonia_fix_log.json', 'w'), ensure_ascii=False, indent=0)
for l in log: print(l)
print(len(log), 'változtatás; pnote', len(pn))
