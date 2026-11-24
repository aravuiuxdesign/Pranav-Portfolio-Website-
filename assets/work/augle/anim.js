/* Motion + interaction layer. Static exports (headless) and reduced-motion get a calm page. */
(function () {
  const root = document.documentElement;
  const headless = navigator.webdriver;
  if (headless) document.querySelectorAll('img[loading="lazy"]').forEach(i => { i.loading = 'eager'; });
  const reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---- before/after sliders (always interactive) ----
  document.querySelectorAll('[data-ba]').forEach(el => {
    const set = x => { const r = el.getBoundingClientRect(); el.style.setProperty('--p', Math.max(2, Math.min(98, (x - r.left) / r.width * 100)) + '%'); };
    let drag = false, touched = false;
    el.addEventListener('pointerdown', e => { drag = true; touched = true; el.setPointerCapture(e.pointerId); set(e.clientX); });
    el.addEventListener('pointermove', e => { if (drag) set(e.clientX); });
    el.addEventListener('pointerup', () => drag = false);
    el.tabIndex = 0; el.setAttribute('role', 'slider'); el.setAttribute('aria-label', 'Before and after comparison');
    el.addEventListener('keydown', e => { const cur = parseFloat(getComputedStyle(el).getPropertyValue('--p')) || 50; if (e.key === 'ArrowLeft') { el.style.setProperty('--p', Math.max(2, cur - 5) + '%'); touched = true; } if (e.key === 'ArrowRight') { el.style.setProperty('--p', Math.min(98, cur + 5) + '%'); touched = true; } });
    if (!headless && !reduce) {
      let seen = false;
      new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting && !seen) { seen = true; const t0 = performance.now(); (function wob(now) { if (touched) return; const k = (now - t0) / 1000; if (k > 2.6) { el.style.setProperty('--p', '50%'); return; } el.style.setProperty('--p', (50 + Math.sin(k * 2.4) * 22 * (1 - k / 2.6)) + '%'); requestAnimationFrame(wob); })(t0); } }), { threshold: .5 }).observe(el);
    }
  });

  if (headless) return;
  root.classList.add('web');
  const navEl=document.querySelector('.site-nav'), navLinks=navEl?[...navEl.querySelectorAll('.nav-links a')]:[];
  const navTargets=navLinks.map(a=>document.querySelector(a.getAttribute('href')));
  const navScroll=()=>{ if(!navEl) return; navEl.classList.toggle('scrolled',scrollY>10); let k=-1; navTargets.forEach((t,i)=>{ if(t&&t.getBoundingClientRect().top<innerHeight*.35) k=i; }); navLinks.forEach((a,i)=>a.classList.toggle('on',i===k)); };
  addEventListener('scroll',navScroll,{passive:true}); navScroll();

  // ---- videos: play only while visible ----
  const vio = new IntersectionObserver(es => es.forEach(e => { const v = e.target; if (e.isIntersecting && !reduce) { const p = v.play(); if (p && p.catch) p.catch(() => {}); } else v.pause(); }), { threshold: 0.15 });
  document.querySelectorAll('video').forEach(v => vio.observe(v));

  // ---- progress bar + chapter nav ----
  const bar = document.getElementById('progress'), nav = document.querySelector('.cnav');
  const chaps = [...document.querySelectorAll('[data-chap]')];
  const links = nav ? [...nav.querySelectorAll('a')] : [];
  const tours = [...document.querySelectorAll('.tour-live')];
  let ticking = false;
  function onScroll() {
    if (ticking) return; ticking = true;
    requestAnimationFrame(() => {
      ticking = false;
      const vh = innerHeight, sh = document.documentElement.scrollHeight - vh;
      if (bar) bar.style.transform = 'scaleX(' + (scrollY / sh) + ')';
      if (nav) {
        nav.classList.toggle('show', scrollY > vh * 0.9);
        let cur = null; chaps.forEach(c => { if (c.getBoundingClientRect().top < vh * 0.45) cur = c.dataset.chap; });
        links.forEach(a => a.classList.toggle('on', a.dataset.c === cur));
      }
      tours.forEach(t => {
        const r = t.getBoundingClientRect(), total = r.height - vh;
        const p = Math.max(0, Math.min(0.9999, -r.top / total));
        const n = t.querySelectorAll('.tour-media img').length, i = Math.floor(p * n);
        if (t.__i !== i) { t.__i = i;
          t.querySelectorAll('.tour-media img').forEach((im, k) => im.classList.toggle('on', k === i));
          t.querySelectorAll('.tour-list button').forEach((b, k) => b.classList.toggle('on', k === i)); }
        const fill = t.querySelector('.tour-bar i'); if (fill) fill.style.width = (p * 100) + '%';
      });
    });
  }
  addEventListener('scroll', onScroll, { passive: true }); addEventListener('resize', onScroll); onScroll();
  tours.forEach(t => t.querySelectorAll('.tour-list button').forEach((b, k, all) => b.addEventListener('click', () => {
    const r = t.getBoundingClientRect(), total = r.height - innerHeight; scrollTo({ top: scrollY + r.top + total * (k + 0.5) / all.length, behavior: 'smooth' });
  })));

  if (reduce) return;
  root.classList.add('anim');
  onScroll();

  // ---- headline word reveal ----
  document.querySelectorAll('.pn .d1, .pn .h1, .pn .h2').forEach(h => {
    const walk = node => [...node.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        const f = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(w => { if (!w) return; if (/^\s+$/.test(w)) { f.appendChild(document.createTextNode(w)); return; }
          const s = document.createElement('span'); s.className = 'w'; const i = document.createElement('i'); i.textContent = w; s.appendChild(i); f.appendChild(s); });
        n.replaceWith(f);
      } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n);
    });
    walk(h); h.querySelectorAll('.w>i').forEach((i, k) => i.style.transitionDelay = (k * 0.05) + 's'); h.setAttribute('data-r', 'h');
  });
  // section labels / paragraphs reveal too
  document.querySelectorAll('.pn .sh .p, .pn .chap .p, .pn .lab').forEach(el => { if (!el.hasAttribute('data-r')) el.setAttribute('data-r', ''); });

  // stagger within each section
  const counts = new Map();
  document.querySelectorAll('[data-r]:not([data-r="h"])').forEach(el => {
    const sec = el.closest('section') || document.body; const n = counts.get(sec) || 0; counts.set(sec, n + 1);
    el.style.setProperty('--d', (Math.min(n % 5, 4) * 0.07) + 's');
  });

  // ---- count-up ----
  const nums = [...document.querySelectorAll('.num:not([data-nocount])')].filter(n => n.firstChild && n.firstChild.nodeType === 3 && /^~?\d+$/.test(n.firstChild.textContent.trim()) && +n.firstChild.textContent.replace('~', '') > 4);
  nums.forEach(n => n.dataset.to = n.firstChild.textContent.trim());
  const count = n => { const raw = n.dataset.to, pre = raw[0] === '~' ? '~' : '', to = +raw.replace('~', ''), t0 = performance.now();
    (function st(now) { const k = Math.min(1, (now - t0) / 1400), e = 1 - Math.pow(1 - k, 3); n.firstChild.textContent = pre + Math.round(to * e); if (k < 1) requestAnimationFrame(st); })(t0); };

  const io = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    e.target.classList.add('in');
    if (e.target.dataset.to) count(e.target);
    if (e.target.querySelector && e.target.querySelector('.quad')) setTimeout(() => window.__fitQuads && window.__fitQuads(), 50);
    io.unobserve(e.target);
  }), { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
  document.querySelectorAll('[data-r]').forEach(el => io.observe(el));
  nums.forEach(n => io.observe(n));
})();
/* day-cycle sync (clock chip + timeline) */
(function(){
  const v=document.querySelector('.daystage video'); if(!v) return;
  const segs=[...document.querySelectorAll('.daytrack .seg')], dot=document.querySelector('.daydot'), t=document.querySelector('.clock-t'), ph=document.querySelector('.clock-p'), fi=document.querySelector('.clock .fi');
  const hourAt=u=>u<.7?6+13.6*(u/.7):19.6+10.4*((u-.7)/.3);
  const names=['Morning','Afternoon','Evening','Night'], icons=['◐','☀','◑','☾'];
  function tick(){
    if(v.duration){
      const u=(v.currentTime/v.duration)%1, h=hourAt(u)%24, hh=Math.floor(h), mm=Math.floor((h-hh)*60);
      if(t) t.textContent=String(hh).padStart(2,'0')+':'+String(mm).padStart(2,'0');
      let k=segs.findIndex(s=>u>=+s.dataset.a&&u<+s.dataset.b); if(k<0)k=3;
      segs.forEach((s,i)=>s.classList.toggle('on',i===k));
      if(ph) ph.textContent=names[k]+' · live lighting'; if(fi) fi.textContent=icons[k];
      if(dot){dot.style.left=(u*100)+'%'; const dt=dot.querySelector('.dot-t'); if(dt&&t) dt.textContent=t.textContent;}
    }
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
})();

/* live "after" hero: video playlist + product carousel, like the new site */
(function(){
  if(navigator.webdriver) return;
  document.querySelectorAll('.lh').forEach(function(lh){
    var vids=[].slice.call(lh.querySelectorAll('video')), slides=[].slice.call(lh.querySelectorAll('.lh-slide')),
        dots=[].slice.call(lh.querySelectorAll('.lh-dots i')), t=lh.querySelector('.lh-t'), titles=lh.dataset.titles.split('|');
    var vi=0, si=0, timer=null, visible=false, reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
    function load(v){ if(!v.src) { v.src=v.dataset.src; v.load(); } }
    function playV(){ var v=vids[vi]; load(v); var p=v.play(); if(p&&p.catch)p.catch(function(){}); load(vids[(vi+1)%vids.length]); }
    vids.forEach(function(v,i){ v.addEventListener('ended',function(){ if(i!==vi) return; var n=(vi+1)%vids.length; vids[n].currentTime=0; vi=n; playV(); vids.forEach(function(x,j){x.classList.toggle('on',j===vi);}); }); });
    function go(n){
      var prev=si; si=n;
      slides.forEach(function(s,i){ s.classList.toggle('is-active',i===si); s.classList.toggle('is-prev',i===prev&&prev!==si); });
      dots.forEach(function(d,i){ d.classList.toggle('on',i===si); d.classList.toggle('done',i<si); });
      t.classList.add('out'); setTimeout(function(){ t.textContent=titles[si]; t.classList.remove('out'); },250);
      // restart the fill animation
      var b=dots[si].querySelector('b'); b.style.display='none'; void b.offsetWidth; b.style.display='';
    }
    function start(){ if(timer||reduce) return; lh.classList.add('run'); timer=setInterval(function(){ go((si+1)%slides.length); },5600); }
    function stop(){ clearInterval(timer); timer=null; }
    new IntersectionObserver(function(es){ es.forEach(function(e){
      visible=e.isIntersecting;
      if(visible){ playV(); start(); } else { vids.forEach(function(v){v.pause();}); stop(); }
    }); },{threshold:.2}).observe(lh);
  });
})();
/* camera clock */
(function(){var c=[].slice.call(document.querySelectorAll('.vclock'));if(!c.length)return;var t0=Date.now(),base=12*3600+20*60+14;
setInterval(function(){var s=base+Math.floor((Date.now()-t0)/1000),h=Math.floor(s/3600)%24,m=Math.floor(s/60)%60,x=s%60;var v=[h,m,x].map(function(n){return String(n).padStart(2,'0')}).join(':');c.forEach(function(e){e.textContent=v})},1000);})();
/* frame-locked ROI tracking */
(function(){
  var boxes=[].slice.call(document.querySelectorAll('.roi.trk')); if(!boxes.length) return;
  Promise.resolve(JSON.parse((document.getElementById('vtracks')||{}).textContent||'{}')).then(function(T){
    document.querySelectorAll('.vcam').forEach(function(cam){
      var v=cam.querySelector('video'), bs=[].slice.call(cam.querySelectorAll('.roi.trk')); if(!v||!bs.length) return;
      function draw(){
        bs.forEach(function(b){var a=T[b.dataset.k][b.dataset.n], n=a.length, f=Math.floor(v.currentTime*24+0.001)%n, p=a[f];
          b.style.left=p[0]+'%';b.style.top=p[1]+'%';b.style.width=p[2]+'%';b.style.height=p[3]+'%';b.classList.toggle('off',!p[4]);});
      }
      if(v.requestVideoFrameCallback){var cb=function(){draw();v.requestVideoFrameCallback(cb)};v.requestVideoFrameCallback(cb);}
      else{(function loop(){draw();requestAnimationFrame(loop)})();}
      v.addEventListener('seeked',draw); draw();
    });
  });
})();
