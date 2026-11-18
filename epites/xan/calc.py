# v97: kereszt-összefüggések a meglévő adatokból -> xan/data.json
import sys,re,json,math,collections,importlib.util,itertools
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
OUT={}
def q(L,f):L=sorted(L);return L[int(f*(len(L)-1))]
# ---- 2. életkor és kerekítés csoportonként (EDR)
A=load('agecalc','/home/claude/roma/age/calc.py');N=A.NMC;OL=load('occlex','/home/claude/roma/occ/lex.py')
G=collections.defaultdict(list)
for r,Ag,f,g in A.recs:
    if not Ag:continue
    for a in Ag:
        if a[1] in 'mf':G['sex_'+a[1]].append(a[0])
    if len(Ag)!=1:continue
    c=A.clean(A.T.get(r['id'],''));a=Ag[0][0]
    mil=bool(OL.MIL.search(c));lib=bool(N.RX['lib'].search(c));ser=bool(re.search(r'\bserv(?:us|a|o|ae)\b|\bvern(?:a|ae)\b',c));fil=bool(re.search(N.PRAE+r' fili(?:us|a|o|ae)\b',c))
    if mil:G['mil'].append(a)
    if lib:G['lib'].append(a)
    if ser:G['ser'].append(a)
    if fil:G['fil'].append(a)
    if 'patron' in f:G['patron'].append(a)
    if r['nb']!='' and r['na']!='':
        m=(int(r['nb'])+int(r['na']))/2;G['t0' if m<50 else 't1' if m<150 else 't2'].append(a)
def st(L):
    ad=[a for a in L if 23<=a<=62];return {'n':len(L),'med':q(L,.5),'nad':len(ad),'w':round(500*sum(1 for a in ad if a%5==0)/len(ad))}
OUT['age']={k:st(v) for k,v in G.items()}
# ---- 3. életkor és temetési hónap (EDB)
sys.path.insert(0,'/home/claude/roma/edb');E=load('edbcalc','/home/claude/roma/edb/calc.py')
grp={'a':[0]*12,'b':[0]*12,'c':[0]*12}
for r in E.LAT:
    c=r['c'];m=E.DEP.search(c)
    if not m:continue
    mi=[i for i,x in enumerate(E.MON) if m.group(4).startswith(x)][0]
    if m.group(3).startswith('kalend') and (m.group(1) or m.group(2)):mi=(mi-1)%12
    ag=[E.rom(x.group(1)) for x in A.AGE.finditer(c) if 0<E.rom(x.group(1))<=120 and not c[x.end():].lstrip().startswith('¤t')]
    if len(ag)==1:grp['a' if ag[0]<10 else 'b' if ag[0]<30 else 'c'][mi]+=1
def sh(v):return sum(v[7:10]),sum(v)
(kb,nb),(kc,nc)=sh(grp['b']),sh(grp['c']);p1,p2=kb/nb,kc/nc;pp=(kb+kc)/(nb+nc);z=(p1-p2)/math.sqrt(pp*(1-pp)*(1/nb+1/nc))
OUT['season']={k:{'n':sum(v),'k':sum(v[7:10]),'m':v} for k,v in grp.items()};OUT['season']['z']=round(z,2);OUT['season']['p']=round(math.erfc(abs(z)/math.sqrt(2)),3)
# ---- 4. a 14 kerület
b=open('/home/claude/roma/body_v60pre.html',encoding='utf8').read()
R=json.loads(re.search(r'const REGSTAT=(\[.*?\]);',b).group(1));v=lambda x:(x[1] if isinstance(x,list) else x)
AQ=['II, VIII, IX, XI, XII, XIII, XIV','I, III, IV, V, VI, VII, VIII, IX, XII, XIV','I, III, IV, V, VI, VII, VIII, IX, X, XIV','IV, V, VI, VII','II, III, V, VI, VIII, X, XII','VII, IX, XIV','I, II, III, IV, V, VI, VII, VIII, IX, X, XI, XII, XIII, XIV']
for s in AQ[:6]:assert 'r:"'+s+'"' in b,s      # a kártya Frontinus-adataival (AQF) egyezik; a hetedik a Claudia + Anio Novus (mind a 14 kerület)
naq=[sum(1 for s in AQ if r['r'] in [x.strip() for x in s.split(',')]) for r in R]
def rank(L):
    s=sorted(range(len(L)),key=lambda i:L[i]);r=[0]*len(L);i=0
    while i<len(s):
        j=i
        while j+1<len(s) and L[s[j+1]]==L[s[i]]:j+=1
        for t in range(i,j+1):r[s[t]]=(i+j)/2+1
        i=j+1
    return r
def pear(a,c):
    n=len(a);ma=sum(a)/n;mb=sum(c)/n;return sum((x-ma)*(y-mb) for x,y in zip(a,c))/math.sqrt(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in c))
sp=lambda a,c:round(pear(rank(a),rank(c)),2)
col=lambda k:[v(r[k]) for r in R]
OUT['reg']={'ins_bal':sp(col('insulae'),col('balnea')),'lac_pis':sp(col('lacus'),col('pistrina')),'aq_ins':sp(naq,col('insulae')),'naq':naq}
# ---- 5. 250–275
I=json.load(open('/home/claude/roma/insc/data.json'));Bd=json.load(open('/home/claude/roma/bld/data.json'));C=json.load(open('/home/claude/roma/chre/data.json'))
tot=lambda d:[sum(c) for c in zip(*d.values())]
it=I['time']['all'];it=tot(it) if isinstance(it,dict) else it;si=dict(zip(I['bins'],it));ss=dict(zip(Bd['bins'],tot(Bd['sitar']['all'])));hc=dict(zip(C['bins'],C['he']))
OUT['crisis']={'hoard_pc':round(100*hc[250]/C['ne'],1),'sitar':round(ss[250]),'sitar_max':round(max(ss[x] for x in range(-100,400,25))),'sitar_min':round(min(ss[x] for x in range(0,300,25))),'insc':round(si[250]),'insc_2c':round(sum(si[x] for x in (100,125,150,175))/4)}
# ---- 1. kereskedők: amfora (β sor) és kőfelirat
sys.path.insert(0,'/home/claude/roma/amph');import beta as BT
import pickle,pandas as pd
rows=pickle.load(open('/home/claude/dl/list/rows.pkl','rb'));T=pd.read_pickle('/home/claude/dl/list/all_text.pkl')
M=[('phoebus',r'mari\w* phoeb',[r'mario phoebo viatori']),('onesimus',r'caecili\w* onesim',[r'caecilio onesimo viatori']),('hospitalis',r'caecili\w* (?:hospital|matern)',[r'caecilius hospitalis et caecilia']),
 ('hermes',r'iuli hermetis',[r'iulio hermesiano diffusori']),('fadius',r'fadi\w* secund',[r'fadio papiria secundo musae']),('olitius',r'oliti apolloni',[r'olitio apollonio'])]
mer={}
for k,pa,ps in M:
    ys=[];n=0
    for a,i,kd,y in BT.ROWS:
        if re.search(pa,BT.clean(i['full']).replace('v','u')):
            n+=1
            if y:ys.append(y)
    st_=[]
    for ix,(reg,p,stt,c,nb_,na_,city) in enumerate(rows):
        if 'fabricationis' in stt:continue
        if any(re.search(x,c) for x in ps):st_.append({'id':T['EDCS-ID'].iloc[ix],'place':T['place'].iloc[ix],'nb':None if nb_!=nb_ else int(nb_),'na':None if na_!=na_ else int(na_)})
    assert st_,k
    mer[k]={'n':n,'y':[min(ys),max(ys)] if ys else None,'ny':len(ys),'stone':st_}
OUT['mer']=mer
json.dump(OUT,open('/home/claude/roma/xan/data.json','w'),ensure_ascii=False)
if __name__=='__main__':
    for k,v in OUT.items():print(k,json.dumps(v,ensure_ascii=False)[:1500])
