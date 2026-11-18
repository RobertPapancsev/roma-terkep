# Római Birodalom térkép – adatfeldolgozás (v1)
# Vetület: Lambert azimutális területtartó, középpont 15°K, 40°É; egység km (x kelet, y észak)
import json,math,os,collections as C
import shapefile
from shapely.geometry import shape,mapping,LineString,MultiLineString,Polygon,MultiPolygon,box
from shapely.ops import transform
from pyproj import Transformer
OUT='/home/claude/imperium'
P4=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km +ellps=WGS84',always_xy=True)
P3=Transformer.from_crs('EPSG:3395','+proj=laea +lat_0=40 +lon_0=15 +units=km +ellps=WGS84',always_xy=True)
f4=lambda x,y,z=None:P4.transform(x,y);f3=lambda x,y,z=None:P3.transform(x,y)
BB=box(-2600,-2300,3500,2300)   # vágókeret (km)
def lines_txt(g,nd):
    out=[]
    for ls in getattr(g,'geoms',[g]):
        if ls.is_empty or len(ls.coords)<2: continue
        out.append(' '.join(('%.'+str(nd)+'f,%.'+str(nd)+'f')%(x,y) for x,y,*_ in ls.coords))
    return out
def poly_txt(g,nd):
    out=[]
    for pg in getattr(g,'geoms',[g]):
        if pg.is_empty or pg.geom_type!='Polygon': continue
        out.append('p'+' '.join(('%.'+str(nd)+'f,%.'+str(nd)+'f')%(x,y) for x,y in pg.exterior.coords[:-1]))
        for r in pg.interiors: out.append('ip'+' '.join(('%.'+str(nd)+'f,%.'+str(nd)+'f')%(x,y) for x,y in r.coords[:-1]))
    return out
base={}
# 1) tenger (AWMC, nyílt víz kb. Kr. u. 200 állapotában)
r=shapefile.Reader('/home/claude/awmc/geodata/Physical Data/open_water_awmc_work/200_ce_open_water/openwater_c_200_ce')
W=[transform(f4,shape(s.__geo_interface__)).buffer(0).intersection(BB) for s in r.shapes()]
from shapely.ops import unary_union
water=unary_union(W)
base['water']=poly_txt(water.simplify(1.5),1)
water_full=water
# 2) tartományok (DARE, kb. Kr. u. 117)
D='/home/claude/klokan/roman-empire/data/'
pv=json.load(open(D+'provinces.geojson'))['features'];lb={f['properties']['name']:f['geometry']['coordinates'] for f in json.load(open(D+'provinces_label.geojson'))['features']}
base['prov']=[]
for f in pv:
    g=transform(f4,shape(f['geometry'])).buffer(0).simplify(1.0)
    n=f['properties']['name'];lx,ly=f4(*lb[n]) if n in lb else (g.representative_point().x,g.representative_point().y)
    base['prov'].append({'n':n,'g':poly_txt(g,1),'l':[round(lx,1),round(ly,1)],'a':round(g.area)})
# 3) a birodalom kiterjedése (AWMC: Kr. e. 60, Kr. u. 117, Kr. u. 200)
A='/home/claude/awmc/geodata/Cultural-Data/political_shading/'
base['ext']={}
for k,fn in [('-60','roman_empire_bce_60/roman_empire_bce_60.geojson'),('117','roman_empire_ce_117_extent/roman_empire_ce_117_extent.geojson'),('200','roman_empire_ce_200_extent/roman_empire_ce_200_extent.geojson')]:
    G=[transform(f4,shape(f['geometry'])).buffer(0) for f in json.load(open(A+fn))['features'] if f['geometry']]
    u=unary_union(G).simplify(1.5);base['ext'][k]=poly_txt(u,1)
# 4) limes / erődvonalak (DARE)
fo=json.load(open(D+'fortifications.geojson'))['features']
base['limes']=[t for f in fo for t in lines_txt(transform(f4,shape(f['geometry'])),2)]
# 4b) folyók és tavak (Natural Earth 10m, közkincs; latin nevek a DARE vektoros változatából)
base['riv']=[]
for f in json.load(open(D+'10m_rivers_lake_centerlines.geojson'))['features']:
    g=transform(f4,shape(f['geometry'])).intersection(BB).simplify(0.8)
    if g.is_empty: continue
    pr=f['properties'];base['riv'].append([pr.get('latin') or '',pr.get('modern') or '',lines_txt(g,1)])
base['lakes']=[]
for f in json.load(open(D+'10m_lakes.geojson'))['features']:
    g=transform(f4,shape(f['geometry'])).buffer(0).intersection(BB).simplify(0.5)
    if not g.is_empty: base['lakes']+=poly_txt(g,1)
# 5) helyek (DARE): fontos típusok az alaprétegbe, a települések (12) csempékbe
TY={'11':'city','13':'civ','17':'leg','18':'fort','53':'fortlet','15':'camp','12':'set'}
seen={}
for fn in ['places_low','places_medium','places_high','places_subsites']:
    for x in json.load(open(D+fn+'.geojson'))['features']: seen[x['properties']['id']]=x
pts=[];spts=[]
for x in seen.values():
    p=x['properties'];t=TY.get(p['type'])
    if not t: continue
    X,Y=f4(*x['geometry']['coordinates'][:2])
    if not BB.contains(LineString([(X,Y),(X+.001,Y)])): continue
    rec=[t,round(X,2),round(Y,2),p['latin'] or '',p['modern'] or '',int(p['startyear'] or 0),int(p['endyear'] or 0),p['id'],p['greek'] or '',int(p['accuracy'] or 0)]
    (spts if t=='set' else pts).append(rec)
base['pts']=pts
print('points base',C.Counter(p[0] for p in pts),'settlements',len(spts))
# 6) utak (Itiner-e): áttekintő réteg + teljes pontosságú csempék
R=json.load(open('/home/claude/dl/itinere/r.json'))['features']
CERT={'Certain':0,'Conjectured':1,'Hypothetical':2}
ov=[];ov3=[];props=[]
TILE=320.0;tiles=C.defaultdict(lambda:{'r':[],'s':[],'w':[]})
for i,f in enumerate(R):
    pr=f['properties'];g=transform(f3,shape(f['geometry']))
    mt=1 if pr['Type']=='Main Road' else 0;ce=CERT.get(pr['Segment_s'],1)
    props.append([pr['Name'] or '',mt,ce,pr['Lower_Date'],pr['Upper_Date'],pr['Citation'] or '',pr['Bibliograp'] or '',pr['Itinerary'] or '',pr['Descriptio'] or ''])
    for t in lines_txt(g.simplify(1.0),1): ov.append([i,mt,ce,t])          # közepes nézet (1 km)
    for t in lines_txt(g.simplify(3.5),0): ov3.append([i,mt,ce,t])         # teljes birodalmi nézet (3,5 km)
    # csempék: a teljes pontosságú vonal minden olyan csempébe bekerül, amelyet érint (a böngésző csak egyszer rajzolja ki)
    x0,y0,x1,y1=g.bounds;txt=lines_txt(g,3)
    for a_ in range(math.floor(x0/TILE),math.floor(x1/TILE)+1):
        for b_ in range(math.floor(y0/TILE),math.floor(y1/TILE)+1):
            if g.intersects(box(a_*TILE,b_*TILE,(a_+1)*TILE,(b_+1)*TILE)):
                for t in txt: tiles['%d_%d'%(a_,b_)]['r'].append([i,mt,ce,t])   # a teljes vonal minden érintett csempébe
base['roads']=ov3
json.dump(ov,open(OUT+'/imp_roads1.json','w'),separators=(',',':'))
json.dump(props,open(OUT+'/imp_roadprops.json','w'),ensure_ascii=False,separators=(',',':'))
# települések csempékbe
for p in spts:
    k='%d_%d'%(math.floor(p[1]/TILE),math.floor(p[2]/TILE));tiles[k]['s'].append(p)
# tenger részletes körvonala csempékbe (a csempe téglalapjával vágva)
for k in list(tiles.keys())+[ '%d_%d'%(a,b) for a in range(-9,12) for b in range(-8,8)]:
    a,b=map(int,k.split('_'));bx=box(a*TILE,b*TILE,(a+1)*TILE,(b+1)*TILE)
    w=water_full.intersection(bx)
    if w.is_empty: continue
    if w.area>=bx.area*0.999: tiles[k]['wf']=1   # a csempe teljesen tenger
    else: tiles[k]['w']=poly_txt(w,2)
idx=[];wfull=[]
for k,v in tiles.items():
    a,b=map(int,k.split('_'))
    if v.get('wf') and not (v['r'] or v['s']): wfull.append([a,b]);continue   # teljesen tengeri csempe: csak a jegyzékben
    if not (v['r'] or v['s'] or v['w'] or v.get('wf')): continue
    json.dump(v,open(OUT+'/tiles/it_%s.json'%k,'w'),ensure_ascii=False,separators=(',',':'))
    idx.append([k,a,b])
base['tiles']=sorted(idx);base['wfull']=sorted(wfull);base['tile']=TILE
json.dump(base,open(OUT+'/imp_base.json','w'),ensure_ascii=False,separators=(',',':'))
print('base KB',os.path.getsize(OUT+'/imp_base.json')//1024,'roadprops KB',os.path.getsize(OUT+'/imp_roadprops.json')//1024)
sz=sorted(os.path.getsize(OUT+'/tiles/'+f) for f in os.listdir(OUT+'/tiles'))
print('tiles',len(sz),'total MB',round(sum(sz)/1e6,1),'max KB',sz[-1]//1024,'median KB',sz[len(sz)//2]//1024)
for k in ['water','prov','limes','roads','pts']: print(k,len(json.dumps(base[k]))//1024,'KB')
