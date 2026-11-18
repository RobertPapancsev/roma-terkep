# OxREP Shipwrecks Database 2.1 (Strauss, Wilson, Flohr 2017) -> wreck/data.json
import sys,math,json,re;sys.path.insert(0,'/home/claude/roma/wreck')
from load import load
from collections import Counter
D=load();W=D['Shipwrecks'];O=D['Shipwreck Objects'];A=D['Amphorae']
def num(x):
    try: return float(x)
    except: return None
for w in W:
    w['e']=num(w['Earliest Date']);w['l']=num(w['Latest Date']);w['lat']=num(w['Latitude']);w['lon']=num(w['Longitude'])
    w['dated']=w['e'] is not None and w['l'] is not None and w['l']>=w['e']
B0,B1,ST=-500,700,50
bins=list(range(B0,B1,ST))
def aor(ws,maxspan=None):
    out=[0.0]*len(bins);n=0
    for w in ws:
        if not w['dated']: continue
        e,l=w['e'],w['l'];sp=l-e
        if maxspan is not None and sp>maxspan: continue
        n+=1
        if sp==0:
            i=int((e-B0)//ST)
            if 0<=i<len(bins): out[i]+=1
            continue
        for i,b in enumerate(bins):
            ov=min(l,b+ST)-max(e,b)
            if ov>0: out[i]+=ov/sp
    return [round(x,2) for x in out],n
res={'n':len(W),'dated':sum(1 for w in W if w['dated']),'bins':bins}
res['all'],res['n_all']=aor(W);res['p100'],res['n_p100']=aor(W,100);res['p50'],res['n_p50']=aor(W,50)
tf=lambda v:v is True or str(v)=='True'
stone=[w for w in W if any(tf(w[k]) for k in ('Marble','Columns etc','Sarcophagi','Blocks'))]
res['stone'],res['n_stone']=aor(stone);res['n_stone_all']=len(stone)
def hav(a,b,c,d):
    a,b,c,d=map(math.radians,(a,b,c,d));return 6371*2*math.asin(math.sqrt(math.sin((c-a)/2)**2+math.cos(a)*math.cos(c)*math.sin((d-b)/2)**2))
# Dressel 20
byid={str(w['locid']):w for w in W};bywid={}
for w in W: bywid.setdefault(w['Wreck ID'],[]).append(w)
d20=set()
for o in O:
    if o['Class']=='Amphorae' and re.search(r'(Dressel|Dr\.?) ?20\b',str(o['Type'])+' '+str(o['objdesc'])): d20.add(str(o['objloc']))
for a in A:
    if re.search(r'(Dressel|Dr\.?) ?20\b',str(a['Amphora type'])+' '+str(a['Comments'] or '')):
        for w in bywid.get(a['Wreck ID'],[]): d20.add(str(w['locid']))
res['d20']=[dict(id=k,name=byid[k]['Wreck Name'],e=byid[k]['e'],l=byid[k]['l'],country=byid[k]['Country'],region=byid[k]['Region'],lat=byid[k]['lat'],lon=byid[k]['lon'],amph=str(byid[k].get('Other cargo'))[:0]) for k in sorted(d20) if k in byid]
res['d20a'],res['n_d20']=aor([byid[k] for k in d20 if k in byid])
res['rome']=sorted([dict(km=round(hav(41.78,12.25,w['lat'],w['lon'])),name=w['Wreck Name'],e=w['e'],l=w['l'],dc=w['Dating comment'],com=(w['Comments'] or '')[:300],cargo=(w['Other cargo'] or '')[:200],amph=str(w['Amphorae']),stone=(w['Stone cargo notes'] or '')[:150],ton=w['Estimated tonnage'],ln=w['Estimated length']) for w in W if w['lat'] is not None and w['lon'] is not None and hav(41.78,12.25,w['lat'],w['lon'])<=60],key=lambda x:(x['km'],x['name']))
json.dump(res,open('/home/claude/roma/wreck/data.json','w'),ensure_ascii=False,indent=0)
if __name__=='__main__':
    print(res['n'],res['dated'],res['n_all'],res['n_p100'],res['n_p50'],res['n_stone_all'],res['n_stone'],res['n_d20'])
    for i,b in enumerate(bins): print(b,res['all'][i],res['p100'][i],res['p50'][i],res['stone'][i],res['d20a'][i])
    for x in res['d20']: print(x)
