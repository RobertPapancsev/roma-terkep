# v91: az occ-kártya keresztény kiegészítésének angol sorai -> en/fix_v91.json
import json,sys
sys.path.insert(0,'src');import occchr_card as OC
M=json.load(open('en/missing.json'))
hl=OC.build('hu').split('\n');el=OC.build('en').split('\n');mp={a:b for a,b in zip(hl,el)}
out=[{"id":u['id'],"e":mp[u['t']]} for u in M if u['t'] in mp];miss=[u for u in M if u['t'] not in mp]
json.dump(out,open('en/fix_v91.json','w'),ensure_ascii=False,indent=0)
print('ok',len(out),'unmatched',len(miss));[print('  ',u['id'],u['t'][:200]) for u in miss[:10]]
