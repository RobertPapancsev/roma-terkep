# LIST (CC BY 4.0) feliratok hozzárendelése a térkép helyeihez: (a) Pleiades-azonosító, (b) ókori lelőhelynév (EDCS 'place' ' / ' utáni része, EDH findspot_ancient_clean) 15 km-en belül; (c) külön: 2 km-es körzet
import pyarrow.parquet as pq,numpy as np,json,glob,re,collections
from shapely import wkb
from pyproj import Transformer
from scipy.spatial import cKDTree
R='/home/claude/imperium/'
t=pq.read_table('/home/claude/dl/list/LIST_v1-2.parquet',columns=['pleiades_id','place','findspot_ancient_clean','type_of_inscription_clean','type_of_inscription_auto','geometry','people','not_before','not_after']).to_pandas()
tr=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km',always_xy=True)
X=np.full(len(t),np.nan);Y=np.full(len(t),np.nan)
for k,g in enumerate(t.geometry):
    if g is None:continue
    try:
        p=wkb.loads(bytes(g))
        if not p.is_empty:X[k],Y[k]=tr.transform(p.x,p.y)
    except Exception:pass
def ty(a,b):
    for v in (a,b):
        if isinstance(v,str) and v.strip() and v not in('NULL','None'):return v.strip()
    return ''
TY=np.array([ty(a,b) for a,b in zip(t.type_of_inscription_clean,t.type_of_inscription_auto)])
norm=lambda s:re.sub(r'[^a-z]','',s.lower().replace('?',''))
BYN=collections.defaultdict(list);BYP=collections.defaultdict(list)
for k,(pl,f,pid) in enumerate(zip(t.place,t.findspot_ancient_clean,t.pleiades_id)):
    ns=set()
    if isinstance(pl,str):
        if ' / ' in pl:
            for a in pl.split(' / ')[1:]:ns.add(norm(a))
        elif pl.strip() not in('?',''):ns.add(norm(pl))  # EDCS: ahol a mai és az ókori név azonos, csak egy név áll
    if isinstance(f,str) and f not in('NULL',''):ns.add(norm(f))
    for n in ns:
        if len(n)>=3:BYN[n].append(k)
    if isinstance(pid,str) and pid.strip().isdigit():BYP[int(pid)].append(k)
ok=~np.isnan(X);IDX=np.where(ok)[0];T=cKDTree(np.c_[X[ok],Y[ok]])
P={}
for p in json.load(open(R+'imp_base.json'))['pts']:P[p[7]]=p
for f in glob.glob(R+'tiles/*.json'):
    for p in json.load(open(f)).get('s',[]):P[p[7]]=p
D=json.load(open(R+'data/agg/dare_parsed.json'))
import ast
PE={}
for k,v in enumerate(t.people):
    if isinstance(v,str) and len(v)>2:
        try:PE[k]=ast.literal_eval(v)
        except Exception:pass
NB=t.not_before.to_numpy(dtype=float);NA=t.not_after.to_numpy(dtype=float)
def social(ix):
    pp=[k for k in ix if k in PE]
    if not pp:return None
    n=0;g=collections.Counter();stc=collections.Counter();ages=[];og=collections.Counter()
    for k in pp:
        for q in PE[k]:
            n+=1;g[q.get('gender')]+=1
            for x in (q.get('status') or '').split(';'):
                x=x.strip().rstrip('?').strip()
                if x:stc[x]+=1
            a=q.get('age: years')
            if a:
                m=re.match(r'\s*(\d+)',str(a))
                if m and 0<int(m.group(1))<=110:ages.append(int(m.group(1)))
            o=q.get('origo')
            if o:
                o=o.replace('*','').replace('?','').strip()
                if o and '[' not in o:og[o]+=1
    r={'ni':len(pp),'n':n,'m':g.get('male',0),'f':g.get('female',0),'st':stc.most_common()}
    if ages:
        ages.sort();b=collections.Counter(min(a//10,7) for a in ages);r['age']=[len(ages),ages[len(ages)//2],[b.get(i,0) for i in range(8)]]
    if og:r['og']=og.most_common(6)
    return r
def cent(ix):
    c=collections.Counter()
    for k in ix:
        a,b=NB[k],NA[k]
        if np.isnan(a) or np.isnan(b) or b-a>200:continue
        m=(a+b)/2;cc=int(m//100)+1 if m>0 else -int((-m)//100)-1
        if -2<=cc<=7:c[cc]+=1
    return sorted(c.items()) if c else None
out={};soc={};st=collections.Counter()
for i,p in P.items():
    x,y=p[1],p[2];d=D.get(i,{})
    names={norm(s) for s in re.split(r'[/,]',(p[3] or '')+'/'+d.get('hist','')) if len(norm(s))>=3}
    pid=None
    for u,_ in d.get('links',{}).get('Pleiades',[]):
        m=re.search(r'places/(\d+)',u)
        if m:pid=int(m.group(1))
    S=set(BYP.get(pid,[])) if pid else set()
    for n in names:
        for k in BYN.get(n,[]):
            if ok[k] and (X[k]-x)**2+(Y[k]-y)**2<=225:S.add(k)
    G=[IDX[j] for j in T.query_ball_point([x,y],2.0)]
    r={}
    if S:
        c=collections.Counter(TY[list(S)]);r['m']=[len(S),[[a,b] for a,b in c.most_common() if a][:6],c.get('',0)];st['m']+=1
    if G:
        c=collections.Counter(TY[G]);r['g']=[len(G),[[a,b] for a,b in c.most_common() if a][:6],c.get('',0)];st['g']+=1
    if r:out[i]=r
    useS=len(S)>=len(G)
    base=sorted(S) if useS else G   # a nagyobb halmaz: név szerinti vagy 2 km-es
    if base:
        z={}
        so=social(base)
        if so:z['so']=so;st['so']+=1
        ce=cent(base)
        if ce:z['ce']=ce;st['ce']+=1
        if z:z['b']='m' if useS else 'g';soc[i]=z
json.dump(out,open(R+'data/agg/list_match.json','w'))
json.dump(soc,open(R+'data/agg/list_social.json','w'),ensure_ascii=False)
print(len(t),int(ok.sum()),st)
for i in ['10898','3','2','10899']:print(i,P[i][3],json.dumps(soc.get(i),ensure_ascii=False)[:600])
