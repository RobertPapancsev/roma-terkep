# Kimutatások adatai (v166): imp_stats.json
import json, math, pandas as pd, numpy as np
from pyproj import Transformer
R='/home/claude/imperium/'; D='/home/claude/dl/'
tg=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km',always_xy=True)
S=json.load(open(R+'imp_search.json'))
def P(lon,lat):
    x,y=tg.transform(lon,lat); return int(round(x)),int(round(y))
def G(name,mod=None):
    c=[s for s in S if s[0]==name and (mod is None or s[1]==mod)]
    if not c: raise SystemExit('nincs: %s %s'%(name,mod))
    return c[0][4],c[0][5]
OUT={}; ST={}
# 1. Városok (Hanson 2016)
c=pd.read_csv(D+'hanson/Cities.csv',encoding='latin-1'); a=pd.read_csv(D+'hanson/Areas.csv',encoding='latin-1')
m=c.merge(a,on='Primary Key',how='left')
cities=[]
for _,r in m.iterrows():
    x,y=P(r['Longitude (X)'],r['Latitude (Y)'])
    ar=None if pd.isna(r['Area']) else float(r['Area'])
    sd=r['Start Date']; sd=None if pd.isna(sd) or sd=='NULL' else int(float(sd))
    cities.append([x,y,ar,r['Ancient Toponym'],r['Province'],sd])
OUT['cities']=cities
ar=m['Area'].dropna()
bins=[0,10,20,50,100,200,5000]; lab=['<10','10–20','20–50','50–100','100–200','200+']
hist=pd.cut(ar,bins=bins,labels=lab,right=False).value_counts().reindex(lab).tolist()
top=m.dropna(subset=['Area']).sort_values('Area',ascending=False).head(12)[['Ancient Toponym','Area','Province']].values.tolist()
ST['cities']={'n':len(m),'na':int(ar.size),'hist':list(zip(lab,hist)),'top':top,'med':float(ar.median()),
  'gt100':int((ar>=100).sum())}
# tartományi régiók: nyugat/kelet (latin/görög) – egyszerű hosszúsági bontás nem jó; tartománylista
prov=m['Province'].value_counts().head(12).items(); ST['cities']['prov']=[[k,int(v)] for k,v in prov]
# 2. Légiók
L23=[  # Tacitus, Ann. 4.5 (Kr. u. 23): tartományonként; a jelölő a tartomány egyik fő táborhelye
 ['Germania Inferior',4,('Castra Vetera','Birten')],['Germania Superior',4,('Mogontiacum','Mainz')],
 ['Hispania',3,('Asturica Augusta','Astorga')],['Africa',2,('Ammaedara','Haïdra')],['Aegyptus',2,('Alexandria','Alexandria')],
 ['Syria',4,('Antiochia','Antakya')],['Pannonia',2,('Poetovio','Ptuj')],['Moesia',2,('Naissus','Niš')],['Dalmatia',2,('Burnum','Plavno Polje')]]
L220=[  # Cassius Dio 55.23–24 (kb. Kr. u. 220-as évek) + a táborhely a modern kutatás szerint
 ['II Augusta','Britannia Superior',('Isca','Caerleon')],['VI Victrix','Britannia Inferior',('Eburacum','York')],['XX Valeria Victrix','Britannia Superior',('Deva','Chester')],
 ['III Gallica','Phoenice',('Raphaneai','Rafniye')],['III Cyrenaica','Arabia',('Bostra','Busra ash-Sham')],['III Augusta','Numidia',('Lambaesis','Lambèse')],
 ['IV Scythica','Syria',('Zeugma','Belkis')],['V Macedonica','Dacia',('Potaissa','Turda')],['VI Ferrata','Iudaea (Syria Palaestina)',('Legio','Tel Megiddo')],
 ['VII Claudia','Moesia Superior',('Viminacium','Stari Kostolac')],['VIII Augusta','Germania Superior',('Argentorate','Strasbourg')],['X Gemina','Pannonia Superior',('Vindobona','Wien')],
 ['X Fretensis','Iudaea (Syria Palaestina)',('Ierusalem','Jerusalem')],['XI Claudia','Moesia Inferior',('Durostorum','Silistra')],['XII Fulminata','Cappadocia',('Melitene','Arslantepe')],
 ['XIII Gemina','Dacia',('Apulum','Alba Julia')],['XIV Gemina','Pannonia Superior',('Carnuntum','Bad Deutsch-Altenburg')],['XV Apollinaris','Cappadocia',('Satala','Satala')],
 ['XXII Primigenia','Germania Superior',('Mogontiacum','Mainz')],['I Italica','Moesia Inferior',('Novae','Svishtov')],['I Adiutrix','Pannonia',('Brigetio','Komárom-Szőny')],
 ['VII Gemina','Hispania',('Legio VII Gemina','León')],['II Adiutrix','Pannonia Inferior',('Aquincum Castra','Aquincum fortress')],['IV Flavia','Moesia Superior',('Singidunum','Beograd')],
 ['XVI Flavia','Syria',('Samosata','Samsat')],['I Minervia','Germania Inferior',('Bonna','Bonn')],['II Traiana','Aegyptus',('Alexandria','Alexandria')],
 ['XXX Ulpia','Germania Inferior',('Castra Vetera','Birten')],['II Italica','Noricum',('Lauriacum','Lorch')],['III Italica','Raetia',('Castra Regina','Regensburg')],
 ['I Parthica','Mesopotamia',('Singara','Balad Sinjar')],['III Parthica','Mesopotamia',(36.83,40.07,'Rhesaina')],['II Parthica','Italia',(41.73,12.66,'Albanum')]]
def gp(k):
    if len(k)==3: return P(k[1],k[0])
    try: return G(*k)
    except SystemExit:
        c=[s for s in S if s[0]==k[0]]
        if c: return c[0][4],c[0][5]
        raise
leg23=[[*gp(k),n,pr] for pr,n,k in L23]
leg220=[]
for nm,pr,k in L220:
    x,y=gp(k); leg220.append([x,y,nm,pr,k[-1] if len(k)==3 else k[0]])
OUT['leg23']=leg23; OUT['leg220']=leg220
json.dump({'leg':L220},open('stats/legions_src.json','w'),ensure_ascii=False)
# 3. Roncsok (Strauss / OxREP)
w=pd.read_excel(D+'wreck/w.xlsx')
w=w.dropna(subset=['Latitude','Longitude','Earliest Date','Latest Date'])
wr=[]; cent={}
for _,r in w.iterrows():
    e,l=int(r['Earliest Date']),int(r['Latest Date'])
    if l<e: e,l=l,e
    x,y=P(r['Longitude'],r['Latitude']); wr.append([x,y,e,l])
    span=max(1,l-e)
    for cc in range(-800,800,100):
        ov=max(0,min(l,cc+100)-max(e,cc))
        if ov>0: cent[cc]=cent.get(cc,0)+ov/span
OUT['wrecks']=wr
ST['wrecks']={'n':len(wr),'cent':[[k,round(v,1)] for k,v in sorted(cent.items()) if -800<=k<800]}
# 4. Éremkincsek (CHRE)
h=pd.read_csv(D+'chre/all.csv',low_memory=False,usecols=['latitude','longitude','terminalYear1','terminalYear2','coinCount','hoardType'])
h=h[h.hoardType.isin(['Hoard','Hoard?'])].dropna(subset=['latitude','longitude','terminalYear1'])
ho=[]; dec={}
for _,r in h.iterrows():
    t=int(r['terminalYear1']); x,y=P(r['longitude'],r['latitude'])
    n=None if pd.isna(r['coinCount']) else int(r['coinCount'])
    ho.append([x,y,t,n]); d10=(t//10)*10; dec[d10]=dec.get(d10,0)+1
OUT['hoards']=ho
ST['hoards']={'n':len(ho),'dec':[[k,v] for k,v in sorted(dec.items()) if -100<=k<=420]}
# 5. Feliratok (LIST) – 100 km-es rács, időszakonként
d=pd.read_parquet(D+'list/LIST_v1-2.parquet',columns=['Longitude','Latitude','not_before','not_after'])
d=d.dropna(subset=['Longitude','Latitude'])
X,Y=tg.transform(d.Longitude.values,d.Latitude.values)
d['x']=X; d['y']=Y; CELL=100
d['cx']=np.floor(d.x/CELL).astype(int); d['cy']=np.floor(d.y/CELL).astype(int)
def grid(sub):
    g=sub.groupby(['cx','cy']).size()
    return [[int(i)*CELL+CELL//2,int(j)*CELL+CELL//2,int(n)] for (i,j),n in g.items() if n>=5]
per={'all':grid(d)}
dd=d.dropna(subset=['not_before','not_after']).copy(); dd=dd[(dd.not_after-dd.not_before)<=100]; dd['mid']=(dd.not_before+dd.not_after)/2
PER=[('p1',-100,0),('p2',0,100),('p3',100,200),('p4',200,300),('p5',300,500)]
for k,a,b in PER: per[k]=grid(dd[(dd.mid>=a)&(dd.mid<b)])
OUT['insc']=per
cnt={k:int(((dd.mid>=a)&(dd.mid<b)).sum()) for k,a,b in PER}
# évtized-hisztogram
q={}
nb=dd.not_before.values; na=dd.not_after.values
for a in range(-100,500,25):
    ov=np.clip(np.minimum(na,a+25)-np.maximum(nb,a),0,None); sp=np.maximum(na-nb,1)
    q[a]=float((ov/sp).sum())
ST['insc']={'n':int(len(d)),'ndated':int(len(dd)),'per':cnt,'q25':[[k,round(v)] for k,v in q.items()]}
# 6. Nikaia 325 – a Gelzer-féle lista tartományonként (fourthcentury.com)
NIC=[['Hispania',1,('Corduba','Córdoba')],['Róma (2 pap)',2,'Roma'],['Aegyptus',13,('Alexandria','Alexandria')],['Thebais',2,('Antinoopolis',"Esch-Scheich 'Abada")],
 ['Libya Superior',4,(32.82,21.86,'Cyrene')],['Libya Inferior',1,(31.35,27.24,'Paraetonium')],['Palaestina',19,('Caesarea','Caesarea')],['Phoenice',10,(33.27,35.2,'Tyrus')],
 ['Coele-Syria',22,('Antiochia','Antakya')],['Arabia',6,('Bostra','Busra ash-Sham')],['Mesopotamia',4,('Edessa','Şanlıurfa')],['Persia',1,(33.09,44.58,'Seleucia-Ctesiphon')],
 ['Cilicia',10,('Tarsus','Gözlü Kule')],['Cappadocia',10,('Caesarea','Kayseri')],['Armenia Minor',4,('Satala','Satala')],['Armenia Maior',5,(40.0,44.5,'Armenia')],
 ['Pontus Polemoniacus',3,(40.6,37.0,'Neocaesarea')],['Paphlagonia',3,(41.4,33.8,'Pompeiopolis')],['Galatia',5,('Ancyra','Ankara')],['Asia',7,('Ephesos','Efes')],
 ['Lydia',9,('Sardis','Sart')],['Phrygia',8,('Laodicea ad Lycum','Eskihisar')],['Pisidia',12,(38.31,31.19,'Antiochia Pisidiae')],['Lycia',1,('Patara','Gelemiş')],
 ['Pamphylia',7,('Perge','Aksu')],['Szigetek',4,('Rhodos','Rhodos')],['Caria',5,(37.71,28.72,'Aphrodisias')],['Isauria',18,('Seleucia ad Calycadnum','Silifke')],
 ['Cyprus',2,(35.18,33.9,'Salamis')],['Bithynia',11,('Nicomedia','İzmit')],['Europa',1,('Perinthus','Marmara Ereğlisi Adliyesi')],['Dacia',1,('Serdica','Sofia')],
 ['Calabria',1,(40.6,17.0,'Calabria')],['Moesia',1,(43.22,27.6,'Marcianopolis')],['Africa',1,('Carthago','Carthago')],['Macedonia',2,(40.64,22.94,'Thessalonica')],
 ['Dardania',1,(42.65,21.2,'Dardania')],['Achaia',3,('Athenae','Athína')],['Thessalia',2,('Larissa','Larissa')],['Dalmatia',1,('Salona','Solin')],
 ['Pannonia',1,('Sirmium','Sremska Mitrovica')],['Galliae',1,(44.09,6.24,'Dinia')],['Gothia',1,(46.0,29.5,'Gothia')],['Bosporus',1,(45.35,36.47,'Panticapaeum')]]
nic=[]
for pr,n,k in NIC:
    if k=='Roma': x,y=G('Roma')
    else: x,y=gp(k)
    nic.append([x,y,n,pr])
OUT['nic']=nic; ST['nic']={'n':sum(n for _,n,_ in NIC)}
# 7. Bányák (Wilson 2025, OxREP Mines 3.0)
m=pd.read_excel(D+'mines/m.xlsx',0).dropna(subset=['latitude','longitude'])
MET=['metalMinedGold','metalMinedSilver','metalMinedLead','metalMinedCopper','metalMinedTin','metalMinedIron','metalMinedMercuryCinnabar','metalMinedZinc']
def yes(v): return str(v).strip().upper() in ('TRUE','1','1.0')
mi=[]; cnt=[0]*8; prov={}; acc=[]
for _,r in m.iterrows():
    mask=sum(1<<i for i,c in enumerate(MET) if yes(r[c]))
    for i in range(8):
        if mask>>i&1: cnt[i]+=1
    x,y=P(r['longitude'],r['latitude']); pv=str(r['province']) if pd.notna(r['province']) else ''
    prov[pv]=prov.get(pv,0)+1
    nm=str(r['site']).strip(); an=str(r['ancientName']).strip() if pd.notna(r['ancientName']) else ''
    mi.append([x,y,mask,nm,pv,an])
OUT['mines']=mi
ST['mines']={'n':len(mi),'met':cnt,'prov':sorted(prov.items(),key=lambda t:-t[1])[:12],
  'dated':int(m[['notBeforeOpeningDate','notAfterClosingDate']].notna().any(axis=1).sum()),'nomask':sum(1 for r in mi if r[2]==0)}
# 8. Klíma-események (McCormick és mtsai 2012, DARMC 2012-1)
c=pd.read_excel(D+'maps/climate.xlsx',1).dropna(subset=['Latitude 1','Longtitude 1','When 1'])
cl=[];cc={}
for _,r in c.iterrows():
    y1=int(r['When 1']); y2=int(r['When 2']) if pd.notna(r['When 2']) else y1
    code=str(r['What-code']).strip(); code={'very bad':'q'}.get(code,code)
    x,y=P(r['Longtitude 1'],r['Latitude 1'])
    cl.append([x,y,y1,y2,code,str(r['Where']).strip() if pd.notna(r['Where']) else '',str(r['What']).strip()[:90] if pd.notna(r['What']) else ''])
    b=(y1//100)*100; cc[b]=cc.get(b,0)+1
OUT['clim']=cl
from collections import Counter
ST['clim']={'n':len(cl),'cent':sorted([[k2,v] for k2,v in cc.items() if -100<=k2<800]),'types':Counter(r[4] for r in cl).most_common()}
# 9. Járványok 312–749 (Harper–McCormick–More–Eliason 2017, DARMC 2017-2)
e=pd.read_excel(D+'maps/epi.bin',1).dropna(subset=['DECLAT','DECLONG','DATE_1'])
ep=[];ev={}
for _,r in e.iterrows():
    x,y=P(r['DECLONG'],r['DECLAT']); d1=int(r['DATE_1']); d2=int(r['DATE_2']) if pd.notna(r['DATE_2']) and str(r['DATE_2']).strip().lstrip('-').isdigit() else d1
    c1=str(r['CODE_1']).strip().rstrip('?')
    ep.append([x,y,d1,d2,c1,str(r['WHERE']).strip()])
    ev.setdefault((d1//25)*25,set()).add(r['EVENT_ID'])
OUT['epi']=ep
ST['epi']={'n':len(ep),'nev':int(e.EVENT_ID.nunique()),'q25':sorted([[k2,len(v)] for k2,v in ev.items()]),'types':Counter(r[4] for r in ep).most_common()}
# 10. Búzaár Egyiptomban (Harper 2016, DARMC 2016-5, 5. munkalap)
pz=pd.read_excel(D+'maps/prices.xlsx','5');pz.columns=['y','g'];pz=pz.dropna()
pz['b']=(pz.y//50*50).astype(int)
ST['wheat']={'n':len(pz),'b50':[[int(b),round(float(g.median()),1),int(len(g))] for b,g in pz.groupby('b').g]}
# 11. ORBIS: utazási idő Rómába/Rómából (Scheidel–Meeks, Stanford; CC BY 3.0 / MIT)
import csv
OS={r['id']:r for r in csv.DictReader(open(D+'orbis/orbis_v2/sites.csv',encoding='utf8'))}
def oc(f): return {r['target']:float(r['cost']) for r in csv.DictReader(open(D+'orbis/'+f)) if float(r['cost'])>=0}
TJ,TN,FJ=oc('to_fast_jul.csv'),oc('to_fast_jan.csv'),oc('from_fast_jul.csv')
ob=[]
for i,sv in OS.items():
    if i not in TJ and i not in TN and i not in FJ: continue
    if sv['label'] in ('Roma',): continue
    x,y=P(float(sv['x']),float(sv['y'])); g=lambda d: round(d[i],1) if i in d else None
    ob.append([x,y,sv['label'],g(TJ),g(TN),g(FJ)])
OUT['orbis']=ob
def band(v): return 0 if v<5 else 1 if v<10 else 2 if v<20 else 3 if v<30 else 4
ST['orbis']={'n':len(ob),'bands':{k2:[sum(1 for r in ob if r[j] is not None and band(r[j])==b) for b in range(5)] for k2,j in (('tj',3),('tn',4),('fj',5))},
  'ex':{n:[r[3],r[4],r[5]] for r in ob for n in ('Londinium','Alexandria','Antiochia','Aquincum','Carthago','Constantinopolis','Gades','Ierusalem','Lugdunum') if r[2]==n}}
# 12. Papiruszok és osztrakonok (HGV / papyri.info, CC BY 3.0)
import gzip
PL={}
for r in csv.DictReader(gzip.open(D+'pleiades/places.csv.gz','rt',encoding='utf8')):
    if r['reprLat'] and r['reprLong']: PL[r['id']]=(float(r['reprLong']),float(r['reprLat']),r['title'])
H=json.load(open(D+'hgv/hgv.json'))
def per(m): return 0 if m<-30 else 1 if m<284 else 2 if m<641 else 3
pa={}; q={}; nd=0; nloc=0
for pid,nm,nb,na in H:
    mid=None
    if nb is not None and na is not None and na>=nb and na-nb<=100:
        mid=(nb+na)/2; nd+=1; span=max(1,na-nb)
        for b in range(-350,1000,25):
            ov=max(0,min(na+1,b+25)-max(nb,b))
            if ov>0: q[b]=q.get(b,0)+ov/max(1,na-nb+1)
    if pid and pid in PL:
        nloc+=1; e=pa.setdefault(pid,[0,0,0,0,0])
        e[0]+=1
        if mid is not None and -350<=mid<1000: e[1+per(mid)]+=1
pap=[]
for pid,e in pa.items():
    lo,la,ti=PL[pid]; x,y=P(lo,la); pap.append([x,y,ti]+e)
OUT['pap']=pap
ST['pap']={'n':len(H),'nloc':nloc,'nplaces':len(pap),'ndated':nd,'q25':[[b,round(v)] for b,v in sorted(q.items()) if -350<=b<850],
  'top':sorted([[r[2],r[3]] for r in pap],key=lambda t:-t[1])[:12],'per':[sum(r[4+i] for r in pap) for i in range(4)]}
# 13. Kikötők (de Graauw, Ancient Ports; DARMC 2013-2, CC BY 4.0) – csak római kori (Ro = X)
po=pd.read_excel(D+'ports/AncientPorts.xlsx','PLACES')
po=po[po['Ro'].astype(str).str.strip()=='X'].dropna(subset=['LATITUDE','LONGITUDE'])
X1=lambda v: str(v).strip()=='X'
BITS=[('a',lambda r: str(r['AM']).strip()=='a'),('re',lambda r: str(r['RE']).strip() in ('r','rs')),('rs',lambda r: str(r['RE']).strip()=='rs'),
      ('bw',lambda r: X1(r['BW'])),('qu',lambda r: X1(r['QU'])),('ph',lambda r: X1(r['PH'])),('fp',lambda r: X1(r['FP'])),('vm',lambda r: X1(r['VM'])),
      ('si',lambda r: X1(r['SI'])),('ho',lambda r: X1(r['HO'])),('sh',lambda r: X1(r['SH'])),('sy',lambda r: X1(r['SY'])),('ps',lambda r: X1(r['PS']))]
pt=[];pc=[0]*len(BITS)
for _,r in po.iterrows():
    m=0
    for i,(kk,f) in enumerate(BITS):
        if f(r): m|=1<<i; pc[i]+=1
    nm=str(r['NAME']).strip() if pd.notna(r['NAME']) else ''
    md=str(r['NAME_MOD']).strip() if pd.notna(r['NAME_MOD']) else ''
    if len(md)>60: md=md[:57].rsplit(' ',1)[0]+'…'
    if nm and len(nm)>40: nm=nm[:38].rsplit(',',1)[0]
    x,y=P(float(r['LONGITUDE']),float(r['LATITUDE'])); pt.append([x,y,nm,'' if nm else md[:40],m])
OUT['ports']=pt
ST['ports']={'n':len(pt),'cnt':dict(zip([b[0] for b in BITS],pc))}
import os
os.makedirs(R+'imp_st',exist_ok=True)
for kk,vv in OUT.items(): json.dump(vv,open(R+'imp_st/'+kk+'.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump(ST,open('stats/summary.json','w'),ensure_ascii=False,indent=0)
print({kk:os.path.getsize(R+'imp_st/'+kk+'.json')//1024 for kk in OUT}); print(json.dumps(ST,ensure_ascii=False)[:3000])
