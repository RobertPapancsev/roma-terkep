# v203: csata-kártya. Forrás: Wikidata (CC0), SPARQL-lekérdezés 2026-11-16 (/home/claude/dl/battles/q2.rq): csata / ostrom / tengeri csata típusú, koordinátás,
# Kr. e. 510 – Kr. u. 500 közé keltezett tételek; szűrés (filt.py): angol Wikipédia-szócikkel rendelkezik, és a résztvevők / a háború / a leírás alapján római vonatkozású.
# Kézzel kizárva: nem római vonatkozású vagy hibás tételek (EXC). Kimenet: imp_st/battles.json sorok: [x,y,név_en,név_hu,év,típus 0-2,korszak 0-4,háború_en,Q-azonosító,hu wiki? 0/1]
import sys, json, collections; sys.path.insert(0,'/home/claude/dl/battles')
from filt import keep
from pyproj import Transformer
R='/home/claude/imperium/'
tg=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km',always_xy=True)
EXC={('Siege of Tauromenium',-394),('Battle of the Strait of Messina',-276),('Siege of Lilybaeum',-276),('Battle of Leontion',-217),('First Battle of Lamia',-209),('Second Battle of Lamia',-209),
 ('Battle of Mantinea',-207),('Battle of the River Amnias',-89),('Battle of Magetobria',-63),('Battle of Hormozdgan',224),('Battle of the Tanais River',373),('Battle of Guoloph',437),('Battle of Avarayr',451),
 ('Battle of Nedao',454),('Battle of Órbigo',456),('Battle of Bolia',469),('Battle of Isonzo',489),('Battle of Badon',500),('Battle of the Utus',477),('Battles of Bedriacum',69),("Ambiorix's Revolt",-54)}
TY={'Q178561':0,'Q188055':1,'Q1261499':2}
def per(y): return 0 if y<-264 else 1 if y<-133 else 2 if y<-30 else 3 if y<285 else 4
rows=[];exc=0
for k in keep:
    if (k['en'],k['y']) in EXC: exc+=1;continue
    x,y=tg.transform(k['lon'],k['lat']);po=k['po'].split('|')[0]
    rows.append([round(x),round(y),k['en'],k['hu'],k['y'],TY[k['t']],per(k['y']),po,k['q'],1 if k['hw'] else 0])
json.dump(rows,open(R+'imp_st/battles.json','w'),ensure_ascii=False,separators=(',',':'))
b=collections.Counter((r[4]//50)*50 for r in rows);wars=collections.Counter(r[7] for r in rows if r[7])
sm={'n':len(rows),'exc':exc,'ty':[sum(1 for r in rows if r[5]==i) for i in range(3)],'per':[sum(1 for r in rows if r[6]==i) for i in range(5)],'tl':[[a,b.get(a,0)] for a in range(-500,500,50)],'wars':wars.most_common(14),'nhu':sum(r[9] for r in rows)}
json.dump(sm,open(R+'data/stats/battles_summary.json','w'),ensure_ascii=False);print(sm)
