import json,math,re,unicodedata
W=json.load(open('wd.json'));M=[m for m in json.load(open('/tmp/rm_mon.json')) if m['td'] in 'ARU' and m['c']]
TYPES={'T':['temple','tempio','templum','aedes','templom','aedicula','sacello','sacellum','szentely','shrine','sanctuary'],'A':['arch','arco','arcus','diadaliv','iv','kapuiv'],'B':['bath','baths','terme','thermae','furdo','balneum'],
 'P':['porta','gate','kapu'],'BR':['pons','ponte','bridge','hid'],'BA':['basilica','bazilika'],'F':['forum','foro','forum'],'C':['column','colonna','columna','oszlop'],'M':['mausoleum','mausoleo','sepulcrum','tomb','tomba','sepolcro','sir','siremlek','pyramid','piramide','piramis','columbarium','colombario'],
 'TH':['theatre','theater','teatro','theatrum','szinhaz'],'CI':['circus','circo','cirkusz'],'PO':['portico','porticus','oszlopcsarnok'],'AQ':['aqua','acquedotto','aqueduct','vizvezetek'],'D':['domus','house','casa','haz','palota','palace','palazzo','villa'],
 'H':['horrea','warehouse','raktar'],'S':['stadium','stadio','stadion'],'AM':['amphitheatre','amphitheater','anfiteatro','amphitheatrum','amfiteatrum'],'CH':['church','chiesa','san','santa','santi','sant','szent','templom','basilica'],'W':['wall','walls','mura','muri','murus','fal'],'O':['obelisk','obelisco','obeliscus','obeliszk'],'MI':['mithraeum','mitreo']}
T2={w:t for t,ws in TYPES.items() for w in ws}
STOP=set('of the di del della dei degli delle al alla e et in a az es és la il le lo de ad apud sub and or roman ancient rome roma romai egykori mai site archaeological remains resti area'.split())
def norm(s):
    s=unicodedata.normalize('NFD',s.lower());s=''.join(c for c in s if unicodedata.category(c)!='Mn').replace('j','i').replace('v','u').replace('ph','f').replace('ae','e').replace('y','i')
    return [t for t in re.findall(r'[a-z]+',s) if t not in STOP and len(t)>2]
def feat(*names):
    ty=set();pr=set()
    for n in names:
        for t in norm(n or ''):
            hu=[k for k in ('templom','diadaliv','furdo','szinhaz','oszlop','bazilik','forum','kapu','siremlek','sirj','piramis','cirkusz','stadion','vizvezet','obeliszk','szentely','haza','palota','csarnok','raktar','fal') if t.startswith(k)]
            if hu: ty.add(T2.get(hu[0],{'bazilik':'BA','sirj':'M','haza':'D','csarnok':'PO','vizvezet':'AQ'}.get(hu[0],'X')));continue
            if t in T2: ty.add(T2[t])
            else: pr.add(t[:5])
    return ty,pr
res=[]
for m in M:
    x,y,sz=m['c'];R=max(110,sz*0.8);ty,pr=feat(m['gr'],m['name']);best=None
    for q,v in W.items():
        if abs(v['x']-x)>R or abs(v['y']-y)>R: continue
        d=math.hypot(v['x']-x,v['y']-y);t2,p2=feat(v['en'],v['it'],v['la'],v['hu'])
        sh=len(pr&p2);tm=len(ty&t2)
        sc=sh*3+tm*1.5-d/40-(2 if ('church building' in v['inst'] and 'CH' not in ty) else 0)
        if best is None or sc>best[0]: best=(sc,q,round(d),sh,tm)
    res.append((m,best))
json.dump([[m['id'],b[1] if b else None,b[0] if b else None] for m,b in res],open('match.json','w'))
for m,b in res:
    if not b: print(f"{m['id']:18s} {m['td']} | {m['name'][:38]:38s} | –");continue
    v=W[b[1]];print(f"{m['id']:18s} {m['td']} | {m['name'][:34]:34s} | {b[0]:4.1f} d{b[2]:3d} n{b[3]}t{b[4]} | {(v['en'] or v['it'])[:36]:36s} | {v['img'][:38]}")
