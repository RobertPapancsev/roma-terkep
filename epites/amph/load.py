import json,collections,re
NS='http://www.semanticweb.org/ontologies/2015/1/EPNet-ONTOP_Ontology#'
def L(n):return json.load(open('/home/claude/dl/ceipac/'+n+'.json'))
def s(u):return u.replace(NS,'') if u else u
PT={s(p):t for p,t,la,lo in L('place')};PLL={s(p):(float(la),float(lo)) for p,t,la,lo in L('place') if la}
PW=collections.defaultdict(set)
for p,w in L('pwithin'):
    if p!=w:PW[s(p)].add(s(w))
PC=collections.defaultdict(set)
for p,c in L('ptype'):
    if not c.endswith('#Place'):PC[s(p)].add(s(c))
AM={}
for a,i,ty,fp,afp,d,b in L('amph'):
    r=AM.setdefault(s(a),{'id':i,'type':set(),'fp':s(fp),'afp':s(afp),'desc':d,'bib':s(b),'dates':[],'prod':set(),'insc':[]})
    if ty:r['type'].add(ty.split('/')[-1].replace(NS,''))
for a,d,b,e,t in L('adate'):
    if s(a) in AM:AM[s(a)]['dates'].append((s(d),b,e,t))
for a,p in L('aprod'):
    if s(a) in AM:AM[s(a)]['prod'].add(s(p))
for a,st,e,g in L('alayer'):
    if s(a) in AM:AM[s(a)]['layer']=(st,e,g)
IC=collections.defaultdict(set)
for i,c,k in L('icls'):IC[s(i)].add(s(c))
IN={}
for i,idn,a,k,f,sm,d in L('insc'):
    if not i.startswith(NS):continue
    r=IN.setdefault(s(i),{'id':idn,'a':s(a),'kind':k,'full':f,'simp':sm,'desc':d,'cls':IC.get(s(i),set())})
    if a and s(a) in AM and s(i) not in AM[s(a)]['insc']:AM[s(a)]['insc'].append(s(i))
def chain(p,depth=4):
    out=set();st=[p]
    for _ in range(depth):
        st=[w for x in st for w in PW.get(x,())]
        out|=set(st)
    return out
