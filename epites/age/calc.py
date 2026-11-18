# v86: Életkor és családi kapcsolatok a sírfeliratokon. Bemenet: recs.json, text.json (EDR). Kimenet: age/data.json
import json,re,collections,sys,statistics
import importlib.util
_s=importlib.util.spec_from_file_location('nmcalc','/home/claude/roma/nm/calc.py');NMC=importlib.util.module_from_spec(_s);_s.loader.exec_module(NMC)
clean=NMC.clean;T=NMC.T;B=NMC.B;W=NMC.W;aw=NMC.aw;PRAE=NMC.PRAE
rome=[r for r in NMC.rome if 'sepulcralis' in ' '.join(r['t']).lower()]
V={'i':1,'v':5,'x':10,'l':50,'c':100}
def rom(s):
    t=0;mx=0
    for ch in reversed(s):
        v=V[ch]
        if v<mx:t-=v
        else:t+=v;mx=v
    return t
NUM=r'([ivxlc]+)\b'
AGE=re.compile(r'\b(?:vix(?:it|sit|et|xit)?|bix(?:it|et)|visit) (?:in pace )?(?:annis|annos|annum|anno|annus|annu|ann|anos|anis|anni) (?:plus minus |p m |pm |plus m )?'+NUM+r'(?: (?:et )?(?:mensibus|menses|mensib|mens|mesibus|mese|mensem|mense|mesis) '+NUM+r')?(?: (?:et )?(?:diebus|dies|die|dieb) '+NUM+r')?')
AGE2=re.compile(r'\bannorum '+NUM)
INF=re.compile(r'\b(?:vix(?:it|sit|et)?|bix(?:it|et)) (?:mensibus|menses|mens|mesibus) '+NUM+r'|\b(?:vix(?:it|sit|et)?|bix(?:it|et)) (?:diebus|dies) '+NUM)
MAR=re.compile(r'\bcum (?:quo|qua|quem|que|eo|ea|quibus)\b|\bmecum\b|\bsecum\b|\bin coniugio\b|\bsine (?:ulla )?(?:querel|lite|iurgio|offensa|discrimin|macula|crimine|animi|bile|stomacho|ullo)')
REL={'spouse':r'\b(?:coniugi|coiugi|coniuci|coiuci|coniugei|uxori|uxsori|marito)\b','contub':r'\bcontubernali\b',
 'child':r'(?<!'+'XX'+r')\bfili(?:o|ae|is|abus)\b','parent':r'\b(?:patri|matri|parentibus)\b(?! patriae)(?! deum)(?! magnae)(?! castrorum)',
 'sibling':r'\b(?:fratri|sorori)\b(?! arvali)','patron':r'\bpatron(?:o|ae|is)\b','freed':r'\blibert(?:o|ae) (?:su[oa]e?|optim|bene|benemerent|carissim|karissim|piissim|fidelissim|dulcissim|merent|idem)',
 'conserv':r'\bconserv(?:o|ae)\b','collib':r'\bco[ln]libert(?:o|ae)\b','alumn':r'\balumn(?:o|ae)\b','amic':r'\bamic(?:o|ae)\b','nepos':r'\b(?:nepoti|nepti|avo|aviae|avunculo|amitae|materterae|patruo|socero|socrui|genero|nurui|vitrico|novercae|privign[oa]e?)\b',
 'nutr':r'\b(?:nutrici|mammae|tatae)\b'}
NOSX=set('merenti fecit annis bene suo sua suae vernae memoriae praetoriae urbanae advenae eius meae filiae nostrae augustae anno vivo viro'.split())
GSX=[('f',re.compile(r'\b(?:filiae|uxori|uxsori|matri|sorori|patronae|alumnae|conservae|collibertae|amicae|nutrici|mammae|aviae|nepti)\b')),('m',re.compile(r'\b(?:filio|marito|patri|fratri|patrono|alumno|conservo|colliberto|amico|avo)\b'))]
RRX={k:re.compile(p.replace("(?<!XX)",'')) for k,p in REL.items()}
FILI=re.compile(PRAE+r' fili(?:o|ae)\b')
SELF=re.compile(r'\b(?:sibi et|et sibi|se viv[oa]|viv[uo]s fecit|viva fecit|vivi fecerunt|sibi posterisque|sibi suisque)\b')
GRP={'fam':['spouse','child','parent','sibling'],'hh':['patron','freed','conserv','collib','contub','alumn','nutr'],'kin':['nepos'],'amic':['amic']}
ages=[];recs=[];mar=[];wed=[]
RC=collections.Counter();nt=0;nself=0
TM={k:[0.0]*len(B) for k in list(GRP)+['self','spouse','child','parent','patron']};TOT=[0.0]*len(B)
ROWS=[]
for r in rome:
    c=clean(T.get(r['id'],''))
    if NMC.tlen(c)<8:continue
    nt+=1
    A=[];M=[]
    for m in AGE.finditer(c):
        a=rom(m.group(1))
        if a>120 or a==0:continue
        pre=c[max(0,m.start()-40):m.start()];post=c[m.end():m.end()+45]
        if post.lstrip().startswith('¤t'):continue  # csonka szám: „XX[- - -]”
        pw=pre.split()
        ismar=bool(MAR.search(' '.join(pw[-5:]))) or bool(re.match(r' (?:cum|mecum|secum|sine|in coniugio)',post[:14]))
        if ismar:
            mq=re.search(r'cum (qua|quo|ea|eo)\b',' '.join(pw[-5:]));M.append((a,{'qua':'f','ea':'f','quo':'m','eo':'m'}[mq.group(1)] if mq else 'u'));continue
        sex='m' if pw and pw[-1]=='qui' else 'f' if pw and pw[-1] in('quae','que','qae') else 'u'
        if sex=='u' and pw and len(pw[-1])>=4 and pw[-1] not in NOSX:
            if pw[-1].endswith('o'):sex='m'      # részes esetű férfinév („Cornelio Bacchico vixit”): a qui/quae-s feliratokon 99%-ban egyezik
            elif pw[-1].endswith('ae') and len(pw)>1 and pw[-2].endswith('ae'):sex='f'   # két -ae végű szó („Ulpiae Felicitati”… „Iuliae Primae vixit”): 98%
        A.append((a,sex,bool(m.group(2)),bool(m.group(3))))
    for m in AGE2.finditer(c):
        a=rom(m.group(1))
        if 0<a<=120 and not c[m.end():].lstrip().startswith('¤t'):A.append((a,'u',False,False))
    for m in INF.finditer(c):
        A.append((0,'u',True,True))
    f={k for k,rx in RRX.items() if rx.search(FILI.sub(' ',c) if k=='child' else c)}
    if len(A)==1 and A[0][1]=='u':
        sx='u'
        if len(M)==1 and M[0][1]!='u':sx=M[0][1]          # „cum qua vixit” = az elhunyt nő
        else:
            cf=FILI.sub(' ',c);g={s for s,rx in GSX if rx.search(cf)}
            if len(g)==1:sx=list(g)[0]                   # egyértelmű nemű megnevezés (filiae, marito…): 96–98%
        if sx!='u':A[0]=(A[0][0],sx,A[0][2],A[0][3])
    slf=bool(SELF.search(c))
    for k in f:RC[k]+=1
    if slf:nself+=1
    for a in A:ages.append(a)
    for a,_ in M:mar.append(a)
    if len(A)==1 and len(M)==1 and M[0][1]!='u' and A[0][1] in ('u',M[0][1]):wed.append((A[0][0]-M[0][0],M[0][1],r['id']))
    g={G for G,ks in GRP.items() if f&set(ks)}
    recs.append((r,A,f,g))
    if len(A)==1 and len(f)==1:ROWS.append((list(f)[0],A[0][0],A[0][1]))
    if r['nb']!='' and r['na']!='':
        a,b=int(r['nb']),int(r['na'])
        if not(b<a or b<B[0] or a>=B[-1]+W):
            w=aw(a,b)
            for i,v in enumerate(w):
                if v:
                    TOT[i]+=v
                    for G in g:TM[G][i]+=v
                    if slf:TM['self'][i]+=v
                    for k in ('spouse','child','parent','patron'):
                        if k in f:TM[k][i]+=v
AG=[a for a,_,_,_ in ages]
hist={s:[0]*17 for s in 'mfu'}
for a,s,_,_ in ages:hist[s][min(a//5,16)]+=1
adult=[a for a in AG if 23<=a<=62];whip=500*sum(1 for a in adult if a%5==0)/len(adult)
def q(L,f):
    L=sorted(L);return L[int(f*(len(L)-1))] if L else None
prec={}
for lo,hi in [(0,5),(5,15),(15,30),(30,50),(50,121)]:
    S=[x for x in ages if lo<=x[0]<hi];prec[f'{lo}-{hi}']=[len(S),sum(1 for x in S if x[2]),sum(1 for x in S if x[3])]
relage={}
for k in RRX:
    L=[a for kk,a,s in ROWS if kk==k]
    if len(L)>=20:relage[k]=[len(L),q(L,.25),q(L,.5),q(L,.75)]
for s,nm in (('f','wife'),('m','husband')):
    L=[a for kk,a,ss in ROWS if kk=='spouse' and ss==s];relage[nm]=[len(L),q(L,.25),q(L,.5),q(L,.75)]
CX=NMC.CX
cx={}
for k,p,e in CX:
    rx=re.compile(p,re.I);S=[x for x in recs if rx.search(x[0]['loc'])]
    L=[a[0] for x in S for a in x[1]];cc=collections.Counter(kk for x in S for kk in x[2])
    cx[k]={'n':len(S),'e':e,'na':len(L),'med':q(L,.5),'u10':sum(1 for a in L if a<10),'rel':cc.most_common(3),'fam':sum(1 for x in S if 'fam' in x[3]),'hh':sum(1 for x in S if 'hh' in x[3])}
D={'bins':B,'w':W,'nt':nt,'nage':len(AG),'ninsc_age':sum(1 for x in recs if x[1]),'hist':hist,'sex':{s:sum(hist[s]) for s in 'mfu'},'med':{s:q([a for a,ss,_,_ in ages if ss==s],.5) for s in 'mf'},'medall':q(AG,.5),
 'u10':sum(1 for a in AG if a<10),'u1':sum(1 for a in AG if a<1),'o60':sum(1 for a in AG if a>=60),'whipple':round(whip),'mult5':round(100*sum(1 for a in adult if a%5==0)/len(adult),1),
 'prec':prec,'mar':{'n':len(mar),'q':[q(mar,.25),q(mar,.5),q(mar,.75)]},'wed':{s:[len([x for x in wed if x[1]==s and x[0]>=10]),q([x[0] for x in wed if x[1]==s and x[0]>=10],.25),q([x[0] for x in wed if x[1]==s and x[0]>=10],.5),q([x[0] for x in wed if x[1]==s and x[0]>=10],.75),len([x for x in wed if x[1]==s and x[0]<10])] for s in 'fm'},
 'rel':dict(RC),'nself':nself,'nrel':sum(1 for x in recs if x[2]),'grp':{G:sum(1 for x in recs if G in x[3]) for G in GRP},'relage':relage,'tot':[round(v,1) for v in TOT],'time':{k:[round(v,1) for v in t] for k,t in TM.items()},'cx':cx}
json.dump(D,open('/home/claude/roma/age/data.json','w'),separators=(',',':'))
json.dump([(x[0]['id'],x[1],sorted(x[2])) for x in recs if x[1] or x[2]],open('/home/claude/roma/age/rows.json','w'))
if __name__=='__main__':
    import collections as _c
    for s in 'fm':print(s,sorted(_c.Counter(x[0] for x in wed if x[1]==s).items()))
    print([x for x in wed if x[0]<10][:12])
    for k in ('nt','nage','ninsc_age','sex','med','medall','u10','u1','o60','whipple','mult5','prec','mar','wed','rel','nself','nrel','grp','relage'):print(k,D[k])
    print([sum(hist[s][i] for s in 'mfu') for i in range(17)])
    for k,v in cx.items():print(k,v)
    for i,x in enumerate(B):
        if TOT[i]>=40:print(x,round(TOT[i]),' '.join(f'{k}:{100*TM[k][i]/TOT[i]:.0f}' for k in TM))
