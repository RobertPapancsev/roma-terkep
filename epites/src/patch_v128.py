# v128: „Róma népessége” – táblázatsorra kattintva a grafikon (és alatta a leírás) a látómezőbe gördül, ha nem látszik,
# és a kijelölt jel kétszer felvillan. Eddig a kijelölés a táblázat fölötti, kigördült grafikonon történt, így „nem történt semmi”.
import shutil
p = 'body_v60pre.html'; b = open(p, encoding='utf8').read()
assert 'popInView' not in b
shutil.copy(p, 'src/body_v60pre_before_v128.html')
def rep(a, x):
    global b; assert b.count(a) == 1, a[:60]; b = b.replace(a, x)
rep('  Object.values(rows).forEach(r=>r.addEventListener("click",()=>show(r.dataset.p)));',
    '  const popInView=e=>{const r=e.getBoundingClientRect();let q=e.parentElement;while(q){const cs=getComputedStyle(q);if(/(auto|scroll)/.test(cs.overflowY)&&q.scrollHeight>q.clientHeight){const o=q.getBoundingClientRect();if(r.top<o.top||r.bottom>o.bottom)return false;}q=q.parentElement;}return r.top>=0&&r.bottom<=innerHeight;};\n'
    '  Object.values(rows).forEach(r=>r.addEventListener("click",()=>{show(r.dataset.p);const tg=info||box;if(!popInView(box)||!popInView(tg))box.scrollIntoView({behavior:"smooth",block:"start"});\n'
    '    box.querySelectorAll("[data-p]").forEach(e=>{e.classList.remove("flash");if(e.dataset.p===r.dataset.p){void e.getBBox();e.classList.add("flash");}});}));')
open(p, 'w', encoding='utf8').write(b)
cp = 'style_v60pre.css'; c = open(cp, encoding='utf8').read(); shutil.copy(cp, 'src/style_v60pre_before_v128.css')
a = '.poptab tr.on{background:rgba(31,95,168,.12)}'; assert c.count(a) == 1
c = c.replace(a, a + '\n.popsvg [data-p].flash{animation:popfl .6s ease-in-out 3}\n@keyframes popfl{50%{opacity:.15}}')
open(cp, 'w', encoding='utf8').write(c); print('ok')
