# CHRR Online (K. Lockyear; ANS, numismatics.org/chrr; ODbL) -> chrr/data.json
import csv,re,json,collections,statistics as st
csv.field_size_limit(10**9)
R=list(csv.DictReader(open('/home/claude/dl/chrr/q.csv',encoding='utf8')))
def n(x):
    try: return int(float(x))
    except: return None
REG={'Italy':'it','Sicily':'it','Sardinia':'it','Elba':'it','Nr. Sicily':'it','San Marino':'it','Spain':'hi','Portugal':'hi','Romania':'ro'}
for r in R:
    m=re.search(r'\(([^;()]+);\s*([A-Z0-9]+)\)\s*$',r['Title']);r['country']=m.group(1).strip()
    r['reg']=REG.get(r['country'],'ot');r['y']=n(r['Terminus Ante Quem']);r['coins']=sum(int(x) for x in re.findall(r':\s*(\d+)',r['Description']))
D=[r for r in R if r['y'] is not None]
B=list(range(-150,20,5))
def hist(rows): return [sum(1 for r in rows if b<=r['y']<b+5) for b in B]
PER=[(-200,-92),(-91,-82),(-81,-71),(-70,-50),(-49,-42),(-41,-31),(-30,14)]
res={'n':len(R),'dated':len(D),'bins':B,'all':hist(D),'it':hist([r for r in D if r['reg']=='it']),'before':sum(1 for r in D if r['y']<-150),
 'nreg':{k:sum(1 for r in D if r['reg']==k) for k in ('it','hi','ro','ot')},
 'per':[{'a':a,'b':b,**{k:sum(1 for r in D if r['reg']==k and a<=r['y']<=b) for k in ('it','hi','ro','ot')},'all':sum(1 for r in D if a<=r['y']<=b),'peryear':round(sum(1 for r in D if a<=r['y']<=b)/(b-a+1 - (1 if a<0<b else 0)),2)} for a,b in PER],
 'coins':{'n':sum(1 for r in D if r['coins']>0),'sum':sum(r['coins'] for r in D),'median':st.median([r['coins'] for r in D if r['coins']>0])},
 'top':collections.Counter(r['y'] for r in D).most_common(6),
 'rome':[dict(t=r['Title'],y=r['y'],d=r['Description'],ref=r['Reference']) for r in R if re.search(r'\bRom[ea]\b',r['Title'])]}
json.dump(res,open('chrr/data.json','w'),ensure_ascii=False)
if __name__=='__main__':
    print(res['n'],res['dated'],res['before'],res['nreg'],res['coins'],res['top'])
    for p in res['per']: print(p)
    for b,x,y in zip(B,res['all'],res['it']): print(b,x,y)
    for x in res['rome']: print(x)
