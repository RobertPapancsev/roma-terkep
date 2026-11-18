# v84: Foglalkozások az EDR római felirataiban. Bemenet: recs.json (insc/parse.py), text.json (occ/text.py). Kimenet: occ/data.json
import json,re,collections,sys,random,unicodedata
sys.path.insert(0,'/home/claude/roma/occ');import lex,excl
EXS=set(map(tuple,excl.EX));EXIDS=set(excl.EXID)
_D=json.load(open('/home/claude/roma/nm/dup.json'));SKIP=set(_D['skip']);GROUP=_D['group']  # ismétlődő rekordok (nm/calc.py)
R=json.load(open('/home/claude/dl/edr/recs.json'));T=json.load(open('/home/claude/dl/edr/text.json'))
rome=[r for r in R if 'Roma' in r['pf']]
def clean(t):
    t=re.sub(r'=\s*/\s*','',t);t=re.sub(r'(?<=[^\s\-])-\s*/\s*(\[?)',r'\1',t)
    t=unicodedata.normalize('NFD',t.lower())
    t=''.join(ch for ch in t if unicodedata.category(ch)!='Mn')
    t=re.sub(r'\(:[^)]*\)','',t)
    t=re.sub(r'\(\((?:mulieris|gaiae)\)\)','mulieris',t)
    t=re.sub(r'\(\([^)]*\)\)',' ',t)
    t=re.sub(r'[\[\]\(\)<>{}`´?!+〚〛《》⌜⌝"]','',t)
    t=re.sub(r'〈:?\s*(vacat|verso|recto)\s*〉',' § ',t)
    t=re.sub(r'〈:\s*([a-z]{3,}(?: diem)?)\s*〉',r' \1 ',t)
    t=re.sub(r'〈([a-z])〉',r'\1',t)
    t=re.sub(r'〈[^〉]*〉',' § ',t)
    t=re.sub(r'[/,.;:·\-=]+',' ',t)
    t=re.sub(r'\s+',' ',t).strip()
    t=re.sub(r'libertis libertabus(?:que)?','LLF',t)
    return t
PRAE=r'(?:marci|luci|gai|quinti|publi|titi|gnaei|auli|sexti|decimi|tiberi|mani|numeri|spuri|servi|appi|kaesonis|vibi)'
LIB=re.compile(r'\blibert(?:us|a|i|o|ae|um|am)\b')
SER=re.compile(r'\bserv(?:us|a|i|o|ae|um|am)\b|\bvern(?:a|ae|am)\b|\bvicari(?:us|a|o|ae)\b')
ING=re.compile(PRAE+r' (?:filius|filia|filio|filiae)\b')
IW=r'(?:august[io]|augustae|augustorum|augg?|caesaris|caesarum|imperatoris|divi [a-z]+)(?: nostri| nostrorum| n)?'
IL=re.compile(IW+r' libert')
ISV=re.compile(IW+r' (?:serv|vern)|'+IW+r'$')
STOPW=set('et dis diis manibus sacrum fecit fecerunt vixit vixsit annis annos annorum mensibus diebus coniugi coiugi sibi suis posterisque dat dedit ollam ossa hic sita situs bene merenti benemerenti in fronte agro pedes'.split())
def seg_before(c,m,n=9):
    out=[]
    for w in reversed(c[:m.start()].split('§')[-1].split()):
        if w in STOPW or len(out)>=n:break
        out.append(w)
    return ' '.join(reversed(out))
def seg_after(c,m,n=4):
    out=[]
    for w in c[m.end():].split('§')[0].split():
        if w in STOPW or len(out)>=n:break
        out.append(w)
    return ' '.join(out)
def tcase(t):
    w=t.split()[-1]
    if t.startswith(('a ','ab ','ad ')):return set('ndgaP')
    s=set()
    if re.search(r'(?:us|or|ex|ix|er|en|es|a|ensis)$',w):s.add('n')
    if re.search(r'(?:llo|lio|eco|upo|opo|nteo)$',w):s.add('n')
    if re.search(r'(?:o|i|ae)$',w):s.add('d')
    if re.search(r'(?:i|is|ae|orum|arum|um)$',w):s.add('g')
    if re.search(r'(?:um|am|em|os|as|es)$',w):s.add('a')
    return s or set('ndga')
def mcase(w):
    if w.endswith(('us','a')) and not w.endswith('verna'):return set('n')
    if w=='verna':return set('n')
    if w.endswith('o'):return set('d')
    if w.endswith('ae'):return set('dg')
    if w.endswith('i'):return set('g')
    if w.endswith(('um','am')):return set('a')
    return set('ndga')
MK=re.compile(r'\b(libert(?:us|a|i|o|ae|um|am)|serv(?:us|a|i|o|ae|um|am)|vern(?:a|ae|am)|vicari(?:us|a|o|ae|i)|filius|filia|filio|filiae)\b')
IWR=re.compile(IW+r'$')
IMPW=re.compile(r'\b(?:caesaris|augusti|augustae|augustorum|augg|imperatoris)\b')
IMPN=re.compile(r'^(?:tiberi|claudi|neronis|caesaris|augusti|germanici|domitiani|imperatoris|traiani|hadriani|nervae|vespasiani|titi|divi|nostri|n|antonini|pii|felicis|aureli|marci|commodi|severi)$')
def status(c,m):
    # A foglalkozásnévhez tartozó névben keresünk: visszafelé a tétel- vagy mondathatárig (legfeljebb 9 szó), előre legfeljebb 4 szó.
    # A névhez legközelebbi, a foglalkozásnévvel esetben egyező jelölés számít (libertus, servus, verna, vicarius, filius).
    pre=seg_before(c,m);post=seg_after(c,m);tc=tcase(m.group(0))
    if re.search(r'pontific\w+ maxim|tribunicia',pre):return 'u'
    best=None
    for mm in MK.finditer(pre):
        if mcase(mm.group(1))&tc and not (best and best.group(1).startswith('libert') and mm.group(1).startswith('vern')):best=mm
    def cls(mm,txt):
        w=mm.group(1);before=txt[:mm.start()].rstrip()
        if w.startswith('fili'):
            if 'P' in tc and w=='filiae':return None
            return 'f' if re.search(PRAE+r'$',before) else None
        imp=bool(IWR.search(before)) or bool(IMPW.search(' '.join(before.split()[-6:])))
        if w.startswith('libert'):return 'il' if imp else 'l'
        return 'is' if imp else 's'
    if best:
        r=cls(best,pre)
        if r:return r
    # cím után álló jelölés: „pistor Tiberi Germanici servus", „medicus Augusti libertus"
    for mm in MK.finditer(post):
        if mm.group(1).startswith('fili'):continue
        if mcase(mm.group(1))&tc:return cls(mm,post)
        break
    # „Felix Caesaris dispensator" / „dispensator Augusti": egynevű személy, császári birtokos
    pw=pre.split()
    mi=IWR.search(pre)
    if mi and len([w for w in pre[:mi.start()].split() if not IMPN.match(w)])<=2:return 'is'
    if len(pw)<=2 and re.match(IW+r'(?:$| )',post+' '):return 'is'
    return 'u'
PN=re.compile(r'^(?:marc(?:us|i|o|um)|luci(?:us|o|um)?|gai(?:us|o|um)?|cai(?:us|o|um)?|quint(?:us|i|o|um)|publi(?:us|o|um)?|tit(?:us|i|o|um)|gnae(?:us|i|o|um)|cnae(?:us|i|o|um)|aul(?:us|i|o|um)|sext(?:us|i|o|um)|decim(?:us|i|o|um)|tiberi(?:us|o|um)?|mani(?:us|o|um)?|numeri(?:us|o|um)?|spuri(?:us|o|um)?|servi(?:us|o|um)?|appi(?:us|o|um)?|sex|l|c|m|q|p|t|a|d|cn|ti)$')
def unk(l):return (not l.strip()) or 'ignoratur' in l.lower() or l.strip() in('Roma','Roma?')
H=[]  # találatok: (rec, kulcs, státusz, részlet)
nmil=0;ntext=0
for r in rome:
    if r['id'] in SKIP:continue
    c=clean(T.get(r['id'],''))
    if len(c)<8:continue
    ntext+=1
    if lex.MIL.search(c):nmil+=1;continue
    gid=[r['id']]+GROUP.get(r['id'],[])
    if EXIDS&set(gid):continue
    for k,rx in lex.CL:
        for m in rx.finditer(c):
            pt=c[:m.start()].split()
            if pt and PN.match(pt[-1]) and not m.group(0).startswith(('a ','ab ','ad ')):continue  # praenomen után: családnév (pl. Sextus Aerarius, Aulus Argentarius)
            if any((g,k) in EXS for g in gid):break
            H.append((r,k,status(c,m),c[max(0,m.start()-70):m.end()+60],c[m.end():m.end()+70].split('§')[0],c));break

# ---- összesítés
import math
ST=['il','is','l','s','f','u']
sect_of={k:s for k,_,_,_,_,s in lex.L}
ids=set(h[0]['id'] for h in H)
occ=collections.defaultdict(lambda:{'n':0,'st':collections.Counter()})
sec={k:{'ids':set(),'st':collections.Counter(),'mid':[]} for k,_,_ in lex.SECT}
for r,k,st,sn,post,c in H:
    occ[k]['n']+=1;occ[k]['st'][st]+=1
    S=sec[sect_of[k]];S['st'][st]+=1
    if r['id'] not in S['ids']:
        S['ids'].add(r['id'])
        if r['nb']!='' and r['na']!='':S['mid'].append((int(r['nb'])+int(r['na']))/2)
def per(m):
    m=sorted(m)
    if not m:return None
    q=lambda f:m[int(f*(len(m)-1))]
    lo=math.floor(q(.25)/25)*25;hi=math.ceil(q(.75)/25)*25
    if hi==lo:hi+=25
    return [lo,hi]
SECT={k:{'n':len(v['ids']),'t':sum(v['st'].values()),'st':[v['st'][s] for s in ST],'per':per(v['mid'])} for k,v in sec.items()}
OCC=[{'k':k,'la':la,'hu':hu,'en':en,'s':s,'n':occ[k]['n'],'st':[occ[k]['st'][x] for x in ST]} for k,la,_,hu,en,s in lex.L if occ[k]['n']>0]
OCC.sort(key=lambda o:-o['n'])
# idő: aoristikus, 25 éves sávok, ágazatonként (feliratonként egyszer ágazatonként)
X0,X1,W=-200,700,25;B=list(range(X0,X1,W))
TM={k:[0.0]*len(B) for k,_,_ in lex.SECT};nd=set()
seen=set()
for r,k,st,sn,post,c in H:
    s=sect_of[k]
    if (r['id'],s) in seen or r['nb']=='' or r['na']=='':continue
    seen.add((r['id'],s));a,b=int(r['nb']),int(r['na'])
    if b<a or b<X0 or a>=X1:continue
    nd.add(r['id']);L=b-a
    for i,x in enumerate(B):
        TM[s][i]+=(1.0 if x<=a<x+W else 0.0) if L==0 else max(0,min(b,x+W)-max(a,x))/L
TM={k:[round(v,1) for v in t] for k,t in TM.items()}
# leletegyüttesek (az insc/calc.py lelőhely-kulcsszavai)
CX=[('statili',r'colombario degli statili','portamaior'),('liviae',r'monumentum liviae',None),('codini',r'vigna codini','columbariacodini'),('volusii',r'monumentum volusiorum',None),
 ('salario',r'sepolcreto salario|tra via salaria e via pinciana|via po\b|via livenza','csalario'),('carmel',r"corso d'italia, chiesa dei carmelitani",None),
 ('spaolo',r's\. paolo fuori',None),('vatican',r'necropoli vaticana|necropoli della via triumphalis',None),('pamphilj',r'villa pamphilj',None),('forum',r'foro romano',None),
 ('marcella',r'monumentum marcellae|vigna codini.*marcell',None),('arrunti',r'arrunti',None)]
by=collections.defaultdict(set)
for r,k,st,sn,post,c in H:by[r['id']].add(k)
CXD={}
for k,p,e in CX:
    rx=re.compile(p,re.I);rows=[r for r in rome if not unk(r['loc']) and rx.search(r['loc'])]
    oc=[r for r in rows if r['id'] in ids];cc=collections.Counter(x for r in oc for x in by[r['id']])
    CXD[k]={'n':len(rows),'o':len(oc),'e':e,'top':cc.most_common(4)}
# címek a szövegben
AD=[('sacravia',r'\bde (?:sacra via|via sacra)\b'),('subura',r'\bde subura\b'),('velabrum',r'\bde velabro\b'),('vicustuscus',r'\bde vico tusco\b|\bad vortumnum\b'),
 ('compitum',r'\bcompito aliario\b'),('castor',r'\bpost aedem castoris\b'),('sexareae',r'\bab sex ar[e]?is\b'),('portusvin',r'\bport[uo] vinario\b'),('forumvin',r'\bde foro vinario\b'),
 ('caputafr',r'\ba caput afric'),('galbae',r'\bhorreis galb'),('lolliana',r'\bhorreis lollianis\b|\bex lollianis\b'),('agrippiana',r'\bhorreis agrippianis\b'),
 ('foresq',r'\bforo esquilino\b'),('fontinalis',r'\bporta fontinale\b'),('marcelli',r'\btheatro marcell'),('libitina',r'\bluco l[iu]b[ie]n?tina'),('mercsobr',r'\bmercurio sobrio\b'),
 ('vicuslongus',r'\bde vico longo\b'),('macliviae',r'\bmacello liviae\b'),('basiulia',r'\bbasilica iulia\b'),('hercmus',r'\bhercule musarum\b'),('cloaca',r'\bcloa?ca maxima\b'),
 ('trigemina',r'\bporta trigemina\b'),('iugarius',r'\bde vico iugario\b'),('circusmax',r'\bde circo maximo\b'),('sallust',r'\bex hortis sallustianis\b'),('viminalis',r'\bde colle viminale\b'),('transtib',r'\btrans ?tiberim\b')]
ADD={}
for k,p in AD:
    rx=re.compile(p);hh=[(r['id'],kk,sn) for r,kk,st,sn,post,c in H if rx.search(' '+post[:48])]
    cc=collections.Counter(kk for _,kk,_ in hh)
    ADD[k]={'n':len(set(i for i,_,_ in hh)),'occ':[x for x,_ in cc.most_common(10)],'ids':sorted(set(i for i,_,_ in hh)),'sn':[s for _,_,s in hh]}
D={'nrome':len(rome),'ntext':ntext,'nmil':nmil,'nocc':len(ids),'npairs':len(H),'nlex':len(lex.L),'ndated':len(nd),'st':[sum(o['st'][i] for o in OCC) for i in range(6)],
   'sect':SECT,'occ':OCC,'bins':B,'w':W,'time':TM,'cx':CXD,'addr':{k:{'n':v['n'],'occ':v['occ'],'ids':v['ids']} for k,v in ADD.items()}}
json.dump(D,open('/home/claude/roma/occ/data.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump([(h[0]['id'],h[1],h[2],h[3],h[4]) for h in H],open('/home/claude/roma/occ/hits.json','w'),ensure_ascii=False)
if __name__=='__main__':
    print({k:D[k] for k in ('nrome','ntext','nmil','nocc','npairs','ndated','st')})
    for k,v in SECT.items():print(k,v)
    print(len([o for o in OCC if o['n']>=10]),[(o['k'],o['n']) for o in OCC[:45]])
    for k,v in CXD.items():print(k,v)
    for k,v in ADD.items():
        print(k,v['n'],v['occ'],v['ids']);[print('      ',s) for s in v['sn']]
