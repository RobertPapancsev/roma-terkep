# v95: éremkincsek (CHRE – Coin Hoards of the Roman Empire, Oxford; CC BY-NC-SA). Bemenet: /home/claude/dl/chre/all.csv, italy_coins.csv (CSV-export, 2026-11-12)
import csv,json,math,collections,re
csv.field_size_limit(10**9)
R=list(csv.DictReader(open('/home/claude/dl/chre/all.csv',encoding='utf8')))
def num(x):
    try:return float(x)
    except:return None
def term(r):
    a,b=num(r['terminalYear1']),num(r['terminalYear2'])
    if a is None and b is None:return None
    a=b if a is None else a;b=a if b is None else b
    return (a+b)/2,a,b
def km(r):
    la,lo=num(r['latitude']),num(r['longitude'])
    if la is None or lo is None:return None
    return 111.2*math.hypot(la-41.8925,(lo-12.4853)*math.cos(math.radians(41.9)))
H=[r for r in R if r['hoardType'] in('Hoard','Hoard?')]
IT=[r for r in H if r['country']=='Italy']
ROME=[r for r in H if r['country']=='Italy' and km(r) is not None and km(r)<=10]
SUB=[r for r in H if r['country']=='Italy' and km(r) is not None and 10<km(r)<=25]
X0,X1,W=-50,500,25;B=list(range(X0,X1,W))
def hist(L):
    h=[0]*len(B);n=0
    for r in L:
        t=term(r)
        if t and X0<=t[0]<X1:h[int((t[0]-X0)//W)]+=1;n+=1
    return h,n
he,ne=hist(H);hi,ni=hist(IT)
def row(r):
    t=term(r);return {'id':r['id'],'name':r['hoardName'],'n':int(num(r['coinCount']) or 0),'t1':int(t[1]) if t else None,'t2':int(t[2]) if t else None,'reign':r['closingReign1'],'km':round(km(r),1),'type':r['hoardType'],'city':r['city'],'cld':r['coinLevelData'],'lat':num(r['latitude']),'lon':num(r['longitude']),'sum':r['summary'][:300]}
rome=sorted([row(r) for r in ROME if term(r)],key=lambda x:(x['t1']+x['t2'])/2)
sub=sorted([row(r) for r in SUB if term(r)],key=lambda x:(x['t1']+x['t2'])/2)
def reigns(L,k=12):
    c=collections.Counter(re.sub(r' \(.*\)$','',r['closingReign1']) for r in L if r['closingReign1'] and r['closingReign1']!='Uncertain');return c.most_common(k)
# érmék: Itália
PER=[(-50,68),(69,192),(193,284),(285,395),(396,500)]
def per(y):
    for i,(a,b) in enumerate(PER):
        if a<=y<=b:return i
TM={r['id']:term(r) for r in IT}
mat=[collections.Counter() for _ in PER];mint=[collections.Counter() for _ in PER];nco=0
for c in csv.DictReader(open('/home/claude/dl/chre/italy_coins.csv',encoding='utf8')):
    t=TM.get(c['hoard'])
    if not t:continue
    p=per(t[0])
    if p is None:continue
    q=int(num(c['quantity']) or 0)
    if q<=0:continue
    nco+=q
    m=c['material'] or '?';mat[p][m]+=q
    mi=c['mint']
    if mi and mi!='Uncertain':mint[p][mi]+=q
OUT={'nall':len(R),'nh':len(H),'nit':len(IT),'nsingle':sum(1 for r in R if r['hoardType']=='Single gold coin'),'bins':B,'w':W,'he':he,'hi':hi,'ne':ne,'ni':ni,'rome':rome,'sub':sub,'nrome':len(ROME),
 'reign_it':reigns(IT),'reign_all':reigns(H),'per':PER,'mat':[dict(m.most_common(6)) for m in mat],'mint':[dict(m.most_common(8)) for m in mint],'mintn':[sum(m.values()) for m in mint],'nco':nco}
json.dump(OUT,open('/home/claude/roma/chre/data.json','w'),ensure_ascii=False)
if __name__=='__main__':
    for k,v in OUT.items():
        if k not in('rome','sub'):print(k,v)
    for r in rome:print(r['id'],r['name'][:44],r['n'],r['t1'],r['t2'],r['reign'],r['km'],r['type'],'|',r['sum'][:110])
    print('--sub');[print(r['id'],r['name'][:44],r['n'],r['t1'],r['t2'],r['reign'],r['km']) for r in sub]
# --- Vezúv, Kr. u. 79: mennyivel korábbi a legkésőbbi érme az elrejtésnél?
VES=re.compile(r'pompe|ercolano|herculaneum|stabia|boscoreale|boscotrecase|torre annunziata|oplont|scafati|terzigno',re.I)
ves=[]
for r in IT:
    if VES.search(r['city']+' '+r['hoardName']+' '+r['ancientPlace']):
        t=term(r)
        if t and t[2]<=79:ves.append(79-t[2])
vs=sorted(ves)
def grp(m):
    m=re.sub(r' OR .*','',m)
    return 'gold' if m=='Gold' else 'silver' if m=='Silver' else 'billon' if m=='Base Silver' else 'bronze' if m in('Copper alloy','Brass','Copper','Bronze','Orichalcum') else 'other'
mat2=[collections.Counter() for _ in PER]
for c in csv.DictReader(open('/home/claude/dl/chre/italy_coins.csv',encoding='utf8')):
    t=TM.get(c['hoard'])
    if not t:continue
    p=per(t[0])
    if p is None:continue
    q=int(num(c['quantity']) or 0)
    if q>0:mat2[p][grp(c['material'] or '?')]+=q
OUT['ves']={'n':len(ves),'le1':sum(1 for v in ves if v<=1),'le10':sum(1 for v in ves if v<=10),'gt25':sum(1 for v in ves if v>25),'med':vs[len(vs)//2] if vs else None}
OUT['mat2']=[dict(m) for m in mat2]
OUT['romesh']=[round(100*(m.get('Rome',0))/s,1) for m,s in zip(mint,OUT['mintn'])]
OUT['nit_cities']=collections.Counter(r['region'] for r in IT).most_common(5)
json.dump(OUT,open('/home/claude/roma/chre/data.json','w'),ensure_ascii=False)
if __name__=='__main__':print(OUT['ves'],OUT['mat2'],OUT['romesh'],OUT['nit_cities'],sorted(collections.Counter(int(v) for v in ves).items())[:40])
