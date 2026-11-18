# v88: Sírtelkek mérete („in fronte pedes … in agro pedes …”). Bemenet: EDR (nm/calc.py tisztítása, ismétlődések nélkül). Kimenet: plot/data.json
import json,re,collections,sys,importlib.util
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
A=load('agecalc','/home/claude/roma/age/calc.py');N=A.NMC;rom=A.rom;B=N.B;W=N.W;aw=N.aw
NUM=r'([ivxlc]+)\b( s\b| semis\b)?'
PED=r'(?:pedes|pides|pedis|pes|ped|p)'
FR=re.compile(r'\bin front(?:e|em) '+PED+' '+NUM);AG=re.compile(r'\bin a[gc]r(?:o|um|os) '+PED+' '+NUM)
QQ=re.compile(r'\bquoquo ?vers(?:us|um) '+PED+' '+NUM)
ROADS=[('appia',[r'via appia',r'vigna codini',r'vigna randanini',r'catacombe? di s\. callisto',r'catacombe di pretestato',r's\. sebastiano fuori',r'catacombe di s\. sebastiano',r'monumentum liviae',r'vigna amendola',r'vigna cantoni',r'tra via appia e via latina']),
 ('latina',[r'via latina',r'vigna aquari']),('ardeatina',[r'via ardeatina',r'catacombe di domitilla',r'via cristoforo colombo']),('ostiensis',[r'via ostiense',r's\. paolo fuori']),
 ('portuensis',[r'via portuense',r'monteverde',r'pozzo pantaleo']),('aurelia',[r'via aurelia',r'villa pamphilj',r's\. pancrazio']),
 ('vaticana',[r'via triumphalis',r'necropoli vaticana',r's\. pietro',r'via cornelia',r'vaticano']),('flaminia',[r'via flaminia']),
 ('salaria',[r'via salaria',r'tra via salaria e via pinciana',r'sepolcreto salario',r'via po\b',r'via livenza',r"corso d'italia",r'catacombe di priscilla',r'via pinciana',r'porta salaria',r'porta pinciana',r'via tevere',r'villa ludovisi']),
 ('nomentana',[r'via nomentana',r'catacombe di s\. agnese',r'villa torlonia']),('tiburtina',[r'via tiburtina',r'agro verano',r's\. lorenzo fuori',r'tra via nomentana e via tiburtina']),
 ('praenestina',[r'via prenestina',r'porta maggiore',r'colombario degli statili',r'fuori porta maggiore']),('labicana',[r'via labicana',r'via casilina',r'marcellino e pietro',r'equites singulares']),('cassia',[r'via cassia'])]
CR=[(k,[re.compile(p,re.I) for p in L]) for k,L in ROADS]
def road(l):
    for k,L in CR:
        if any(p.search(l) for p in L):return k
    return None
def val(m,c):
    if c[m.end():].lstrip().startswith('¤t'):return None   # csonka szám
    v=rom(m.group(1))
    if v<=0 or v>2000:return None
    return v+(0.5 if m.group(2) else 0)
P=[]   # (rec, fronte, agro)
nfr=0
if __name__=='__main__' or True:
    for r in N.rome:
        c=N.clean(N.T.get(r['id'],''))
        if 'in front' not in c and 'quoquo' not in c:continue
        got=None
        for seg in c.split('§'):
            f=FR.search(seg);a=AG.search(seg)
            if f:nfr+=1
            if f and a and len(FR.findall(seg))==1 and len(AG.findall(seg))==1:
                fv=val(f,seg);av=val(a,seg)
                if fv and av:got=(fv,av);break
            q=QQ.search(seg)
            if q and not f:
                v=val(q,seg)
                if v:got=(v,v);break
        if got:P.append((r,got[0],got[1]))
def q(L,f):
    L=sorted(L);return L[int(f*(len(L)-1))]
FT=0.296
F=[p[1] for p in P];G=[p[2] for p in P];AR=[p[1]*p[2] for p in P]
sizes=collections.Counter((p[1],p[2]) for p in P)
fh=collections.Counter(min(int(x),40) for x in F)
bands=[(0,50),(50,100),(100,150),(150,200),(200,300),(300,500),(500,1000),(1000,10**9)]
ah=[sum(1 for a in AR if lo<=a<hi) for lo,hi in bands]
RD=collections.defaultdict(list)
for r,f,a in P:
    k=road(r['loc']) if not A.NMC.clean(r['loc'])=='' else None
    if k:RD[k].append((f,a))
roads={k:{'n':len(v),'f':q([x[0] for x in v],.5),'a':q([x[1] for x in v],.5),'ar':q([x[0]*x[1] for x in v],.5),'q1':q([x[0]*x[1] for x in v],.25),'q3':q([x[0]*x[1] for x in v],.75)} for k,v in RD.items() if len(v)>=15}
# idő: középérték korszakonként (a keltezés közepe szerint)
per=[(-100,-25),(-25,25),(25,75),(75,150),(150,300)]
PT=[]
for lo,hi in per:
    S=[(f,a) for r,f,a in P if r['nb']!='' and r['na']!='' and lo<=(int(r['nb'])+int(r['na']))/2<hi and int(r['na'])-int(r['nb'])<=150]
    PT.append({'lo':lo,'hi':hi,'n':len(S),'f':q([x[0] for x in S],.5) if S else None,'a':q([x[1] for x in S],.5) if S else None,'ar':q([x[0]*x[1] for x in S],.5) if S else None})
D={'n':len(P),'nfr':nfr,'f':[q(F,.25),q(F,.5),q(F,.75)],'a':[q(G,.25),q(G,.5),q(G,.75)],'ar':[q(AR,.25),q(AR,.5),q(AR,.75)],'max':max(AR),'top':[[f,a,n] for (f,a),n in sizes.most_common(12)],
   'sq':sum(1 for p in P if p[1]==p[2]),'deeper':sum(1 for p in P if p[2]>p[1]),'wider':sum(1 for p in P if p[1]>p[2]),'f12':sum(1 for x in F if x==12),'ahist':ah,'bands':[[lo,hi if hi<10**9 else None] for lo,hi in bands],'roads':roads,'per':PT,
   'big':sorted([[p[1],p[2],p[0]['id'],p[0]['loc'][:60]] for p in P],key=lambda x:-x[0]*x[1])[:8],'ft':FT}
json.dump(D,open('/home/claude/roma/plot/data.json','w'),ensure_ascii=False,separators=(',',':'))
if __name__=='__main__':
    for k,v in D.items():print(k,v)
    print(sorted(fh.items()))
