# v107: köztársaság kori éremkincsek (CHRR) az „Éremkincsek” kártya végén
import shutil,sys
sys.path.insert(0,'src');import chrr_card as A
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'chrrsvg' not in b
shutil.copy(p,'src/body_v60pre_before_v107.html');shutil.copy(cp,'src/style_v60pre_before_v107.css')
L=b.split('\n');i=next(k for k,x in enumerate(L) if 'id="chrecard"' in x);e=next(k for k in range(i,len(L)) if L[k].strip()=='</section>')
L[e:e]=A.build('hu').rstrip('\n').split('\n');b='\n'.join(L)
k='      <li><b>Építkezések időrendben.</b>';assert b.count(k)==1;b=b.replace(k,A.SRCLI('hu')+'\n'+k)
assert c.count('</style>')==1
c=c.replace('</style>','''/* v107: CHRR */
#chrecard .chrrsvg{width:100%;height:auto;max-width:900px;display:block}#chrecard .chrrsvg .b1{fill:#b9c7d8}#chrecard .chrrsvg .b2{fill:#1f5fa8}#chrecard .chrrsvg .bd{fill:#c8792b;opacity:.14}
#chrecard .chrrsvg .gr{stroke:var(--line);stroke-width:1}#chrecard .chrrsvg .tk{stroke:var(--muted);stroke-width:1}#chrecard .chrrsvg .ax{font:15px var(--font-mono,monospace);fill:var(--muted)}#chrecard .chrrsvg .bl{font-weight:700;fill:var(--ink,#333)}
#chrecard .sw.chb1{background:#b9c7d8}#chrecard .sw.chb2{background:#1f5fa8}
#chrecard .regtab.chrrtab{min-width:0;width:100%}#chrecard .chrrtab th{white-space:normal}#chrecard .chrrtab th,#chrecard .chrrtab td{padding:3px 5px}
</style>''')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok')
