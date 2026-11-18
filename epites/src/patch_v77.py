# v77: a lenyitott kártya széles képernyőn a térkép mellé, a jobb oldali oszlopba kerül (fülek: a kártya és az Adatlap); bezáráskor visszakerül a helyére
import shutil
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
assert 'id="dock"' not in b
shutil.copy(p,'src/body_v60pre_before_v77.html');shutil.copy(cp,'src/style_v60pre_before_v77.css')
def rep(s,a,x,n=1):
    assert s.count(a)==n,(a[:60],s.count(a));return s.replace(a,x)
b=rep(b,'    <aside class="panel" id="panel" aria-live="polite"></aside>',
'''    <div class="side" id="side">
      <div class="docktabs" id="docktabs" role="tablist" hidden><button id="dt-card" role="tab" aria-selected="true"></button><button id="dt-info" role="tab" aria-selected="false">Adatlap</button><button id="dt-close" title="A kártya visszakerül a térkép alá">Vissza a térkép alá ✕</button></div>
      <div class="dock" id="dock" hidden></div>
    <aside class="panel" id="panel" aria-live="polite"></aside>
    </div>''')
old_fold='''  const tg=()=>{const o=c.classList.toggle("open");h.setAttribute("aria-expanded",String(o));};'''
new_fold='''  const tg=()=>{if(c.parentNode===dock){undockCard();return;}if(!c.classList.contains("open")&&canDock()){dockCard(c);return;}const o=c.classList.toggle("open");h.setAttribute("aria-expanded",String(o));};'''
b=rep(b,old_fold,new_fold)
# a kártya-csukó kód elé: a dokk függvényei
b=rep(b,'/* helytakarékos kártyák: a térkép alatti kártyák címsorra csukva jelennek meg, kattintásra nyílnak */',
'''/* v77: a lenyitott kártya széles képernyőn a térkép mellé kerül (dokk), fülekkel válthat az adatlapra; bezáráskor visszamegy a helyére */
const side=document.getElementById("side"),dock=document.getElementById("dock"),dtabs=document.getElementById("docktabs"),dtCard=document.getElementById("dt-card"),dtInfo=document.getElementById("dt-info");
let docked=null,dockPh=null,dockMuted=false;
const canDock=()=>innerWidth>1020&&getComputedStyle(side).position==="sticky";
function dockTab(t){const k=t==="card"&&!!docked;dock.hidden=!k;panel.hidden=k;dtCard.setAttribute("aria-selected",String(k));dtInfo.setAttribute("aria-selected",String(!k));if(k)dock.scrollTop=0;}
function undockCard(){if(!docked)return;const c=docked,h=c.querySelector("h2");docked=null;dockPh.replaceWith(c);dockPh=null;c.classList.remove("open","docked");if(h)h.setAttribute("aria-expanded","false");dtabs.hidden=true;dock.hidden=true;panel.hidden=false;}
function dockCard(c){undockCard();const h=c.querySelector("h2");dockPh=document.createComment("dock");c.replaceWith(dockPh);dock.appendChild(c);docked=c;c.classList.add("open","docked");if(h)h.setAttribute("aria-expanded","true");
  dtCard.textContent=h?(h.firstChild&&h.firstChild.nodeType===3?h.firstChild.textContent:h.textContent).trim():"";dtabs.hidden=false;dockTab("card");
  const r=document.querySelector(".mapbox").getBoundingClientRect();if(r.top<-40||r.top>innerHeight*0.5)document.querySelector(".main").scrollIntoView({block:"start"});}
dtCard.addEventListener("click",()=>dockTab("card"));dtInfo.addEventListener("click",()=>dockTab("info"));document.getElementById("dt-close").addEventListener("click",undockCard);
/* ha a térképen vagy a kártyán valamit kiválasztanak, az adatlap jelenik meg */
if(window.MutationObserver)new MutationObserver(()=>{if(docked&&!dock.hidden)dockTab("info");}).observe(panel,{childList:true});
addEventListener("resize",()=>{if(docked&&!canDock())undockCard();});
/* helytakarékos kártyák: a térkép alatti kártyák címsorra csukva jelennek meg, kattintásra nyílnak */''')
b=rep(b,'''const syncPanel=()=>{const a=panel.previousElementSibling;if(!a)return;panel.style.maxHeight=(innerWidth>900&&getComputedStyle(panel).position!=="static")?Math.max(360,a.offsetHeight)+"px":"";};
if(window.ResizeObserver&&panel.previousElementSibling)new ResizeObserver(syncPanel).observe(panel.previousElementSibling);addEventListener("resize",syncPanel);syncPanel();''',
'''const syncPanel=()=>{const a=side.previousElementSibling;if(!a)return;side.style.maxHeight=(innerWidth>900&&getComputedStyle(side).position!=="static")?Math.max(360,a.offsetHeight)+"px":"";};
if(window.ResizeObserver&&side.previousElementSibling)new ResizeObserver(syncPanel).observe(side.previousElementSibling);addEventListener("resize",syncPanel);syncPanel();''')
c=rep(c,'aside.panel{background:var(--sheet);border:1px solid var(--line);border-radius:6px;padding:18px 20px;position:sticky;top:12px;max-height:calc(100vh - 24px);overflow:auto}\n@media (max-width:1020px){aside.panel{position:static;max-height:none}}',
'''aside.panel{background:var(--sheet);border:1px solid var(--line);border-radius:6px;padding:18px 20px;overflow:auto;flex:1 1 auto;min-height:0}
.side{position:sticky;top:12px;max-height:calc(100vh - 24px);display:flex;flex-direction:column;min-width:0}
@media (max-width:1020px){.side{position:static;max-height:none!important}}
/* v77: a térkép mellé dokkolt kártya */
.docktabs{display:flex;gap:4px;align-items:flex-end;flex:none;margin-bottom:-1px;position:relative;z-index:1}
.docktabs[hidden],.dock[hidden],aside.panel[hidden]{display:none}
.docktabs button{font:500 13px var(--font-body);padding:6px 12px;border:1px solid var(--line);border-bottom:none;border-radius:6px 6px 0 0;background:var(--paper);color:var(--muted);cursor:pointer;max-width:190px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.docktabs button[aria-selected=true]{background:var(--sheet);color:var(--ink);font-weight:600}
.docktabs #dt-close{margin-left:auto;border:1px solid var(--line);border-radius:999px;padding:4px 10px;font-size:12px;align-self:center;margin-bottom:4px;background:var(--sheet)}
.docktabs #dt-close:hover{border-color:#b23a2a;color:#b23a2a}
.dock{background:var(--sheet);border:1px solid var(--line);border-radius:0 6px 6px 6px;overflow:auto;flex:1 1 auto;min-height:0}
.dock section.card.docked{border:none;margin:0;box-shadow:none;border-radius:0;width:auto;max-width:none}
.dock .regwrap{max-width:100%}''')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok')
