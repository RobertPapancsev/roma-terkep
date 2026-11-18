# Amfora-kártya adatai (v184): imp_st/amph.json + stats/amph_summary.json
# Forrás: Blumenkranz–Brughmans–Carreras, west_roman_amphorae (GitHub, MIT); Carreras et al., Antiquity 2026 (CC BY 4.0)
import json, math, pandas as pd
from pyproj import Transformer
R='/home/claude/imperium/'
tg=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km',always_xy=True)
d=pd.read_excel(R+'data/amph/west_roman_amphorae_data.xlsx')
# Koordináta-javítások: a forrásban tizedesjel-hibák vannak (szélesség ×10^6, hosszúság ×10)
FIX={}
def fix(r):
    lat,lon=r.Latitude,r.Longitude
    if lat>1000: lat=lat/1e6
    if lon>20 and r['Early Imperial province'] in ('Belgica','Germania Inferior'): lon=lon/10
    return lat,lon
d[['lat','lon']]=d.apply(lambda r: pd.Series(fix(r)),axis=1)
# Vienne (Lugdunensis/Lyonese körzet) a forrásban Bécs koordinátáival szerepel -> Vienne, Franciaország
d.loc[d.site_h1=='Vienne',['lat','lon']]=[45.525,4.874]
# Westgate Milecastle (Hadrianus-fal, Newcastle): előjelhiba (keleti hosszúság helyett nyugati)
d.loc[d.site_h1=='Westgate Milecastle','lon']=-d.loc[d.site_h1=='Westgate Milecastle','Longitude'].abs()
DROP={'Les Bonnettes','Actiparc'}   # bizonytalan hely: a szélesség sem illik a tartományhoz (Arras környéki lelőhelyek)
CHG=sorted(set(d[(d.lat.round(5)!=d.Latitude.round(5))|(d.lon.round(5)!=d.Longitude.round(5))].site_h1)-DROP)
CK={'wine':0,'olive-oil':1,'garum':2,'dates':3,'olives':3}
sites=[]
for s,g in d.groupby('site_h1'):
    if s in DROP: continue
    lat,lon=g.lat.iloc[0],g.lon.iloc[0]
    x,y=tg.transform(lon,lat)
    by=[0,0,0,0]
    for _,r in g.iterrows(): by[CK[r.contents]]+=float(r.frequency_density)
    tot=sum(by); dom=max(range(4),key=lambda i:by[i])
    types=[t.strip() for t in g.sort_values('frequency_density',ascending=False).amphora_type.tolist()]
    sites.append([int(round(x)),int(round(y)),s.strip(),g['Early Imperial province'].iloc[0],[round(v,1) for v in by],dom,len(types),types[:4]])
# évszázadonkénti megoszlás (a típus gyártási idején egyenletesen elosztva)
C=list(range(-100,600,100)); cent={c:[0,0,0,0] for c in C}
for _,r in d.iterrows():
    L,U=int(r.Lower_date_type),int(r.Upper_date_type); span=max(1,U-L); k=CK[r.contents]
    for c in C:
        ov=max(0,min(U,c+100)-max(L,c))
        if ov: cent[c][k]+=r.frequency_density*ov/span
# a Caesaraugusta nélkül is (a legnagyobb egyedi súly), ellenőrzéshez
cent2={c:[0,0,0,0] for c in C}
for _,r in d[d.site_h1!='Caesaraugusta'].iterrows():
    L,U=int(r.Lower_date_type),int(r.Upper_date_type); span=max(1,U-L); k=CK[r.contents]
    for c in C:
        ov=max(0,min(U,c+100)-max(L,c))
        if ov: cent2[c][k]+=r.frequency_density*ov/span
sh=lambda v:[round(100*a/sum(v),1) if sum(v) else 0 for a in v]
json.dump(sites,open(R+'imp_st/amph.json','w'),ensure_ascii=False,separators=(',',':'))
S={'nrows':len(d),'nsites':d.site_h1.nunique(),'nmap':len(sites),'ntypes':d.amphora_type.nunique(),
   'prov':d.groupby('Early Imperial province').site_h1.nunique().sort_values(ascending=False).to_dict(),
   'dom':[sum(1 for s in sites if s[5]==i) for i in range(4)],
   'cent':{c:[round(v) for v in cent[c]] for c in C},'share':{c:sh(cent[c]) for c in C},'share_noCA':{c:sh(cent2[c]) for c in C},'cent_noCA':{c:[round(v) for v in cent2[c]] for c in C},
   'nfix':len(CHG),'fix':CHG,'drop':sorted(DROP),'tot':[round(sum(s[4][i] for s in sites)) for i in range(4)]}
json.dump(S,open(R+'data/stats/amph_summary.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(S,ensure_ascii=False))
