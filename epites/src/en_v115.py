import json,sys,re
sys.path.insert(0,'src');import v115_edits as V, dis_card as DC
M=json.load(open('en/missing.json'))
mp={}
q=lambda s:re.findall(r'"((?:[^"\\]|\\.)*)"',s)
pairs=[(h,e) for o,h,e in V.E if h and e]+V.NEW
for h,e in pairs:
    a,b=q(h),q(e);assert len(a)==len(b),(a,b)
    for x,y in zip(a,b):
        mp[x]=y
hl=DC.build('hu').rstrip('\n').split('\n');el=DC.build('en').rstrip('\n').split('\n');assert len(hl)==len(el)
mp.update({a:b for a,b in zip(hl,el)})
out=[{"id":u['id'],"e":mp[u['t']]} for u in M if u['t'] in mp];miss=[u for u in M if u['t'] not in mp]
json.dump(out,open('en/fix_v115.json','w'),ensure_ascii=False,indent=0)
print('ok',len(out),'unmatched',len(miss));[print('  ',u['id'],u['t'][:200]) for u in miss[:10]]
