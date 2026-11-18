/* v109: katasztrofak - a tuzvesz eve a terkepen (dis/data.py) */
const DISF=__DISF__;
var disYear=null;
(function(){const card=document.getElementById("discard");if(!card)return;const st=document.getElementById("disstat"),en=document.documentElement.lang==="en";let on=[];
  const fy=y=>en?(y<0?(-y)+" BC":"AD "+y):(y<0?"Kr. e. "+(-y):"Kr. u. "+y);
  function clear(){on.forEach(id=>{if(nodes[id])nodes[id].g.classList.remove("burn");});on=[];card.querySelectorAll(".cur").forEach(r=>r.classList.remove("cur"));st.hidden=true;}
  function show(y){clear();const ids=DISF[y];if(!ids)return;ids.forEach(id=>{if(nodes[id]){nodes[id].g.classList.add("burn");on.push(id);}});
    card.querySelectorAll('[data-fy="'+y+'"]').forEach(r=>r.classList.add("cur"));
    st.firstElementChild.textContent=st.querySelector(on.length?".dn":".dz").textContent.replace("{y}",fy(y)).replace("{n}",on.length);st.hidden=false;}
  function fit(){if(!on.length)return;let x0=1e9,x1=-1e9,y0=1e9,y1=-1e9;on.forEach(id=>{const c=nodes[id].m._c;if(!c)return;x0=Math.min(x0,c[0]);x1=Math.max(x1,c[0]);y0=Math.min(y0,-c[1]);y1=Math.max(y1,-c[1]);});if(x0>x1)return;
    const ar=vb[3]/vb[2],w=Math.max(vb[2],(x1-x0)*1.5+200,((y1-y0)*1.5+200)/ar),h=w*ar;setVB([(x0+x1)/2-w/2,(y0+y1)/2-h/2,w,h]);}
  disYear=function(y){if(y==="all"||!DISF[y])clear();else show(y);};
  card.querySelectorAll("svg [data-fy], tr[data-fy] .fgo").forEach(el=>el.addEventListener("click",e=>{e.preventDefault();const y=+el.closest("[data-fy]").dataset.fy;setYear(y);fit();}));
  document.getElementById("disclr").addEventListener("click",clear);
  disYear(state.year);
})();
