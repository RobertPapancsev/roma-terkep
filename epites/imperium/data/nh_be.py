# Belgium (Flandria): Agentschap Onroerend Erfgoed – Inventaris Onroerend Erfgoed, erfgoedobjecten a »Romeinse tijd«
# keltezéssel (thesaurus dateringen/1223 és alfogalmai; API 2026-11-13). Licenc: Modellicentie gratis hergebruik / CC BY-SA 4.0.
# Tisztán tájképi (landschappelijk) tételek csak akkor, ha a nevükben »Romein« szerepel. Koordináta: a kontúr középpontja (EPSG:31370).
import json, re, sys
sys.path.insert(0, '/home/claude/imperium/data'); from nh_common import laea, match
import numpy as np
D = json.load(open('/home/claude/dl/be/vl_rom.json')); tr = laea('EPSG:31370')
S = []
for k, v in D.items():
    dis = {d['naam'] for d in v['disciplines']}
    if dis == {'Landschappelijk'} and not re.search(r'romein', v['naam'], re.I): continue
    c = v['locatie'].get('contour')
    if not c: continue
    pts = np.array([q for poly in c['coordinates'] for ring in poly for q in ring])
    typ = [t['label'] for g in v['kenmerkgroepen'] for t in g['thesaurus'] if t['kenmerk']['naam'] == 'typologie'][:2]
    S.append({'s': v['naam'], 'u': f'https://inventaris.onroerenderfgoed.be/erfgoedobjecten/{k}', 'x': ', '.join(typ),
              'g': v['locatie'].get('gemeente') or '', 'xy': tr.transform(*pts.mean(axis=0))})
match(S, 'be', ('Atuatuca Tungrorum', 'Aduatuca Tungrorum', 'Oudenburg', 'Blicquy', 'Velzeke'))
