# v108: „Katasztrófák Rómában” kártya, „A város számokban” csoport
import shutil,sys
sys.path.insert(0,'src');import dis_card as A
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'discard' not in b
shutil.copy(p,'src/body_v60pre_before_v108.html');shutil.copy(cp,'src/style_v60pre_before_v108.css')
def rep(s,a,x):
    assert s.count(a)==1,(a[:60],s.count(a));return s.replace(a,x)
b=rep(b,'    <section class="card" id="bldcard">',A.build('hu')+'    <section class="card" id="bldcard">')
b=rep(b,'"Építkezések időrendben":"az','"Katasztrófák Rómában: tűz, árvíz, földrengés":"'+A.SUB[0]+'","Építkezések időrendben":"az')
b=rep(b,'      <li><b>Építkezések időrendben.</b>',A.SRCLI('hu')+'\n      <li><b>Építkezések időrendben.</b>')
b=rep(b,'popcard:"szam",','popcard:"szam",discard:"szam",')
# v109: a tűzvész éve a térképen
b=rep(b,'if(edbYear)edbYear(y);}','if(edbYear)edbYear(y);if(disYear)disYear(y);}')
b=rep(b,'/* v79: építkezések időrendben (bld/data.json) */',A.js()+'/* v79: építkezések időrendben (bld/data.json) */')
c=rep(c,'</style>','''/* v108: katasztrófák */
#discard{--dfi:#c0392b;--dfl:#2f7fb8;--dqk:#8a6d3b}
#discard .dissvg{width:100%;height:auto;max-width:900px;display:block}#discard .dissvg .gr{stroke:var(--line);stroke-width:1}#discard .dissvg .bl{stroke:var(--muted);stroke-width:1;opacity:.5}
#discard .dissvg .ax{font:15px var(--font-mono,monospace);fill:var(--muted)}#discard .dissvg .rl{font:600 15px var(--font-sans,sans-serif);fill:var(--ink,#333)}
#discard .dissvg .fi1{fill:var(--dfi)}#discard .dissvg .fi0{fill:var(--dfi);opacity:.55}#discard .dissvg .fl{fill:var(--dfl)}#discard .dissvg .flr{fill:var(--dfl);opacity:.45}
#discard .dissvg .qk0{fill:var(--dqk);opacity:.6}#discard .dissvg .qk1{fill:var(--dqk)}
#discard .sw.dfi1{background:var(--dfi)}#discard .sw.dfi0{background:var(--dfi);opacity:.55}#discard .sw.dfl{background:var(--dfl)}#discard .sw.dqk{background:var(--dqk);border-radius:50%}
#discard .regtab.distab,#discard .regtab.distab2{min-width:0;width:100%}#discard .distab2 td:nth-child(n+2),#discard .distab2 th:nth-child(n+2){white-space:normal;text-align:left}#discard .distab2 td:first-child{white-space:nowrap}#discard .distab2 tr.big td:nth-child(-n+2){font-weight:600}
.m.burn .s{stroke:#c0392b!important;stroke-width:3!important;fill:#c0392b!important;fill-opacity:.4!important}
#discard .dissvg [data-fy]{cursor:pointer}#discard .dissvg .cur{stroke:#000;stroke-width:1.5}#discard tr.cur td{background:rgba(192,57,43,.12)}#discard .fgo{white-space:nowrap}#discard .disstat b{color:var(--dfi)}
#discard .disbars{margin:6px 0}#discard .dbr{display:flex;align-items:center;gap:6px;margin:2px 0;font:12px var(--font-mono,monospace)}#discard .dbl{width:2.6em;text-align:right;color:var(--muted)}#discard .dbb{height:12px;background:var(--dfi);border-radius:2px;min-width:1px}#discard .dbn{color:var(--muted)}
</style>''')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c)
t=open('src/patch_tabs.py',encoding='utf8').read()
if 'discard' not in t: t=rep(t,'popcard:"szam",','popcard:"szam",discard:"szam",');open('src/patch_tabs.py','w',encoding='utf8').write(t)
e=open('en/build.py',encoding='utf8').read()
if 'Katasztrófák Rómában' not in e: e=rep(e,'subs={"','subs={"Katasztrófák Rómában: tűz, árvíz, földrengés":"'+A.SUB[1]+'","');open('en/build.py','w',encoding='utf8').write(e)
print('ok')
