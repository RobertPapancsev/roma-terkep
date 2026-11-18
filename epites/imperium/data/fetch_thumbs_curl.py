# Bélyegképek letöltése curl-lel (sorban, 1,5 mp szünet; 429-nél vár) a prioritási sorrendben. Kimenet: thumbs/<md5>.webp
import json, os, time, hashlib, io, subprocess, urllib.parse
from PIL import Image
A='/home/claude/imperium/data/'; D=A+'thumbs/'
T=json.load(open(A+'agg/img_titles_prio.json')); FAIL=A+'agg/thumb_fail.json'
F=json.load(open(FAIL)) if os.path.exists(FAIL) else {}
UA='roman-empire-map/1.0 (personal non-commercial research map; slow sequential downloads)'
ok=0
for i,t in enumerate(T):
    key=hashlib.md5(t.encode()).hexdigest()
    if os.path.exists(D+key+'.webp') or t in F: continue
    n=t.replace(' ','_'); h=hashlib.md5(n.encode()).hexdigest(); q=urllib.parse.quote(n)
    if n.rsplit('.',1)[-1].lower() not in ('jpg','jpeg','png','gif','webp'): continue
    u='https://upload.wikimedia.org/wikipedia/commons/thumb/%s/%s/%s/330px-%s'%(h[0],h[:2],q,q)
    wait=30; b=None
    for att in range(5):
        r=subprocess.run(['curl','-sS','-m','60','-A',UA,'-o','/tmp/th.bin','-w','%{http_code}',u],capture_output=True,text=True)
        code=r.stdout.strip()
        if code=='200': b=open('/tmp/th.bin','rb').read(); break
        if code in ('400','404','410'): F[t]='notfound'; json.dump(F,open(FAIL,'w'),ensure_ascii=False); break
        print('HTTP',code,'várok',wait,flush=True); time.sleep(wait); wait*=2
    if b:
        try:
            im=Image.open(io.BytesIO(b)).convert('RGB')
            if im.width>280: im=im.resize((280,round(im.height*280/im.width)),Image.LANCZOS)
            im.save(D+key+'.webp','WEBP',quality=62,method=6); ok+=1
        except Exception as e: F[t]='decode'; json.dump(F,open(FAIL,'w'),ensure_ascii=False)
    if ok and ok%50==0: print(i,'/',len(T),'ok',ok,flush=True)
    time.sleep(1.5)
print('vége ok',ok,flush=True)
