# felmérés: a Monte Testaccio olajkereskedőinek neve a kőfeliratokon (LIST: EDCS+EDH szövegek)
import sys,re,pickle,collections
sys.path.insert(0,'/home/claude/roma/amph');import beta as BT
rows=pickle.load(open('/home/claude/dl/list/rows.pkl','rb'))
cnt=collections.Counter()
for a,i,kd,y in BT.ROWS:
    if isinstance(kd,str):continue
    t=BT.clean(i['full']).replace('v','u')
    w=[x for x in t.replace('/',' ').split() if x not in BT.PRAE and not BT.NUMP.match(x)]
    if len(w)==2 and all(re.fullmatch(r'[a-z]{4,}',x) for x in w):cnt[(w[0],w[1])]+=1
names=[(k,n) for k,n in cnt.most_common() if n>=3]
print(len(names))
def stem(x):return re.sub(r'(i|ii|ae|is|orum|onis|etis|i)$','',x)
for (nom,cog),n in names:
    s1=re.sub(r'(ii|i|ae)$','',nom);s2=re.sub(r'(onis|ionis|etis|entis|i|ae|is)$','',cog)
    if len(s2)<4:continue
    rx=re.compile(r'\b'+s1+r'(?:us|ius|i|ii|o|io|um|ium|a|ae|iae|iam)? '+s2+r'[a-z]{0,5}\b')
    hits=collections.Counter();ex=[]
    for reg,p,st,c,nb,na,city in rows:
        if 'tituli fabricationis' in st or 'sigilla' in st:continue
        m=rx.search(c.replace('v','u'))
        if m:hits[p]+=1;ex.append((p,c[max(0,m.start()-60):m.end()+70]))
    if hits:print(f'{nom} {cog} (amforán ×{n}):',dict(hits));[print('     ',p,'|',x) for p,x in ex[:4]]
