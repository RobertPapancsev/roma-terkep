# v104: „Hajóroncsok és ólomszennyezés” kártya, Gazdaság csoport
import shutil,sys
sys.path.insert(0,'src');import ship_card as A
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'shipcard' not in b
shutil.copy(p,'src/body_v60pre_before_v104.html');shutil.copy(cp,'src/style_v60pre_before_v104.css')
def rep(s,a,x):
    assert s.count(a)==1,(a[:60],s.count(a));return s.replace(a,x)
b=rep(b,'    <section class="card" id="bldcard">',A.build('hu')+'    <section class="card" id="bldcard">')
b=rep(b,'"Építkezések időrendben":"az','"Hajóroncsok és ólomszennyezés":"'+A.SUB[0]+'","Építkezések időrendben":"az')
b=rep(b,'      <li><b>Építkezések időrendben.</b>',A.SRCLI('hu')+'\n      <li><b>Építkezések időrendben.</b>')
b=rep(b,'chrecard:"gazd",','chrecard:"gazd",shipcard:"gazd",')
c=rep(c,'</style>','''/* v104: hajóroncsok */
#shipcard{--sh1:#b9c7d8;--sh2:#1f5fa8}
#shipcard .shipsvg{width:100%;height:auto;max-width:900px;display:block}#shipcard .shipsvg .b1{fill:var(--sh1)}#shipcard .shipsvg .b2{fill:var(--sh2)}
#shipcard .shipsvg .gr{stroke:var(--line);stroke-width:1}#shipcard .shipsvg .tk{stroke:var(--muted);stroke-width:1}#shipcard .shipsvg .ax{font:15px var(--font-mono,monospace);fill:var(--muted)}
#shipcard .shipsvg .ln{fill:none;stroke:var(--sh2);stroke-width:1.6;stroke-linejoin:round}#shipcard .shipsvg .bd{fill:#c8792b;opacity:.14}#shipcard .shipsvg .bl{font-weight:700;fill:var(--ink,#333)}
#shipcard .sw.shb1{background:var(--sh1)}#shipcard .sw.shb2{background:var(--sh2)}
#shipcard .regtab.shiptab{min-width:0;width:100%}#shipcard .shiptab th{white-space:normal}#shipcard .shiptab th,#shipcard .shiptab td{padding:3px 5px}#shipcard .regtab.shipltab{min-width:0;width:100%}#shipcard .regtab.shipltab td:nth-child(3),#shipcard .regtab.shipltab th:nth-child(3){white-space:normal;text-align:left}#shipcard .regtab.shipltab th:nth-child(2){white-space:normal}
</style>''')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c)
t=open('src/patch_tabs.py',encoding='utf8').read()
if 'shipcard' not in t: t=rep(t,'chrecard:"gazd",','chrecard:"gazd",shipcard:"gazd",');open('src/patch_tabs.py','w',encoding='utf8').write(t)
e=open('en/build.py',encoding='utf8').read()
if 'Hajóroncsok és ólomszennyezés' not in e: e=rep(e,'subs={"','subs={"Hajóroncsok és ólomszennyezés":"'+A.SUB[1]+'","');open('en/build.py','w',encoding='utf8').write(e)
print('ok')
