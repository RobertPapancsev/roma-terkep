# v96 angol sorai -> en/fix_v96.json
import json,sys
sys.path.insert(0,'src');import patch_srcl as P
M=json.load(open('en/missing.json'));mp={P.line(k,'hu'):P.line(k,'en') for k in P.SRC}
out=[{"id":u['id'],"e":mp[u['t']]} for u in M if u['t'] in mp];miss=[u for u in M if u['t'] not in mp]
json.dump(out,open('en/fix_v96.json','w'),ensure_ascii=False,indent=0)
print('ok',len(out),'unmatched',len(miss));[print('  ',u['id'],u['t'][:200]) for u in miss[:10]]
