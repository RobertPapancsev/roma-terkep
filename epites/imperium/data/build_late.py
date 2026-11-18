# v196: késő római (Diocletianus utáni) tartományhatárok – AWMC political_shading/roman_empire_provinces post_diocletian (ODbL).
# A forrás 96 névtelen határvonal-szakasz (nem zárt sokszög). A tartományneveket a székhelyüknél írjuk ki (a székhely a térkép DARE-gazetteeréből);
# csak azok a nevek kerülnek fel, amelyek székhelye egyértelműen megvan a gazetteerben.
import json, warnings; warnings.filterwarnings('ignore')
from shapely.geometry import shape
from pyproj import Transformer
R='/home/claude/imperium/'
P4=Transformer.from_crs('EPSG:4326','+proj=laea +lat_0=40 +lon_0=15 +units=km +ellps=WGS84',always_xy=True)
F=json.load(open('/home/claude/awmc/geodata/Cultural-Data/political_shading/roman_empire_provinces post_diocletian/roman_empire_provinces post_diocletian.geojson'))['features']
lines=[]
for f in F:
    g=shape(f['geometry']).simplify(0.01)
    lines.append(' '.join('%.1f,%.1f'%P4.transform(x,y) for x,y,*_ in g.coords))
S=json.load(open(R+'imp_search.json'))
CAP=[('Britannia Prima?','Corinium',None),('Britannia Secunda?','Eburacum',None),('Flavia Caesariensis?','Lindum',None),('Maxima Caesariensis?','Londinium',None),
 ('Belgica Prima','Augusta Treverorum','Trier'),('Belgica Secunda','Durocortorum',None),('Germania Prima','Mogontiacum','Mainz'),('Germania Secunda','Claudia Ara Agrippinensium',None),('Maxima Sequanorum','Vesontio',None),
 ('Lugdunensis Prima','Lugdunum','Lyon'),('Viennensis','Vienna',None),('Narbonensis Prima','Narbo',None),('Narbonensis Secunda','Aquae Sextiae','Aix-en-Provence'),('Novempopulana','Elusa',None),
 ('Aquitanica Prima','Avaricum',None),('Aquitanica Secunda','Burdigala',None),('Baetica','Corduba',None),('Lusitania','Augusta Emerita','Mérida'),('Gallaecia','Bracara Augusta',None),('Tarraconensis','Tarraco',None),('Carthaginiensis','Carthago Nova','Cartagena'),
 ('Mauretania Tingitana','Tingis',None),('Venetia et Histria','Aquileia','Aquileia'),('Aemilia et Liguria','Mediolanium','Milano'),('Flaminia et Picenum','Ravenna',None),('Campania','Capua',None),('Sicilia','Syracusae',None),('Sardinia','Carales',None),
 ('Raetia Prima','Curia',None),('Raetia Secunda','Augusta Vindelicum',None),('Pannonia Prima','Savaria',None),('Pannonia Secunda','Sirmium',None),('Valeria','Sopianae',None),('Noricum Ripense','Lauriacum',None),('Noricum Mediterraneum','Virunum',None),('Dalmatia','Salona',None),
 ('Moesia Prima','Viminacium',None),('Dacia Ripensis','Ratiaria',None),('Dacia Mediterranea','Serdica',None),('Dardania','Scupi',None),('Praevalitana','Scodra',None),('Macedonia','Thessalonica',None),('Epirus Nova','Dyrrachion','Durrës'),('Creta','Gortyna','Gortyn'),
 ('Europa','Perinthus',None),('Thracia','Philippopolis','Plovdiv'),('Haemimontus','Hadrianopolis','Hadrianopolis'),('Moesia Secunda','Marcianopolis',None),('Scythia','Tomi','Constanța'),
 ('Asia','Ephesos','Efes'),('Hellespontus','Cyzicus',None),('Lydia','Sardis',None),('Caria','Aphrodisias','Geyre'),('Lycia','Myra',None),('Pamphylia','Perge',None),('Phrygia Pacatiana','Laodicea ad Lycum','Eskihisar'),('Phrygia Salutaris','Synnada',None),('Lycaonia','Iconium',None),
 ('Bithynia','Nicomedia',None),('Paphlagonia','Gangra',None),('Galatia','Ancyra',None),('Helenopontus','Amaseia',None),('Cappadocia','Caesarea','Kayseri'),('Armenia Prima','Sebasteia',None),('Armenia Secunda','Melitene',None),
 ('Cilicia','Tarsus',None),('Isauria','Seleucia ad Calycadnum','Silifke'),('Syria','Antiochia','Antakya'),('Phoenice','Tyrus','Tyre'),('Palaestina','Caesarea','Caesarea'),('Arabia','Bostra',None),('Osrhoene','Edessa','Şanlıurfa'),('Euphratensis','Hierapolis','Manbij'),('Cyprus','Salamis','Salamis'),
 ('Aegyptus','Alexandria','Alexandria'),('Thebais','Ptolemais Hermeiou','El-Manshah'),('Libya Superior','Ptolemais','Tolmeitha'),('Africa Proconsularis','Carthago','Carthago'),('Byzacena','Hadrumetum',None),('Numidia','Cirta',None),('Mauretania Sitifensis','Sitifis',None),('Mauretania Caesariensis','Iol Caesarea','Cherchell'),('Tripolitania','Lepcis Magna',None)]
lab=[];miss=[]
for nm,a,m in CAP:
    c=[s for s in S if s[0]==a and (m is None or s[1]==m) and s[7] in('city','leg')]
    if nm.endswith('?'): continue   # a négy britanniai provincia helye vitatott: nem írjuk ki
    if len(c)==1: lab.append([round(c[0][4]),round(c[0][5]),nm,a])
    else: miss.append((nm,a,len(c)))
json.dump({'l':lines,'n':lab},open(R+'imp_late.json','w'),ensure_ascii=False,separators=(',',':'))
print(len(lines),len(lab),'kimaradt:',miss)
