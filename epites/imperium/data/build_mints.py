# v200: pénzverde-kártya. Forrás: Nomisma.org SPARQL-lekérdezés (2026-11-12): típusok száma verdénként a Roman Imperial Coinage (OCRE) és a Roman Republican Coinage (CRRO) szerint,
# a verde első és utolsó katalogizált típusának évével; koordináta: a Nomisma verde-rekordjához kapcsolt Pleiades-hely.
# Kimenet: imp_st/mints2.json sorok: [x,y,név,RIC-típus,RRC-típus,első év,utolsó év]
import csv, gzip, json, collections
from pyproj import Transformer
csv.field_size_limit(10**9)
R='/home/claude/imperium/';N='/home/claude/dl/nomisma/'
tg=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km',always_xy=True)
M={r['m']:r for r in csv.DictReader(open(N+'mints.csv'))}
PL={}
for row in csv.DictReader(gzip.open('/home/claude/dl/pleiades/places.csv.gz','rt',encoding='utf-8')):
    if row['reprLat']: PL[row['id']]=(float(row['reprLong']),float(row['reprLat']))
agg={};unl=collections.Counter()
for r in csv.DictReader(open(N+'types.csv')):
    s=r['src'][-3:]
    if r['src'][-4:] not in('/ric','/rrc'): continue
    m=M.get(r['m']);pid=(m or {}).get('p','').rstrip('/').split('/')[-1]
    if not m or pid not in PL: unl[s]+=int(r['n']);continue
    # az „… comitatensian mint” rekordokat az anyaverdéhez vonjuk
    key=pid
    a=agg.setdefault(key,{'l':m['l'].replace(' comitatensian mint',''),'ric':0,'rrc':0,'s':9999,'e':-9999,'xy':PL[pid],'nd':0})
    if 'comitatensian' not in m['l']: a['l']=m['l']
    a[s]+=int(r['n'])
    if r['s0']: a['s']=min(a['s'],int(r['s0']));a['e']=max(a['e'],int(r['e1']))
    else: a['nd']=1   # ennél a sornál a lekérdezés nem adott keltezést
rows=[]
for a in agg.values():
    x,y=tg.transform(*a['xy']);rows.append([round(x),round(y),a['l'],a['ric'],a['rrc']]+([None,None] if a['nd'] else [a['s'],a['e']]))
# v206: a négy hiányzó/hibás keltezés pótlása külön Nomisma-lekérdezésből (2026-11-16, típusonkénti nmo:hasStartDate / hasEndDate, forrás: RIC):
#   Róma RIC: Kr. e. 19 – Kr. u. 491 (40 típus keltezetlen); RRC-vel együtt Kr. e. 280-tól. Mediolanum: 249–491. Köln: 260–274.
#   Trier: 293–455; egyetlen, Kr. u. 1–14-re keltezett típust (a korábbi „Kr. u. 1” oka) kiugró adatként nem veszünk figyelembe.
OVR={'Rome':(-280,491),'Mediolanum':(249,491),'Cologne':(260,274),'Trier':(293,455)}
for r in rows:
    if r[2] in OVR: r[5],r[6]=OVR[r[2]]
rows.sort(key=lambda r:-(r[3]+r[4]))
json.dump(rows,open(R+'imp_st/mints2.json','w'),ensure_ascii=False,separators=(',',':'))
tot=sum(r[3]+r[4] for r in rows)
cent=[]
sm={'n':len(rows),'tot':tot,'ric':sum(r[3] for r in rows),'rrc':sum(r[4] for r in rows),'unl':dict(unl),'rome':rows[0][3]+rows[0][4],'top':[[r[2],r[3]+r[4],r[5],r[6]] for r in rows[1:16]],'cent':cent,
    'nodate':[r[2] for r in rows if r[5] is None],'pann':[[r[2],r[3]+r[4],r[5],r[6]] for r in rows if r[2] in('Siscia','Sirmium','Carnuntum','Vindobona')]}
json.dump(sm,open(R+'data/stats/mints2_summary.json','w'),ensure_ascii=False)
print(sm)

