# v96: forrássor közvetlenül minden adatblokk (táblázat, grafikon, sávdiagram) alatt
import re,shutil,json,sys
SRC={'aq':('Frontinus, <i>De aquaeductu</i> 64–86 (Kr. u. 97), R. H. Rodgers kiadása (2003) szerint.','Frontinus, <i>De aquaeductu</i> 64–86 (AD 97), after the edition of R. H. Rodgers (2003).'),
 'reg':('a 4. századi kerületjegyzék (<i>Notitia</i> és <i>Curiosum</i>).','the 4th-century regionary catalogue (<i>Notitia</i> and <i>Curiosum</i>).'),
 'ceipac':('CEIPAC – Roman Open Data (romanopendata.eu), saját összesítés.','CEIPAC – Roman Open Data (romanopendata.eu), our own summary.'),
 'edr':('Epigraphic Database Roma (EDR), saját összesítés.','Epigraphic Database Roma (EDR), our own summary.'),
 'edredb':('Epigraphic Database Roma (EDR) és Epigraphic Database Bari (EDB), saját összesítés.','Epigraphic Database Roma (EDR) and Epigraphic Database Bari (EDB), our own summary.'),
 'edb':('Epigraphic Database Bari (EDB), saját összesítés.','Epigraphic Database Bari (EDB), our own summary.'),
 'edbedr':('Epigraphic Database Bari (EDB) és Epigraphic Database Roma (EDR), saját összesítés.','Epigraphic Database Bari (EDB) and Epigraphic Database Roma (EDR), our own summary.'),
 'list':('LIST v1.2 (az EDCS és az EDH egyesített adatai), saját összesítés.','LIST v1.2 (the merged data of EDCS and EDH), our own summary.'),
 'chre':('Coin Hoards of the Roman Empire (CHRE), saját összesítés.','Coin Hoards of the Roman Empire (CHRE), our own summary.'),
 'bld1':('SITAR, a római régészeti nyilvántartás; saját összesítés.','SITAR, the archaeological record of Rome; our own summary.'),
 'bld2':('a térkép saját adatai (az épületek első építésének éve).','the map’s own data (year of first construction of the buildings).'),
 'pop':('az alábbi két táblázat (modern becslések és ókori számadatok), a kutató, illetve az ókori szerző megnevezésével.','the two tables below (modern estimates and ancient figures), naming the scholar or the ancient author.')}
def line(k,l):return '      <p class="hint srcl"><b>'+('Forrás:' if l=='hu' else 'Source:')+'</b> '+SRC[k][0 if l=='hu' else 1]+'</p>'
if __name__=='__main__':
    p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
    assert 'class="hint srcl"' not in b and 'chrecard' in b
    shutil.copy(p,'src/body_v60pre_before_v96.html');shutil.copy(cp,'src/style_v60pre_before_v96.css')
    L=b.split('\n');out=[];card=None;h='';amph=False;pend=None;n=collections=0;cnt={}
    i=0
    def key(card,h,kind,l):
        if card=='aq':return 'aq'
        if card=='regcard':return 'reg'
        if card=='foodcard':return 'ceipac' if amph else None
        if card in('insccard','nmcard','agecard','plotcard','milcard'):return 'edr'
        if card=='occcard':return 'edredb' if 'keresztény' in h else 'edr'
        if card=='edbcard':return 'edbedr' if h.startswith('Életkor: keresztény') else 'edb'
        if card=='listcard':return 'list'
        if card=='chrecard':return 'chre'
        if card=='bldcard':return 'bld1' if 'bldchart1' in l else 'bld2'
        if card=='popcard':return 'pop' if kind=='chart' else None
        return None
    while i<len(L):
        l=L[i];m=re.search(r'<section class="card"(?: id="(\w+)")?',l)
        if m:
            card=m.group(1) or ('aq' if 'Róma vízvezetékei' in L[i+1] else '?');amph=False;h=''
        if '</section>' in l:card=None
        mh=re.search(r'<h[34][^>]*>(.*?)</h[34]>',l)
        if mh:
            h=re.sub(r'<[^>]+>','',mh.group(1))
            if 'Az amforafeliratok adatbázisa' in h:amph=True
        out.append(l)
        if card:
            kind=None;end=i
            if '<div class="regwrap">' in l:
                kind='table'
                while '</table></div>' not in L[end]:end+=1
            elif re.search(r'<div class="(bldchart|aqchart|popchart|aqtot)[ "]',l):kind='chart'
            elif re.search(r'<div class="foodest',l):
                kind='bars'
                while L[end].rstrip()!='      </div>':end+=1
            if kind:
                k=key(card,h,kind,l)
                out.extend(L[i+1:end+1]);i=end
                if k:
                    while i+1<len(L) and re.search(r'<p class="hint (?:aqleg|bldleg|popleg|popinfo)',L[i+1]):
                        i+=1;out.append(L[i])
                    out.append(line(k,'hu'));cnt[k]=cnt.get(k,0)+1
        i+=1
    b='\n'.join(out)
    assert c.count('</style>')==1
    c=c.replace('</style>','/* v96: forrássor az adatblokkok alatt */\n.card p.hint.srcl{font-size:.86em;opacity:.8;margin-top:.25em}\n</style>')
    open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok',cnt,sum(cnt.values()))
