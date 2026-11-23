/* Scales the 1920px-wide case study to fit its container, keeping text sharp. */
(function(){
  function fit(wrap){
    var cs=wrap.querySelector('.q100cs'); if(!cs) return;
    var s=Math.min(1,wrap.clientWidth/1920);
    cs.style.transform='scale('+s+')';
    wrap.style.height=Math.ceil(cs.offsetHeight*s)+'px';
  }
  function init(){
    document.querySelectorAll('.q100cs-wrap').forEach(function(w){
      fit(w);
      if('ResizeObserver' in window){ new ResizeObserver(function(){fit(w)}).observe(w); }
      else { window.addEventListener('resize',function(){fit(w)}); }
      w.querySelectorAll('img').forEach(function(i){ if(!i.complete) i.addEventListener('load',function(){fit(w)}); });
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(init);
})();
