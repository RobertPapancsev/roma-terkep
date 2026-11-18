# DARE-helyek HTML-adatlapjainak (a terület és az alhelyek neve csak itt van) letöltése (CC BY-SA 3.0), helyenként egy fájl
import json,glob,os,sys,urllib.request,concurrent.futures as CF,time
OUT='/home/claude/dl/dare_html/'
ids=set(p[7] for p in json.load(open('/home/claude/imperium/imp_base.json'))['pts'])
for f in glob.glob('/home/claude/imperium/tiles/*.json'):
    ids|=set(p[7] for p in json.load(open(f))['s'])
extra=sys.argv[1:]  # opcionális: további azonosítók fájlja
if extra: ids|=set(open(extra[0]).read().split())
todo=[i for i in ids if not os.path.exists(OUT+i+'.html')]
print('összesen',len(ids),'hiányzik',len(todo),flush=True)
def get(i):
    for k in range(3):
        try:
            r=urllib.request.urlopen(urllib.request.Request('http://imperium.ahlfeldt.se/places/%s.html'%i,headers={'User-Agent':'roman-map-research (personal, non-commercial)'}),timeout=30).read()
            open(OUT+i+'.html','wb').write(r);return 1
        except Exception as e:
            time.sleep(2+k*3)
    return 0
ok=0
with CF.ThreadPoolExecutor(16) as ex:
    for n,r in enumerate(ex.map(get,todo)):
        ok+=r
        if n%1000==0: print(n,ok,flush=True)
print('kész',ok,'/',len(todo))
