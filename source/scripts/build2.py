# Builds src/Case-Augle.dc.html — v2: tighter, visual, recruiter-first case study in the portfolio theme
import re
SRC = open('/home/claude/pf/aug/build.py').read()
TEMPLATE = SRC[SRC.index("page = f'''"):SRC.index("open('/home/claude/pf/src/Case-Augle.dc.html'")]
base_css = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&amp;display=swap">\n'
            + open('/home/claude/pf/aug/base_css.txt').read())

CSS = r"""
/* ===== augle case study v2 ===== */
.ag{--ink:#0B0D14;--mut:#5E6372;--line:#E7EBF2;--soft:#F6F8FB;--blue:#2D5BFF;--bt:#EEF2FF;--gx:clamp(20px,5vw,112px);--sy:clamp(88px,8.5vw,152px)}
.ag .wrap{max-width:1440px;margin:0 auto;padding:0 var(--gx)}
.ag .it{font-family:'Instrument Serif',Georgia,serif;font-style:italic;font-weight:400;letter-spacing:-.01em;color:var(--blue)}
.ag .k{font:500 11.5px 'Geist Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}
.ag .pill-k{display:inline-flex;align-items:center;gap:8px;height:32px;padding:0 12px 0 6px;border-radius:999px;background:#FFF;border:1px solid var(--line);font:500 11.5px 'Geist Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--ink)}
.ag .pill-k b{display:grid;place-items:center;min-width:22px;height:22px;padding:0 6px;border-radius:999px;background:var(--blue);color:#FFF;font-weight:500}
.ag h1{margin:22px 0 0;font-size:clamp(52px,8vw,148px);line-height:.92;letter-spacing:-.055em;font-weight:400;color:var(--ink)}
.ag h2{margin:18px 0 0;font-size:clamp(34px,3.8vw,64px);line-height:1;letter-spacing:-.04em;font-weight:400;color:var(--ink);max-width:18ch}
.ag h3{margin:0;font-size:clamp(19px,1.45vw,24px);line-height:1.2;letter-spacing:-.02em;font-weight:500;color:var(--ink)}
.ag p{margin:0;color:#3A4152;font-size:clamp(16px,1.08vw,18px);line-height:1.65}
.ag .lead{font-size:clamp(19px,1.6vw,26px);line-height:1.42;letter-spacing:-.015em;color:var(--ink);max-width:40ch}
.ag section{padding:var(--sy) 0 0}
.ag .sh{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:24px;margin-bottom:clamp(36px,3.6vw,64px)}
.ag .sh .lead{max-width:34ch;color:var(--mut);font-size:clamp(16px,1.15vw,19px)}
/* hero */
.ag .hero{padding:clamp(140px,13vw,210px) 0 0}
.ag .hero .sub{margin-top:clamp(24px,2.4vw,40px);max-width:52ch;color:var(--mut);font-size:clamp(17px,1.25vw,21px);line-height:1.55}
.ag .meta{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0;margin-top:clamp(40px,4vw,72px);border-top:1px solid var(--line)}
.ag .meta>div{padding:20px 24px 0 0}.ag .meta>div+div{padding-left:24px;border-left:1px solid var(--line)}
.ag .meta p{margin-top:10px;font-size:15px;line-height:1.5;color:var(--ink)}
.ag .heroimg{margin-top:clamp(48px,5vw,88px);border-radius:28px;overflow:hidden;background:var(--soft)}
.ag .heroimg img{display:block;width:100%;height:auto}
/* tldr + numbers */
.ag .tldr{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(12px,1.2vw,20px)}
.ag .tldr>div{padding:clamp(22px,2vw,32px);border-radius:24px;background:var(--soft);border:1px solid var(--line)}
.ag .tldr p{margin-top:12px;font-size:15.5px;line-height:1.55;color:var(--ink)}
.ag .nums{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));margin-top:clamp(12px,1.2vw,20px);border-radius:24px;background:#FFF;border:1px solid var(--line)}
.ag .nums>div{padding:clamp(22px,2.2vw,36px)}.ag .nums>div+div{border-left:1px solid var(--line)}
.ag .nums b{display:block;font-size:clamp(40px,4vw,68px);font-weight:400;letter-spacing:-.05em;line-height:1;color:var(--ink)}
.ag .nums b small{font-size:.45em;letter-spacing:-.02em;color:var(--blue);margin-left:4px}
.ag .nums span{display:block;margin-top:10px;font-size:14px;line-height:1.45;color:var(--mut)}
/* cards */
.ag .g2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(12px,1.2vw,20px)}
.ag .g3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(12px,1.2vw,20px)}
.ag .g4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(12px,1.2vw,20px)}
.ag .cd{padding:clamp(22px,2vw,32px);border-radius:24px;background:#FFF;border:1px solid var(--line);transition:transform .6s cubic-bezier(.22,1,.36,1),box-shadow .6s}
.ag .cd.soft{background:var(--soft)}
.ag .cd:hover{transform:translateY(-3px);box-shadow:0 30px 60px -44px rgba(20,40,130,.4)}
.ag .cd .n{display:inline-block;margin-bottom:18px;padding:4px 9px;border-radius:999px;background:var(--bt);color:var(--blue);font:500 11.5px 'Geist Mono',monospace}
.ag .cd p{margin-top:10px;font-size:15.5px;line-height:1.55}
.ag .cd ul{margin:14px 0 0;padding:0;list-style:none}
.ag .cd li{position:relative;padding:9px 0 9px 22px;border-top:1px solid var(--line);font-size:15px;line-height:1.5;color:#3A4152}
.ag .cd li:first-child{border-top:0}
.ag .cd li::before{content:"";position:absolute;left:2px;top:17px;width:8px;height:8px;border-radius:50%;background:var(--blue)}
.ag .ins .f{display:block;margin-top:16px;padding-top:14px;border-top:1px solid var(--line);font-size:14.5px;line-height:1.5;color:var(--ink)}
.ag .ins .f b{display:block;margin-bottom:4px;font:500 11px 'Geist Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--blue)}
.ag .quote{padding:clamp(28px,3.4vw,56px);border-radius:28px;background:radial-gradient(60% 100% at 100% 0%,rgba(45,91,255,.08),transparent 70%),var(--soft);border:1px solid var(--line)}
.ag .quote p{font-size:clamp(26px,2.7vw,46px);line-height:1.12;letter-spacing:-.03em;color:var(--ink);max-width:26ch}
/* figures */
.ag figure{margin:0}
.ag figure .im{border-radius:20px;overflow:hidden;background:var(--soft);border:1px solid var(--line)}
.ag figure img{display:block;width:100%;height:auto}
.ag figure .im.cover img{aspect-ratio:16/10;object-fit:cover}
.ag figcaption{margin-top:12px;font-size:14px;line-height:1.5;color:var(--mut)}
.ag figcaption b{color:var(--ink);font-weight:500}
.ag .mt{margin-top:clamp(12px,1.2vw,20px)}
.ag .mt2{margin-top:clamp(28px,3vw,48px)}
/* reel */
.ag .reel{position:relative;border-radius:28px;overflow:hidden;background:#0B0D14;aspect-ratio:16/9}
.ag .reel video{display:block;width:100%;height:100%;object-fit:cover}
.ag .reel .tag{position:absolute;left:18px;bottom:18px;display:inline-flex;align-items:center;gap:8px;height:34px;padding:0 14px;border-radius:999px;background:rgba(255,255,255,.92);font:500 11.5px 'Geist Mono',monospace;letter-spacing:.06em;text-transform:uppercase;color:var(--ink)}
.ag .reel .tag i{width:7px;height:7px;border-radius:50%;background:#FF4D4D}
/* role loop */
.ag .loop{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin-top:18px}
.ag .loop div{position:relative;padding:16px 14px;border-radius:16px;background:#FFF;border:1px solid var(--line);font-size:14px;line-height:1.35;color:var(--ink)}
.ag .loop div b{display:block;margin-bottom:6px;font:500 11px 'Geist Mono',monospace;color:var(--blue)}
.ag .loop div.ai{background:var(--blue);border-color:var(--blue);color:#FFF}.ag .loop div.ai b{color:#C9D6FF}
.ag .loop div:not(:last-child)::after{content:"";position:absolute;right:-8px;top:50%;width:6px;height:2px;background:var(--blue);opacity:.5}
.ag .chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.ag .chips span{display:inline-flex;align-items:center;height:34px;padding:0 14px;border-radius:999px;background:#FFF;border:1px solid var(--line);font-size:14px;color:var(--ink)}
/* evolution */
.ag .evo{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(12px,1.2vw,20px)}
.ag .evo .st{display:flex;align-items:center;gap:10px;margin-bottom:14px}
.ag .evo .st b{display:grid;place-items:center;width:28px;height:28px;border-radius:50%;background:var(--bt);color:var(--blue);font:500 12px 'Geist Mono',monospace}
.ag .evo .st.on b{background:var(--blue);color:#FFF}
.ag .evo .ph{height:100%;display:flex;flex-direction:column}
.ag .evo .blank{flex:1;min-height:200px;display:grid;place-items:center;border-radius:20px;background:repeating-linear-gradient(135deg,var(--soft) 0 12px,#FFF 12px 24px);border:1px dashed #D3DAE8;color:var(--mut);font:500 11.5px 'Geist Mono',monospace;letter-spacing:.06em;text-transform:uppercase;text-align:center;padding:20px}
/* flow */
.ag .flow{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:10px}
.ag .flow div{position:relative;padding:18px 14px;border-radius:18px;background:var(--soft);border:1px solid var(--line)}
.ag .flow b{display:block;font:500 11px 'Geist Mono',monospace;color:var(--blue)}
.ag .flow span{display:block;margin-top:8px;font-size:15px;font-weight:500;line-height:1.25;color:var(--ink)}
.ag .flow em{display:block;margin-top:6px;font-style:normal;font-size:12.5px;line-height:1.4;color:var(--mut)}
.ag .flow div:not(:last-child)::after{content:"";position:absolute;right:-8px;top:50%;width:6px;height:2px;background:var(--blue);opacity:.5}
/* decisions */
.ag .dec{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:clamp(24px,4vw,72px);align-items:center;padding:clamp(28px,3vw,48px);border-radius:28px;background:var(--soft);border:1px solid var(--line)}
.ag .dec+.dec{margin-top:clamp(12px,1.2vw,20px)}
.ag .dec.flip>div:first-child{order:2}
.ag .dec h3{font-size:clamp(24px,2.2vw,36px);letter-spacing:-.03em;line-height:1.08;font-weight:400}
.ag .dec .rows{margin-top:22px}
.ag .dec .rows div{display:grid;grid-template-columns:96px 1fr;gap:14px;padding:12px 0;border-top:1px solid var(--line)}
.ag .dec .rows dt,.ag .dec .rows .l{font:500 11px 'Geist Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--mut);padding-top:3px}
.ag .dec .rows p{font-size:15px;line-height:1.55;color:var(--ink)}
.ag .dec .rows .tr p{color:var(--mut)}
.ag .clock{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:8px;padding:clamp(20px,2vw,32px);border-radius:20px;background:#FFF;border:1px solid var(--line)}
.ag .clock div{text-align:center}
.ag .clock i{display:block;height:120px;border-radius:12px;background:#EEF2FF;position:relative;overflow:hidden}.ag .clock i::after{content:"";position:absolute;left:0;right:0;bottom:0;background:var(--blue);border-radius:0 0 12px 12px}.ag .clock i.b62::after{height:62%}.ag .clock i.b70::after{height:70%}.ag .clock i.b100::after{height:100%}.ag .clock i.b78::after{height:78%}.ag .clock i.b48::after{height:48%}.ag .clock i.b66::after{height:66%}.ag .clock i.b56::after{height:56%}.ag .dn{display:inline-block;padding:4px 9px;border-radius:999px;background:var(--bt);color:var(--blue);font:500 11.5px 'Geist Mono',monospace}.ag .dh{margin-top:16px}
.ag .clock span{display:block;margin-top:8px;font:500 10.5px 'Geist Mono',monospace;letter-spacing:.04em;text-transform:uppercase;color:var(--mut)}
.ag .clock .cap{grid-column:1/-1;margin-top:14px;padding-top:14px;border-top:1px solid var(--line);font-size:14px;color:var(--mut);text-align:left}
.ag .map{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;margin-top:12px}
.ag .map div{padding:14px 12px;border-radius:14px;background:#FFF;border:1px solid var(--line);font-size:13px;line-height:1.35;color:var(--mut)}
.ag .map div b{display:block;margin-bottom:4px;font-size:14px;font-weight:500;color:var(--ink)}
.ag .map div.on{background:var(--blue);border-color:var(--blue);color:#DDE5FF}.ag .map div.on b{color:#FFF}
/* palette */
.ag .sw{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px}
.ag .sw i{display:block;height:96px;border-radius:16px;border:1px solid var(--line)}
.ag .sw span{display:block;margin-top:10px;font-size:14px;font-weight:500;color:var(--ink)}
.ag .sw em{display:block;margin-top:2px;font-style:normal;font:500 11px 'Geist Mono',monospace;color:var(--mut)}
.ag .phone{max-width:280px;margin:0 auto}.ag .phone .im{border-radius:30px}
/* table */
.ag .tbl{width:100%;border-collapse:collapse;font-size:15px;line-height:1.5}
.ag .tbl th{text-align:left;padding:14px 16px;font:500 11px 'Geist Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--mut);border-bottom:1px solid var(--line)}
.ag .tbl td{padding:16px;border-bottom:1px solid var(--line);vertical-align:top;color:#3A4152}
.ag .tbl td:first-child{color:var(--ink);font-weight:500}
.ag .tblw{border-radius:24px;border:1px solid var(--line);background:#FFF;overflow:auto}
.ag .tblw .tbl tr:last-child td{border-bottom:0}
.ag .st{display:inline-block;padding:3px 9px;border-radius:999px;font:500 10.5px 'Geist Mono',monospace;letter-spacing:.05em;text-transform:uppercase;white-space:nowrap}
.ag .st.i{background:#E6F6EC;color:#16703E}.ag .st.p{background:var(--bt);color:var(--blue)}.ag .st.n{background:#FFF1E5;color:#9A4B07}
.ag .note{margin-top:clamp(12px,1.2vw,20px);padding:16px 20px;border-radius:16px;background:#FFF;border:1px dashed #D3DAE8;font-size:14.5px;line-height:1.6;color:var(--mut)}
.ag .note b{color:var(--ink);font-weight:500}
/* end */
.ag .end{margin-top:var(--sy);padding:clamp(80px,9vw,150px) 0;text-align:center;background:var(--soft);border-top:1px solid var(--line)}
.ag .end h2{margin:16px auto 0;font-size:clamp(48px,7vw,124px);max-width:none}
.ag .nextp{display:inline-flex;align-items:center;gap:12px;margin-top:32px;height:56px;padding:0 10px 0 26px;border-radius:999px;background:var(--ink);color:#FFF !important;font:500 15px 'Geist',sans-serif;text-decoration:none;transition:background .3s}
.ag .nextp i{display:grid;place-items:center;width:38px;height:38px;border-radius:50%;background:#FFF;color:var(--ink);font-style:normal}
.ag .nextp:hover{background:var(--blue)}
.ag .toc{display:flex;flex-wrap:wrap;gap:8px;margin-top:28px}
.ag .toc a{display:inline-flex;align-items:center;height:34px;padding:0 14px;border-radius:999px;background:#FFF;border:1px solid var(--line);font:500 11.5px 'Geist Mono',monospace;letter-spacing:.06em;text-transform:uppercase;color:var(--ink);text-decoration:none;transition:background .3s,color .3s,border-color .3s}
.ag .toc a:hover{background:var(--blue);border-color:var(--blue);color:#FFF}

/* live site */
.ag .live{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:24px 40px;margin-top:clamp(28px,3vw,44px);padding:clamp(22px,2.2vw,34px) clamp(22px,2.4vw,40px);border-radius:28px;background:radial-gradient(60% 120% at 100% 0%,rgba(45,91,255,.10),transparent 70%),var(--soft);border:1px solid var(--line)}
.ag .live-l{flex:1 1 420px;max-width:60ch}
.ag .live-tag{display:inline-flex;align-items:center;gap:8px;height:30px;padding:0 12px;border-radius:999px;background:#FFF;border:1px solid var(--line);font:500 11.5px 'Geist Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--ink)}
.ag .live-tag i{width:8px;height:8px;border-radius:50%;background:#22C55E;box-shadow:0 0 0 0 rgba(34,197,94,.55);animation:livep 2s infinite}
@keyframes livep{70%{box-shadow:0 0 0 9px rgba(34,197,94,0)}100%{box-shadow:0 0 0 0 rgba(34,197,94,0)}}
.ag .live h3{margin-top:14px;font-size:clamp(26px,2.4vw,40px);line-height:1.05;letter-spacing:-.035em;font-weight:400}
.ag .live p{margin-top:10px;font-size:15.5px;line-height:1.55;color:var(--mut)}
.ag .live-r{display:flex;flex-direction:column;align-items:flex-start;gap:10px}
.ag .live-btn{display:inline-flex;align-items:center;gap:14px;height:60px;padding:0 10px 0 28px;border-radius:999px;background:var(--blue);color:#FFF !important;font:500 16px 'Geist',sans-serif;text-decoration:none;box-shadow:0 18px 40px -18px rgba(45,91,255,.65);transition:background .3s,transform .4s cubic-bezier(.22,1,.36,1)}
.ag .live-btn i{display:grid;place-items:center;width:42px;height:42px;border-radius:50%;background:#FFF;color:var(--blue);font-style:normal;transition:transform .4s cubic-bezier(.22,1,.36,1)}
.ag .live-btn:hover{background:#1E45E0;transform:translateY(-2px)}.ag .live-btn:hover i{transform:rotate(45deg)}
.ag .live-btn:focus-visible{outline:3px solid #0B0D14;outline-offset:3px}
.ag .live-url{padding-left:6px;font:500 12px 'Geist Mono',monospace;color:var(--mut)}
.ag a.heroimg{position:relative;display:block;cursor:pointer}
.ag .heroimg-cta{position:absolute;right:20px;bottom:20px;display:inline-flex;align-items:center;height:44px;padding:0 18px;border-radius:999px;background:rgba(255,255,255,.94);color:var(--ink);font:500 14px 'Geist',sans-serif;box-shadow:0 10px 30px -12px rgba(11,13,20,.35);opacity:0;transform:translateY(6px);transition:opacity .35s,transform .35s}
.ag a.heroimg:hover .heroimg-cta,.ag a.heroimg:focus-visible .heroimg-cta{opacity:1;transform:none}
@media (max-width:1100px){.ag .flow{grid-template-columns:repeat(4,minmax(0,1fr))}.ag .tldr,.ag .nums,.ag .g4{grid-template-columns:repeat(2,minmax(0,1fr))}.ag .nums>div:nth-child(3){border-left:0}.ag .nums>div:nth-child(n+3){border-top:1px solid var(--line)}.ag .loop,.ag .map{grid-template-columns:repeat(3,minmax(0,1fr))}.ag .sw{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:820px){.ag .meta{grid-template-columns:1fr 1fr}.ag .meta>div:nth-child(3){border-left:0;padding-left:0}.ag .g2,.ag .g3,.ag .evo,.ag .dec{grid-template-columns:1fr}.ag .dec.flip>div:first-child{order:0}.ag .flow{grid-template-columns:1fr 1fr}.ag .tldr,.ag .nums{grid-template-columns:1fr}.ag .nums>div+div{border-left:0;border-top:1px solid var(--line)}.ag .loop,.ag .map{grid-template-columns:1fr 1fr}.ag .loop div::after,.ag .flow div::after{display:none}}
"""

def head(n, label, title, lead=''):
    l = f'<p class="lead rv">{lead}</p>' if lead else ''
    return f'<div class="sh"><div><span class="pill-k rv"><b>{n}</b>{label}</span><h2 class="rv">{title}</h2></div>{l}</div>'

def fig(key, cap, cls=''):
    return f'<figure class="rv"><div class="im {cls}"><img src="@@{key}@@" alt="" loading="lazy"></div><figcaption>{cap}</figcaption></figure>'

def sec(id_, inner):
    return f'<section id="{id_}"><div class="wrap">{inner}</div></section>'

IMPL = '<span class="st i">Shipped</span>'; PROTO = '<span class="st p">Prototype</span>'; PLAN = '<span class="st n">Planned</span>'
P = []

# ---------- hero
P.append('''<div class="hero"><div class="wrap">
<span class="pill-k rv"><b>01</b>Case study · Augle AI</span>
<h1 class="rv">Making industrial<br>automation <span class="it">tangible.</span></h1>
<p class="sub rv">A company website built around a live 3D factory. Visitors can watch vision, robotics and inspection work together, then get straight to products and contact.</p>
<div class="live rv">
<div class="live-l"><span class="live-tag"><i></i>Live site</span><h3>Experience the <span class="it">real</span> thing.</h3><p>The full interactive factory, running in your browser: the live overview, the seven-station tour and the lighting presets. Best on a laptop or desktop.</p></div>
<div class="live-r"><a class="live-btn" href="https://augle-ai-website-working-automation.vercel.app/" target="_blank" rel="noopener">Open the live website <i aria-hidden="true"><svg width="16" height="16" viewBox="0 0 24 24"><path d="M7 17L17 7M9 7h8v8" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></i></a><span class="live-url">augle-ai-website-working-automation.vercel.app</span></div>
</div>
<div class="meta rv">
<div><span class="k">My role</span><p>Research, concept, art direction, UX/UI, interaction design, AI-assisted front-end</p></div>
<div><span class="k">Platform</span><p>Responsive website with a real-time 3D scene (WebGL)</p></div>
<div><span class="k">Built with</span><p>React, TypeScript, Three.js (R3F), GSAP, Claude</p></div>
<div><span class="k">Status</span><p>Working prototype, deployed for review</p></div>
</div>
<div class="toc rv"><a href="#challenge">Challenge</a><a href="#role">Role</a><a href="#research">Research</a><a href="#concept">Concept</a><a href="#factory">Factory</a><a href="#decisions">Key decisions</a><a href="#ui">UI system</a><a href="#build">Build</a><a href="#outcome">Outcome</a></div>
<a class="heroimg rv" href="https://augle-ai-website-working-automation.vercel.app/" target="_blank" rel="noopener" aria-label="Open the live Augle AI website in a new tab"><img src="@@ag_lap_wide@@" alt="The Augle AI homepage open on a laptop, showing the live 3D factory overview"><span class="heroimg-cta">Open the live website ↗</span></a>
</div></div>''')

# ---------- tldr + numbers
P.append('''<section id="summary" style="padding-top:clamp(48px,5vw,88px)"><div class="wrap">
<div class="tldr">
<div class="rv"><span class="k">Problem</span><p>Industrial automation is hard to picture from photos and paragraphs, and buyers still need fast access to product facts.</p></div>
<div class="rv"><span class="k">My role</span><p>I led research, concept, art direction and UX/UI, and built the site with Claude as my implementation partner.</p></div>
<div class="rv"><span class="k">Solution</span><p>A live, connected factory on the homepage, with an <i>optional</i> guided tour and the content one scroll away.</p></div>
<div class="rv"><span class="k">Outcome</span><p>A deployed working prototype. Not yet user-tested, so no impact metrics are claimed. A validation plan is ready.</p></div>
</div>
<div class="nums rv">
<div><b>7</b><span>connected stations, from pick-and-place to dispatch</span></div>
<div><b>9.5<small>s</small></b><span>one shared production beat drives every machine</span></div>
<div><b>4</b><span>lighting moods, plus light that follows the real sun</span></div>
<div><b>1</b><span>click to start the tour. Nobody is forced through it</span></div>
</div>
<div class="reel rv mt2"><video data-auto src="@@v_uireel@@" poster="@@v_uireel_poster@@" muted="" loop="" playsinline="" preload="metadata" aria-label="Showreel of the Augle factory: overview, seven-station tour and lighting presets"></video><span class="tag"><i></i>Recorded from the working site</span></div>
</div></section>''')

# ---------- 01 challenge
P.append(sec('challenge', head('01','The challenge','Show how it works, <span class="it">without</span> getting in the way.',
 'Augle AI builds computer vision, inspection and custom AI for manufacturers. Its value is invisible in a product photo.') + '''
<div class="quote rv"><span class="k">How might we</span><p style="margin-top:14px">make industrial automation <span class="it">tangible</span> through an immersive factory, while keeping business information clear and easy to reach?</p></div>
<div class="g3 mt">
<div class="cd rv"><span class="n">Tension 01</span><h3>Immersion vs efficiency</h3><p>A buyer looking for a spec sheet shouldn't have to sit through a camera journey.</p></div>
<div class="cd rv"><span class="n">Tension 02</span><h3>Realism vs performance</h3><p>Detail that reads well up close costs geometry, shadows and frame rate on ordinary laptops.</p></div>
<div class="cd rv"><span class="n">Tension 03</span><h3>Story vs credibility</h3><p>Robots everywhere can suggest Augle makes robots. It doesn't. The story had to stay on vision and connection.</p></div>
</div>'''))

# ---------- 02 role
P.append(sec('role', head('02','My role','Designer and creative director, <span class="it">building with AI.</span>',
 'I owned the thinking and every decision. Claude wrote most of the code from my specifications, and I reviewed every pass.') + '''
<div class="g2">
<div class="cd soft rv"><h3>What I owned</h3><ul>
<li>Company and domain research, positioning and copy corrections</li>
<li>Concept of one connected factory, station sequence and camera intent</li>
<li>Art direction: light white world, navy type, one blue action colour</li>
<li>UX of the optional tour: entry, pause, skip, exit and hand-off to content</li>
<li>UI system, liquid-glass restraint and the lighting idea</li>
<li>Quality bar: review, testing, and accepting or rejecting every build</li></ul></div>
<div class="cd soft rv"><h3>How I worked with AI</h3><p>The skill that mattered most was writing briefs that produce useful iterations: scope, constraints, what must not change, the exact interaction sequence and how to check it.</p>
<div class="loop"><div><b>01</b>Research &amp; references</div><div><b>02</b>Write the spec</div><div class="ai"><b>03</b>Claude builds</div><div><b>04</b>Review in browser</div><div><b>05</b>Refine the brief</div></div>
<div class="chips"><span>React 18</span><span>TypeScript</span><span>Vite</span><span>Three.js · R3F · Drei</span><span>GSAP</span><span>SunCalc</span><span>Claude</span></div></div>
</div>'''))

# ---------- 03 research
P.append(sec('research', head('03','Research','Research ran through the <span class="it">whole</span> build.',
 'Every iteration raised a new question, from how a welding cell is laid out to how a paint booth is lit. Each answer changed the brief.') + '''
<div class="g4">
<div class="cd ins rv"><span class="n">Company</span><h3>What does Augle sell?</h3><p>Vision inspection (Q100 systems) and custom AI. Not robots.</p><span class="f"><b>So I</b>Rewrote copy around vision and connection: “Robotics, vision and AI. Connected in one factory.”</span></div>
<div class="cd ins rv"><span class="n">Domain</span><h3>How does a real line flow?</h3><p>Each station hands a part to the next. Nothing appears out of thin air.</p><span class="f"><b>So I</b>Put every machine on one production clock, with parts appearing only inside enclosures.</span></div>
<div class="cd ins rv"><span class="n">Visual</span><h3>How do credible brands look?</h3><p>Robotics and vision leaders keep imagery clean and let one strong visual carry the page.</p><span class="f"><b>So I</b>Chose a white environment, navy type and a single royal-blue action colour.</span></div>
<div class="cd ins rv"><span class="n">Technical</span><h3>Video or real-time 3D?</h3><p>Video can't be paused per station or connected to content. No licensed realistic robot models were available.</p><span class="f"><b>So I</b>Went real-time 3D with detailed procedural models.</span></div>
</div>
<p class="note"><b>No user research on this project.</b> Audience needs (operations leaders, quality engineers, technical buyers) were working hypotheses. The one assumption I refused to make: that visitors want a 3D tour because it looks impressive.</p>'''))

# ---------- 04 concept
P.append(sec('concept', head('04','Concept','From one dark robot to a <span class="it">connected</span> white factory.',
 'One robot arm says “robots”. A whole working line says “connected intelligence”. The concept changed three times.') + '''
<div class="evo">
<div class="ph rv"><div class="st"><b>1</b><span class="k">Dark hero</span></div><div class="blank">Single robot arm on dark<br>· felt like sci-fi, not a supplier ·</div><p style="margin-top:14px;font-size:15px">Dramatic, but one robot told the wrong story.</p></div>
<div class="ph rv"><div class="st"><b>2</b><span class="k">Light iteration</span></div>''' + fig('ag_liquid','<b>Light, first pass.</b> Background video replaced by a live scene; still crowded with two actions and a heavy dock.') + '''</div>
<div class="ph rv"><div class="st on"><b>3</b><span class="k">Final direction</span></div>''' + fig('ag_refined','<b>Refined home.</b> One primary action, station pills around open floor, balanced navigation.') + '''</div>
</div>
<div class="mt2">''' + fig('ag_hero','<b>The factory became the hero.</b> A high, angled overview with seven stations on the perimeter and clear floor in the middle for the message: <i>“Intelligence in motion. At every stage.”</i>') + '</div>'))

# ---------- 05 factory
STN = [('01','Pick &amp; place','Part from infeed to fixture'),('02','Assembly','Cover placed, screws driven'),('03','Welding','Two-robot hand-over'),('04','Painting','Controlled passes in a booth'),('05','Inspection','Scan, check features, PASS'),('06','Packaging','Carton formed, sealed'),('07','Dispatch','AMRs move pallets to the dock')]
flow = '<div class="flow rv">' + ''.join(f'<div><b>{n}</b><span>{t}</span><em>{d}</em></div>' for n,t,d in STN) + '</div>'
P.append(sec('factory', head('05','The factory','Seven stations, one line, <span class="it">honest</span> motion.',
 'The tour follows one part from start to dispatch. If a weld happens in mid-air, the scene stops communicating and starts distracting.') + flow + '''
<div class="g3 mt2">''' + fig('ag_pick','<b>01 Pick &amp; place.</b> Six-axis arm with a parallel gripper.','cover') + fig('ag_assembly','<b>02 Assembly.</b> Cover placement and screw driving.','cover') + fig('ag_paint','<b>04 Painting.</b> Booth with floor grating and controlled passes.','cover') + '''</div>
<div class="g3 mt">''' + fig('ag_inspect','<b>05 Inspection.</b> The monitor boxes each checked feature, then shows PASS.','cover') + fig('ag_pack','<b>06 Packaging.</b> Carton erector, sealer and palletising.','cover') + fig('ag_dispatch','<b>07 Dispatch.</b> Five AMRs on separate lanes.','cover') + '''</div>
<p class="note"><b>Honest by design.</b> The inspection screen is representative: a scripted scan that always passes. It does not process real production data, and the site never implies it does.</p>'''))

# ---------- 06 decisions
P.append(sec('decisions', head('06','Key decisions','Four decisions that <span class="it">shaped</span> the work.',
 'Each started as a problem I found in review. Here is what I chose, why, and what it cost.') + '''
<div class="dec rv"><div>
<span class="dn">Decision 01</span>
<h3 class="dh">I made the immersive tour <span class="it">optional.</span></h3>
<div class="rows">
<div><span class="l">Problem</span><p>Scroll-driven, the tour was compulsory: stations skipped at speed, cards collided with controls, and there was no way out to the content.</p></div>
<div><span class="l">Decision</span><p>The homepage opens on the live overview. “Explore the factory” starts the tour, with pause and skip always docked. The end card hands off to contact and content.</p></div>
<div><span class="l">Why</span><p>A technical buyer shouldn't pay for my storytelling with their time.</p></div>
<div class="tr"><span class="l">Trade-off</span><p>Fewer visitors may see the full tour.</p></div>
</div></div>
<div>''' + fig('ag_end','<b>End of tour.</b> A clear exit to “Talk to Augle AI”, then normal scrolling.') + '''
<div class="map"><div><b>Overview</b>Live factory, one action</div><div class="on"><b>Explore</b>Explicit click</div><div><b>7 stations</b>Pause · Skip</div><div><b>Next chapter</b>Contact CTA</div><div><b>Content</b>Products, company</div></div></div>
</div>

<div class="dec flip rv"><div>
<span class="dn">Decision 02</span>
<h3 class="dh">One production clock, <span class="it">independent</span> of scroll.</h3>
<div class="rows">
<div><span class="l">Problem</span><p>Scrubbing animation with scroll ran machines in reverse and made parts pop in and out.</p></div>
<div><span class="l">Decision</span><p>A new part enters every 9.5 seconds (set by the welding cell) and every station runs one cycle per beat. Scrolling only moves the camera.</p></div>
<div><span class="l">Why</span><p>Believable flow is part of the UX. Wrong machinery costs credibility.</p></div>
<div class="tr"><span class="l">Trade-off</span><p>A more complex simulation architecture.</p></div>
</div></div>
<div class="clock"><div><i class="b62"></i><span>Pick</span></div><div><i class="b70"></i><span>Assemble</span></div><div><i class="b100"></i><span>Weld</span></div><div><i class="b78"></i><span>Paint</span></div><div><i class="b48"></i><span>Inspect</span></div><div><i class="b66"></i><span>Pack</span></div><div><i class="b56"></i><span>Dispatch</span></div><p class="cap">Illustrative: each station fits its cycle inside the 9.5 s beat. Welding is the longest, so it sets the pace.</p></div>
</div>

<div class="dec rv"><div>
<span class="dn">Decision 03</span>
<h3 class="dh">Silhouettes, not shine, made it <span class="it">real.</span></h3>
<div class="rows">
<div><span class="l">Problem</span><p>The factory looked clean but toy-like. Darker shadows and shinier surfaces didn't help.</p></div>
<div><span class="l">Decision</span><p>A realism audit, then six passes on proportions, joints, end effectors, cable dress packs, fasteners and a proper material library.</p></div>
<div><span class="l">Why</span><p>Realism is a system of geometry, material, light, motion and scale, not one slider.</p></div>
<div class="tr"><span class="l">Trade-off</span><p>About 19% more geometry, so performance had to be watched.</p></div>
</div></div>
<div>''' + fig('ag_weld','<b>03 Welding.</b> I specified it step by step: the handler loads the fixture, clamps close, a second robot with a 45° swan-neck torch runs the seam, and sparks appear only during the pass.') + '''</div>
</div>

<div class="dec flip rv"><div>
<span class="dn">Decision 04</span>
<h3 class="dh">Light that follows the <span class="it">real</span> sun.</h3>
<div class="rows">
<div><span class="l">Problem</span><p>Fixed daylight felt static, and early lighting was faint, washed out, and too similar between day and night.</p></div>
<div><span class="l">Decision</span><p>By default the factory is lit by the sun's actual position for the visitor's approximate location. A control previews morning, afternoon, evening and night.</p></div>
<div><span class="l">Why</span><p>A memorable, place-aware moment that rewards a second visit.</p></div>
<div class="tr"><span class="l">Trade-off</span><p>Extra state and checks. The look is art-directed, not physically measured.</p></div>
</div></div>
<div class="g2">''' + fig('ag_morning','<b>Morning</b>') + fig('ag_afternoon','<b>Afternoon</b>') + fig('ag_evening','<b>Evening</b>') + fig('ag_night','<b>Night</b>') + '''</div>
</div>'''))

# ---------- 07 UI system
P.append(sec('ui', head('07','UI system','A <span class="it">quiet</span> interface over a busy scene.',
 'The factory is dense, so the interface had to be calm: clear hierarchy, generous whitespace and controls that never collide.') + '''
<div class="sw rv">
<div><i style="background:#FFFFFF"></i><span>White</span><em>Environment</em></div>
<div><i style="background:#F7F9FC"></i><span>Page tint</span><em>#F7F9FC</em></div>
<div><i style="background:#0B1530"></i><span>Dark navy</span><em>#0B1530 · type</em></div>
<div><i style="background:#0056D2"></i><span>Royal blue</span><em>#0056D2 · action</em></div>
<div><i style="background:linear-gradient(90deg,#0056D2,#008CFF 65%,#4EDCE5)"></i><span>Cyan to blue</span><em>Accents only</em></div>
</div>
<div class="g4 mt">
<div class="cd rv"><span class="n">Type</span><h3>Manrope</h3><p>One large two-line headline, with the accent word in blue.</p></div>
<div class="cd rv"><span class="n">Spacing</span><h3>8 px rhythm</h3><p>Hero spacing, card padding and section gaps on one scale.</p></div>
<div class="cd rv"><span class="n">Controls</span><h3>64 / 44 px</h3><p>Desktop header and docks at 64 px, mobile targets at 44 px.</p></div>
<div class="cd rv"><span class="n">Actions</span><h3>One primary</h3><p>A single filled blue action per view. Everything else stays quiet.</p></div>
</div>
<div class="g3 mt2" style="align-items:start">''' + fig('ag_panel','<b>Lighting control.</b> Location, “Use my location” and four presets, styled to match the other glass controls.') + fig('ag_solutions','<b>Solutions.</b> Product names follow the company’s own site.') + '<div class="phone">' + fig('ag_mobile','<b>Mobile, 375 px.</b> Checked for layout and overflow.') + '''</div></div>
<div class="cd soft mt rv"><h3>Liquid glass, with restraint</h3><p>Glass ties the interface to the scene, but only where it helps. Over the 3D scene it is rendered on the GPU from the finished frame, so what sits behind a panel is genuinely refracted, while text stays in the HTML. Iterations removed coloured borders, raised contrast and reduced distortion behind text. Readable edges and a recognisable primary button always came first.</p></div>'''))

# ---------- 08 build
P.append(sec('build', head('08','Build &amp; quality','Built to be <span class="it">checked,</span> not just shown.',
 'A clear structure, a deterministic simulation and fallbacks for people and devices that can’t take the full experience.') + '''
<div class="g3">
<div class="cd rv"><span class="n">Structure</span><h3>Separated by concern</h3><ul><li><b>sim/</b> production logic, robot programs, AMR routes</li><li><b>world/</b> and <b>machines/</b> the factory and moving machines</li><li><b>scene/</b> lights, camera rig, GPU glass</li><li><b>config/</b> editable colours, timing and copy</li></ul></div>
<div class="cd rv"><span class="n">Accessibility</span><h3>Fallbacks built in</h3><ul><li>Reduced motion rests the camera and slows machines</li><li>Pause motion and a skip link</li><li>Static poster when WebGL isn't available</li><li>Quality tiers for weaker devices</li></ul></div>
<div class="cd rv"><span class="n">Checks</span><h3>What was verified</h3><ul><li>Type check and production build pass</li><li>Sim checks: spacing, robot reach, weld hand-over, AMR loops</li><li>Layouts at 1440, 800 and 390 px with no overflow</li><li>72 fps at every station on one test laptop</li></ul></div>
</div>
<p class="note"><b>Who checked it:</b> me, in the browser, plus automated scripts. None of this is a user study, and phones haven't been performance-tested yet.</p>'''))

# ---------- 09 outcome
P.append(sec('outcome', head('09','Outcome','A working prototype, and a <span class="it">plan</span> to prove it.',
 'The result is deployed for review. Its impact hasn’t been measured yet, so here is exactly what exists and how I’d validate it.') + '''
<div class="g2">
<div class="tblw rv"><table class="tbl"><thead><tr><th>What exists</th><th>Status</th></tr></thead><tbody>
<tr><td>Live factory overview, 7 stations on one clock</td><td>''' + IMPL + '''</td></tr>
<tr><td>Optional tour with pause, skip and hand-off to content</td><td>''' + IMPL + '''</td></tr>
<tr><td>Products, solutions, industries and company sections</td><td>''' + IMPL + '''</td></tr>
<tr><td>Reduced motion, skip link, WebGL fallback</td><td>''' + IMPL + '''</td></tr>
<tr><td>Sun-following lighting and four presets</td><td>''' + PROTO + '''</td></tr>
<tr><td>Working enquiry form and analytics</td><td>''' + PLAN + '''</td></tr>
</tbody></table></div>
<div class="tblw rv"><table class="tbl"><thead><tr><th>Validation plan</th><th>Success looks like</th></tr></thead><tbody>
<tr><td>Five-second test</td><td>Visitors say “vision and inspection”, not “robot maker”</td></tr>
<tr><td>Find a solution</td><td>Found without entering the tour</td></tr>
<tr><td>Product facts</td><td>What Q100 does, found in under a minute</td></tr>
<tr><td>Leave the tour halfway</td><td>Exit found without help</td></tr>
<tr><td>Contact</td><td>Enquiry sent without a mail client</td></tr>
<tr><td>Phone and keyboard only</td><td>All key tasks completable</td></tr>
</tbody></table></div>
</div>'''))

# ---------- 10 reflection
P.append(sec('reflection', head('10','Reflection','What I’d <span class="it">keep</span>, and what I’d change.') + '''
<div class="g3">
<div class="cd soft rv"><span class="n">Learned</span><h3>Immersion must be optional</h3><p>Visitors need control over anything immersive, and practical information has to stay one scroll away.</p></div>
<div class="cd soft rv"><span class="n">Learned</span><h3>AI needs direction</h3><p>Precise briefs with constraints and “do not change” lists produced far better iterations than enthusiastic ones.</p></div>
<div class="cd soft rv"><span class="n">Next time</span><h3>Users earlier</h3><p>Everything passed my checks, but none of it has met a real visitor. I’d define success criteria and test key tasks from the start.</p></div>
</div>'''))

P.append('''<div class="end"><div class="wrap"><span class="k">Next project</span><h2 class="rv">Nom <span class="it">Nom</span></h2><a class="nextp" href="Case-NomNom.dc.html">View case study <i aria-hidden="true">→</i></a></div></div>''')

BODY = '\n'.join(P)
import json
ns = {'base_css': base_css, 'CSS': CSS, 'BODY': BODY}
exec(TEMPLATE, ns)
page = ns['page']
open('/home/claude/pf/src/Case-Augle.dc.html', 'w').write(page)
print(len(page))

# --- wrap in the proven shell (keeps v26 transitions + reveal safety) ---
_old = open('/home/claude/pf/bk_Case-Augle_v1.dc.html').read()
_a = _old.index('/* ===== augle case study ===== */'); _b = _old.index('.ag-hdr{')
_safe = "\n/* safety: content must show even if reveal never fires */\n.ag .rv{animation:rvsafe .01s linear 1.8s forwards}\n@keyframes rvsafe{to{opacity:1;filter:none;transform:none}}\n"
_pg = _old[:_a] + CSS + _safe + _old[_b:]
_pg = _pg.replace('<helmet>\n', '<helmet>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&amp;display=swap">\n', 1)
_pg = _pg[:_pg.index('<main>')] + '<main>\n' + BODY + '\n' + _pg[_pg.index('</main>'):]
_pg = _pg.replace('"height":16000', '"height":13200')
open('/home/claude/pf/src/Case-Augle.dc.html', 'w').write(_pg)
print('shell ok', len(_pg))
