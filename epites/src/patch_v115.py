# v115: SITAR-alapú javítások (Forum Holitorium templomai, Curiae Veteres, Minucia, Ludus Dacicus, Meta Sudans, Castra Priora/Misenatium, Circus Varianus) + régészeti tűznyomok a katasztrófakártyán
import shutil,sys,json,re
sys.path.insert(0,'src');import v115_edits as V, dis_card as DC
p='body_v60pre.html';b=open(p,encoding='utf8').read()
assert 'ianusholitorium' not in b
shutil.copy(p,'src/body_v60pre_before_v115.html');shutil.copy('style_v60pre.css','src/style_v60pre_before_v115.css')
def rep(a,x,n=1):
    global b;assert b.count(a)==n,(a[:70],b.count(a));b=b.replace(a,x)
for old,hu,en in V.E:
    if not hu: continue
    if b.count(old)>1:
        i=b.index('{id:"ludusdacicus"');k=b.index(old,i);b=b[:k]+hu+b[k+len(old):]
    else: rep(old,hu)
# új épület a spes blokk után
i=b.index('{id:"spes",');j=b.index(']},\n',i)+4
b=b[:j]+'\n'.join(h for h,e in V.NEW)+'\n'+b[j:]
# geometriák
G=json.load(open('src/v115_geom.json'))
def setg(k,v,keep=None):
    global b
    m=re.search(r'"%s": "[^"]*"'%re.escape(k),b);assert m,k
    old=m.group(0);new='"%s": "%s"'%(k,v)
    if keep: new+=',\n"%s": %s'%(keep,old.split(': ',1)[1])
    b=b[:m.start()]+new+b[m.end():]
setg('spes',G['spes'],keep='spes_osm')
setg('junosospita',G['junosospita'],keep='junosospita_osm')
setg('curiaeveteres',G['curiaeveteres'],keep='curiaeveteres_osm')
rep('"junosospita": "','"ianusholitorium": "%s",\n"junosospita": "'%G['ianusholitorium'])
rep('"circusvarianus": "','"circusvarianus_2": "%s",\n"circusvarianus": "'%G['circusvarianus_2'])
rep('"spes":"R",','"spes":"R","ianusholitorium":"R",')
rep('"spes":["temple"],','"spes":["temple"],"ianusholitorium":["temple"],')
# katasztrófakártya újragenerálása
i=b.index('    <section class="card" id="discard">');j=b.index('    </section>\n',i)+len('    </section>\n')
b=b[:i]+DC.build('hu')+b[j:]
open(p,'w',encoding='utf8').write(b);print('ok')
