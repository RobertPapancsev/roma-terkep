# v85: Jogállás-jelölések és császári családnevek időben. Bemenet: recs.json, text.json (EDR). Kimenet: nm/data.json
import json,re,collections,sys,unicodedata
R=json.load(open('/home/claude/dl/edr/recs.json'));T=json.load(open('/home/claude/dl/edr/text.json'))
rome=[r for r in R if 'Roma' in r['pf']]
def tlen(c):return len(re.sub(r'\s*¤t?\s*',' ',c).strip())
def clean(t):
    t=re.sub(r'=\s*/\s*','',t);t=re.sub(r'(?<=[^\s\-])-\s*/\s*(\[?)',r'\1',t)
    t=re.sub(r'(?<=[A-Za-z\)])\[[\s\-–?]*\]',' ¤t ',t);t=re.sub(r'\[[\s\-–?]*\]',' ¤ ',t);t=re.sub(r'(?:-\s){2,}-',' ¤ ',t)  # ¤ = elveszett szöveg (lacuna); ¤t = a hiány közvetlenül a szóhoz vagy számhoz tapad („XX[- - -]”), tehát az csonka
    t=unicodedata.normalize('NFD',t.lower());t=''.join(ch for ch in t if unicodedata.category(ch)!='Mn')
    t=re.sub(r'\(:[^)]*\)','',t);t=re.sub(r'\(\((?:mulieris|gaiae)\)\)','mulieris',t);t=re.sub(r'\(\([^)]*\)\)',' ',t)
    t=re.sub(r'[\[\]\(\)<>{}`´?!+〚〛《》⌜⌝"]','',t)
    t=re.sub(r'〈:?\s*(vacat|verso|recto)\s*〉',' § ',t);t=re.sub(r'〈:\s*([a-z]{3,}(?: diem)?)\s*〉',r' \1 ',t);t=re.sub(r'〈([a-z])〉',r'\1',t)
    t=re.sub(r'〈[^〉]*〉',' § ',t);t=re.sub(r'[/,.;:·\-=]+',' ',t);return re.sub(r'\s+',' ',t).strip()
# Ismétlődő rekordok: ugyanaz a (legalább 40 betűs) szöveg több EDR-számon (többpéldányos vagy kétszer felvett felirat). A személyekre vonatkozó számításokban egyszer számít.
_G=collections.defaultdict(list)
for _r in sorted(rome,key=lambda r:r['id']):
    _c=clean(T.get(_r['id'],''))
    if len(_c)>=40 and '¤' not in _c:_G[_c].append(_r['id'])
GROUP={v[0]:v[1:] for v in _G.values() if len(v)>1};SKIP={i for v in GROUP.values() for i in v}
json.dump({'skip':sorted(SKIP),'group':GROUP},open('/home/claude/roma/nm/dup.json','w'))
rome=[r for r in rome if r['id'] not in SKIP]
PRAE=r'(?:marci|luci|gai|cai|quinti|publi|titi|gnaei|cnaei|auli|sexti|decimi|tiberi|mani|numeri|spuri|servi|appi)'
IW=r'(?:august[io]|augustae|augustorum|augg?|caesaris|caesarum|imperatoris)(?: nostri| nostrorum| n)?'
RX={'lib':re.compile(r'\blibert(?:us|a|o|ae|um|am|i)\b'),
    'ilib':re.compile(IW+r' libert'),
    'ser':re.compile(r'\b(?:con)?serv(?:us|a|o|ae|um|am|i)\b(?! (?:dei|christi|domini))|\bvern(?:a|ae|am)\b'),
    'iser':re.compile(IW+r' (?:serv|vern)'),
    'fil':re.compile(PRAE+r' (?:filius|filia|filio|filiae|fili)\b')}
NOM=['iuli','claudi','flavi','coccei','ulpi','aeli','aureli','septimi']
EMP=r'(?! (?:[a-z]+ ){0,4}(?:caesar|august|imperator|germanic|nostri ser|nostri ver))'
NRX={n:re.compile(r'(?<!divi )(?<!divo )\b'+n+r'(?:us|a|i|o|ae|um|am)?\b'+EMP) for n in NOM}
ALRX={n:re.compile(r'\b'+n+r'(?:us|a|i|o|ae|um|am)? (?:[a-z]+ ){0,2}?'+IW+r' libert') for n in NOM}
# nem személynév: szavazókerület és álkerület (filius Claudia), légiók (VII Claudia, XXX Ulpia), épületek (basilica Iulia, aqua Claudia, forum Ulpium), hónap, késő császárok és consulok (domino nostro Flavio, consulatu Flavi)
NOTN=re.compile(r'^(?:filius|filio|fili|filia|filiae|basilica|basilicae|aqua|aquae|foro|forum|mense|mensis|nostro|nostri|nostrorum|nn|consulatu|consulatum|consule|consulibus|legionis|legio|colonia|kalendas|nonas|idus|kalendis|nonis|idibus|[ivxl]+)$')
def nomhit(c,rx):
    for m in rx.finditer(c):
        p=c[:m.start()].split()
        if p and NOTN.match(p[-1]):continue
        return True
    return False
X0,X1,W=-200,700,25;B=list(range(X0,X1,W))
def aw(a,b):
    L=b-a;return [(1.0 if x<=a<x+W else 0.0) if L==0 else max(0,min(b,x+W)-max(a,x))/L for x in B]
K=list(RX)+NOM
TM={k:[0.0]*len(B) for k in K};TOT=[0.0]*len(B);CNT=collections.Counter();AL=collections.Counter();ntext=0;ndated=0
ROWS=[]
for r in rome:
    c=clean(T.get(r['id'],''))
    if tlen(c)<8:continue
    ntext+=1
    f={k for k,rx in RX.items() if rx.search(c)}|{n for n,rx in NRX.items() if nomhit(c,rx)}
    for k in f:CNT[k]+=1
    for n,rx in ALRX.items():
        if rx.search(c):AL[n]+=1
    ROWS.append((r['loc'],f))
    if r['nb']=='' or r['na']=='':continue
    a,b=int(r['nb']),int(r['na'])
    if b<a or b<X0 or a>=X1:continue
    ndated+=1;w=aw(a,b)
    for i,v in enumerate(w):
        if v:
            TOT[i]+=v
            for k in f:TM[k][i]+=v
D={'bins':B,'w':W,'ntext':ntext,'ndated':ndated,'cnt':dict(CNT),'al':dict(AL),'tot':[round(v,1) for v in TOT],'time':{k:[round(v,1) for v in t] for k,t in TM.items()}}
CX=[('statili',r'colombario degli statili','portamaior'),('liviae',r'monumentum liviae',None),('codini',r'vigna codini','columbariacodini'),('volusii',r'monumentum volusiorum',None),
 ('salario',r'sepolcreto salario|tra via salaria e via pinciana|via po\b|via livenza','csalario'),('spaolo',r's\. paolo fuori',None),('vatican',r'necropoli vaticana|necropoli della via triumphalis',None),
 ('pamphilj',r'villa pamphilj',None),('equites',r'equites singulares',None),('callisto',r'catacombe? di s\. callisto',None),('domitilla',r'catacombe di domitilla',None),('priscilla',r'catacombe di priscilla',None),('pretestato',r'catacombe di pretestato',None)]
D['cx']={}
for k,p,e in CX:
    rx=re.compile(p,re.I);rows=[f for l,f in ROWS if rx.search(l)]
    n=len(rows);cc=collections.Counter(x for f in rows for x in f)
    D['cx'][k]={'n':n,'e':e,'c':{x:cc.get(x,0) for x in K}}
json.dump(D,open('/home/claude/roma/nm/data.json','w'),separators=(',',':'))
if __name__=='__main__':
    print(ntext,ndated,CNT,AL)
    for i,x in enumerate(B):
        if TOT[i]>=40:print(x,round(TOT[i]),' '.join(f'{k}:{100*TM[k][i]/TOT[i]:.0f}' for k in K))
    for k,v in D['cx'].items():print(k,v['n'],{x:round(100*y/max(1,v['n'])) for x,y in v['c'].items()})
