import glob,re,json,collections,sys
R=[]
for f in glob.glob('/home/claude/dl/edr/x/*/*.xml'):
    s=open(f,encoding='utf8',errors='replace').read()
    m=re.search(r'<origPlace>(.*?)</origPlace>',s,re.S);op=re.findall(r'<placeName[^>]*>([^<]*)</placeName>',m.group(1)) if m else []
    pv=re.search(r'<provenance type="found">(.*?)</provenance>',s,re.S)
    loc=re.search(r'<placeName type="locus">([^<]*)</placeName>',pv.group(1)).group(1) if pv and re.search(r'<placeName type="locus">([^<]*)</placeName>',pv.group(1)) else ''
    pf=re.findall(r'<placeName>([^<]*)</placeName>',pv.group(1)) if pv else []
    d=re.search(r'<origDate notBefore-custom="(-?\d*)" notAfter-custom="(-?\d*)"',s)
    t=re.findall(r'<term ref="[^"]*typeins[^"]*">([^<]*)</term>',s)
    ot=re.search(r'<objectType[^>]*>([^<]*)</objectType>',s);ma=re.search(r'<material[^>]*>([^<]*)</material>',s)
    lang=re.search(r'<TEI[^>]*xml:lang="([^"]*)"',s)
    R.append(dict(id=re.search(r'<idno type="localID">([^<]*)',s).group(1),op=op,pf=pf,loc=loc,nb=d.group(1) if d else '',na=d.group(2) if d else '',t=t,ot=ot.group(1) if ot else '',ma=ma.group(1) if ma else '',lang=lang.group(1) if lang else ''))
json.dump(R,open('/home/claude/dl/edr/recs.json','w'),ensure_ascii=False)
print(len(R))
