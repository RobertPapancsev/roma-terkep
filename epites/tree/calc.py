# v113: Büntgen et al. 2011 (NOAA WDC Paleo 2011-026) – közép-európai AMJ csapadék és JJA hőmérséklet, Kr. e. 398 – Kr. u. 800
import json,statistics as S,sys
src=sys.argv[1]
P={};T={}
for ln in open(src,encoding='latin-1').read().split('\n')[106:2620]:
    y=ln[:6].strip()
    if not y.lstrip('-').isdigit(): continue
    y=int(y);p=ln[6:17].strip();t=ln[52:66].strip()
    if p: P[y]=float(p)
    if t: T[y]=float(t)
A,B=-398,800
def mov(D,w=31):
    h=w//2;o=[]
    for y in range(A,B+1):
        v=[D[k] for k in range(y-h,y+h+1) if k in D]
        o.append(round(S.mean(v),3) if len(v)==w else None)
    return o
ref=S.mean(P[y] for y in range(1901,2001))
cent=[]
for a in range(-300,700,100):
    ys=[y for y in range(a+1,a+101)] if a>=0 else [y for y in range(a,a+100)]
    cent.append({'a':a,'p':round(S.mean(P[y] for y in ys),1),'psd':round(S.pstdev([P[y] for y in ys]),1),'t':round(S.mean(T[y] for y in ys),2),'tsd':round(S.pstdev([T[y] for y in ys]),2),
                 'dry':sum(1 for y in ys if P[y]<150),'wet':sum(1 for y in ys if P[y]>250)})
per=[]
for nm,a,b in [('a',-300,250),('b',251,300),('c',301,400),('d',401,500),('e',501,550)]:
    ys=[y for y in range(a,b+1)]
    per.append({'k':nm,'a':a,'b':b,'p':round(S.mean(P[y] for y in ys),1),'psd':round(S.pstdev([P[y] for y in ys]),1),'t':round(S.mean(T[y] for y in ys),2)})
ex=sorted(range(-300,601),key=lambda y:P[y])
out={'A':A,'B':B,'P':[P.get(y) for y in range(A,B+1)],'T':[T.get(y) for y in range(A,B+1)],'Pm':mov(P),'Tm':mov(T),'ref':round(ref,1),'tref':round(S.mean(T[y] for y in range(1901,2001)),2),
     'cent':cent,'per':per,'dry5':[(y,P[y]) for y in ex[:5]],'wet5':[(y,P[y]) for y in ex[-5:][::-1]],
     'cold5':[(y,T[y]) for y in sorted(range(-300,601),key=lambda y:T[y])[:5]],'t536':[(y,T[y],P[y]) for y in range(534,546)]}
json.dump(out,open('data.json','w'))
for c in cent: print(c)
for c in per: print(c)
print(out['ref'],out['tref'],out['dry5'],out['wet5'],out['cold5']);print(out['t536'])
