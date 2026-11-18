# v89: EDB (Epigraphic Database Bari) EpiDoc-fájlok beolvasása. Zenodo 10.5281/zenodo.3575485; a fájlok licence: CC BY-NC-SA 3.0. Kimenet: /home/claude/dl/edb/recs.json
import glob,re,json,html
R=[]
for f in glob.glob('/home/claude/dl/edb/x/EDB/*.xml'):
    s=open(f,encoding='utf8',errors='replace').read()
    g=lambda p:(lambda m:html.unescape(m.group(1).strip()) if m else '')(re.search(p,s,re.S))
    d=re.search(r'<origDate[^>]*notAfter-custom="(-?\d*)"[^>]*notBefore-custom="(-?\d*)"',s) or re.search(r'<origDate[^>]*notBefore-custom="(-?\d*)"[^>]*notAfter-custom="(-?\d*)"',s)
    nb=na=''
    if d:
        if 'notAfter-custom' in d.group(0).split('notBefore-custom')[0]:na,nb=d.group(1),d.group(2)
        else:nb,na=d.group(1),d.group(2)
    ed=re.search(r'<div type="edition" xml:lang="([^"]*)"',s)
    R.append(dict(id=g(r'<idno type="localID">([^<]*)'),title=g(r'<title>([^<]*)</title>'),nb=nb,na=na,t=re.findall(r'<term ref="[^"]*typeins[^"]*">([^<]*)</term>',s),ot=g(r'<objectType[^>]*>([^<]*)</objectType>'),ma=g(r'<material[^>]*>([^<]*)</material>'),
        dec=[html.unescape(x) for x in re.findall(r'<rs[^>]*type="decoration"[^>]*>([^<]*)</rs>',s)],ex=g(r'<rs[^>]*type="execution"[^>]*>([^<]*)</rs>'),me=g(r'<rs type="metre">([^<]*)</rs>'),lang=ed.group(1) if ed else '',
        text=g(r'<!--(.*?)-->\s*<div type="edition"'),bib=g(r'<bibl>([^<]*)</bibl>'),place=g(r'<origPlace>\s*<placeName[^>]*>([^<]*)</placeName>')))
json.dump(R,open('/home/claude/dl/edb/recs.json','w'),ensure_ascii=False)
print(len(R))
