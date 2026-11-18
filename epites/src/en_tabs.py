import json,sys
sys.path.insert(0,'src');import patch_tabs as P
M=json.load(open('en/missing.json'));mp=dict(zip(P.bar('hu'),P.bar('en')))
out=[{"id":u['id'],"e":mp[u['t']]} for u in M if u['t'] in mp];miss=[u for u in M if u['t'] not in mp]
json.dump(out,open('en/fix_v98.json','w'),ensure_ascii=False,indent=0)
print('ok',len(out),'unmatched',len(miss));[print('  ',u['id'],u['kind'],u['t'][:200]) for u in miss[:10]]
