# v185: RAAD (Germania, Franconi et al. 2023) és Sonata (Itália, Komar et al. 2025) amfora-kártyák adatai
import json, math, re, pandas as pd
from pyproj import Transformer
R='/home/claude/imperium/'
tg=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km',always_xy=True)
P=lambda lon,lat:[int(round(v)) for v in tg.transform(lon,lat)]
SUM={}
# ---------- RAAD ----------
r=pd.read_csv(R+'data/raad/RAAD_data_restructured.csv')
MOJI={'¸':'ü','ˆ':'ö','ﬂ':'ß'}
def nm(s):
    if not isinstance(s,str): return ''
    for a,b in MOJI.items(): s=s.replace(a,b)
    return ' '.join(w if w in ('i','ii','a','b','de','bei','aan','den','fer') else w[:1].upper()+w[1:] for w in s.split(' ')).replace('Kops Plateau','Kops-plateau').replace("L'homme De Fer","L’Homme de Fer")
OR={'gaul':0,'iberianpeninsula':1,'unknown(iberianpeninsula)':1,'italy':2,'em':3,'northafrica':4,'germania':5,'raetia':5}
CT=lambda c:0 if c=='wine' else 1 if c in('olive oil','olive oil?') else 2 if c=='fish sauce' else 3
ST={'military':0,'settlement':1,'settlement/ military':1,'villa':2}
r['loc']=r.lat.round(3).astype(str)+'_'+r.long.round(3).astype(str)
locs=[]
for lk,g in r.groupby('loc',sort=False):
    asm=[]
    for sn,a in g.groupby('site_number'):
        q=a.quantification_abbreviation.iloc[0]
        ct=[0,0,0,0]
        for _,x in a.iterrows(): ct[CT(x.contents)]+=x.frequency
        orr=[0]*6
        for t,b in a.groupby('RAAD_type_number'):
            o=OR.get(b.origin_h1.iloc[0]); 
            if o is not None: orr[o]+=1
        asm.append({'n':nm(a.site_name_modern.iloc[0]),'an':nm(a.site_name_ancient.iloc[0]) if isinstance(a.site_name_ancient.iloc[0],str) else '',
            't':a.major_site_type.iloc[0],'p':a.roman_province.iloc[0].title(),'d':[int(a.site_start_date.iloc[0]),int(a.site_end_date.iloc[0])],'q':q,'nt':int(a.RAAD_type_number.nunique()),'f':int(a.frequency.sum()),'ct':ct,'or':orr})
    lat,lon=g.lat.iloc[0],g.long.iloc[0]
    st=sorted({ST[a['t']] for a in asm}); stc=st[0] if len(st)==1 else 1
    if 'settlement/ military' in g.major_site_type.values: stc=1
    orl=[0]*6
    for t,b in g.groupby('RAAD_type_number'):
        o=OR.get(b.origin_h1.iloc[0])
        if o is not None: orl[o]+=1
    locs.append([*P(lon,lat),stc,int(g.RAAD_type_number.nunique()),orl,[[a['n'],a['an'],a['t'],a['p'],a['d'],a['q'],a['nt'],a['f'],[round(100*v/max(1,sum(a['ct']))) for v in a['ct']]] for a in asm]])
json.dump(locs,open(R+'imp_st/raad.json','w'),ensure_ascii=False,separators=(',',':'))
# hőtérkép: helyek száma, ahol az adott eredetű amfora jelen van 50 éves szakaszonként
B=list(range(-100,450,50)); H=[[0]*len(B) for _ in range(6)]
for lk,g in r.groupby('loc'):
    for o in range(6):
        gg=g[g.origin_h1.map(lambda v:OR.get(v))==o]
        for j,b in enumerate(B):
            e=b+50
            ok=((gg.site_start_date<e)&(gg.site_end_date>b)&(gg.raad_type_start_date.isna()|((gg.raad_type_start_date<e)&(gg.raad_type_end_date>b)))).any()
            if ok: H[o][j]+=1
SUM['raad']={'nasm':int(r.site_number.nunique()),'nloc':len(locs),'nform':int(r.RAAD_type_number.nunique()),'nrow':len(r),'B':B,'H':H,
  'q':r.groupby('quantification_abbreviation').site_number.nunique().to_dict(),'st':r.groupby('major_site_type').site_number.nunique().to_dict(),
  'prov':r.groupby('roman_province').site_number.nunique().to_dict()}
# ---------- Sonata ----------
s=pd.read_csv(R+'data/sonata/Sonata_data.csv')
s=s[s.Frequency.notna()&s.Lower_context_date.notna()].copy()
s['Longitude']=s.Longitude.astype(object); s.loc[s.Site=='porto maurizio, liguria','Longitude']='8.019'   # Excel-dátummá torzult hosszúság
s['Latitude']=s.Latitude.astype(float); s['Longitude']=s.Longitude.astype(float)
s.loc[s.Grouped_sites=='altinum','Latitude']=45.546; s.loc[s.Grouped_sites=='altinum','Longitude']=12.395   # a forrásban a pannoniai Altinum (Kölked) koordinátája
GN={'roma':'Roma','milan':'Milano','naples':'Napoli','padova':'Padova','scopietto':'Scoppieto','cuma':'Cuma','roma-suburbium':'Roma, suburbium'}
CS=lambda c:0 if c=='wine' else 1 if c=='olive oil' else 2 if c=='fish sauce' else 3
son=[]
for gname,g in s.groupby('Grouped_sites',sort=False):
    ct=[0,0,0,0]
    for _,x in g.iterrows(): ct[CS(x.content)]+=x.Frequency
    lat,lon=g.Latitude.median(),g.Longitude.median()
    nmn=GN.get(gname,' '.join(w[:1].upper()+w[1:] for w in gname.split(' ')).replace('Di ','di ').replace('Dei ','dei '))
    son.append([*P(lon,lat),nmn,g.Tyrrhenian_vs_Adriatic.iloc[0].split(',')[0],[int(v) for v in ct],max(range(4),key=lambda i:ct[i]),int(g.Site.nunique()),int(g.Amphora_type_merged.nunique()),
                [int(g.Lower_context_date.min()),int(g.Upper_context_date.max())],sorted({t for t in g.Site_type})])
json.dump(son,open(R+'imp_st/sonata.json','w'),ensure_ascii=False,separators=(',',':'))
C=list(range(-400,700,100)); cen={c:[0.0]*4 for c in C}
for _,x in s.iterrows():
    L,U=x.Lower_context_date,x.Upper_context_date; sp=max(1,U-L); k=CS(x.content)
    for c in C:
        ov=max(0,min(U,c+100)-max(L,c))
        if ov: cen[c][k]+=x.Frequency*ov/sp
SUM['son']={'nsite':int(s.Site.nunique()),'ngroup':len(son),'nfr':int(s.Frequency.sum()),'ntype':int(s.Amphora_type_merged.nunique()),
  'cent':{c:[round(v) for v in cen[c]] for c in C},'tot':[int(sum(o[4][i] for o in son)) for i in range(4)]}
json.dump(SUM,open(R+'data/stats/amph2_summary.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(SUM,ensure_ascii=False)[:3000]); print(len(locs),len(son))
