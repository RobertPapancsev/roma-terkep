# v187: Russell 2013 kőbánya-gazetteer -> imp_st/quarries.json + stats/quarries_summary.json
import json, re
from collections import Counter
from pyproj import Transformer
R='/home/claude/imperium/'
tg=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km',always_xy=True)
Q=json.load(open(R+'data/quarries/quarries.json'))
IGN=r'granit|granodiorit|porphyr|basalt|diorit|gabbro|syenit|andesit|lava|tonalit|trachyt|gneiss|serpentin|dolerit|rhyolit|obsidian'
COL=r'\b(red|green|black|yellow|pink|polychrome|breccia|cipollino|pavonazzetto|giallo|rosso|verde|africano|portasanta|coloured|colored|multi-coloured|violet|purple|brown|orange|ochre|nero|bigio|onyx)\b'
def cat(m):
    s=m.lower()
    if re.search(IGN,s): return 4
    if 'breccia' in s or 'puddingstone' in s: return 1
    if 'marble' in s: return 1 if re.search(COL,s) else 0
    if re.search(r'alabaster|gypsum',s): return 5
    if re.search(r'limestone|travertine|chalk',s): return 2
    if re.search(r'sandstone|quartzite|conglomerate|greensand|\bgrit|millstone',s): return 3
    return 6
def reach(m):   # 0 = csak helyi használat, 1 = kivitték (a leírás szerint biztosan vagy valószínűleg)
    s=re.sub(r'inter-\s+','inter-',m.lower())
    return 1 if re.search(r'export|regionally',s) else 0
out=[]
for q in Q:
    x,y=tg.transform(q['Longitude'],q['Latitude'])
    out.append([int(round(x)),int(round(y)),q['Site'],q['Province'],q['Country'],cat(q['Material']),reach(q['Material']),q['Bibliography'][:140]])
json.dump(out,open(R+'imp_st/quarries.json','w'),ensure_ascii=False,separators=(',',':'))
C=Counter(o[5] for o in out); Rr=Counter(o[6] for o in out)
S={'n':len(out),'cat':[C.get(i,0) for i in range(7)],'reach':[Rr.get(i,0) for i in range(2)],
   'cat_reach':{i:[sum(1 for o in out if o[5]==i and o[6]==r) for r in range(2)] for i in range(7)},
   
   'pann':sorted([[o[2],o[3],o[5],o[6]] for o in out if 'Pannonia' in o[3]]),
   'prov':Counter(o[3] for o in out).most_common(12)}
json.dump(S,open(R+'data/stats/quarries_summary.json','w'),ensure_ascii=False,indent=1)
print(S['cat'],S['reach'],S['cat_reach']);print(S['pann']);print(S['prov'])
print([q['Material'] for q in Q if cat(q['Material'])==6][:12])
