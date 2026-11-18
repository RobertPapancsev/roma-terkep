# v116: a SITAR-ban név szerint szereplő, hiányzó ókori emlékek felvétele (18 elem) + Horti Maecenatis kiegészítés + Notitia-hivatkozások
import shutil,sys,json
sys.path.insert(0,'src');import v116_new as V
P={p['id']:p for p in json.load(open('/tmp/sitar_all.json'))}
p='body_v60pre.html';b=open(p,encoding='utf8').read()
assert 'id:"portacapena"' not in b
shutil.copy(p,'src/body_v60pre_before_v116.html');shutil.copy('style_v60pre.css','src/style_v60pre_before_v116.css')
def rep(a,x,n=1):
    global b;assert b.count(a)==n,(a[:70],b.count(a));b=b.replace(a,x)
def rings(ids):
    out=[]
    for i in ids:
        for poly in P[i]['g']:
            for k,r in enumerate(poly): out.append(('p' if k==0 else 'ip')+r)
    return '|'.join(out)
GEO={k:(rings(a),rings(c) if c else None) for k,(a,c) in V.GEO.items()}
x,y=[float(v) for v in P[954]['g'][0][0].split(' ')[0].split(',')];GEO['viatecta']=('c%.1f,%.1f,4'%(x,y),None)  # egyetlen pont: kör
json.dump(GEO,open('src/v116_geom.json','w'))
# elemek beszúrása az ianusholitorium blokk után
i=b.index('{id:"ianusholitorium",');j=b.index(']},\n',i)+4
b=b[:j]+'\n'.join(h for e in V.E for h,_ in e)+'\n'+b[j:]
osm=''.join('"%s": "%s",\n'%(k,g) for k,(g,g2) in GEO.items())+''.join('"%s_2": "%s",\n'%(k,g2) for k,(g,g2) in GEO.items() if g2)
rep('"ianusholitorium": "',osm+'"ianusholitorium": "')
rep('"spes":"R","ianusholitorium":"R",','"spes":"R","ianusholitorium":"R",'+''.join('"%s":"%s",'%kv for kv in V.TD.items()))
rep('"spes":["temple"],"ianusholitorium":["temple"],','"spes":["temple"],"ianusholitorium":["temple"],'+''.join('"%s":["%s"],'%kv for kv in V.FN.items()))
for old,hu,en in V.MOD: rep(old,hu)
open(p,'w',encoding='utf8').write(b);print('ok',len(V.E))
