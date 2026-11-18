# v90: „Róma a birodalom feliratai között” kártya. Adat: list/data.json; szöveg: src/list_card.py
import shutil,sys
sys.path.insert(0,'src');import list_card as LC
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'listcard' not in b and 'edbcard' in b
shutil.copy(p,'src/body_v60pre_before_v90.html');shutil.copy(cp,'src/style_v60pre_before_v90.css')
def rep(s,a,x,n=1):
    assert s.count(a)==n,(a[:60],s.count(a));return s.replace(a,x)
card,src,sub=LC.build('hu')
b=rep(b,'    <section class="card" id="bldcard">',card+'    <section class="card" id="bldcard">')
b=rep(b,'"Építkezések időrendben":"az','"Róma a birodalom feliratai között":"'+sub+'","Építkezések időrendben":"az')
b=rep(b,'      <li><b>Építkezések időrendben.</b>',src+'\n      <li><b>Építkezések időrendben.</b>')
c=rep(c,'</style>','''/* v90: Róma a birodalom feliratai között */
#listcard{--lroma:#c0392b;--litalia:#e08a1e;--lprov:#2f7fb8;--lct:#8a5a44}
#listcard.open{grid-column:1/-1}
#listcard .lroma{background:var(--lroma);stroke:var(--lroma)}#listcard .litalia{background:var(--litalia);stroke:var(--litalia)}#listcard .lprov{background:var(--lprov);stroke:var(--lprov)}
#listcard .listsvg{width:100%;height:auto;max-width:900px;display:block}#listcard .listsvg path.listl{fill:none;stroke-width:2.2;stroke-linejoin:round;stroke-linecap:round}
#listcard .listbars .fe{grid-template-columns:minmax(0,1fr) minmax(80px,1.5fr) 4em}#listcard .listbars .fev{text-align:right}
#listcard .listbars .feb span.lct{background:var(--lct)}#listcard .listbars .feb span.lcr{background:repeating-linear-gradient(90deg,var(--lroma) 0 10px,transparent 10px 13px)}
#listcard .listtab th i{font-style:italic;font-weight:inherit}
</style>''')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok')
