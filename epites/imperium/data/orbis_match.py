# ORBIS (W. Scheidel – E. Meeks, Stanford; hálózati adatok CC BY 3.0): Róma-központú lekérdezések (roma/orbis/data.json) párosítása a térkép helyeivel
import json,csv,glob,re,math
from pyproj import Transformer
R='/home/claude/imperium/'
tr=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km',always_xy=True)
S={r[0]:(r[1],float(r[3]),float(r[4])) for r in csv.reader(open('/home/claude/dl/orbis/orbis_v2/sites.csv',encoding='utf8')) if r and r[0].isdigit()}
D={s['id']:s for s in json.load(open('/home/claude/roma/orbis/data.json'))['sites']}
P={}
for p in json.load(open(R+'imp_base.json'))['pts']:P[p[7]]=p
for f in glob.glob(R+'tiles/*.json'):
    for p in json.load(open(f)).get('s',[]):P[p[7]]=p
norm=lambda s:re.sub(r'[^a-z]','',(s or '').lower())
pts=list(P.values())
out={};log=[]
for k,s in D.items():
    n,lon,lat=S[k];x,y=tr.transform(lon,lat)
    best=None
    for p in pts:
        d=math.hypot(p[1]-x,p[2]-y)
        if d>25:continue
        names={norm(a) for a in re.split(r'[/,]',(p[3] or '')+'/'+(p[4] or '')) if a.strip()}
        nm=norm(n.split('(')[0]) in names
        sc=(0 if nm else 1,d)
        if (nm or d<=3) and (best is None or sc<best[0]):best=(sc,p,nm,d)
    if best:
        p=best[1];i=p[7]
        if i in out and out[i]['dk']<=best[3]:continue
        out[i]={'o':n,'dk':round(best[3],1),'nm':best[2],'tj':round(s['tj'],1),'tw':round(s['tw'],1) if s.get('tw') else None,'fj':round(s['fj'],1) if s.get('fj') else None,'cj':round(s['cj'],2) if s.get('cj') else None,'km':s['km']}
    else: log.append(n)
json.dump(out,open(R+'data/agg/orbis_match.json','w'),ensure_ascii=False)
print(len(D),len(out),'name',sum(v['nm'] for v in out.values()),'unmatched',len(log));print(log[:40])
for i in ['10898','3','10899']:print(i,out.get(i))
