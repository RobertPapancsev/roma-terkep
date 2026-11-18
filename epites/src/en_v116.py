import json,sys,re
sys.path.insert(0,'src');import v116_new as V
M=json.load(open('en/missing.json'))
q=lambda s:re.findall(r'"((?:[^"\\]|\\.)*)"',s)
mp={}
for e in V.E:
    for h,en in e:
        a,b=q(h),q(en);assert len(a)==len(b),(a,b)
        for x,y in zip(a,b): mp[x]=y
for old,h,en in V.MOD:
    if en:
        a,b=q(h),q(en);assert len(a)==len(b)
        for x,y in zip(a,b): mp[x]=y
mp['a Campus Martius nyugati részén; a „vörösök” istállójának (Stabulum Factionis Russatae) maradványai a Largo Perosinál, a Via Giulia mellett kerültek elő, a másik háromé nem ismert']='in the western part of the Campus Martius; remains of the stable of the “Reds” (Stabulum Factionis Russatae) were found at Largo Perosi, next to Via Giulia; the other three are unknown'
out=[{"id":u['id'],"e":mp[u['t']]} for u in M if u['t'] in mp];miss=[u for u in M if u['t'] not in mp]
json.dump(out,open('en/fix_v116.json','w'),ensure_ascii=False,indent=0)
print('ok',len(out),'unmatched',len(miss));[print('  ',u['id'],u['t'][:200]) for u in miss[:12]]
