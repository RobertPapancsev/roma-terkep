# v79: építési aktivitás – a térkép saját adataiból. Kimenet: bld/data.json
import json,glob,re,collections
X0,X1,W=-800,800,25
B=list(range(X0,X1,W))
GS={'house':['STRUTTURE INSEDIATIVE E ABITATIVE'],'water':['INFRASTRUTTURE IDRAULICHE'],'cult':['LUOGHI DI CULTO'],'tomb':['CONTESTI FUNERARI'],
 'public':["STRUTTURE DI PUBBLICA UTILITA'","STRUTTURE DA SPETTACOLO, SVAGO, ATTIVITA' CULTURALI",'STRUTTURE AMMINISTRATIVE ','MONUMENTI ONORARI E CELEBRATIVI','STRUTTURE ASSISTENZIALI'],
 'trade':['STRUTTURE PRODUTTIVE E COMMERCIALI ','INFRASTRUTTURE PORTUALI','INFRASTRUTTURE AGRARIE'],
 'infra':['INFRASTRUTTURE VIARIE','INFRASTRUTTURE DI FORTIFICAZIONE/MILITARI'],'other':['DA IDENTIFICARE','ALTRO']}
G1=list(GS);cls={c:g for g,L in GS.items() for c in L}
U={}
for f in glob.glob('st_*.json'):
    for p in json.load(open(f))['parts']:U[p['id']]=p
OK={'strutture','rivestimenti pavimentali','rivestimenti parietali'}
E=[]
for p in U.values():
    if p.get('o') not in OK or p.get('c') not in cls:continue
    for e in p.get('ch',[]):
        if e[0]=='cronologia di impianto\\fondazione' and e[1] is not None and e[2] is not None and e[2]>=e[1]:E.append((cls[p['c']],e[1],e[2]))
def aor(rows,maxspan=None):
    A={g:[0.0]*len(B) for g in G1};n=0
    for g,a,b in rows:
        if maxspan is not None and b-a>maxspan:continue
        if b<X0 or a>=X1:continue
        n+=1;L=b-a
        for k,x in enumerate(B):
            if L==0: ov=1.0 if x<=a<x+W else 0.0
            else: ov=max(0,min(b,x+W)-max(a,x))/L
            A[g][k]+=ov
    return {g:[round(v,2) for v in A[g]] for g in G1},n
sAll,nAll=aor(E);sTight,nTight=aor(E,100)
# a térkép elemei
b=open('body_v60pre.html',encoding='utf8').read()
FN=json.loads(re.search(r'^const FN=(\{.*?\});',b,re.M).group(1))
H=re.findall(r'\{id:"([a-z0-9_]+)",((?:[a-z]+:(?:"[^"]*"|-?\d+|true|false),)*)',b)
G2=['temple','church','house','bath','aqua','gate','tomb','other'];M={g:[0]*len(B) for g in G2};nm=0;out=0
for i,rest in H:
    d=dict(re.findall(r'([a-z]+):("[^"]*"|-?\d+|true|false)',rest))
    if 'from' not in d:continue
    f=int(d['from'])
    g='church' if d.get('ch')=='true' else (FN.get(i,['other'])[0])
    if f<X0 or f>=X1:out+=1;continue
    k=(f-X0)//W;M[g][k]+=1;nm+=1
D={"bins":B,"w":W,"sitar":{"all":sAll,"tight":sTight,"nAll":nAll,"nTight":nTight,"nEntries":len(E)},"map":{"c":M,"n":nm,"out":out}}
json.dump(D,open('bld/data.json','w'),separators=(',',':'))
print('entries',len(E),'all',nAll,'tight',nTight,'map',nm,'out',out)
def top(S):
    tot=[sum(S[g][k] for g in S) for k in range(len(B))];o=sorted(range(len(B)),key=lambda k:-tot[k])[:6]
    return [(B[k],round(tot[k],1)) for k in o]
print('sitar all top',top(sAll));print('sitar tight top',top(sTight))
tm=[sum(M[g][k] for g in G2) for k in range(len(B))];print('map top',sorted([(B[k],tm[k]) for k in range(len(B))],key=lambda x:-x[1])[:8])
print({g:sum(M[g]) for g in G2})
print({g:round(sum(sAll[g]),1) for g in G1})
