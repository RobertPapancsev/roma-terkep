# v80: (1) a térkép mellé dokkolt kártya 50%-kal szélesebb (400 -> 600 px), ha táblázat vagy grafikon van benne; (2) a séták megállóinál a térkép mindig a megállóra áll, ésszerű nagyítással (220–520 m széles nézet)
import shutil
p='body_v60pre.html';b=open(p,encoding='utf8').read();cp='style_v60pre.css';c=open(cp,encoding='utf8').read()
shutil.copy(p,'src/body_v60pre_before_v80.html');shutil.copy(cp,'src/style_v60pre_before_v80.css')
def rep(s,a,x,n=1):
    assert s.count(a)==n,(a[:60],s.count(a));return s.replace(a,x)
b=rep(b,'function undockCard(){if(!docked)return;const c=docked,h=c.querySelector("h2");',
'function undockCard(){if(!docked)return;document.querySelector(".main").classList.remove("dockwide");syncPanel();const c=docked,h=c.querySelector("h2");')
b=rep(b,'dock.appendChild(c);docked=c;c.classList.add("open","docked");',
'dock.appendChild(c);docked=c;c.classList.add("open","docked");document.querySelector(".main").classList.toggle("dockwide",!!c.querySelector("table,svg,.aqchart,.foodbar,.foodest,.popchart,.bldchart"));syncPanel();setTimeout(()=>{if(typeof setVB==="function")setVB(vb.slice());},60);')
b=rep(b,'''  select(st.id);drawWalk();}''','''  {const c=(nodes[st.id]&&nodes[st.id].m._c)||WCX[st.id];if(c&&isFinite(c[0])&&isFinite(c[1])){const w=Math.min(Math.max(vb[2],220),520),h=w*vb[3]/vb[2];setVB([c[0]-w/2,-c[1]-h/2,w,h]);}}
  select(st.id);drawWalk();}''')
c=rep(c,'@media (max-width:1020px){.main{grid-template-columns:1fr}}','.main.dockwide{grid-template-columns:minmax(0,1fr) min(600px,46vw)}\n@media (max-width:1020px){.main,.main.dockwide{grid-template-columns:1fr}}')
c=rep(c,'.docktabs button{font:500 13px var(--font-body);padding:6px 12px;border:1px solid var(--line);border-bottom:none;border-radius:6px 6px 0 0;background:var(--paper);color:var(--muted);cursor:pointer;max-width:190px;','.docktabs button{font:500 13px var(--font-body);padding:6px 12px;border:1px solid var(--line);border-bottom:none;border-radius:6px 6px 0 0;background:var(--paper);color:var(--muted);cursor:pointer;max-width:260px;')
b=rep(b,'?Math.max(360,a.offsetHeight)+"px":"";};','?Math.max(360,a.offsetHeight,document.querySelector(".main").classList.contains("dockwide")?innerHeight-24:0)+"px":"";};')
open(p,'w',encoding='utf8').write(b);open(cp,'w',encoding='utf8').write(c);print('ok')
