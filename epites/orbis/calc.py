# ORBIS (W. Scheidel, E. Meeks, Stanford; orbis.stanford.edu) – hálózati lekérdezések Róma (50327) középponttal, 2026-11-12 -> orbis/data.json
import csv,json,math
D='/home/claude/dl/orbis/'
S={r[0]:(r[1],float(r[3]),float(r[4])) for r in csv.reader(open(D+'orbis_v2/sites.csv',encoding='utf8')) if r and r[0].isdigit()}
def ld(f): return {r['target']:float(r['cost']) for r in csv.DictReader(open(D+f+'.csv'))}
Q={k:ld(k) for k in ['to_fast_jul','to_fast_jan','from_fast_jul','to_cheap_jul_donkey','to_cheap_jul_wagon','to_cheap_jan_donkey']}
def hav(a,b,c,d):
    a,b,c,d=map(math.radians,(a,b,c,d));return 6371*2*math.asin(math.sqrt(math.sin((c-a)/2)**2+math.cos(a)*math.cos(c)*math.sin((d-b)/2)**2))
R=S['50327']
sites=[]
for k,(n,x,y) in S.items():
    if k=='50327' or k not in Q['to_fast_jul']: continue
    sites.append(dict(id=k,n=n,km=round(hav(R[2],R[1],y,x)),tj=Q['to_fast_jul'][k],tw=Q['to_fast_jan'].get(k),fj=Q['from_fast_jul'].get(k),cj=Q['to_cheap_jul_donkey'].get(k),cw=Q['to_cheap_jul_wagon'].get(k),cjan=Q['to_cheap_jan_donkey'].get(k)))
json.dump(dict(n=len(sites),sites=sites),open('orbis/data.json','w'),ensure_ascii=False)
if __name__=='__main__':
    print(len(sites),len(S))
    pick=['50286','50322','50268','50323','50251','50034','50086','50516','50455','50107','50250','50264','50429','50379','50179','50235','50124','50105','50035','50343','50359','50389','50050','50549','50129','50169','50613','50024','50094','50017','50138','50230','50396','50290','50160','50088']
    for k in pick:
        s=next(x for x in sites if x['id']==k);print(s['n'],s['km'],s['tj'],s['tw'],s['fj'],s['cj'],s['cw'],s['cjan'])
    import statistics as st
    print('max days',max(sites,key=lambda s:s['tj'])['n'],max(s['tj'] for s in sites),'median',st.median(s['tj'] for s in sites),'max cost',max(sites,key=lambda s:s['cj'])['n'],max(s['cj'] for s in sites))
