# Helyadatlap-kiegészítések összeállítása (DARE, Pleiades, Wikidata, LIST, CHRE) → imp_info/ii_NN.json (id%64 szerint)
import json,glob,re,collections,numpy as np,pandas as pd
from scipy.spatial import cKDTree
R='/home/claude/imperium/';A=R+'data/agg/'
# --- térképi helyek (alap + csempék) ---
P={}
for p in json.load(open(R+'imp_base.json'))['pts']: P[p[7]]=p
for f in glob.glob(R+'tiles/*.json'):
    for p in json.load(open(f)).get('s',[]): P[p[7]]=p
D=json.load(open(A+'dare_parsed.json'));WQ=json.load(open(A+'wikidata_by_q.json'));WP=json.load(open(A+'wikidata_by_pleiades.json'))
# --- Pleiades ---
pl=pd.read_csv('/home/claude/dl/pleiades/places.csv.gz',usecols=['id','title','description','featureTypes','timePeriodsKeys'])
PL={int(r.id):r for r in pl.itertuples()}
nm=pd.read_csv('/home/claude/dl/pleiades/names.csv.gz',usecols=['pid','title','nameAttested','nameLanguage','timePeriodsKeys'])
NM=collections.defaultdict(list)
for r in nm.itertuples():
    try: pid=int(str(r.pid).rsplit('/',1)[1])
    except: continue
    NM[pid].append(r)
def cl(s): return [x.strip() for x in str(s).split(',') if x.strip() and x.strip()!='nan']
# --- LIST (2 km) és CHRE (10 km) ---
LM=json.load(open(A+'list_match.json'));LS=json.load(open(A+'list_social.json'));OR=json.load(open(A+'orbis_match.json'))
MI=json.load(open(A+'mints.json'));PO=json.load(open(A+'ports.json'))
PHU=json.load(open(A+'pleiades_hu.json'))  # a Pleiades-leírások saját magyar fordítása
# v126: Itália – EDR (saját összesítés a szövegekből), GNA (római kori MOSI-rekordok), MiC Luoghi della cultura
ED=json.load(open(A+'edr_social.json'));GN=json.load(open(A+'gna_match.json'));LC=json.load(open(A+'luoghi_match.json'))
# v130: Hispania – Kasztília és León lelőhelykatalógusa, CEIPAC-amforák (saját összesítés)
CY=json.load(open(A+'cyl_match.json'));CE=json.load(open(A+'ceipac_match.json'));IC=json.load(open(A+'icac_match.json'))  # IC: v131
SL=json.load(open(A+'rnpd_match.json'))  # SL: v132 Szlovénia (RNPD)
MC=json.load(open(A+'nmk_match.json'))  # MC: v133 Észak-Macedónia (Wikidata)
RL=json.load(open(A+'lmi_match.json'))  # RL: v134 Románia (LMI 2015)
FR=json.load(open(A+'fr_match.json'))  # FR: v135 Franciaország (Mérimée, Inrap, Párizs)
AO=json.load(open(A+'arkeopen_match.json'))  # AO: v136 ArkeOpen
UK=json.load(open(A+'uk_match.json'))  # UK: v137 Brit védett emlékek
import glob as _g
NH=[(f.split('nh_')[1][:-5],json.load(open(f))) for f in sorted(_g.glob(A+'nh_*.json'))]  # NH: v143-tól országos műemléklisták (közös formátum)
NL=json.load(open(A+'nl_match.json'))  # NL: v142 Hollandia, RCE régészeti rijksmonumentek
CH=json.load(open(A+'ch_match.json'))  # CH: v141 Svájc, KGS-Inventar
AT=json.load(open(A+'at_match.json'))  # AT: v140 Ausztria, BDA-műemléklista (Wikidata)
BY=json.load(open(A+'by_match.json'))  # BY: v139 Bajorország, BLfD Bodendenkmäler (Wikidata)
RR=json.load(open(A+'rrsp_match.json'))  # RR: v138 Roman Rural Settlement Project (csak összesítés)
def port_merge(L):
    aa=[];seen=set()
    for r in L:
        for a in r.get('aa',[]):
            k=a.split(',')[0].strip()
            if a not in seen:seen.add(a);aa.append(a)
    ST=['BW','QU','PL','MO','CN','SL','SH','SY','EX','LK','PH','HO','VM','FT','FP','QR','FO','SW'];PER=['Li','Mi','My','Pn','Eg','Gr','He','Ro','By']
    s={x for r in L for x in r.get('s',[])};pe={x for r in L for x in r.get('per',[])}
    o={'n':len(L),'s':[x for x in ST if x in s],'per':[x for x in PER if x in pe]}
    if aa:o['aa']=aa[:12];o['naa']=len(aa)
    re_=[r.get('re') for r in L if r.get('re')]
    if re_:o['re']='rs' if all(x=='rs' for x in re_) else 'r'
    if any(r.get('si') for r in L):o['si']=1
    if any(r.get('ps') for r in L):o['ps']=1
    o['nb']=[r['nb'] for r in L]
    return o
C=np.load(A+'chre_xy.npz',allow_pickle=True);CT=cKDTree(np.c_[C['x'],C['y']]);CTY=C['ty'];CCC=C['cc']
KEEP=['wikipedia:en','trismegistos.org','PECS','livius:place','vici.org','theatrum.de','amphi-theatrum','romaq.org','whc','roman-britain.org','brill-s-new-pauly','arachne:topographie']
out=collections.defaultdict(dict);st=collections.Counter()
for i,p in P.items():
    o={};d=D.get(i,{});lk=d.get('links',{})
    dd={}
    for k in ('lrp','area'):
        if d.get(k):dd[k]=d[k]
    if d.get('prec'):dd['prec']=d['prec']
    if d.get('sub'):dd['sub']=[[a,b] for a,b,_ in d['sub']][:40];dd['nsub']=len(d['sub'])
    if d.get('parent'):dd['par']=d['parent']
    ll=[]
    for k in KEEP:
        for u,t in lk.get(k,[])[:2]:
            if not u.startswith('http'):u='https://'+u
            ll.append([k,u])
    if ll:dd['L']=ll
    if dd:o['d']=dd;st['d']+=1
    # Pleiades
    pid=None
    for u,_ in lk.get('Pleiades',[]):
        m=re.search(r'places/(\d+)',u)
        if m:pid=int(m.group(1));break
    if pid and pid in PL:
        r=PL[pid];pp={'id':pid}
        if isinstance(r.description,str) and r.description.strip():pp['ds']=r.description.strip()
        if pp.get('ds') in PHU:pp['dh']=PHU[pp['ds']]
        ft=sorted({x for x in cl(r.featureTypes) if x not in('unknown','unlabeled','label','numbered feature')})
        if ft:pp['ft']=ft
        tp=cl(r.timePeriodsKeys)
        if tp:pp['tp']=tp
        ns=[];seen=set()
        for n in NM.get(pid,[]):
            nt=n.nameAttested if isinstance(n.nameAttested,str) and n.nameAttested.strip() else n.title
            if not isinstance(nt,str):continue
            key=(nt,n.nameLanguage)
            if key in seen:continue
            seen.add(key);ns.append([nt,n.nameLanguage if isinstance(n.nameLanguage,str) else '',cl(n.timePeriodsKeys)])
        if ns:pp['n']=ns[:14]
        o['p']=pp;st['p']+=1
    elif pid:o['p']={'id':pid}
    # Wikidata: DARE QID elsőbbséggel, különben Pleiades-azonosító alapján
    q=None
    for u,t in lk.get('wikidata',[]):
        t=t.strip()
        if t.startswith('Q'):q=t;break
    w=None
    if q and q in WQ and WQ[q]:w=dict(WQ[q]);w['q']=q
    elif pid and str(pid) in WP:w=dict(WP[str(pid)])
    if w:
        o['w']={k:w[k] for k in ('q','hu','en','img') if k in w};st['w']+=1
        if 'hu' in w:st['hu']+=1
        if 'img' in w:st['img']+=1
    x,y=p[1],p[2]
    if i in LM:o['i']=LM[i];st['i']+=1
    if i in LS:
        o['so']=LS[i];st['so']+=1
    if i in OR:o['or']=OR[i];st['or']+=1
    if i in MI:o['mi']=MI[i];st['mi']+=1
    if i in PO:o['po']=port_merge(PO[i]);st['po']+=1
    if i in ED:o['ed']=ED[i];st['ed']+=1
    if i in GN:o['gn']={k:GN[i][k] for k in ('n','c','r')};st['gn']+=1
    if i in LC:o['lc']=LC[i];st['lc']+=1
    if i in CY:o['cy']=CY[i];st['cy']+=1
    if i in CE:o['am']=CE[i];st['am']+=1
    if i in IC:o['wo']=IC[i];st['wo']+=1
    if i in SL:o['sl']=SL[i];st['sl']+=1
    if i in MC:o['mc']=MC[i];st['mc']+=1
    if i in RL:o['rl']=RL[i];st['rl']+=1
    if i in AO:o['ao']=AO[i];st['ao']+=1
    if i in UK:o['uk']=UK[i];st['uk']+=1
    if i in RR:o['rr']=RR[i];st['rr']+=1
    if i in BY:o['by']=BY[i];st['by']+=1
    if i in AT:o['at']=AT[i];st['at']+=1
    if i in CH:o['ch']=CH[i];st['ch']+=1
    if i in NL:o['nl']=NL[i];st['nl']+=1
    nh=[[c,X[i]] for c,X in NH if i in X]
    if nh:o['nh']=nh;st['nh']+=1
    if i in FR:
        for k,v in FR[i].items():o[k]=v;st[k]+=1
    ix=CT.query_ball_point([x,y],10.0)
    if ix:
        yy=[CTY[j] for j in ix if CTY[j]>-9e4];o['h']=[len(ix),int(min(yy)) if yy else None,int(max(yy)) if yy else None,int(sum(CCC[j] for j in ix))];st['h']+=1
    if o: out[int(i)%64][i]=o
for k,v in out.items(): json.dump(v,open(R+f'imp_info/ii_{k}.json','w'),ensure_ascii=False,separators=(',',':'))
print(len(P),st)
a=out[10898%64]['10898'];print(json.dumps(a,ensure_ascii=False)[:2500])
