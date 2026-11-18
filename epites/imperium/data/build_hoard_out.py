# v205: a CHRE-kincsleletek megjelölése aszerint, hogy a birodalom legnagyobb kiterjedésén (AWMC Kr. u. 117 ∪ 200, 30 km-es ráhagyással) kívül esnek-e.
# imp_st/hoards.json sorok: [x,y,záró év,érmeszám] -> [x,y,záró év,érmeszám,kívül 0/1]
import json, collections
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union
from shapely.prepared import prep
R='/home/claude/imperium/'
b=json.load(open(R+'imp_base.json'));polys=[]
for k in ('117','200'):
    for r in b['ext'][k]:
        s=r[1:] if r[0]=='i' else r
        if s[0]!='p': continue
        pts=[tuple(map(float,q.split(','))) for q in s[1:].split()]
        if len(pts)>=3:
            p=Polygon(pts)
            polys.append(p if p.is_valid else p.buffer(0))
U=unary_union(polys).buffer(30);PU=prep(U);print('terület (M km2):',round(U.area/1e6,2))
H=json.load(open(R+'imp_st/hoards.json'))
for h in H:
    del h[4:];h.append(0 if PU.contains(Point(h[0],h[1])) else 1)
json.dump(H,open(R+'imp_st/hoards.json','w'),separators=(',',':'))
out=[h for h in H if h[4]]
dec=collections.Counter((h[2]//50)*50 for h in out)
per=lambda y:0 if y<69 else 1 if y<193 else 2 if y<260 else 3 if y<285 else 4
sm={'n':len(H),'out':len(out),'coins':sum(h[3] or 0 for h in out),'per':[sum(1 for h in out if per(h[2])==i) for i in range(5)],'perall':[sum(1 for h in H if per(h[2])==i) for i in range(5)],'tl':sorted(dec.items()),
    'north':sum(1 for h in out if h[1]>600 and h[0]>-900),'east':sum(1 for h in out if h[0]>2300)}
json.dump(sm,open(R+'data/stats/hoard_out_summary.json','w'));print(sm)
