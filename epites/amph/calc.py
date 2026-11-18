# v92: a Rómában talált amforák feliratai (CEIPAC / Roman Open Data) -> amph/data.json
import sys,re,json,collections
sys.path.insert(0,'/home/claude/roma/amph');import base as B,delta as DL
D=B.D;R=B.ROME
def spots(a):return {D.PT.get(w,'') for w in D.chain(a['fp'])}|{D.PT.get(a['fp'],'')}
TEST=[a for a in R if any('Testaccio' in s for s in spots(a))]
d20=[a for a in R if 'dressel_20' in a['type']]
kinds=collections.Counter();cls=collections.Counter()
for a in R:
    for i in a['insc']:
        x=D.IN[i]
        if x['kind']=='Stamp':kinds['stamp']+=1
        elif x['kind']=='Sketch':kinds['graf']+=1
        else:
            kinds['tit']+=1
            for c in x['cls']:cls[c.replace('TitulusCode-','')]+=1
# --- év: az adatbázis keltezése; ha nincs, a δ-felirat konzulpárja (csak az adatbázisban egyértelműen egy évhez kötött párok)
def cons(t):
    t=B.norm(t);t=re.sub(r'[?+<>{}.…]','',t);out=[]
    for seg in re.split(r'\s*/\s*',t):
        m=re.search(r'([a-z ]*?\b[a-z]{3,}(?: aug\w*| caesare?| ii+| iv| v)*(?: et | )[a-z ]*?[a-z]{3,}(?: ii+| iv)?) co?s\b',seg)
        if m:out.append(' '.join(re.sub(r'\b(imp|imperatore|imperator|domino nostro|ddominis nnostris|dd nn|d n|aug|augusto|augg|caesare|filio|augusti|publio|martio|severo|aurelio|r|scil)\b','',m.group(1)).split()))
    return out
CM=collections.defaultdict(collections.Counter)
for a,i,d in DL.ROWS:
    y,s=B.year(a)
    if y and s=='t':
        for c in cons(i['full']):CM[c][y]+=1
CY={c:max(v,key=v.get) for c,v in CM.items() if sum(v.values())>=2 and max(v.values())==sum(v.values())}
CY.update({'valeriano ii et lucillo':265,'alexandro iii et dione':229,'alexandro iii et cassio dione':229,'iii et cassio dione':229})
def yr(a,i=None):
    y,s=B.year(a)
    if i is not None:
        for c in cons(i['full']):
            if c in CY:return CY[c],'x'
    return y,s
PER=[(138,161),(174,191),(207,230),(246,267)]
def per(y):
    for k,(a,b) in enumerate(PER):
        if a<=y<=b:return k
    return None
DK=['astigi','corduba','hispalis','lacca','malaca','portus']
dis=collections.Counter(d for a,i,d in DL.ROWS if d);dp=[collections.Counter() for _ in PER];nodate=collections.Counter();outside=0
for a,i,d in DL.ROWS:
    if not d:continue
    y,s=yr(a,i)
    if y is None:nodate[d]+=1;continue
    k=per(y)
    if k is None:outside+=1;continue
    dp[k][d]+=1
# --- évek: egyetlen évre keltezett amforák
ys=collections.Counter();ysrc=collections.Counter()
for a in R:
    y,s=B.year(a)
    if y is not None and y>0:ys[y]+=1;ysrc[s]+=1
# --- bélyegek és műhelyek
PP=json.load(open('/home/claude/dl/ceipac/prodplace.json'));NS=D.NS
PN={p.replace(NS,''):(t,la,lo) for p,t,la,lo in PP['p']}
CONV={}
for p,w,t,la,lo in PP['w']:
    if t in('Corduba','Astigi','Hispalis'):CONV[p.replace(NS,'')]=t
st=[(a,D.IN[i]) for a in d20 for i in a['insc'] if D.IN[i]['kind']=='Stamp']
wk=collections.Counter();cv=collections.Counter();nw=0
for a,i in st:
    ps=a['prod']
    if len(ps)==1:
        p=next(iter(ps));wk[p]+=1;cv[CONV.get(p,'?')]+=1
    elif len(ps)>1:nw+=1
# --- γ: a tiszta olaj súlya római fontban
V={'i':1,'v':5,'x':10,'l':50,'c':100}
def rom(s):
    t=0;mx=0
    for ch in reversed(s):
        v=V[ch]
        if v<mx:t-=v
        else:t+=v;mx=v
    return t
gam=[]
for a in d20:
    for i in a['insc']:
        x=D.IN[i]
        if 'TitulusCode-GAM' in x['cls'] and x['full']:
            t=B.norm(x['full'])
            if re.fullmatch(r'c{1,3}[lxvi]*',t):gam.append(rom(t))
gam=[g for g in gam if 150<=g<=300];gs=sorted(gam)
OUT={'nall':len(D.AM),'nrome':len(R),'ntest':len(TEST),'nd20':len(d20),'kinds':dict(kinds),'cls':dict(cls),
 'years':sorted(ys.items()),'ysrc':dict(ysrc),'nyear':sum(ys.values()),
 'dis':{k:dis[k] for k in DK},'ndis':sum(dis.values()),'ndel':len(DL.ROWS),'per':PER,'dp':[{k:c[k] for k in DK} for c in dp],'dnodate':sum(nodate.values()),'doutside':outside,
 'nst':len(st),'nstw':sum(wk.values()),'nstmulti':nw,'conv':dict(cv),'work':[{'n':PN[p][0],'c':CONV.get(p,'?'),'k':n,'lat':PN[p][1],'lon':PN[p][2]} for p,n in wk.most_common(12)],'nwork':len(wk),
 'gam':{'n':len(gam),'med':gs[len(gs)//2],'q1':gs[len(gs)//4],'q3':gs[3*len(gs)//4],'mode':collections.Counter(gam).most_common(3)}}
json.dump(OUT,open('/home/claude/roma/amph/data.json','w'),ensure_ascii=False)
if __name__=='__main__':
    for k,v in OUT.items():print(k,v)
    print(sorted(CY.items(),key=lambda x:x[1]))
