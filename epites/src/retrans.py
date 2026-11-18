# fordítás újraleképezése szöveg alapján egy alapváltozás után
import json,glob,shutil,subprocess,os,sys
U=json.load(open('en/units.json'))['units'];O={x['id']:x['e'] for x in json.load(open('en/out_all.json'))}
for f in sorted(glob.glob('en/fix_*.json')):
    for x in json.load(open(f)):O[x['id']]=x['e']
t2e={u['t']:O[u['id']] for u in U if u['id'] in O}
json.dump(t2e,open('/tmp/t2e.json','w'),ensure_ascii=False)
for f in glob.glob('en/fix_*.json'):
    shutil.move(f,'src/'+os.path.basename(f).replace('.json','_applied.json'))
subprocess.run(['python3','en/extract.py'],check=True)
U=json.load(open('en/units.json'))['units']
out=[];miss=[]
for u in U:
    if u['t'] in t2e:out.append({"id":u['id'],"e":t2e[u['t']]})
    else:miss.append(u)
json.dump(out,open('en/out_all.json','w'),ensure_ascii=False)
json.dump(miss,open('en/missing.json','w'),ensure_ascii=False,indent=0)
print('missing',len(miss))
