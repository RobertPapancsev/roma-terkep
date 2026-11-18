# v186: Büntgen et al. 2011 közép-európai nyári klíma (NOAA WDS Paleo) -> imp_st nélküli kártya-adat (stats/clim2_summary.json)
import re, json, pandas as pd, numpy as np
R='/home/claude/imperium/'
L=open(R+'data/clim/buentgen2011europe.txt',encoding='latin-1').read().split('\n')
i=[k for k,l in enumerate(L) if l.startswith('Year   PrecipAMJ')][0]; rows=[]
for l in L[i+1:]:
    if not l.strip(): break
    rows.append(l)
def f(s):
    s=s.strip(); return float(s) if s else np.nan
D=pd.DataFrame([[int(l[0:6]),f(l[6:17]),f(l[52:63])] for l in rows],columns=['y','p','t']).set_index('y')
D=D.loc[-500:800]
sm=D.rolling(31,center=True,min_periods=21).mean()
out={'y0':-500,'y1':800,'t':[None if np.isnan(v) else round(v,2) for v in D.t],'p':[None if np.isnan(v) else round(v,1) for v in D.p],
     'ts':[None if np.isnan(v) else round(v,3) for v in sm.t],'ps':[None if np.isnan(v) else round(v,1) for v in sm.p]}
per=lambda a,b,c: round(float(D.loc[a:b,c].mean()),2)
S={'tR':per(1,250,'t'),'tL':per(250,550,'t'),'pR':per(1,250,'p'),'pL':per(250,550,'p'),'pRep':per(-300,-1,'p'),'tRep':per(-300,-1,'t'),
   'sdR':round(float(D.loc[1:250,'t'].std()),2),'sdL':round(float(D.loc[250:550,'t'].std()),2),'psdR':round(float(D.loc[1:250,'p'].std()),1),'psdL':round(float(D.loc[250:550,'p'].std()),1),
   'tmin':[int(D.loc[1:800,'t'].idxmin()),round(float(D.loc[1:800,'t'].min()),2)],'p0':int(D.p.first_valid_index()),'pmean_all':round(float(D.p.mean()),1)}
json.dump(out,open(R+'imp_st/clim2.json','w'),separators=(',',':'))
json.dump(S,open(R+'data/stats/clim2_summary.json','w'),indent=1); print(S)
