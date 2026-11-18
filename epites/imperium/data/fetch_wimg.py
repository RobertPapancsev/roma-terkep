# Séták képeinek letöltése: Commons-metaadat (licenc, szerző, leírás) + 400 px-es bélyegkép → imp_wimg/<md5>.webp
import json, os, re, subprocess, time, hashlib, html, urllib.parse, sys
sys.path.insert(0, os.path.dirname(__file__))
from walk_img import WI
B='/home/claude/imperium/'; MC=B+'data/agg/wimg_meta.json'
M=json.load(open(MC)) if os.path.exists(MC) else {}
UA='RomaMap/1.0 (personal non-commercial study map)'
def curl(u,out=None):
    for t in range(6):
        a=['curl','-sS','-m','40','-A',UA,u]+(['-o',out] if out else [])
        r=subprocess.run(a,capture_output=True,text=True)
        if out:
            if os.path.exists(out) and os.path.getsize(out)>2000: return True
        else:
            try: return json.loads(r.stdout)
            except Exception: pass
        time.sleep(15*(t+1))
    return None
T=sorted({v['f'] for w in WI.values() for v in w.values()} - set(M))
for i in range(0,len(T),10):
    ch=T[i:i+10]
    u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(dict(action='query',titles='|'.join(ch),prop='imageinfo',iiprop='extmetadata|url|size',iiurlwidth=480,iiextmetadatafilter='LicenseShortName|LicenseUrl|Artist|Credit|ImageDescription|DateTimeOriginal',format='json'))
    d=curl(u)
    if not d: raise SystemExit('API hiba')
    norm={n['to']:n['from'] for n in d['query'].get('normalized',[])}
    for pg in d['query']['pages'].values():
        t=norm.get(pg['title'],pg['title'])
        if 'missing' in pg: print('HIÁNYZIK',t); continue
        ii=pg['imageinfo'][0]; m=ii.get('extmetadata',{})
        g=lambda k: re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',m.get(k,{}).get('value','')))).strip()
        M[t]={'lic':g('LicenseShortName'),'lu':m.get('LicenseUrl',{}).get('value',''),'a':g('Artist') or g('Credit'),'desc':g('ImageDescription')[:600],'thumb':ii.get('thumburl'),'page':ii.get('descriptionurl')}
    json.dump(M,open(MC,'w'),ensure_ascii=False,indent=0); time.sleep(5)
from PIL import Image
for t,v in M.items():
    fn=B+'imp_wimg/'+hashlib.md5(t.encode()).hexdigest()[:12]+'.webp'
    if os.path.exists(fn) or not v.get('thumb'): continue
    tmp='/tmp/wimg_dl'
    if os.path.exists(tmp): os.remove(tmp)
    if not curl(v['thumb'],tmp): print('nem tölthető le',t); continue
    im=Image.open(tmp).convert('RGB'); im.thumbnail((480,360)); im.save(fn,'WEBP',quality=78); print('ok',t,im.size); time.sleep(3)
print(len(M),'meta')
