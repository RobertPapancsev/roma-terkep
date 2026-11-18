# v82: Feliratok – az EDR (Epigraphic Database Roma, Zenodo 10.5281/zenodo.18468635, v12, CC BY 4.0) római feliratainak összesítése.
# Bemenet: /home/claude/dl/edr/recs.json (insc/parse.py). Kimenet: insc/data.json
import json,re,collections
R=json.load(open('/home/claude/dl/edr/recs.json'))
rome=[r for r in R if 'Roma' in r['pf']]
def typ(r):
    t=' '.join(r['t']).lower()
    if 'sepulcralis' in t:return 'tomb'
    if 'sacer' in t:return 'sacred'
    if 'honorarius' in t:return 'honor'
    if 'oper. publ' in t:return 'build'
    return 'other'
T=['tomb','sacred','honor','build','other']
for r in rome:r['ty']=typ(r)
def unk(l):return (not l.strip()) or 'ignoratur' in l.lower() or l.strip() in('Roma','Roma?')
X0,X1,W=-200,700,25;B=list(range(X0,X1,W))
def aor(rows,maxspan=None):
    A={t:[0.0]*len(B) for t in T};n=0
    for r in rows:
        if r['nb']=='' or r['na']=='':continue
        a,b=int(r['nb']),int(r['na'])
        if b<a:continue
        if maxspan is not None and b-a>maxspan:continue
        if b<X0 or a>=X1:continue
        n+=1;L=b-a
        for k,x in enumerate(B):
            ov=(1.0 if x<=a<x+W else 0.0) if L==0 else max(0,min(b,x+W)-max(a,x))/L
            A[r['ty']][k]+=ov
    return {t:[round(v,1) for v in A[t]] for t in T},n
sAll,nAll=aor(rome);sT,nT=aor(rome,100)
# utak: kulcsszavak a lelőhely leírásában (sorrend számít: előbb a konkrétabb)
ROADS=[('appia',[r'via appia',r'vigna codini',r'vigna randanini',r'catacombe? di s\. callisto',r'catacombe di pretestato',r's\. sebastiano fuori',r'catacombe di s\. sebastiano',r'monumentum liviae',r'vigna amendola',r'vigna cantoni',r'tra via appia e via latina']),
 ('latina',[r'via latina',r'vigna aquari']),
 ('ardeatina',[r'via ardeatina',r'catacombe di domitilla',r'via cristoforo colombo']),
 ('ostiensis',[r'via ostiense',r's\. paolo fuori']),
 ('portuensis',[r'via portuense',r'monteverde',r'pozzo pantaleo']),
 ('aurelia',[r'via aurelia',r'villa pamphilj',r's\. pancrazio']),
 ('vaticana',[r'via triumphalis',r'necropoli vaticana',r's\. pietro',r'via cornelia',r'vaticano']),
 ('flaminia',[r'via flaminia']),
 ('salaria',[r'via salaria',r'tra via salaria e via pinciana',r'sepolcreto salario',r'via po\b',r'via livenza',r"corso d'italia",r'catacombe di priscilla',r'via pinciana',r'porta salaria',r'porta pinciana',r'via tevere',r'villa ludovisi']),
 ('nomentana',[r'via nomentana',r'catacombe di s\. agnese',r'villa torlonia']),
 ('tiburtina',[r'via tiburtina',r'agro verano',r's\. lorenzo fuori',r'tra via nomentana e via tiburtina']),
 ('praenestina',[r'via prenestina',r'porta maggiore',r'colombario degli statili',r'fuori porta maggiore']),
 ('labicana',[r'via labicana',r'via casilina',r'marcellino e pietro',r'equites singulares']),
 ('cassia',[r'via cassia'])]
CR=[(k,[re.compile(p,re.I) for p in L]) for k,L in ROADS]
def road(l):
    for k,L in CR:
        if any(p.search(l) for p in L):return k
    return None
RC={k:{t:0 for t in T} for k,_ in ROADS};nroad=0
for r in rome:
    if unk(r['loc']):continue
    k=road(r['loc'])
    if k:RC[k][r['ty']]+=1;nroad+=1
# leletegyüttesek
CX=[('statili',r'colombario degli statili','portamaior'),
 ('liviae',r'monumentum liviae',None),
 ('codini',r'vigna codini','columbariacodini'),
 ('volusii',r'monumentum volusiorum',None),
 ('salario',r'sepolcreto salario|tra via salaria e via pinciana|via po\b|via livenza','csalario'),
 ('carmel',r"corso d'italia, chiesa dei carmelitani",None),
 ('equites',r'equites singulares',None),
 ('jmonte',r'ebraica di monteverde',None),
 ('jrand',r'ebraica di vigna randanini|vigna randanini',None),
 ('jtorl',r'ebraiche di villa torlonia',None),
 ('callisto',r'catacombe? di s\. callisto',None),
 ('pretestato',r'catacombe di pretestato',None),
 ('domitilla',r'catacombe di domitilla',None),
 ('priscilla',r'catacombe di priscilla',None),
 ('spaolo',r's\. paolo fuori',None),
 ('vatican',r'necropoli vaticana|necropoli della via triumphalis',None),
 ('pamphilj',r'villa pamphilj',None),
 ('forum',r'foro romano',None),
 ('colosseum',r'colosseo','colosseum'),
 ('paedag',r'paedagogium','paedagogium'),
 ('foraug',r'foro di augusto','forumaug'),
 ('pacis',r'templum pacis','pacis'),
 ('fortra',r'foro di traiano','forumtra'),
 ('argentina',r'largo argentina','tempa')]
CXR=[(k,re.compile(p,re.I),e) for k,p,e in CX]
CXD={}
for k,p,e in CXR:
    rows=[r for r in rome if not unk(r['loc']) and p.search(r['loc'])]
    mids=sorted((int(r['nb'])+int(r['na']))/2 for r in rows if r['nb']!='' and r['na']!='')
    q=lambda f:int(round(mids[int(f*(len(mids)-1))])) if mids else None
    tc=collections.Counter(r['ty'] for r in rows)
    CXD[k]={"n":len(rows),"q1":q(.25),"q3":q(.75),"t":{t:tc.get(t,0) for t in T},"e":e}
loc=sum(1 for r in rome if not unk(r['loc']))
dated=sum(1 for r in rome if r['nb']!='' and r['na']!='')
TT=collections.Counter(r['ty'] for r in rome)
D={"bins":B,"w":W,"n":len(rome),"loc":loc,"dated":dated,"types":{t:TT[t] for t in T},"time":{"all":sAll,"tight":sT,"nAll":nAll,"nTight":nT},"roads":RC,"nroad":nroad,"cx":CXD}
json.dump(D,open('insc/data.json','w'),separators=(',',':'))
print(len(rome),'loc',loc,'dated',dated,TT,'nAll',nAll,'nT',nT,'nroad',nroad)
for k,v in sorted(RC.items(),key=lambda x:-sum(x[1].values())):print(k,sum(v.values()),v['tomb'])
for k,v in sorted(CXD.items(),key=lambda x:-x[1]['n']):print(k,v['n'],v['q1'],v['q3'],v['t'])
tot=[sum(sAll[t][k] for t in T) for k in range(len(B))]
print(sorted([(B[k],round(tot[k])) for k in range(len(B))],key=lambda x:-x[1])[:8])
for t in T: 
    tt=sAll[t];m=max(range(len(B)),key=lambda k:tt[k]);print(t,B[m],round(tt[m]))
