# v81: nagy nézet a táblázatos/grafikonos kártyákhoz: a térkép mellé tett kártya egy gombbal nagy ablakban nyitható (Esc vagy ✕ zárja); a grafikonok a nagyobb szélességhez igazodnak
import shutil
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'id="bigview"' not in b
shutil.copy(p,'src/body_v60pre_before_v81.html');shutil.copy(cp,'src/style_v60pre_before_v81.css')
def rep(s,a,x,n=1):
    assert s.count(a)==n,(a[:60],s.count(a));return s.replace(a,x)
b=rep(b,'<button id="dt-close" title="A kártya visszakerül a térkép alá">','<button id="dt-big" title="A kártya nagy ablakban, a részletek jobban látszanak">⤢ Nagy nézet</button><button id="dt-close" title="A kártya visszakerül a térkép alá">')
b=rep(b,'''    <aside class="panel" id="panel" aria-live="polite"></aside>
    </div>
  </div>''','''    <aside class="panel" id="panel" aria-live="polite"></aside>
    </div>
    <div class="bigview" id="bigview" hidden><div class="bvwin" role="dialog" aria-modal="true"><div class="bvbar"><span class="bvt" id="bvt"></span><button id="bv-close">Bezárás ✕</button></div><div class="bvbody" id="bvbody"></div></div></div>
  </div>''')
b=rep(b,'dtCard.addEventListener("click",()=>dockTab("card"));',
'''/* v81: nagy nézet */
const bigv=document.getElementById("bigview"),bvbody=document.getElementById("bvbody");
function openBig(){if(!docked)return;dockTab("card");bvbody.appendChild(docked);document.getElementById("bvt").textContent=dtCard.textContent;bigv.hidden=false;document.body.classList.add("bvopen");document.getElementById("bv-close").focus();}
function closeBig(){if(bigv.hidden)return;if(docked&&docked.parentNode===bvbody)dock.appendChild(docked);bigv.hidden=true;document.body.classList.remove("bvopen");}
document.getElementById("dt-big").addEventListener("click",openBig);document.getElementById("bv-close").addEventListener("click",closeBig);
bigv.addEventListener("click",e=>{if(e.target===bigv){closeBig();return;}if(e.target.closest&&e.target.closest("[data-go],[data-goto],#foodbtn,#aqflow,.regsel button"))setTimeout(closeBig,0);});
document.addEventListener("keydown",e=>{if(e.key==="Escape"&&!bigv.hidden){closeBig();e.stopPropagation();}},true);
dtCard.addEventListener("click",()=>dockTab("card"));''')
b=rep(b,'function undockCard(){if(!docked)return;','function undockCard(){if(!docked)return;closeBig();')
b=rep(b,'const c=docked,h=c.querySelector("h2");docked=null;dockPh.replaceWith(c);','const c=docked,h=c.querySelector("h2");docked=null;dockPh.replaceWith(c);')
# a kártya címére kattintás nagy nézetben ne csukja be a kártyát, csak a nagy nézetet
b=rep(b,'const tg=()=>{if(c.parentNode===dock){undockCard();return;}','const tg=()=>{if(c.parentNode===bvbody){closeBig();return;}if(c.parentNode===dock){undockCard();return;}')
b=rep(b,'W=Math.max(320,Math.min(900,box.clientWidth||660));H=W<520?240:300;','W=Math.max(320,Math.min(1600,box.clientWidth||660));H=W<520?240:Math.min(560,Math.max(300,Math.round(W*0.36)));')
b=rep(b,'const Wd=Math.max(320,Math.min(900,box.clientWidth||660)),H=Wd<520?180:220','const Wd=Math.max(320,Math.min(1600,box.clientWidth||660)),H=Wd<520?180:Math.min(420,Math.max(220,Math.round(Wd*0.28)))')
c=rep(c,'</style>','''/* v81: nagy nézet */
.main:not(.dockwide) #dt-big{display:none}
.docktabs #dt-big{border:1px solid var(--line);border-radius:999px;padding:4px 10px;font-size:12px;align-self:center;margin-bottom:4px;background:var(--sheet);color:var(--ink);margin-left:auto}
.main.dockwide .docktabs #dt-big+#dt-close{margin-left:6px}
.docktabs #dt-big:hover{border-color:var(--accent);color:var(--accent)}
.bigview{position:fixed;inset:0;background:rgba(10,14,15,.55);z-index:1000;display:flex;align-items:center;justify-content:center}
.bigview[hidden]{display:none}
.bvwin{background:var(--sheet);border:1px solid var(--line);border-radius:8px;width:min(1500px,94vw);height:92vh;display:flex;flex-direction:column;box-shadow:0 10px 40px rgba(0,0,0,.35)}
.bvbar{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 16px;border-bottom:1px solid var(--line);font:600 14px var(--font-body)}
.bvbar button{font:500 13px var(--font-body);padding:5px 12px;border:1px solid var(--line);border-radius:999px;background:var(--sheet);color:var(--ink);cursor:pointer}
.bvbar button:hover{border-color:#b23a2a;color:#b23a2a}
.bvbody{overflow:auto;flex:1 1 auto;padding:4px 18px 18px}
.bvbody section.card{border:none;box-shadow:none;margin:0;max-width:none;width:auto;font-size:15px}
.bvbody .regtab{font-size:14px}
.bvbody .aqrow{grid-template-columns:200px 1fr;font-size:14px}
body.bvopen{overflow:hidden}
</style>''')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok')
