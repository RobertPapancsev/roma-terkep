import sys,json,time
sys.path.insert(0,'/home/claude/dl');import sq
P='PREFIX : <http://www.semanticweb.org/ontologies/2015/1/EPNet-ONTOP_Ontology#> PREFIX dcterms: <http://purl.org/dc/terms/> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> '
def dump(name,sel,where,step=10000):
    out=[];off=0
    while True:
        for t in range(4):
            try:r=sq.rows(P+f'SELECT {sel} WHERE {{ {{ SELECT {sel} WHERE {{ {where} }} ORDER BY {sel.split()[0]} {sel.split()[1] if len(sel.split())>1 else ""} }} }} LIMIT {step} OFFSET {off}');break
            except Exception as e:print('retry',name,off,e);time.sleep(5)
        else:raise SystemExit('fail '+name)
        out+=r;off+=step
        if len(r)<step:break
    json.dump(out,open(name+'.json','w'),ensure_ascii=False);print(name,len(out),out[:2])
Q={
 'amph':('?a ?id ?type ?fp ?afp ?desc ?bib','?a a :Amphora . ?a dcterms:identifier ?id . OPTIONAL{?a :hasAmphoricType ?type} OPTIONAL{?a :hasFindingPlace ?fp} OPTIONAL{?a :hasAncientFindingPlace ?afp} OPTIONAL{?a dcterms:description ?desc} OPTIONAL{?a :mainBibliographicReference ?bib}'),
 'adate':('?a ?d ?b ?e ?t','?a a :Amphora . ?a :hasProductionDate ?d . OPTIONAL{?d :hasBeginningDate ?b} OPTIONAL{?d :hasEndDate ?e} OPTIONAL{?d dcterms:title ?t}'),
 'aprod':('?a ?p','?a a :Amphora . ?a :hasProductionPlace ?p'),
 'alayer':('?a ?s ?e ?g','?a a :Amphora . ?a :foundInLayerStartingAt ?s . OPTIONAL{?a :foundInLayerEndingAt ?e} OPTIONAL{?a :foundInGrid ?g}'),
 'place':('?p ?t ?lat ?lon','?p a :Place . ?p dcterms:title ?t . OPTIONAL{?p :hasLatitude ?lat . ?p :hasLongitude ?lon}'),
 'pwithin':('?p ?w','?p a :Place . ?p :fallsWithin ?w'),
 'ptype':('?p ?c','?p a :Place . ?p a ?c . FILTER(?c IN (:Country,:Municipality,:ModernSpot,:SpecificSpot))'),
 'insc':('?i ?id ?a ?kind ?full ?simp ?desc','?i a :Inscription . ?i dcterms:identifier ?id . OPTIONAL{?i :isCarriedBy ?a} OPTIONAL{?i :hasInscriptionTypeName ?kind} OPTIONAL{?i :hasFullTranscription ?full} OPTIONAL{?i :hasSimplifiedTranscription ?simp} OPTIONAL{?i dcterms:description ?desc}'),
 'icls':('?i ?c ?k','?i a :TitulusPictus . ?i :hasTitulusClass ?c . OPTIONAL{?i :hasTitulusCode ?k}'),
 'icomp':('?i ?c ?t ?v ?cl','?i :isComposedOf ?c . OPTIONAL{?c dcterms:title ?t} OPTIONAL{?c :hasLineValue ?v} OPTIONAL{?c :hasTitulusClass ?cl}'),
 'iprod':('?i ?p','?i a :Inscription . ?i :hasProductionPlace ?p'),
 'bib':('?b ?p ?o','?b a :BibliographicResource . ?b ?p ?o . FILTER(isLiteral(?o))'),
}
for k in (sys.argv[1:] or Q):dump(k,*Q[k])
