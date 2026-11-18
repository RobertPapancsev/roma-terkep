# v92: az amforafeliratok angol sorai -> en/fix_v92.json
import json,sys
sys.path.insert(0,'src');import amph_card as AC
M=json.load(open('en/missing.json'))
h,hs=AC.build('hu');e,es=AC.build('en')
hl=h.split('\n')+[hs];el=e.split('\n')+[es];assert len(hl)==len(el);mp={a:b for a,b in zip(hl,el)}
out=[{"id":u['id'],"e":mp[u['t']]} for u in M if u['t'] in mp];miss=[u for u in M if u['t'] not in mp]
json.dump(out,open('en/fix_v92.json','w'),ensure_ascii=False,indent=0)
print('ok',len(out),'unmatched',len(miss));[print('  ',u['id'],u['t'][:200]) for u in miss[:10]]
