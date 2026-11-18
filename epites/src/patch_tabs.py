# v98: témacsoportok fülekkel a térkép alatti kártyákhoz
import shutil
TABS=[('bej','Bejárás','Exploring'),('gazd','Gazdaság','Economy'),('tars','Társadalom','Society'),('szam','A város számokban','The city in numbers'),('all','Minden kártya','All cards')]
def bar(l):
    i=1 if l=='hu' else 2
    L=['  <div class="grptabs" id="grptabs" role="tablist" aria-label="'+('Témacsoportok' if l=='hu' else 'Topic groups')+'">']
    for t in TABS:L.append(f'    <button role="tab" data-g="{t[0]}" aria-selected="false">{t[i]}</button>')
    L.append('  </div>');return L
JS='''/* v98: témacsoportok – a térkép alatti kártyák fülek szerint */
(function(){const bar=document.getElementById("grptabs"),low=document.querySelector(".lower");if(!bar||!low)return;
  const G={walkcard:"bej",foodcard:"gazd",chrecard:"gazd",orbiscard:"gazd",pricecard:"gazd",shipcard:"gazd",treecard:"gazd",occcard:"gazd tars",bldcard:"gazd",insccard:"tars",nmcard:"tars",agecard:"tars",plotcard:"tars",milcard:"tars",edbcard:"tars",listcard:"tars",origcard:"tars",dietcard:"tars",dprrcard:"tars",popcard:"szam",discard:"szam",regcard:"szam",notwrap:"bej"};
  const items=[...low.children].filter(e=>e.matches("section.card,details"));
  items.forEach(e=>{e.dataset.grp=G[e.id]||(e.querySelector("ol.aqlist")?"bej gazd":"bej");});      // azonosító nélkül: vízvezetékek, utak, korai keresztény Róma, a térkép olvasása
  const inG=(e,g)=>e.dataset.grp.split(" ").includes(g);const btns=[...bar.querySelectorAll("button")];let cur="bej";
  btns.forEach(b=>{const n=b.dataset.g==="all"?items.length:items.filter(e=>inG(e,b.dataset.g)).length;const s=document.createElement("span");s.className="gn";s.textContent=n;b.appendChild(s);});
  function show(g){cur=g;btns.forEach(b=>b.setAttribute("aria-selected",String(b.dataset.g===g)));
    document.querySelectorAll("[data-grp]").forEach(e=>{if(e.parentNode===low)e.hidden=!(g==="all"||inG(e,g));});
    try{sessionStorage.setItem("grp",g);}catch(_){}}
  btns.forEach(b=>b.addEventListener("click",()=>show(b.dataset.g)));
  let g0="bej";try{g0=sessionStorage.getItem("grp")||"bej";}catch(_){}
  show(btns.some(b=>b.dataset.g===g0)?g0:"bej");
  /* ha egy rejtett csoport kártyája kerül vissza a rácsba (például a dokkolt kártya bezárásakor), a fül szerint jelenjen meg */
  if(window.MutationObserver)new MutationObserver(()=>{items.forEach(e=>{if(e.parentNode===low)e.hidden=!(cur==="all"||inG(e,cur));else e.hidden=false;});}).observe(low,{childList:true});
})();
'''
CSS='''/* v98: témacsoportok fülei */
.grptabs{display:flex;flex-wrap:wrap;gap:6px;margin-top:22px;border-bottom:1px solid var(--line);padding-bottom:0}
.grptabs button{font:inherit;font-size:.95em;background:none;border:1px solid transparent;border-bottom:none;border-radius:6px 6px 0 0;padding:8px 14px;cursor:pointer;color:inherit;opacity:.75;margin-bottom:-1px}
.grptabs button:hover{opacity:1}
.grptabs button[aria-selected="true"]{background:var(--sheet);border-color:var(--line);opacity:1;font-weight:600}
.grptabs .gn{margin-left:6px;font-size:.8em;opacity:.6;font-weight:400}
.grptabs+.lower{margin-top:14px}
@media print{.grptabs{display:none}}
</style>'''
if __name__=='__main__':
    p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
    assert 'id="grptabs"' not in b and 'A kereskedők a kőfeliratokon' in b
    shutil.copy(p,'src/body_v60pre_before_v98.html');shutil.copy(cp,'src/style_v60pre_before_v98.css')
    a='  <div class="lower">';assert b.count(a)==1
    b=b.replace(a,'\n'.join(bar('hu'))+'\n'+a)
    a2='/* az adatlap-panel ne legyen magasabb a térképnél';assert b.count(a2)==1
    b=b.replace(a2,JS+a2)
    assert c.count('</style>')==1;c=c.replace('</style>',CSS)
    open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok')
