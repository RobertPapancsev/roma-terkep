import json,re,sys,collections
KW=r'\broman\b|römisch|\bromaine?s?\b|\broman[oaie]s?\b|\bromak|rímsk|római|ρωμαϊκ|ρωμαϊ|rimsk|римск|romak|روماني|رومان|רומי|castellum|villa rustica|limes|legionary|roman bath|thermae|römerkastell|antik.? rim|late antiqu|spätantik|késő antik|ancient roman'
TY=r'roman|castrum|castellum|villa rustica|legionary fortress|limes|thermae|mithraeum'
PER=r'Roman Empire|ancient Rome|Roman Republic|Roman Kingdom|Late Antiquity|Roman Britain|Roman Dacia|Roman Egypt|Roman Syria|Roman Gaul'
NEG=r'saint roman|sveti roman|свети роман|\bst\.? roman|romano-cat|catolic|katolick|byzantin|ottoman|hammam|madras|medrese|mosque|church of|catholic|katol|kathol|katolík|romanesque|romanik|román stílus|románsk|romansk|romain[e]? (de|du) |romani(an|a)\b|rumun|román|romska|romsk|Rom(a|ani) (people|minority)|roma people|cigány|romanes|románico|romanico|romântico|romantic|byzantine revival|neo-roman'
def load(cc):
    d=json.load(open(f'/home/claude/dl/wdh/{cc}.json'))['results']['bindings']; out=[]
    for x in d:
        lab=x.get('lab',{}).get('value',''); le=x.get('len',{}).get('value',''); t=x.get('t',{}).get('value',''); p=x.get('per',{}).get('value','')
        why=None
        if re.search(PER,p): why='per'
        elif re.search(TY,t,re.I) and not re.search(r'romanesque',t,re.I) and not re.search(r'byzantin|ottoman',lab+' '+le,re.I): why='type'
        elif re.search(KW,lab+' | '+le,re.I) and not re.search(NEG,lab+' | '+le,re.I): why='name'
        if why: out.append(dict(q=x['i']['value'].rsplit('/',1)[1],lab=lab,le=le,t=t,p=p,h=x.get('h',{}).get('value',''),adm=x.get('adm',{}).get('value',''),c=x['c']['value'],why=why))
    return d,out
if __name__=='__main__':
    for cc in sys.argv[1:]:
        d,o=load(cc); print(cc,len(d),'->',len(o),collections.Counter(x['why'] for x in o))
        for x in o[:int(sys.argv[0] and 25)]: print('  ',x['why'],'|',(x['le'] or x['lab'])[:60],'|',x['lab'][:40],'|',x['t'][:40],'|',x['p'][:30])
