import json,sys
sys.path.insert(0,'src');import dis_card as A
M=json.load(open('en/missing.json'))
hl=A.build('hu').rstrip('\n').split('\n')+[A.SRCLI('hu')];el=A.build('en').rstrip('\n').split('\n')+[A.SRCLI('en')]
assert len(hl)==len(el);mp={a:b for a,b in zip(hl,el)}
out=[{"id":u['id'],"e":mp[u['t']]} for u in M if u['t'] in mp];miss=[u for u in M if u['t'] not in mp]
json.dump(out,open('en/fix_v108.json','w'),ensure_ascii=False,indent=0)
print('ok',len(out),'unmatched',len(miss));[print('  ',u['id'],u['t'][:200]) for u in miss[:10]]
