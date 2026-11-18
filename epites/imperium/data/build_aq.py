# v202: vízvezetékek és csatornák nyomvonala. Forrás: Ancient World Mapping Center (AWMC) geodata – aqueducts, canals (a Barrington Atlas alapján rajzolt vonalak; ODbL).
import json, warnings; warnings.filterwarnings('ignore')
from shapely.geometry import shape
from pyproj import Transformer
R='/home/claude/imperium/';A='/home/claude/awmc/geodata/Cultural-Data/'
P4=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km +ellps=WGS84',always_xy=True)
out={};st={}
for k,f in (('a','aqueducts/aqueducts.geojson'),('k','canals/canals.geojson')):
    out[k]=[];km=0;n=0
    for ft in json.load(open(A+f))['features']:
        if not ft['geometry']: continue
        g=shape(ft['geometry']);n+=1
        for q in ([g] if g.geom_type=='LineString' else list(g.geoms)):
            q=q.simplify(0.0005);pts=[P4.transform(x,y) for x,y,*_ in q.coords]
            if len(pts)<2: continue
            km+=sum(((a[0]-b[0])**2+(a[1]-b[1])**2)**.5 for a,b in zip(pts,pts[1:]))
            out[k].append(' '.join('%.2f,%.2f'%t for t in pts))
    st[k]=(n,len(out[k]),round(km))
# v208: kézzel pótolt, közelítő nyomvonalak (az AWMC-ből hiányzó, de jól adatolt vezetékek). Sor: [vonal, név_hu, név_en]
# Aquincum: a Római fürdő forrásaitól a polgárvároson át, a mai Szentendrei út mentén a katonai amfiteátrumig, kb. 5 km (Kaba 1976; Havas 2005; BTM Aquincumi Füzetek 10).
# Töréspontok: forráscsoport (Római Strandfürdő, közelítő), polgárváros (térkép helynévtára), Szentendrei út – Záhony utca (közelítő), legiotábor (helynévtár), katonai amfiteátrum (Heath-adatkészlet).
X=[
 ([(19.0525,47.5745),(19.0497,47.5646),(19.0470,47.5590),(19.0414,47.5423),(19.03907,47.53295)],
  'Aquincum vízvezetéke: a Római fürdő forrásaitól a polgárvároson át a katonai amfiteátrumig, kb. 5 km. A nyomvonal közelítő (a mai Szentendrei út mentén); pillérei ma is láthatók. Forrás: Kaba 1976; Havas 2005.',
  'Aqueduct of Aquincum: from the springs at Római fürdő through the civil town to the military amphitheatre, c. 5 km. Approximate course (along today’s Szentendrei út); piers still visible. Source: Kaba 1976; Havas 2005.'),
 # v209: Pannonia további, az AWMC-ből hiányzó vezetékei – sematikus vonalak a forrásvidék és a város között
 ([(16.9230,48.1330),(16.9044,48.1399)],
  'Carnuntum, Pfaffenberg-vezeték: a Pfaffenberg felől a legiotábor felé vezetett. Sematikus vonal, a pontos nyomvonal nincs berajzolva. Carnuntumnak több vezetéke volt (Solafeld, nyugati canabae, távvezeték a legiotáborhoz); ezek nyomvonalához nem volt szabad adat. Forrás: Doneus–Gugl, Carnuntum légirégészeti feldolgozása; Nedelik–Petznek 2017.',
  'Carnuntum, Pfaffenberg conduit: led from the Pfaffenberg towards the legionary fortress. Schematic line, the exact course is not drawn. Carnuntum had several conduits (Solafeld, western canabae, long-distance line to the fortress); no open data were available for their courses. Source: Doneus–Gugl, aerial archaeology of Carnuntum; Nedelik–Petznek 2017.'),
 ([(16.2470,48.1375),(16.3000,48.1480),(16.3715,48.2117)],
  'Vindobona vízvezetéke: a Bécsi-erdőből, a mai Kalksburg környékéről délnyugat felől vezetett a legiotáborhoz, kb. 17 km. Sematikus vonal (a rajzolt hossz rövidebb a valódinál). Forrás: Kubitschek 1908; Mosser–Adler-Wölfl.',
  'Aqueduct of Vindobona: led from the Vienna Woods, around today’s Kalksburg, from the south-west to the legionary fortress, c. 17 km. Schematic line (drawn shorter than the real length). Source: Kubitschek 1908; Mosser–Adler-Wölfl.'),
 ([(19.6000,45.0850),(19.6070,45.0470),(19.6107,44.9664)],
  'Sirmium vízvezetéke: a Fruška gora Vranjaš-forrásától (Manđelos közelében) vezetett a városba; a szerb műemléki ismertető szerint több mint 24 km hosszú volt. Sematikus vonal, a forrás helye közelítő.',
  'Aqueduct of Sirmium: led from the Vranjaš spring on Fruška Gora (near Manđelos) to the city; according to the Serbian heritage description it was more than 24 km long. Schematic line, the position of the spring is approximate.'),
 ([(16.5490,47.6760),(16.5920,47.6861)],
  'Scarbantia vízvezetéke: a Sopron és Bánfalva között talált föld alatti építményt 1925-ben római vízvezetékként azonosították. Sematikus vonal. Forrás: Gabrieli G., Arrabona 24–25 (1988).',
  'Aqueduct of Scarbantia: the underground structure found between Sopron and Bánfalva was identified in 1925 as a Roman aqueduct. Schematic line. Source: G. Gabrieli, Arrabona 24–25 (1988).'),
]
out['x']=[];st['x']=[]
for ll,hu,en in X:
    pts=[P4.transform(x,y) for x,y in ll]
    st['x'].append(round(sum(((a[0]-b[0])**2+(a[1]-b[1])**2)**.5 for a,b in zip(pts,pts[1:])),1))
    out['x'].append([' '.join('%.2f,%.2f'%t for t in pts),hu,en])
json.dump(out,open(R+'imp_aq.json','w'),ensure_ascii=False,separators=(',',':'))
import os;print(st,os.path.getsize(R+'imp_aq.json'))
