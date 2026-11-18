# v94 angol sorai -> en/fix_v94.json
import json,sys
sys.path.insert(0,'src');import amph2_card as A2
M=json.load(open('en/missing.json'))
hl=A2.build('hu').split('\n')+['      <h3 class="aqh">A tizenegy vezeték a térképen</h3>'];el=A2.build('en').split('\n')+['      <h3 class="aqh">The eleven aqueducts on the map</h3>']
assert len(hl)==len(el);mp={a:b for a,b in zip(hl,el)}
out=[{"id":u['id'],"e":mp[u['t']]} for u in M if u['t'] in mp];miss=[u for u in M if u['t'] not in mp]
json.dump(out,open('en/fix_v94.json','w'),ensure_ascii=False,indent=0)
print('ok',len(out),'unmatched',len(miss));[print('  ',u['id'],u['t'][:200]) for u in miss[:10]]
