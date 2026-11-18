# Portugália: Direção-Geral do Território, SRUP – Imóveis Classificados (WFS, CC BY 4.0; letöltve 2026-11-13):
# a »Localizados« és a »com Zona de Proteção« réteg együtt, a megnevezés (DESIGNACAO) szerint egyszer.
# Római a megnevezés alapján: ROMAN(A/O/AS/OS), LUSITANO-ROMAN…, MILIÁRIO, CASTELLUM, ismert római városnevek; kizárva:
# ROMÂNICO/ROMÂNICA (román stílus), S. ROMÃO. A »CASTRO« (vaskori erődített település) önmagában nem elég.
# Koordináta: a geometria pontjainak átlaga (EPSG:3763). Link: a classificação hivatalos hiperlinkje, ha van.
import re, sys, html
sys.path.insert(0, '/home/claude/imperium/data'); from nh_common import laea, match
import numpy as np
tr = laea('EPSG:3763'); KW = r'ROMAN[AO]S?\b|LUSITANO-ROMAN|MILIÁRIO|CASTELLUM|CONIMBRIGA|MIROBRIGA|AMMAIA|EBUROBRITTIUM|BALSA|CETÓBRIGA|TRÓIA|SÃO CUCUFATE|\bMILREU\b|CERRO DA VILA|TRESMINAS|VILLA ROMANA'
NEG = r'ROMÂNIC|ROMANIC|S\. ROMÃO|SÃO ROMÃO'
S = {}
LOW = {'de', 'da', 'do', 'das', 'dos', 'e', 'a', 'o', 'em', 'com', 'na', 'no', 'nas', 'nos', 'ao', 'à', 'às', 'por', 'ou', 'entre', 'junto'}
def tc(s):
    return ' '.join(w.lower() if i and w.lower() in LOW else w.capitalize() for i, w in enumerate(s.split()))
for f in ('/home/claude/dl/pt/ic.gml', '/home/claude/dl/pt/icz.gml'):
    t = open(f, encoding='utf-8').read()
    for m in re.finditer(r'<gml:featureMember>(.*?)</gml:featureMember>', t, re.S):
        b = m.group(1); g = lambda k: html.unescape((re.search(r'<gmgml:%s>([^<]*)</gmgml:%s>' % (k, k), b) or [None, ''])[1]).strip()
        d = g('DESIGNACAO')
        if not re.search(KW, d) or re.search(NEG, d) or d in S: continue
        nums = [float(v) for v in re.findall(r'-?\d+\.\d+', ' '.join(re.findall(r'<gml:(?:posList|pos|coordinates)[^>]*>([^<]*)<', b)))]
        if len(nums) < 2: continue
        xy = np.array(nums[:len(nums) // 2 * 2]).reshape(-1, 2).mean(axis=0)
        S[d] = {'s': tc(d), 'u': g('SERV_HIPERLINK').replace(' ', '%20') if g('SERV_HIPERLINK').startswith('http') else '', 'x': g('CLASSIFICACAO'),
                'g': tc(g('MUNICIPIOS')), 'xy': tr.transform(*xy)}
match(list(S.values()), 'pt', ('Conimbriga', 'Olisipo', 'Ebora', 'Pax Iulia', 'Bracara Augusta', 'Scallabis', 'Ammaia', 'Mirobriga'))
