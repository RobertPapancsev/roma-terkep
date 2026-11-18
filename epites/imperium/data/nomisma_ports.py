# Pénzverdék (nomisma.org SPARQL, 2026-11-12; fogalmak CC BY, típuskatalógusok partnerlicenccel – csak saját darabszám-összesítés)
# és kikötők (A. de Graauw: Geodatabase of Ancient Coastal Settlements, Ports and Harbours, AncientPorts.xlsx, CC BY 4.0) → data/agg/mints.json, ports.json
import csv,json,re,collections,glob,math
import openpyxl
R='/home/claude/imperium/';N='/home/claude/dl/nomisma/'
D=json.load(open(R+'data/agg/dare_parsed.json'))
P={}
for p in json.load(open(R+'imp_base.json'))['pts']:P[p[7]]=p
for f in glob.glob(R+'tiles/*.json'):
    for p in json.load(open(f)).get('s',[]):P[p[7]]=p
PID=collections.defaultdict(list)
for i in P:
    for u,_ in D.get(i,{}).get('links',{}).get('Pleiades',[]):
        m=re.search(r'places/(\d+)',u)
        if m:PID[int(m.group(1))].append(i)
# ---- pénzverdék
ML={};MP=collections.defaultdict(set)
for r in csv.DictReader(open(N+'mints.csv')):
    ML[r['m']]=r['l'];m=re.search(r'places/(\d+)',r['p'])
    if m:MP[r['m']].add(int(m.group(1)))
SL={r['s']:r['l'] for r in csv.DictReader(open(N+'srclab.csv'))}
AL={r['a']:r['l'] for r in csv.DictReader(open(N+'authlab.csv'))}
TY=collections.defaultdict(list)
for r in csv.DictReader(open(N+'types.csv')):TY[r['m']].append(r)
AU=collections.defaultdict(list)
for r in csv.DictReader(open(N+'auth.csv')):AU[r['m']].append((int(r['n']),r['a']))
def yr(s):
    try:return int(s)
    except:return None
mints=collections.defaultdict(list)
for m,lab in ML.items():
    places={i for p in MP[m] for i in PID.get(p,[])}
    if not places:continue
    ser=collections.Counter();y0=[];y1=[]
    for r in TY.get(m,[]):
        ser[SL.get(r['src'],r['src'].rsplit('/',1)[-1])]+=int(r['n'])
        if yr(r['s0']) is not None:y0.append(yr(r['s0']))
        if yr(r['e1']) is not None:y1.append(yr(r['e1']))
    au=[[AL.get(a,a.rsplit('/',1)[-1].replace('_',' ')),n] for n,a in sorted(AU.get(m,[]),reverse=True)[:6]]
    rec={'u':m,'l':lab,'nt':sum(ser.values()),'ser':ser.most_common(),'y':[min(y0) if y0 else None,max(y1) if y1 else None],'au':au}
    for i in places:mints[i].append(rec)
json.dump(mints,open(R+'data/agg/mints.json','w'),ensure_ascii=False)
print('mints',len(ML),'with place',len({r['u'] for v in mints.values() for r in v}),'places',len(mints))
for i in ['10898','3']:print(i,json.dumps(mints.get(i),ensure_ascii=False)[:500])
s=[i for i,p in P.items() if p[3] in('Siscia','Lugdunum','Antiochia')]
for i in s:print(P[i][3],json.dumps(mints.get(i),ensure_ascii=False)[:700])
# ---- kikötők
wb=openpyxl.load_workbook('/home/claude/dl/ports/AncientPorts.xlsx',read_only=True,data_only=True)
ws=wb['PLACES'];rows=ws.iter_rows(values_only=True);H=[h for h in next(rows)]
ix={h:k for k,h in enumerate(H) if h}
from pyproj import Transformer
tr=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km',always_xy=True)
norm=lambda s:re.sub(r'[^a-z]','',(s or '').lower())
STR=['BW','QU','PL','MO','CN','SL','SH','SY','EX','LK','PH','HO','VM','FT','FP','QR','FO','SW']
PER=['Li','Mi','My','Pn','Eg','Gr','He','Ro','By']
ports={};st=collections.Counter();pts=list(P.values())
def g(r,k):
    v=r[ix[k]] if k in ix and ix[k]<len(r) else None
    return v.strip() if isinstance(v,str) else v
for r in rows:
    if r is None or r[0] is None:continue
    lat,lon=g(r,'LATITUDE'),g(r,'LONGITUDE')
    if not isinstance(lat,(int,float)) or not isinstance(lon,(int,float)):continue
    cand=set()
    m=re.search(r'places/(\d+)',str(g(r,'DARE') or ''))
    if m and m.group(1) in P:cand.add(m.group(1));how='dare'
    if not cand:
        m=re.search(r'places/(\d+)',str(g(r,'PLEIADES') or ''))
        if m:cand|=set(PID.get(int(m.group(1)),[]));how='pleiades'
    if not cand and g(r,'NAME'):
        x,y=tr.transform(lon,lat);names={norm(a) for a in re.split(r'[,/]',str(g(r,'NAME')))}
        best=None
        for p in pts:
            d=math.hypot(p[1]-x,p[2]-y)
            if d<=10 and norm(p[3]) in names and (best is None or d<best[0]):best=(d,p[7])
        if best:cand.add(best[1]);how='name'
    if not cand:st['nomatch']+=1;continue
    rec={'nb':g(r,'NB'),'n':g(r,'NAME'),'mod':g(r,'NAME_MOD'),'f':g(r,'FOUNDATION')}
    aa=g(r,'AUTH_ANC')
    if aa:rec['aa']=[a.strip() for a in str(aa).replace('\xa0',' ').split(';') if a.strip()]
    rec['re']=g(r,'RE');rec['si']=g(r,'SI');rec['su']=g(r,'SU');rec['ps']=g(r,'PS');rec['pp']=g(r,'PP')
    rec['s']=[k for k in STR if g(r,k)]
    rec['per']=[k for k in PER if g(r,k)]
    rec={k:v for k,v in rec.items() if v not in(None,'',[])}
    for i in cand:
        ports.setdefault(i,[]).append(rec)
    st[how]+=1
json.dump(ports,open(R+'data/agg/ports.json','w'),ensure_ascii=False,default=str)
print('ports',st,'places',len(ports))
for i in ['10898']+[i for i,p in P.items() if p[3] in('Ostia','Carthago','Caesarea')][:3]:print(P[i][3],json.dumps(ports.get(i),ensure_ascii=False,default=str)[:900])
c=collections.Counter(str(v.get(k)) for vs in ports.values() for v in vs for k in ['re','si','su','ps','pp'] );print(c.most_common(30))
