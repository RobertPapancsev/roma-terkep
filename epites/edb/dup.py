# v89c: ugyanannak a feliratnak több EDB-rekordja (ICVR I. kötet és a későbbi topográfiai kötetek, múzeumi gyűjtemények).
# 1) kereszthivatkozás a bibliográfiában (kötetkód + szám) ÉS a szöveg legalább 88%-ban egyezik;
# 2) azonos szöveg (≥18 betű) vagy közel azonos szöveg (≥90%, ≥28 betű), ha van benne név, és a nevek egyeznek; zarándokfirkák kizárva.
import re,json,collections,difflib
CODE={'257':'I','69':'II','162':'III','184':'IV','163':'V','108':'VI','183':'VII','104':'VIII','182':'IX','181':'X'}
MON=['ianuar','februar','mart','april','mai','iuni','iuli','august','septemb','octob','novemb','decemb']
STOP=set('''hic requiescit requiescet quiescit quiescet cesquet cesquit in pace pacem bene merenti benemerenti venemerenti benemerentibus qui que quae vixit bixit vixsit annis annos annus anus anos annum mensibus menses meses mensis mesis diebus dies kalendas calendas kalendis kalendarum nonas nonis idus idibus
depositus deposita deposit depositio deposito decessit recessit fecit fecerunt feci coniugi coiugi coniux coniunx coiux parentes dulcis dulcissimo dulcissimae dulcissime filio filiae filie filius filia et sibi suo suae sua locus consulatu consule consulibus conssulibus consules viro clarissimo viris clarissimis vviris cclarissimis
viriscclarissimis vviriscclarissimis dominis nostris domino nostro augusto plus minus plusminus se vivi vivo viva biba bibo vibi dis manibus die sub cum marito uxore pridie numero dormit anima animae innocenti innocentissimae carissimo carissimae posuit posuerunt pater mater frater soror fratri sorori patri matri
ενθαδε κειται κιται κατακειται κατακιτε εζησεν ετη ετων μηνασ μηνεσ μηνων ημερασ ημερων εν ειρηνη μνημησ χαριν γλυκυτατω γλυκυτατη τεκνω θυγατρι υιω και προ καλανδων ειδων νωνων κατετεθη ετελευτησεν εποιησεν εποιησαν'''.split())
# egyenként átolvasva: bizonytalan, ezért NEM vonjuk össze
NOT={('32037','32296'),('36330','36393'),('33642','33644'),('23184','23308'),('8603','17089')}
def toks(t):
    t=t.replace('¤t',' ').replace('¤',' ').replace('§',' ')
    return [x for x in t.split() if len(x)>=4 and x not in STOP and not re.fullmatch(r'[ivxlc]+',x) and not any(x.startswith(m) for m in MON)]
def ns(s):
    s=re.sub(r'add.*$','',s.lower());return re.sub(r'[^0-9a-z]','',s)
def find(R0,gclean,road):
    X=json.load(open('/home/claude/dl/edb/bibl.json'))
    RR={r['id']:r for r in R0}
    def txt(r):
        s=r['c'] or '';g=gclean(r['text']) if 'grc' in r['lang'] else ''
        return (s+' '+g) if (s and g and s!=g) else (s or g)
    TX={i:txt(r) for i,r in RR.items()};K={i:re.sub(r'[^a-zα-ω]','',t.replace('¤t','').replace('¤','')) for i,t in TX.items()}
    def sim(a,c):return difflib.SequenceMatcher(None,K[a],K[c],autojunk=False).ratio() if K[a] and K[c] else -1
    VOL={};P=collections.defaultdict(list)
    for i,b in X.items():
        if b and i in RR:
            m=re.match(r'ICVR ([IVX]+), (\d+)(.*)$',b[0].strip())
            if m:VOL[i]=m.group(1);P[(m.group(1),m.group(2))].append((i,ns(m.group(3))))
    L={}
    for i,b in X.items():
        if i not in RR:continue
        for x in b[1:]:
            m=re.match(r'\s*(\d+),\s+(\d+)(.*)$',x.strip())
            if not m or m.group(1) not in CODE:continue
            s1=ns(m.group(3))
            for j,s2 in P.get((CODE[m.group(1)],m.group(2)),[]):
                if j==i or (s1 and s2 and s1!=s2):continue
                a,c=sorted((i,j),key=int);v=sim(a,c)
                if v>=0.88:L[(a,c)]=('xref',v)
    blk=collections.defaultdict(list)
    for i,s in K.items():
        if len(s)<18 or 'tit. a viatore scriptus devotionis causa' in RR[i]['t']:continue
        for b in {s[:10],s[-10:],s[len(s)//2-5:len(s)//2+5]}:blk[b].append(i)
    TK={}
    def tk(i):
        if i not in TK:TK[i]=toks(TX[i])
        return TK[i]
    done=set()
    for b,v in blk.items():
        if len(v)<2 or len(v)>60:continue
        for x in range(len(v)):
            for y in range(x+1,len(v)):
                a,c=sorted((v[x],v[y]),key=int)
                if (a,c) in done or (a,c) in L:continue
                done.add((a,c));ka,kc=K[a],K[c]
                if min(len(ka),len(kc))/max(len(ka),len(kc))<0.85:continue
                ta,tc=tk(a),tk(c)
                if not ta or not tc:continue
                cons=bool(re.search(r'cons+ul|clarissim|augusto',TX[a]+TX[c]))
                if ka==kc:
                    if cons and len(ka)<60:continue
                    if '¤' in TX[a]+TX[c]:
                        if len(ka)<40:continue
                    elif len(ka)<24 and min(len(ta),len(tc))<2:continue
                    L[(a,c)]=('same',1.0);continue
                if min(len(ka),len(kc))<28 or (cons and len(ka)<60):continue
                s=difflib.SequenceMatcher(None,ka,kc,autojunk=False).ratio()
                if s<0.9 or (a,c) in NOT:continue
                sh,lo=(ta,tc) if len(ta)<=len(tc) else (tc,ta)
                if all(max(difflib.SequenceMatcher(None,w,u).ratio() for u in lo)>=0.72 for w in sh):L[(a,c)]=('near',s)
    par={}
    def f(x):
        while par.get(x,x)!=x:x=par[x]
        return x
    for a,c in L:
        ra,rc=f(a),f(c)
        if ra!=rc:par[rc]=ra
    G=collections.defaultdict(list)
    for i in set(x for p in L for x in p):G[f(i)].append(i)
    drop=set()
    for g in G.values():
        keep=sorted(g,key=lambda i:(road(RR[i]['cem']) is None,VOL.get(i)=='I',RR[i]['cem'] in('Inscription from Rome','incertae originis'),-len(K[i]),int(i)))[0]
        drop|=set(g)-{keep}
    return drop,L,TX
