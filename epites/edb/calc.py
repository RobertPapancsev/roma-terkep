# v89: Keresztény feliratok Rómában (EDB, 3–8. század). Bemenet: /home/claude/dl/edb/recs.json (edb/parse.py). Kimenet: edb/data.json
import json,re,collections,importlib.util
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
A=load('agecalc','/home/claude/roma/age/calc.py');N=A.NMC;clean=N.clean;rom=A.rom
import sys;sys.path.insert(0,'/home/claude/roma/edb');import greek as GK
R0=json.load(open('/home/claude/dl/edb/recs.json'))
def cem(t):return re.sub(r' - [^-]*$','',t.replace('Inscription from Rome, ','')).strip()
for r in R0:r['cem']=cem(r['title']);r['c']=clean(r['text']) if 'la' in r['lang'] else ''
# ismétlődések: azonos temető és azonos (legalább 40 betűs, hiány nélküli) latin szöveg
seen=set();R=[]
for r in sorted(R0,key=lambda r:int(r['id'] or 0)):
    k=(r['cem'],r['c'])
    if len(r['c'])>=40 and '¤' not in r['c']:
        if k in seen:continue
        seen.add(k)
    R.append(r)
R1=R
ROADS=[('appia',r'Callisti|Area Lucinae|Crypta s\.Cornelii|Praetextati|Catacumbas|ad viam Appiam|ad Vibiam'),('ardeatina',r'Domitillae|Nerei et Achillei|ad viam Ardeatinam'),('appard',r'[Ii]nter vias Appiam et Ardeatinam'),
 ('ostiensis',r'Commodillae|s\.Pauli|s\.Theclae'),('portuensis',r'Pontiani|Generosae'),('aurelia',r'Pancrat|Pancrazio|Calepodii|Processi et Martiniani'),('vaticana',r'S\.Petri|viam Corneliam'),
 ('flaminia',r'Valentini'),('salaria',r'Bassillae|Pamphili|Priscill|priscillianae|Iordanorum|Felicitat|viam Anapo'),('nomentana',r's\.Agnetis|Coem\. Maius|Nicomedis|s\.Alexandri'),
 ('tiburtina',r'Cyriacae|Hippolyti|Novatiani'),('labicana',r'Marcellini et Petri|Castuli'),('latina',r'Aproniani|Aquae Marianae|Trebii Iusti|D\.Compagni')]
RRX=[(k,re.compile(p)) for k,p in ROADS]
def road(c):
    for k,rx in RRX:
        if rx.search(c):return k
    return None
# v89c: ugyanaz a felirat több rekordban (edb/dup.py)
import dup as DUP
DROP,DLINK,DTX=DUP.find(R1,GK.gclean,road)
R=[r for r in R1 if r['id'] not in DROP]
X0,X1,W=150,750,25;B=list(range(X0,X1,W))
def aw(a,b):
    L=b-a;return [(1.0 if x<=a<x+W else 0.0) if L==0 else max(0,min(b,x+W)-max(a,x))/L for x in B]
def q(L,f):
    L=sorted(L);return L[int(f*(len(L)-1))] if L else None
def chr_(r):return any(('Monogr' in d) or d=='chi-rho' for d in r['dec']) or bool(re.search(r'\(\(monogramma Christi|\(\(christogramma',r['text']))
def crs(r):return any(d.lower().startswith(('cross','crux')) for d in r['dec']) or bool(re.search(r'\(\(crux',r['text']))
SYM=collections.Counter()
for r in R:
    for m in set(x.strip().lower() for x in re.findall(r'\(\(([^)]{2,40})\)\)',r['text'])):SYM[m]+=1
SYG=[('bird',r'avis|columba'),('palm',r'palma'),('anchor',r'ancora'),('fish',r'piscis|delphin'),('vessel',r'^vas\b|cantharus|amphora'),('tree',r'arbor'),('wreath',r'corona'),('sheep',r'ovis|agnus'),('orans',r'orans'),('ship',r'navis'),('shepherd',r'pastor')]
SG=collections.Counter()
for r in R:
    ms=set(x.strip().lower() for x in re.findall(r'\(\(([^)]{2,40})\)\)',r['text']))
    for k,p in SYG:
        if any(re.search(p,m) for m in ms):SG[k]+=1
T={k:[0.0]*len(B) for k in ('all','grc','chr','crs')}
for r in R:
    if r['nb']=='' or r['na']=='':continue
    a,b=int(r['nb']),int(r['na'])
    if b<a or b<X0 or a>=X1:continue
    w=aw(a,b);g='grc' in r['lang'];c1=chr_(r);c2=crs(r)
    for i,v in enumerate(w):
        if v:
            T['all'][i]+=v
            if g:T['grc'][i]+=v
            if c1:T['chr'][i]+=v
            if c2:T['crs'][i]+=v
CC=collections.Counter(r['cem'] for r in R)
CEM=[]
for c,n in CC.most_common(40):
    if c in('Inscription from Rome','incertae originis'):continue
    S=[r for r in R if r['cem']==c];mid=[(int(r['nb'])+int(r['na']))/2 for r in S if r['nb']!='' and r['na']!='']
    CEM.append({'c':c,'n':n,'road':road(c),'q1':q(mid,.25),'q3':q(mid,.75),'grc':sum(1 for r in S if 'grc' in r['lang']),'chr':sum(1 for r in S if chr_(r)),'pict':sum(1 for r in S if r['ex'] in('Pictus','Scariphatus','Exaratus','Carbone scriptus'))})
RD=collections.Counter(road(r['cem']) for r in R)
# latin szöveg: életkor, formulák, tisztségek, temetés hónapja
LAT=[r for r in R if 'la' in r['lang'] and N.tlen(r['c'])>=8]
for r in R:r['g']=GK.gclean(r['text']) if 'grc' in r['lang'] else ''
GRC=[r for r in R if 'grc' in r['lang'] and len(re.sub(r'[¤t§ ]','',r['g']))>=6]
ages=[];pm=0
for r in LAT:
    c=r['c']
    for m in A.AGE.finditer(c):
        a=rom(m.group(1))
        if not 0<a<=120 or c[m.end():].lstrip().startswith('¤t'):continue
        pw=c[max(0,m.start()-40):m.start()].split()
        if A.MAR.search(' '.join(pw[-5:])):continue
        ages.append(a)
        if re.search(r'plus minus|p m |pm ',m.group(0)):pm+=1
nla=len(ages);GA={}
# v89c: a görög életkorok egyenként átolvasva; a gépi olvasat javításai (házasság hossza, törött számnév, kétszer írt életkor, szám a szó előtt)
GFIX={'6433':[70],'12797':[50],'35575':[70],'14947':[33],'10865':[],'23770':[32],'6852':[50]}
for r in GRC:
    if any(True for _ in A.AGE.finditer(r['c'])):continue   # kétnyelvű: a latin rész már számolt
    ga=GFIX.get(r['id'],GK.ages(r['g']));GA[r['id']]=bool(ga);ages.extend(ga)
ngr=len(ages)-nla
adult=[a for a in ages if 23<=a<=62]
MON=['ianuar','februar','mart','april','mai','iuni','iuli','august','septemb','octob','novemb','decemb']
MRX='(?:'+'|'.join(MON)+r')[a-z]*'
DEP=re.compile(r'\b(?:deposit[a-z]*|depossio|depositio|d p|decessit|recessit|defunct[a-z]*|obiit|quiev[a-z]+|requiev[a-z]+)\b(?: (?:est|in pace|die|sub die|in fide|fidelis)){0,3} (pridie |postridie )?(?:(?:ante )?(?:diem )?([ivx]+) )?(kalend[a-z]*|nonas|nonis|idus|idibus|iduum|nonarum) ('+MRX+')')
months=[0]*12
for r in LAT:
    m=DEP.search(r['c'])
    if not m:continue
    mi=[i for i,x in enumerate(MON) if m.group(4).startswith(x)][0]
    if m.group(3).startswith('kalend') and (m.group(1) or m.group(2)):mi=(mi-1)%12   # „III kalendas Septembres” augusztusra esik
    months[mi]+=1
TIT=[('episc',r'\bepiscop|\bpapa\b|\bpapae\b'),('presb',r'\bpresb[yi]ter|\bpraesb[yi]ter|\bprb\b'),('diac',r'(?<!sub)(?<!archi)\bdiacon|\bdiacon'),('subd',r'\bsubdiacon'),('acol',r'\bacol[uiy]t|\bacolot'),('lect',r'\blector(?:is|i|em|e)?\b'),('exor',r'\bexorcist'),
 ('foss',r'\bfoss?or(?:is|i|em|e|es|um|ibus)?\b'),('virgo',r'\bvirgo dei|\bvirgo sacra|\bvirgini sacrae|\bancilla dei|\bancillae dei|\bvirgo devota|\bsacra virgo'),('neof',r'\bneo[fp]h?[iy]t'),('mart',r'\bmart[yiu]r(?:is|i|em|es|um|ibus)?\b')]
mla=sum(months)
for r in GRC:
    if DEP.search(r['c']):continue
    mi=GK.month(r['g'],GA.get(r['id'],False))
    if mi is not None:months[mi]+=1
# v89c: a tisztségek találatai egyenként átolvasva; kizárva az olvasó megszólítása (lector), a Martyrius-féle személynevek és a presbyterium
TEX={'lect':{'17451','34549','35368','35220','14469'},'mart':{'16840','9893','25850','35335','4103','3697'},'presb':{'27138'}}
TC={k:len(({r['id'] for r in LAT if re.search(p,r['c'])}|{r['id'] for r in GRC if k in GK.TIT and re.search(GK.TIT[k],r['g'])})-TEX.get(k,set())) for k,p in TIT}
FORM=[('pace',r'\bin pace\b'),('dep',r'\bdeposit|\bdepossio\b'),('bm',r'\bbene ?merenti\b'),('dm',r'\bdis manibus\b'),('locus',r'\blocus\b'),('vivo',r'\bse viv[oa]\b|\bse bib[oa]\b'),('emit',r'\bemit\b|\bcomparavit\b|\bconparavit\b')]
FC={k:len({r['id'] for r in LAT if re.search(p,r['c'])}|{r['id'] for r in GRC if k in GK.FORM and re.search(GK.FORM[k],r['g'])}) for k,p in FORM}
ntxt=len({r['id'] for r in LAT}|{r['id'] for r in GRC})
EDR=json.load(open('/home/claude/roma/age/data.json'))
D={'n0':len(R0),'n':len(R),'ndup':len(R0)-len(R),'dated':sum(1 for r in R if r['nb']!='' and r['na']!=''),'lang':dict(collections.Counter(r['lang'] for r in R)),'type':collections.Counter(x for r in R for x in r['t']).most_common(6),
 'ex':dict(collections.Counter(r['ex'] for r in R)),'chr':sum(1 for r in R if chr_(r)),'crs':sum(1 for r in R if crs(r)),'metr':sum(1 for r in R if r['me']=='Metrical'),'sym':SYM.most_common(30),'sg':dict(SG),
 'bins':B,'w':W,'time':{k:[round(v,1) for v in t] for k,t in T.items()},'cem':CEM,'ncem':len(CC),'road':{k:v for k,v in RD.items() if k},'noroad':RD[None],
 'nlat':len(LAT),'ngrc':len(GRC),'ntxt':ntxt,'mla':mla,'mgr':sum(months)-mla,'age':{'n':len(ages),'nla':nla,'ngr':ngr,'med':q(ages,.5),'u10':sum(1 for a in ages if a<10),'o60':sum(1 for a in ages if a>=60),'whipple':round(500*sum(1 for a in adult if a%5==0)/len(adult)),'pm':pm,'hist':[sum(1 for a in ages if min(a//5,16)==i) for i in range(17)]},
 'edr':{'med':EDR['medall'],'u10':EDR['u10']/EDR['nage'],'o60':EDR['o60']/EDR['nage'],'whipple':EDR['whipple'],'n':EDR['nage']},'months':months,'tit':TC,'form':FC}
json.dump(D,open('/home/claude/roma/edb/data.json','w'),ensure_ascii=False,separators=(',',':'))
if __name__=='__main__':
    for k,v in D.items():
        if k not in('time','cem','bins'):print(k,v)
    for c in CEM[:32]:print(c)
    print([(B[i],round(T['all'][i]),round(100*T['grc'][i]/T['all'][i]),round(100*T['chr'][i]/T['all'][i]),round(100*T['crs'][i]/T['all'][i])) for i in range(len(B)) if T['all'][i]>=30])
