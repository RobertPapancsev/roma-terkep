# v88: a „Sírtelkek mérete” és a „Katonák Róma sírfeliratain” kártya angol sorai (src/mp_card.py két nyelven) -> en/fix_v88.json
import json,sys,re
sys.path.insert(0,'src');import mp_card as MC
M=json.load(open('en/missing.json'))
h,hs,_=MC.build('hu');e,es,_=MC.build('en')
hl=h.split("\n")+hs;el=e.split("\n")+es;assert len(hl)==len(el)
mp={a:b for a,b in zip(hl,el)}
out=[];miss=[]
for u in M:
    if u['t'] in mp:out.append({"id":u['id'],"e":mp[u['t']]})
    else:miss.append(u)
json.dump(out,open('en/fix_v88.json','w'),ensure_ascii=False,indent=0)
for o in out:
    x=re.sub(r'<[^>]+>','',o['e'])
    if re.search(r'[őűáéíóöüú]',x):print('HU?',o['id'],x[:140])
print('ok',len(out),'unmatched',len(miss));[print('  ',u['id'],u['t'][:120]) for u in miss[:10]]
