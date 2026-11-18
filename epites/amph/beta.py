# v94: a β sor (az olajat szállító kereskedő vagy a császári pénztár neve) a Rómában talált Dressel 20 amforákon
import sys,re,collections
sys.path.insert(0,'/home/claude/roma/amph');import base as B,calc as C
D=B.D
PRAE=set('a aa c cc cn d dd g l ll m mm p pp q qq sex t tt ti k n ser sp'.split())
NUMP=re.compile(r'^(?:i{2,5}|iv|v|duorum|trium|quattuor|quinque|quinquorum)$')
SPELL=set('luci lvci marci titi quinti gai cai publi sexti'.split())
# egyenként átolvasva: írásváltozatok összevonása; None = nem családnév vagy bizonytalan
ALIAS={'lun':'iun','caecilioru':'caecil','caecilis':'caecil','caec':None,'memmio':'memm','laer':'laber','iiul':'iul','caud':'claud','atinis':'atin','atiniis':'atin','aimil':'aemil',
 'duoum':'stertin','soc':None,'periit':None,'dsms':None,'cclg':None,'ccuuu':None,'uer':None,'luc':None,'marc':None,'isc':None,'domin':None}
def clean(t):
    t=B.norm(t);t=re.sub(r'[·.^?<>{}=+]',' ',t);t=re.sub(r'\bscil\b|\bvacat\b',' ',t);return re.sub(r'\s+',' ',t).strip()
try:
    import betaex;GEX=betaex.GENS;KEX=betaex.KIND
except ImportError:GEX={};KEX={}
def gens(t):
    w=[x for x in t.replace('/',' ').split() if x not in PRAE and not NUMP.match(x)]
    if len(w)>=3 and w[0] in SPELL:w=w[1:]          # kiírt praenomen: „Luci Aeli Optati”
    if not w or '-' in w[0] or len(w[0])<4:return None
    g=w[0].replace('v','u')
    g=re.sub(r'(iorum|orum|iarum|ior|iae|ius|ii|i|ae|ia)$','',g)
    g=ALIAS.get(g,g)
    return g if g and len(g)>=3 else None
def kind(i):
    if i['id'] in KEX:return KEX[i['id']]
    t=clean(i['full'])
    if re.search(r'\bfisci\b|patrimoni',t):return 'fisc'
    if re.search(r'domin|\bnnn\b|augg|severi.*antonini|^ii augustorum|^avgvstorvm',t):return 'dom'
    if re.fullmatch(r'[-/ ]*|desiderantur|desideratur|vestigia.*|evanuit.*|evanid.*',t):return 'unread'
    g=GEX.get(i['id']) or gens(t)
    return ('priv',g) if g else 'frag'
ROWS=[]
for a in B.ROME:
    if 'dressel_20' not in a['type']:continue
    for ii in a['insc']:
        i=D.IN[ii]
        if 'TitulusCode-BET' in i['cls'] and i['full']:
            y=None
            for jj in a['insc']:
                j=D.IN[jj]
                if 'TitulusCode-DEL' in j['cls'] and j['full']:
                    yy,_=C.yr(a,j)
                    if yy:y=yy
            if y is None:y,_=B.year(a)
            ROWS.append((a,i,kind(i),y))
if __name__=='__main__':
    k=collections.Counter(r[2] if isinstance(r[2],str) else 'priv' for r in ROWS);print(len(ROWS),k)
    yk=collections.defaultdict(collections.Counter)
    for a,i,kd,y in ROWS:
        if y and kd!='unread' and kd!='frag':yk[y][kd if isinstance(kd,str) else 'priv']+=1
    for y in sorted(yk):print(y,dict(yk[y]))
    g=collections.Counter(r[2][1] for r in ROWS if not isinstance(r[2],str));print(len(g),g.most_common(70))
    if len(sys.argv)>1:
        byg=collections.defaultdict(collections.Counter)
        for a,i,kd,y in ROWS:
            if not isinstance(kd,str):byg[kd[1]][clean(i['full'])]+=1
            elif kd in sys.argv[1:]:byg['#'+kd][i['id']+':'+clean(i['full'])]+=1
        for gg,c in sorted(byg.items(),key=lambda x:(-sum(x[1].values()),x[0])):print(gg,sum(c.values()),'|',' ; '.join(f'{t} ×{n}' if n>1 else t for t,n in c.most_common()))
