# v95: „Éremkincsek: mikor rejtettek el pénzt” kártya. Adat: chre/data.json; szöveg: src/chre_card.py
import shutil,sys
sys.path.insert(0,'src');import chre_card as CC
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'chrecard' not in b and 'Kik szállították az olajat' in b
shutil.copy(p,'src/body_v60pre_before_v95.html');shutil.copy(cp,'src/style_v60pre_before_v95.css')
def rep(s,a,x):
    assert s.count(a)==1,(a[:60],s.count(a));return s.replace(a,x)
card,src,sub=CC.build('hu')
b=rep(b,'    <section class="card" id="bldcard">',card+'    <section class="card" id="bldcard">')
b=rep(b,'"Építkezések időrendben":"az','"Éremkincsek: mikor rejtettek el pénzt":"'+sub+'","Építkezések időrendben":"az')
b=rep(b,'      <li><b>Építkezések időrendben.</b>',src+'\n      <li><b>Építkezések időrendben.</b>')
c=rep(c,'</style>','''/* v95: éremkincsek */
#chrecard{--ce:#2f7fb8;--ci:#e08a1e;--crt:#c0392b;--cev:#777}
#chrecard.open{grid-column:1/-1}
#chrecard .ce{background:var(--ce);stroke:var(--ce)}#chrecard .ci{background:var(--ci);stroke:var(--ci)}#chrecard .ik.crt{background:var(--crt)}#chrecard .ik.cev{background:repeating-linear-gradient(90deg,var(--cev) 0 3px,transparent 3px 6px)}
#chrecard .chresvg{width:100%;height:auto;max-width:900px;display:block}#chrecard .chresvg path.chrel{fill:none;stroke-width:2.2;stroke-linejoin:round;stroke-linecap:round}
#chrecard .chresvg line.chrt{stroke:var(--crt);stroke-width:2.4;opacity:.8}#chrecard .chresvg line.chev{stroke:var(--cev);stroke-width:1;stroke-dasharray:3 3}
#chrecard .chretab td:first-child{white-space:nowrap}
</style>''')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok')
