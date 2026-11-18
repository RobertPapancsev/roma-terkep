import pickle,re,collections,sys,json
sys.path.insert(0,'/home/claude/roma/list');import calc as C
rows=pickle.load(open('/home/claude/dl/list/rows.pkl','rb'))
A=C.A
AGE2=re.compile(r'\bannorum (?:plus minus |p m |pm )?([ivxlc]+)\b')
AGE3=re.compile(r'\b(?:vixi|vixisti|vixit in saeculo|vixit in seculo|bixit in saeculo) (?:annos|annis) (?:plus minus |p m |pm )?([ivxlc]+)\b')
NOT2=re.compile(r'\b(?:cum|post|per|intra|ante|militavit|stipendiorum)$')
def ages(c):
    out=[];sp=[]
    for rx in (A.AGE,AGE3,AGE2):
        for m in rx.finditer(c):
            if any(a<m.end() and m.start()<b for a,b in sp):continue
            a=C.rom(m.group(1))
            if not 0<a<=120 or c[m.end():].lstrip().startswith('¤t'):continue
            pw=c[max(0,m.start()-40):m.start()].split()
            if A.MAR.search(' '.join(pw[-5:])):continue
            if rx is AGE2 and pw and NOT2.search(pw[-1]):continue
            sp.append((m.start(),m.end()));out.append(a)
    return out
S=collections.defaultdict(collections.Counter);AG=collections.defaultdict(list);seen=set();KW=collections.defaultdict(collections.Counter)
REC=[]
for idx,(reg,p,st,c,nb,na,city) in enumerate(rows):
    s=S[reg];s['n']+=1
    if C.INSTR.search(st):s['instr']+=1;continue
    L=C.tlen(c)
    if L<15:s['short']+=1;continue
    if L>=40 and '¤' not in c:
        k=(p,c)
        if k in seen:s['dup']+=1;continue
        seen.add(k)
    s['stone']+=1
    f={k:bool(rx.search(c)) for k,rx in C.F.items()}
    ag=ages(c)
    sepk=bool(C.SEP.search(st));sept=f['dm'] or f['hse'] or f['sttl'] or f['vix'] or bool(ag)
    chr_=bool(C.CHR.search(st))
    if sepk:s['sepk']+=1
    if sept:s['sept']+=1
    if sepk and sept:s['sepkt']+=1
    if chr_:s['chr']+=1
    if not st:s['nokw']+=1
    if sepk or sept:
        s['ep']+=1
        for k,v in f.items():
            if v:s['e_'+k]+=1
        if ag:s['e_age']+=1
        AG[reg].extend(ag)
        if not chr_:
            s['pe']+=1
            for k in('lib','ser','mil','dm','hse','sttl','bm'):
                if f[k]:s['p_'+k]+=1
        if chr_:s['e_chr']+=1
    for k,kw in (('lib','liberti/libertae'),('mil','milites'),('ser','servi/servae')):
        a=f[k];b=kw in st;KW[k][(reg=='roma',a,b)]+=1
    REC.append((idx,reg,sepk or sept,chr_,nb,na,f['lib'],f['mil'],f['ser']))
pickle.dump((dict(S),dict(AG),REC),open('/home/claude/dl/list/stats.pkl','wb'))
def q(L,f):L=sorted(L);return L[int(f*(len(L)-1))]
for reg in ['roma','italia','insulae','africa','hispania','gallia','britannia','danuvius','oriens','alia']:
    s=S[reg];e=s['ep'];a=AG[reg];ad=[x for x in a if 23<=x<=62]
    print(reg,dict(n=s['n'],instr=s['instr'],short=s['short'],dup=s['dup'],stone=s['stone'],sepk=s['sepk'],sept=s['sept'],both=s['sepkt'],ep=e,chr=s['chr'],nokw=s['nokw']))
    print('   pagan',s['pe'],{k[2:]:round(100*v/s['pe'],1) for k,v in s.items() if k.startswith('p_')})
    print('   ',{k[2:]:round(100*v/e,1) for k,v in s.items() if k.startswith('e_')},'ages',len(a),'med',q(a,.5),'u10',round(100*sum(1 for x in a if x<10)/len(a),1),'o60',round(100*sum(1 for x in a if x>=60)/len(a),1),'whipple',round(500*sum(1 for x in ad if x%5==0)/len(ad)))
print({k:dict(v) for k,v in KW.items()})
