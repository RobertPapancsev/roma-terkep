# v198: amfiteátrum-kártya. Forrás: S. Heath, roman-amphitheaters (GitHub, közkincs/Unlicense), roman-amphitheaters.geojson.
# Kimenet: imp_st/arena.json sorok: [x,y,név,latin név,ország,befogadóképesség|0,külső nagytengely|0,külső kistengely|0,korcsoport 0-5,láthatóság 0-4,típus 0-2]
import json, collections
from pyproj import Transformer
R='/home/claude/imperium/'
tg=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km',always_xy=True)
F=json.load(open('/home/claude/dl/heath/amph.geojson'))['features']
G={'republican':0,'caesarean':0,'augustan':1,'julio-claudian':1,'neronian':1,'first-century':2,'flavian':2,'late-first-century':2,
   'late-first-early-second-century':3,'trajanic':3,'hadrianic':3,'early-second-century':3,'second-century':3,'late-second-century':3,
   'severan':4,'third-century':4,'post-severan':4,'fourth-century':4,'imperial':5}
VIS={'good':0,'partial':1,'poor':2,'street-plan':3,'none':4}
rows=[];S=json.load(open(R+'imp_search.json'));far=[]
for f in F:
    p=f['properties'];lon,lat=f['geometry']['coordinates'][:2];x,y=tg.transform(lon,lat)
    cap=(p.get('capacity') or {}).get('quantity') or 0;d=p.get('dimensions') or {}
    lt=p.get('latintoponym');lt=lt if isinstance(lt,str) else ''
    bt=p['buildingtype'];ty=0 if bt=='amphitheater' else 1 if bt=='gallo-roman-amphitheater' else 2
    rows.append([round(x),round(y),p['label'],lt,p['moderncountry'],int(cap),d.get('exteriormajor') or 0,d.get('exteriorminor') or 0,G[p['chronogroup']],VIS[p['visibility']],ty])
    dm=min(((s[4]-x)**2+(s[5]-y)**2)**.5 for s in S if s[7] in('city','leg','civ','fort','set'))
    if dm>15: far.append((p['label'],round(dm),p['moderncountry']))
# v199: színházak és cirkuszok a Pleiades (CC BY 3.0) helytípusai alapján – csak római/késő antik korú, koordinátás tételek; típus 3 = színház, 4 = cirkusz/hippodrom
import gzip,csv; csv.field_size_limit(10**9)
nth=nci=0
for row in csv.DictReader(gzip.open('/home/claude/dl/pleiades/places.csv.gz','rt',encoding='utf-8')):
    ts=[t.strip() for t in (row.get('featureTypes') or '').split(',')];ks=row.get('timePeriodsKeys') or ''
    ty=3 if 'theatre' in ts else 4 if ('circus' in ts or 'hippodrome' in ts) else 0
    if row['title'].strip()=='Villa Maxentii': continue   # ugyanaz az építmény, mint a 'Circus of Maxentius'
    if not ty or not row['reprLat'] or not ('roman' in ks or 'late-antique' in ks): continue
    x,y=tg.transform(float(row['reprLong']),float(row['reprLat']))
    rows.append([round(x),round(y),row['title'].strip(),'','',0,0,0,5,5,ty,int(row['id'])])
    if ty==3: nth+=1
    else: nci+=1
rows.sort(key=lambda r:r[2])
AM=[r for r in rows if r[10]<3]
json.dump(rows,open(R+'imp_st/arena.json','w'),ensure_ascii=False,separators=(',',':'))
cn=collections.Counter(r[4] for r in rows if r[10]<3)
rows_all=rows;rows=AM
sm={'nth':nth,'nci':nci,'n':len(rows),'ncap':sum(1 for r in rows if r[5]),'ndim':sum(1 for r in rows if r[6]),'grp':[sum(1 for r in rows if r[8]==i) for i in range(6)],
    'countries':cn.most_common(8),'top':[[r[2],r[5]] for r in sorted(rows,key=lambda r:-r[5])[:10]],'sumcap':sum(r[5] for r in rows),
    'med':sorted(r[5] for r in rows if r[5])[sum(1 for r in rows if r[5])//2],'ty':[sum(1 for r in rows if r[10]==i) for i in range(3)],'vis':[sum(1 for r in rows if r[9]==i) for i in range(5)]}
json.dump(sm,open(R+'data/stats/arena_summary.json','w'),ensure_ascii=False)
print(sm);print('gazetteer-helytől >15 km:',far)
