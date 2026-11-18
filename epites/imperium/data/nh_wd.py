# Országos örökséglisták a Wikidatán keresztül (v144): azok a tételek, amelyeknek van örökségvédelmi besorolása (P1435),
# koordinátája (P625) és országa (P17), és római emléknek minősülnek: korszak (P2348: Római Birodalom, ókori Róma, Római Köztársaság,
# késő antikvitás stb.), vagy típus (P31: római …, castrum, castellum, villa rustica, legiotábor, limes, thermae, mithraeum),
# vagy a név (helyi vagy angol címke: római/Roman/romano/ρωμαϊκ/римск/rimsk/romak/روماني/רומי …; kizárva: román stílus,
# katolikus, bizánci, oszmán, hammam stb.). Lekérdezés: 2026-11-13 (dl/wdh/<ország>.json), szűrés: dl/wdh/filt.py.
import json, re, sys
sys.path.insert(0, '/home/claude/imperium/data'); sys.path.insert(0, '/home/claude/dl/wdh')
from nh_common import laea, match
from filt import load
tr = laea()
def run(cc, names=()):
    d, o = load(cc); seen = set(); S = []
    for x in o:
        if x['q'] in seen: continue
        seen.add(x['q'])
        if not x['c'].lower().startswith('point('): continue
        lon, lat = map(float, x['c'][6:-1].split())
        nm = x['le'] or x['lab']
        if x['le'] and x['lab'] and x['lab'] != x['le'] and re.search(r'[A-Za-zÀ-ž]', x['lab']) and len(x['lab']) < 60: nm = x['le']
        h = x['h'].split('|')[0] if x['h'] else ''
        S.append({'s': nm, 'u': 'https://www.wikidata.org/wiki/' + x['q'], 'x': h, 'g': x['adm'], 'xy': tr.transform(lon, lat)})
    if S: match(S, cc, names)
    return len(d), len(S)
if __name__ == '__main__':
    for cc in sys.argv[1:]: print(cc, run(cc))
