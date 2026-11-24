/* Drive mode: a mobile robot rendered from the 3D factory, driven over a rendered floor. */
(function(){
  var el=document.querySelector('.drive'); if(!el) return;
  var spd=el.querySelector('.dh-speed'),hd=el.querySelector('.dh-head'),st=el.querySelector('.dh-state');
  var botWrap=el.querySelector('.drive-bot'), bot=botWrap.querySelector('img'), tgt=el.querySelector('.drive-target');
  var M=window.__DRIVE; if(!M) return;
  // camera used for the renders (metres)
  var C=M.cam, T=M.look, F=M.fov*Math.PI/180, AR=16/9;
  function sub(a,b){return [a[0]-b[0],a[1]-b[1],a[2]-b[2]]} function dot(a,b){return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]}
  function cross(a,b){return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]} function nrm(a){var l=Math.hypot(a[0],a[1],a[2]);return [a[0]/l,a[1]/l,a[2]/l]}
  var f=nrm(sub(T,C)), r=nrm(cross(f,[0,1,0])), u=cross(r,f), th=Math.tan(F/2);
  function proj(x,z){var p=sub([x,0,z],C), zc=dot(p,f); return {x:(dot(p,r)/(zc*th*AR)+1)/2, y:(1-dot(p,u)/(zc*th))/2, d:zc}}
  function unproj(sx,sy){ // screen (0..1) -> floor point
    var nx=sx*2-1, ny=1-sy*2, dir=nrm([f[0]+r[0]*nx*th*AR+u[0]*ny*th, f[1]+r[1]*nx*th*AR+u[1]*ny*th, f[2]+r[2]*nx*th*AR+u[2]*ny*th]);
    if(dir[1]>=-1e-4) return null; var t=-C[1]/dir[1]; return [C[0]+dir[0]*t, C[2]+dir[2]*t]; }
  var base=proj(M.at[0],M.at[2]);
  var s={x:M.at[0],z:M.at[2],yaw:M.startYaw||0.5,v:0}, keys={}, goal=null, N=M.n, last=0, raf=0, cur=-1;
  var B=M.bounds; // [xmin,xmax,zmin,zmax]
  function frameFor(y){var k=Math.round(((y%(2*Math.PI))+2*Math.PI)%(2*Math.PI)/(2*Math.PI)*N)%N;return k}
  function place(){
    var W=el.clientWidth, H=el.clientHeight, p=proj(s.x,s.z), sc=base.d/p.d*(W/M.w);
    var k=frameFor(s.yaw); if(k!==cur){cur=k; bot.src=M.src.replace('{i}',String(k).padStart(2,'0'));}
    var o=M.off[k]; bot.style.left=(-o[0])+'px'; bot.style.top=(-o[1])+'px';
    botWrap.style.transform='translate('+(p.x*W)+'px,'+(p.y*H)+'px) scale('+sc+')';
    botWrap.style.zIndex=Math.round(p.y*1000);
  }
  // preload frames
  for(var i=0;i<N;i++){var im=new Image(); im.src=M.src.replace('{i}',String(i).padStart(2,'0'));}
  function step(t){
    var dt=Math.min(.05,(t-last)/1000||0); last=t;
    var fwd=(keys.f?1:0)-(keys.b?1:0), turn=(keys.l?1:0)-(keys.r?1:0);
    if(fwd||turn) goal=null;
    if(goal){var dx=goal[0]-s.x, dz=goal[1]-s.z, dist=Math.hypot(dx,dz);
      if(dist<.12){goal=null; tgt.classList.remove('on');}
      else{var want=Math.atan2(-dz,dx), d=((want-s.yaw+Math.PI*3)%(Math.PI*2))-Math.PI;
        turn=Math.max(-1,Math.min(1,d*2.2)); fwd=Math.abs(d)<0.6?Math.min(1,dist*1.2):0;}}
    s.yaw+=turn*2.4*dt;
    var tv=fwd*2.0; s.v+= (tv-s.v)*Math.min(1,dt*6);
    var nx=s.x+Math.cos(s.yaw)*s.v*dt, nz=s.z-Math.sin(s.yaw)*s.v*dt;
    s.x=Math.max(B[0],Math.min(B[1],nx)); s.z=Math.max(B[2],Math.min(B[3],nz));
    place(); var mv=Math.abs(s.v)>.05||!!turn; el.classList.toggle('moving',mv); if(spd){spd.textContent=Math.abs(s.v).toFixed(1); hd.textContent=Math.round(((s.yaw*180/Math.PI)%360+360)%360); st.textContent=goal?'Driving to target':(mv?'Manual drive':'Idle');}
    if(Math.abs(s.v)>.01||fwd||turn||goal) raf=requestAnimationFrame(step); else raf=0;
  }
  function kick(){ if(!raf){last=performance.now(); raf=requestAnimationFrame(step);} el.classList.add('used'); }
  var map={KeyW:'f',ArrowUp:'f',KeyS:'b',ArrowDown:'b',KeyA:'l',ArrowLeft:'l',KeyD:'r',ArrowRight:'r'};
  var active=false;
  function live(){active=true;el.classList.add('drv-on');if(document.activeElement!==el)el.focus({preventScroll:true});}
  el.querySelector('.drive-start button').addEventListener('click',function(e){e.stopPropagation();live();});
  el.querySelector('.drive-reset').addEventListener('click',function(e){e.stopPropagation();s.x=M.at[0];s.z=M.at[2];s.yaw=M.startYaw||.5;s.v=0;goal=null;tgt.classList.remove('on');place();if(st)st.textContent='Idle';});
  el.addEventListener('pointerdown',function(e){ if(e.target.closest('.drive-start,.drive-reset,.drive-hud')) return; live();
    if(e.target.closest('.drive-pad')) return;
    var R=el.getBoundingClientRect(), g=unproj((e.clientX-R.left)/R.width,(e.clientY-R.top)/R.height); if(!g) return;
    g=[Math.max(B[0],Math.min(B[1],g[0])),Math.max(B[2],Math.min(B[3],g[1]))]; goal=g;
    var p=proj(g[0],g[1]); tgt.style.left=(p.x*100)+'%'; tgt.style.top=(p.y*100)+'%'; tgt.classList.add('on'); kick(); });
  el.addEventListener('focusout',function(e){ if(e.relatedTarget&&el.contains(e.relatedTarget)) return; setTimeout(function(){ if(el.contains(document.activeElement)) return; active=false; keys={}; el.classList.remove('drv-on');},0);});
  el.querySelectorAll('button').forEach(function(b){b.addEventListener('mousedown',function(e){e.preventDefault();});});
  el.addEventListener('focus',function(){active=true; el.classList.add('drv-on');});
  window.addEventListener('keydown',function(e){ var k=map[e.code]; if(!k||!active) return; e.preventDefault(); keys[k]=true; kick(); });
  window.addEventListener('keyup',function(e){ var k=map[e.code]; if(k) keys[k]=false; });
  el.querySelectorAll('.drive-pad button').forEach(function(b){var k=b.dataset.k;
    b.addEventListener('pointerdown',function(e){e.preventDefault();active=true;keys[k]=true;kick();});
    ['pointerup','pointerleave','pointercancel'].forEach(function(ev){b.addEventListener(ev,function(){keys[k]=false;});});});
  window.addEventListener('resize',place);
  if('ResizeObserver' in window) new ResizeObserver(place).observe(el);
  place();
})();
