# v90: a list/calc.py + list/stats.py eredményeiből a kártya adatai (list/data.json)
import pickle,json,collections,sys,math
sys.path.insert(0,'/home/claude/roma/list');import calc as C
S,AG,REC=pickle.load(open('/home/claude/dl/list/stats.pkl','rb'))
rows=pickle.load(open('/home/claude/dl/list/rows.pkl','rb'))
ORD=['roma','italia','insulae','africa','hispania','gallia','britannia','danuvius','oriens']
def q(L,f):L=sorted(L);return L[int(f*(len(L)-1))]
R={}
for k in ORD:
    s=S[k];a=AG[k];ad=[x for x in a if 23<=x<=62];pe=s['pe']
    R[k]={'n':s['n'],'instr':s['instr'],'short':s['short'],'dup':s['dup'],'stone':s['stone'],'ep':s['ep'],'chr':s['e_chr'],'pe':pe,
     'f':{x:round(100*s['p_'+x]/pe,1) for x in('dm','hse','sttl','bm','lib','ser','mil')},
     'age':{'n':len(a),'med':q(a,.5),'q1':q(a,.25),'q3':q(a,.75),'u10':round(100*sum(1 for x in a if x<10)/len(a),1),'o60':round(100*sum(1 for x in a if x>=60)/len(a),1),'whipple':round(500*sum(1 for x in ad if x%5==0)/len(ad)),'nad':len(ad),
            'hist':[sum(1 for x in a if min(x//10,9)==i) for i in range(10)]}}
# idő: kőfeliratok, legfeljebb 200 éves keltezési sávval
B=C.B;T={g:[0.0]*len(B) for g in('roma','italia','prov')};nd=collections.Counter();nw=collections.Counter()
for idx,reg,ep,chr_,nb,na,lib,mil,ser in REC:
    g='roma' if reg=='roma' else 'italia' if reg=='italia' else 'prov'
    nd[g+'_all']+=1
    if nb!=nb or na!=na:continue
    nd[g+'_dated']+=1
    if na-nb>200:nw[g]+=1;continue
    for i,v in enumerate(C.aw(nb,na)):T[g][i]+=v
# városok
city=collections.Counter();pop={}
import pandas as pd
t=pd.read_pickle('/home/claude/dl/list/all_meta.pkl')
cs=collections.Counter();ci=collections.Counter()
keep={r[0] for r in REC}
for i,(c,p) in enumerate(zip(t['urban_context_city'],t['urban_context_pop_est'])):
    if isinstance(c,str):
        ci[c]+=1;pop[c]=p
        if i in keep:cs[c]+=1
CIT=[{'c':c,'n':n,'stone':cs[c],'pop':int(pop[c])} for c,n in sorted(ci.items(),key=lambda x:-cs[x[0]])[:10]]
D={'n':len(rows),'ord':ORD,'reg':R,'alia':S['alia']['n'],'bins':B,'w':C.W,'time':{g:[round(v,1) for v in x] for g,x in T.items()},'dated':dict(nd),'wide':dict(nw),'cities':CIT,
 'edr':{k:v for k,v in json.load(open('/home/claude/roma/age/data.json')).items() if k in('medall','u10','o60','whipple','nage')}}
json.dump(D,open('/home/claude/roma/list/data.json','w'),ensure_ascii=False,separators=(',',':'))
print(D['dated'],D['wide']);print(D['cities'])
for g in T:print(g,[round(v) for v in T[g]])
print([round(100*T['roma'][i]/(T['roma'][i]+T['italia'][i]+T['prov'][i])) for i in range(len(B))])
for k in ORD:print(k,R[k]['age'],R[k]['f'])
