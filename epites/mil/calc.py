# v88: A Rómában állomásozó alakulatok a sírfeliratokon. Bemenet: EDR (tisztítás és ismétlődések: nm/calc.py; életkor: age/calc.py). Kimenet: mil/data.json
import json,re,collections,sys,importlib.util
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
A=load('agecalc','/home/claude/roma/age/calc.py');N=A.NMC;rom=A.rom;B=N.B;W=N.W;aw=N.aw
PL=load('plotcalc','/home/claude/roma/plot/calc.py');road=PL.road
COH=r'\b(?:cohor[st]|cohort?is|cohorte|cohorti|cohortem|chortis|chorte|chors|cortis|coh)'
U=[('praet',re.compile(COH+r' ([ivxl]+) (?:piae vindicis |pia vindice |[a-z]+ae? )?p?r(?:ae|e)toria|\b(?:miles|militi|militis|militem) praetorian|\bcastris praetori')),
 ('urb',re.compile(COH+r' ([ivxl]+) urban')),
 ('vig',re.compile(COH+r' ([ivxl]+) vigilum')),
 ('eqs',re.compile(r'\beq(?:ues|uitis|uiti|uitem|uites|uitum|uitibus|u)? singular|\bsingulari(?:s|um|bus)? (?:august|imperator|domini)')),
 ('cla',re.compile(r'\bclass(?:is|e|i|em) (?:praetoriae? |praetoria |pr )?(?:piae? vindicis? )?(?:misen|raven)')),
 ('ger',re.compile(r'\bcorpor(?:is)? custo[ds]|\bex collegio germanorum')),
 ('fru',re.compile(r'\bfrumentari(?:us|i|o|um)? legion|\bcastr\w+ peregrin|\bprinceps peregrin')),
 ('part',re.compile(r'\blegio(?:nis|ni|ne|nem)? ii parthic'))]
UK=[k for k,_ in U]
CLAK=re.compile(r'\bclass(?:is|e|i|em) (?:praetoriae? |praetoria |pr )?(?:piae? vindicis? )?(misen|raven)')
SERV=re.compile(r'\bmilitavit (?:annis|annos|annum|ann|anis) (?:plus minus )?([ivxl]+)\b|\bstipendiorum ([ivxl]+)\b')
NAT=re.compile(r'\bnatione ([a-z]+)')
NATN=[('Pannonius',r'^pannoni'),('Noricus',r'^noric'),('Bessus',r'^bess'),('Raetus',r'^r[a]?et'),('Dacus',r'^dac'),('Batavus',r'^bat[a]?[uv]|^badau'),('Syrus',r'^s[uy]r'),('Thrax',r'^t[h]?ra[xce]'),('Sardus',r'^sard'),('Afer',r'^af[e]?r'),('Cilix',r'^cili[xc]'),('Ubius',r'^ubi'),('Dalmata',r'^d[ae]lmat'),
 ('Aegyptius',r'^aegypt|^alexandrin'),('Maurus',r'^maur'),('Hispanus',r'^hispan'),('Helvetius',r'^helveti'),('Frisius',r'^frisi'),('Marsacus',r'^marsa[cq]'),('Germanus',r'^german'),('Italus',r'^ital'),('Moesus',r'^m[o]?es'),('Ponticus',r'^ponti'),('Graecus',r'^graec'),('Suebus',r'^suae?b'),('Baetasius',r'^baetas'),('Cannanefas',r'^cann[ao]n'),('Tunger',r'^tung'),('Britto',r'^brit'),('Corsus',r'^cors'),('Phryx',r'^phry'),('Bithynus',r'^bith'),('Asianus',r'^asian'),('Cappadox',r'^cappad')]
NATR=[(n,re.compile(p)) for n,p in NATN]
def nat(w):
    for n,rx in NATR:
        if rx.search(w):return n
    return None
rome=[r for r in N.rome if 'sepulcralis' in ' '.join(r['t']).lower()]
CNT=collections.Counter();num={k:collections.Counter() for k in ('praet','urb','vig')};cla=collections.Counter()
TM={k:[0.0]*len(B) for k in UK};RD={k:collections.Counter() for k in UK};NT={k:collections.Counter() for k in UK}
AGEL={k:[] for k in UK};SV={k:[] for k in UK};EN={k:[] for k in UK};MID={k:[] for k in UK};nany=0;nloc={k:0 for k in UK}
SAMP=collections.defaultdict(list)
for r in rome:
    c=N.clean(N.T.get(r['id'],''))
    if N.tlen(c)<8:continue
    f=[]
    for k,rx in U:
        ms=list(rx.finditer(c))
        if ms:
            f.append(k)
            if k in num:
                for v in {rom(m.group(1)) for m in ms if m.group(1)}:num[k][v]+=1
            SAMP[k].append((r['id'],c[max(0,ms[0].start()-40):ms[0].end()+40]))
    if not f:continue
    nany+=1
    for m in {x for x in CLAK.findall(c)}:cla[m]+=1
    for k in f:CNT[k]+=1
    if r['nb']!='' and r['na']!='':
        a,b=int(r['nb']),int(r['na'])
        if not(b<a or b<B[0] or a>=B[-1]+W):
            for i,v in enumerate(aw(a,b)):
                if v:
                    for k in f:TM[k][i]+=v
            for k in f:MID[k].append((a+b)/2)
    rk=road(r['loc'])
    for k in f:
        if rk:RD[k][rk]+=1;nloc[k]+=1
    if len(f)==1:
        k=f[0]
        for w in {nat(x) for x in NAT.findall(c)}-{None}:NT[k][w]+=1
        ag=[];sv=[]
        for m in A.AGE.finditer(c):
            if c[m.end():].lstrip().startswith('¤t'):continue
            pw=c[max(0,m.start()-40):m.start()].split()
            if A.MAR.search(' '.join(pw[-5:])):continue
            v=rom(m.group(1))
            if 0<v<=120:ag.append(v)
        for m in SERV.finditer(c):
            if c[m.end():].lstrip().startswith('¤t'):continue
            v=rom(m.group(1) or m.group(2))
            if 0<v<=60:sv.append(v)
        if len(ag)==1:AGEL[k].append(ag[0])
        if len(sv)==1:SV[k].append(sv[0])
        if len(ag)==1 and len(sv)==1 and 10<=ag[0]-sv[0]<=45:EN[k].append(ag[0]-sv[0])
def q(L,f):
    L=sorted(L);return L[int(f*(len(L)-1))] if L else None
def st(L):return [len(L),q(L,.25),q(L,.5),q(L,.75)]
def per(L):
    if len(L)<5:return None
    lo=int(q(L,.25)//25*25);hi=int(-(-q(L,.75)//25)*25)
    return [lo,hi if hi>lo else lo+25]
D={'bins':B,'w':W,'nany':nany,'cnt':dict(CNT),'num':{k:sorted(v.items()) for k,v in num.items()},'cla':dict(cla),'time':{k:[round(v,1) for v in t] for k,t in TM.items()},
 'per':{k:per(MID[k]) for k in UK},'roads':{k:{'n':nloc[k],'top':RD[k].most_common(3)} for k in UK},'nat':{k:NT[k].most_common(6) for k in UK},
 'age':{k:st(AGEL[k]) for k in UK},'serv':{k:st(SV[k]) for k in UK},'enl':{k:st(EN[k]) for k in UK},'enl_all':st([x for k in UK for x in EN[k]])}
json.dump(D,open('/home/claude/roma/mil/data.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump({k:v for k,v in SAMP.items()},open('/home/claude/roma/mil/samples.json','w'),ensure_ascii=False)
if __name__=='__main__':
    for k,v in D.items():
        if k not in('bins','time'):print(k,v)
