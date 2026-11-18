# v76: a séták megállói: ha több megálló esik ugyanarra a helyre, egy jel látszik az aktuális (vagy a következő) megálló számával; a jelre kattintva a csoportban következő megállóra lép. Dupla gyűrű jelzi, hogy ott több megálló van.
import shutil
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
shutil.copy(p,'src/body_v60pre_before_v76.html');shutil.copy(cp,'src/style_v60pre_before_v76.css')
def rep(s,a,x,n=1):
    assert s.count(a)==n,(a[:60],s.count(a));return s.replace(a,x)
old='''  pts.forEach((c,k)=>{const g=el("g",{class:"wstop"+(k===wi?" cur":""),"data-k":k},gWalk);el("circle",{cx:c[0],cy:Y(c[1]),r:9},g);el("text",{x:c[0],y:Y(c[1])+3.5,"text-anchor":"middle"},g).textContent=k+1;g.addEventListener("click",ev=>{ev.stopPropagation();showStop(k);});});}'''
new='''  const grp=new Map();pts.forEach((c,k)=>{const key=Math.round(c[0])+","+Math.round(c[1]);if(!grp.has(key))grp.set(key,{c,ks:[]});grp.get(key).ks.push(k);});
  grp.forEach(({c,ks})=>{const show=ks.includes(wi)?wi:(ks.find(k=>k>wi)??ks[0]);
    const g=el("g",{class:"wstop"+(show===wi?" cur":"")+(ks.length>1?" multi":""),"data-k":show},gWalk);
    if(ks.length>1){el("circle",{cx:c[0],cy:Y(c[1]),r:12.5,class:"wring"},g);el("title",{},g).textContent=ks.map(k=>k+1).join(" · ");}
    el("circle",{cx:c[0],cy:Y(c[1]),r:9},g);el("text",{x:c[0],y:Y(c[1])+3.5,"text-anchor":"middle"},g).textContent=show+1;
    g.addEventListener("click",ev=>{ev.stopPropagation();const nx=show===wi&&ks.length>1?ks[(ks.indexOf(wi)+1)%ks.length]:show;showStop(nx);});});}'''
b=rep(b,old,new)
c=rep(c,'.walkg .wstop.cur text{fill:#fff}','.walkg .wstop.cur text{fill:#fff}\n.walkg .wstop circle.wring{fill:none;stroke:#b23a2a;stroke-width:1.5px;vector-effect:non-scaling-stroke}\n.walkg .wstop.cur circle.wring{fill:none}')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok')
