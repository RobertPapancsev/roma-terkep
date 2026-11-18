import glob,re,json
R={}
for f in glob.glob('/home/claude/dl/edr/x/*/*.xml'):
    s=open(f,encoding='utf8',errors='replace').read()
    i=re.search(r'<idno type="localID">([^<]*)',s).group(1)
    m=re.search(r'<!--(.*?)-->\s*<div type="edition"',s,re.S)
    if not m: continue
    t=m.group(1).strip()
    R[i]=t
json.dump(R,open('/home/claude/dl/edr/text.json','w'),ensure_ascii=False)
print(len(R))
