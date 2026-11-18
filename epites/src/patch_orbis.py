# v111: ORBIS-kártya, Gazdaság csoport
import shutil,sys
sys.path.insert(0,'src');import orbis_card as A
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'orbiscard' not in b
shutil.copy(p,'src/body_v60pre_before_v111.html');shutil.copy(cp,'src/style_v60pre_before_v111.css')
def rep(s,a,x):
    assert s.count(a)==1,(a[:60],s.count(a));return s.replace(a,x)
b=rep(b,'    <section class="card" id="bldcard">',A.build('hu')+'    <section class="card" id="bldcard">')
b=rep(b,'"Építkezések időrendben":"az','"Milyen messze volt Róma? Utazási idő és szállítási költség":"'+A.SUB[0]+'","Építkezések időrendben":"az')
b=rep(b,'      <li><b>Építkezések időrendben.</b>',A.SRCLI('hu')+'\n      <li><b>Építkezések időrendben.</b>')
b=rep(b,'chrecard:"gazd",','chrecard:"gazd",orbiscard:"gazd",')
c=rep(c,'</style>','''/* v111: ORBIS */
#orbiscard{--ose:#1f5fa8;--oin:#c8792b}
#orbiscard .orbsvg{width:100%;height:auto;max-width:900px;display:block}#orbiscard .orbsvg .gr{stroke:var(--line);stroke-width:1}#orbiscard .orbsvg .tk{stroke:var(--muted);stroke-width:1}
#orbiscard .orbsvg .ax{font:15px var(--font-mono,monospace);fill:var(--muted)}#orbiscard .orbsvg .lb{font:15px var(--font-sans,sans-serif);fill:var(--ink,#333)}
#orbiscard .orbsvg .pse{fill:var(--ose);opacity:.85}#orbiscard .orbsvg .pin{fill:var(--oin);opacity:.9}#orbiscard .sw.opse{background:var(--ose);border-radius:50%}#orbiscard .sw.opin{background:var(--oin);border-radius:50%}
#orbiscard .regtab.orbtab{min-width:0;width:100%}#orbiscard .orbtab th{white-space:normal}#orbiscard .orbtab td:first-child{white-space:normal}#orbiscard .orbtab th,#orbiscard .orbtab td{padding:3px 5px}
</style>''')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c)
t=open('src/patch_tabs.py',encoding='utf8').read()
if 'orbiscard' not in t: t=rep(t,'chrecard:"gazd",','chrecard:"gazd",orbiscard:"gazd",');open('src/patch_tabs.py','w',encoding='utf8').write(t)
e=open('en/build.py',encoding='utf8').read()
if 'Milyen messze volt Róma' not in e: e=rep(e,'subs={"','subs={"Milyen messze volt Róma? Utazási idő és szállítási költség":"'+A.SUB[1]+'","');open('en/build.py','w',encoding='utf8').write(e)
print('ok')
