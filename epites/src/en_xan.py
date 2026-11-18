# v97 angol sorai -> en/fix_v97.json
import json,sys
sys.path.insert(0,'src');import xan_card as XC
M=json.load(open('en/missing.json'));H=XC.build('hu');E=XC.build('en');mp={}
for k in H:
    hl=H[k].rstrip('\n').split('\n');el=E[k].rstrip('\n').split('\n');assert len(hl)==len(el),k
    mp.update(zip(hl,el))
out=[{"id":u['id'],"e":mp[u['t']]} for u in M if u['t'] in mp];miss=[u for u in M if u['t'] not in mp]
json.dump(out,open('en/fix_v97.json','w'),ensure_ascii=False,indent=0)
print('ok',len(out),'unmatched',len(miss));[print('  ',u['id'],u['t'][:200]) for u in miss[:10]]
