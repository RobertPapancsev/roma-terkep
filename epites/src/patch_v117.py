# v117: „A 14 kerület számokban” – a térképes körök kikapcsolnak, ha a kártyát bezárják vagy másik kártyát nyitnak meg
import shutil
p='body_v60pre.html';b=open(p,encoding='utf8').read()
assert 'cardclose' not in b
shutil.copy(p,'src/body_v60pre_before_v117.html')
def rep(a,x):
    global b;assert b.count(a)==1,a[:60];b=b.replace(a,x)
# 1) dokkolt kártya bezárásakor esemény
rep('dockPh.replaceWith(c);dockPh=null;c.classList.remove("open","docked");',
    'dockPh.replaceWith(c);dockPh=null;c.classList.remove("open","docked");c.dispatchEvent(new Event("cardclose"));')
# 2) dokkoláskor (másik kártya megnyitása) és keskeny képernyőn nyitáskor/záráskor esemény
rep('docked=c;c.classList.add("open","docked");','docked=c;c.classList.add("open","docked");document.dispatchEvent(new CustomEvent("cardopen",{detail:c}));')
rep('const o=c.classList.toggle("open");h.setAttribute("aria-expanded",String(o));};',
    'const o=c.classList.toggle("open");h.setAttribute("aria-expanded",String(o));if(o)document.dispatchEvent(new CustomEvent("cardopen",{detail:c}));else c.dispatchEvent(new Event("cardclose"));};')
# 3) a kerületi kártya figyeli az eseményeket
rep('    if(regKey){const za=document.getElementById("z-all");if(za)za.click();}drawReg();}));})();',
    '    if(regKey){const za=document.getElementById("z-all");if(za)za.click();}drawReg();}));\n'
    '  const off=()=>{if(!regKey)return;regKey=null;bs.forEach(x=>x.setAttribute("aria-pressed","false"));document.querySelectorAll(".regtab [data-k]").forEach(c=>c.classList.remove("on"));drawReg();};\n'
    '  const rc=document.getElementById("regcard");if(rc)rc.addEventListener("cardclose",off);\n'
    '  document.addEventListener("cardopen",e=>{if(e.detail!==rc)off();});})();')
open(p,'w',encoding='utf8').write(b);print('ok')
