



import { useState, useRef, useEffect } from 'react'

const CSS = `
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --navy-900:#0d1b2e;--navy-800:#112240;--navy-700:#1a3356;
  --white:#ffffff;--off-white:#f7f8fc;--surface:#f0f3f9;--surface-2:#e8ecf5;
  --accent:#2e6fda;--accent-light:#4d8af0;--accent-dim:rgba(46,111,218,0.08);
  --gold:#e8a930;
  --text-dark:#0d1b2e;--text-mid:#3d5270;--text-soft:#6b80a0;--text-muted:#9baec8;
  --text-nav:#cdd9ee;--text-nav-soft:#8da3c0;
  --success:#1a9e6a;--success-dim:rgba(26,158,106,0.1);
  --error:#d63f4d;--error-dim:rgba(214,63,77,0.1);
  --border-light:rgba(13,27,46,0.09);--border-navy:rgba(255,255,255,0.08);
  --radius-sm:8px;--radius:12px;--radius-lg:18px;--radius-xl:24px;
  --shadow:0 8px 32px rgba(13,27,46,0.12);
  --font-serif:'Playfair Display',Georgia,serif;
  --font-sans:'Plus Jakarta Sans',sans-serif;
  --font-mono:'Fira Code',monospace;
}
html{scroll-behavior:smooth}
body{background:var(--off-white);color:var(--text-dark);font-family:var(--font-sans);font-size:14px;line-height:1.6;min-height:100vh;overflow-x:hidden}
::-webkit-scrollbar{width:5px}::-webkit-scrollbar-track{background:var(--surface)}
::-webkit-scrollbar-thumb{background:var(--surface-2);border-radius:4px}
.shell{min-height:100vh;display:flex;flex-direction:column}

/* HEADER */
.hdr{background:var(--navy-900);height:66px;display:flex;align-items:center;justify-content:space-between;padding:0 48px;position:sticky;top:0;z-index:200;overflow:hidden}
.hdr-logo{display:flex;align-items:center;gap:14px;position:relative;z-index:1}
.logo-mark{width:38px;height:38px;background:var(--accent);border-radius:10px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 4px rgba(46,111,218,.2),0 4px 16px rgba(46,111,218,.35)}
.logo-name{font-family:var(--font-serif);font-size:19px;font-weight:700;color:var(--white);line-height:1.1}
.logo-sub{font-size:9px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:var(--accent-light);margin-top:1px}
.hdr-center{display:flex;align-items:center;gap:6px;font-size:11px;color:var(--text-nav-soft);position:relative;z-index:1}
.hdr-sep{width:1px;height:14px;background:var(--border-navy);margin:0 4px}
.hdr-badge{display:flex;align-items:center;gap:8px;padding:6px 16px;border-radius:100px;background:rgba(46,111,218,.15);border:1px solid rgba(46,111,218,.3);font-size:10px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--accent-light);position:relative;z-index:1}
.live-dot{width:7px;height:7px;border-radius:50%;background:#4ade80;box-shadow:0 0 0 2px rgba(74,222,128,.3);animation:livePulse 2s ease-in-out infinite}
@keyframes livePulse{0%,100%{box-shadow:0 0 0 2px rgba(74,222,128,.3)}50%{box-shadow:0 0 0 6px rgba(74,222,128,0)}}

/* HERO */
.hero{background:var(--navy-800);padding:28px 48px 32px;position:relative;overflow:hidden;border-bottom:1px solid rgba(255,255,255,.05)}
.hero-content{position:relative;z-index:1}
.hero-ey{display:flex;align-items:center;gap:10px;font-size:10px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--accent-light);margin-bottom:10px}
.hero-ey-line{width:32px;height:1px;background:var(--accent-light);opacity:.5}
.hero-title{font-family:var(--font-serif);font-size:30px;font-weight:700;color:var(--white);line-height:1.2;margin-bottom:8px}
.hero-title em{font-style:italic;color:var(--gold)}
.hero-sub{font-size:13px;color:var(--text-nav);max-width:520px}
.hero-stats{display:flex;gap:32px;margin-top:20px}
.stat-num{font-family:var(--font-serif);font-size:22px;font-weight:700;color:var(--white);line-height:1}
.stat-label{font-size:10px;color:var(--text-nav-soft);letter-spacing:.1em;text-transform:uppercase;margin-top:3px}
.stat-div{width:1px;background:var(--border-navy)}

.main-grid{flex:1;display:grid;grid-template-columns:460px 1fr;max-width:1600px;margin:0 auto;width:100%;padding:32px 48px 40px;gap:28px;align-items:start}

/* LEFT PANEL */
.left-panel{position:sticky;top:88px;background:var(--white);border-radius:var(--radius-xl);border:1px solid var(--border-light);box-shadow:var(--shadow);overflow:hidden}
.lp-top{background:var(--navy-800);padding:28px 28px 24px;position:relative;overflow:hidden}
.lp-ey{font-size:9px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:var(--accent-light);margin-bottom:8px;position:relative;z-index:1}
.lp-title{font-family:var(--font-serif);font-size:24px;font-weight:700;color:var(--white);line-height:1.2;position:relative;z-index:1}
.lp-sub{font-size:12px;color:var(--text-nav-soft);margin-top:5px;position:relative;z-index:1}
.step-bar{display:flex;align-items:center;gap:6px;margin-top:16px;position:relative;z-index:1}
.s-num{width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700}
.s-num.done{background:var(--success);color:white}
.s-num.active{background:var(--accent);color:white;box-shadow:0 0 0 3px rgba(46,111,218,.3)}
.s-num.idle{background:rgba(255,255,255,.1);color:var(--text-nav-soft)}
.s-lbl{font-size:10px;letter-spacing:.06em;color:var(--text-nav-soft);font-weight:500}
.s-lbl.active{color:white}
.s-con{flex:1;height:1px;background:rgba(255,255,255,.1);max-width:20px}
.tab-bar{display:flex;border-bottom:1px solid var(--border-light)}
.tab-btn{flex:1;padding:15px 8px;display:flex;flex-direction:column;align-items:center;gap:5px;background:transparent;border:none;cursor:pointer;font-family:var(--font-sans);font-size:9px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--text-muted);transition:color .2s;position:relative}
.tab-btn::after{content:'';position:absolute;bottom:0;left:16px;right:16px;height:2px;background:var(--accent);border-radius:2px 2px 0 0;transform:scaleX(0);transition:transform .22s}
.tab-btn.active{color:var(--accent)}.tab-btn.active::after{transform:scaleX(1)}
.tab-btn:hover:not(.active){color:var(--text-mid)}
.tab-icon-box{width:28px;height:28px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:13px;background:var(--surface);transition:background .2s}
.tab-btn.active .tab-icon-box{background:var(--accent-dim);color:var(--accent)}
.upload-body{padding:24px 24px 0}
.drop-zone{border:2px dashed var(--border-light);border-radius:var(--radius-lg);padding:40px 24px;text-align:center;cursor:pointer;background:var(--off-white);transition:all .22s;position:relative;overflow:hidden}
.drop-zone:hover,.drop-zone.drag-over{border-color:var(--accent);border-style:solid;box-shadow:0 0 0 4px var(--accent-dim)}
.drop-title{font-family:var(--font-serif);font-size:16px;font-weight:600;color:var(--text-dark)}
.drop-sub{font-size:12px;color:var(--text-soft);margin-top:3px}
.type-pills{display:flex;gap:6px;justify-content:center;margin-top:12px}
.type-pill{padding:3px 10px;border-radius:100px;background:var(--surface-2);border:1px solid var(--border-light);font-size:9px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--text-mid)}
.file-card{display:flex;align-items:center;gap:12px;padding:12px 14px;background:var(--off-white);border:1px solid var(--border-light);border-radius:var(--radius);animation:fadeUp .28s ease}
@keyframes fadeUp{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.file-badge{width:40px;height:40px;border-radius:10px;background:var(--navy-800);flex-shrink:0;display:flex;align-items:center;justify-content:center}
.file-info{flex:1;min-width:0}
.file-name{font-size:12px;font-weight:600;color:var(--text-dark);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.file-meta{font-size:10px;color:var(--text-soft);font-family:var(--font-mono);margin-top:2px}
.file-del{width:28px;height:28px;border-radius:var(--radius-sm);background:var(--error-dim);border:1px solid rgba(214,63,77,.15);color:var(--error);cursor:pointer;font-size:11px;display:flex;align-items:center;justify-content:center;transition:all .18s;flex-shrink:0}
.file-del:hover{background:var(--error);color:white}
.field-wrap{display:flex;align-items:center;gap:10px;padding:0 12px;background:var(--off-white);border:1.5px solid var(--border-light);border-radius:var(--radius);transition:all .2s}
.field-wrap:focus-within{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-dim);background:white}
.field-icon{color:var(--text-muted);font-size:12px;flex-shrink:0}
.field-input{flex:1;padding:12px 0;background:transparent;border:none;outline:none;color:var(--text-dark);font-family:var(--font-sans);font-size:13px}
.field-input::placeholder{color:var(--text-muted)}
.field-ta{width:100%;padding:14px 16px;min-height:160px;background:var(--off-white);border:1.5px solid var(--border-light);border-radius:var(--radius);color:var(--text-dark);font-family:var(--font-sans);font-size:13px;resize:vertical;outline:none;transition:all .2s;line-height:1.6}
.field-ta:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-dim);background:white}
.field-ta::placeholder{color:var(--text-muted)}
.proc-sec{padding:20px 24px 24px}
.proc-sep{height:1px;background:var(--border-light);margin:0 0 20px}
.proc-btn{width:100%;padding:16px 20px;background:var(--navy-900);border:none;border-radius:var(--radius);color:white;font-family:var(--font-sans);font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;transition:all .22s;position:relative;overflow:hidden;box-shadow:0 4px 16px rgba(13,27,46,.25)}
.proc-btn::before{content:'';position:absolute;top:0;left:-100%;width:100%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.08),transparent);transition:left .5s}
.proc-btn:hover::before{left:100%}
.proc-btn:hover{background:var(--navy-700);transform:translateY(-2px);box-shadow:0 8px 24px rgba(13,27,46,.3)}
.btn-ring{width:28px;height:28px;border-radius:7px;background:rgba(46,111,218,.3);display:flex;align-items:center;justify-content:center}
.status-card{display:flex;align-items:center;gap:14px;padding:15px 16px;border-radius:var(--radius);border:1px solid var(--border-light);background:var(--off-white)}
.sc-ic{width:44px;height:44px;border-radius:12px;flex-shrink:0;display:flex;align-items:center;justify-content:center}
.sc-ic.proc{background:rgba(46,111,218,.1);border:1px solid rgba(46,111,218,.2)}
.sc-ic.ready{background:var(--success-dim);border:1px solid rgba(26,158,106,.2)}
.sc-t{font-size:13px;font-weight:600;color:var(--text-dark)}
.sc-s{font-size:10px;color:var(--text-soft);font-family:var(--font-mono);margin-top:3px}
.spinner{width:18px;height:18px;border:2px solid rgba(46,111,218,.2);border-top-color:var(--accent);border-radius:50%;animation:spin .75s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}

/* RIGHT */
.right-panel{background:var(--white);border-radius:var(--radius-xl);border:1px solid var(--border-light);box-shadow:var(--shadow);display:flex;flex-direction:column;min-height:640px;position:relative;overflow:hidden}
.chat-overlay{position:absolute;inset:0;z-index:20;background:rgba(247,248,252,.92);backdrop-filter:blur(6px);display:flex;align-items:center;justify-content:center;animation:fadeIn .3s ease}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
.overlay-box{text-align:center;padding:40px 32px;background:var(--white);border-radius:var(--radius-xl);border:1px solid var(--border-light);box-shadow:var(--shadow);max-width:320px}
.ov-ic{width:64px;height:64px;border-radius:var(--radius-lg);background:var(--navy-800);margin:0 auto 16px;display:flex;align-items:center;justify-content:center}
.ov-title{font-family:var(--font-serif);font-size:22px;font-weight:700;color:var(--text-dark);margin-bottom:8px}
.ov-sub{font-size:12px;color:var(--text-soft);line-height:1.6}
.chat-hdr{background:var(--navy-900);padding:18px 24px;display:flex;align-items:center;justify-content:space-between;border-radius:var(--radius-xl) var(--radius-xl) 0 0;position:relative;overflow:hidden;flex-shrink:0}
.ch-info{display:flex;align-items:center;gap:12px;position:relative;z-index:1}
.ch-ic{width:36px;height:36px;border-radius:10px;background:rgba(46,111,218,.25);border:1px solid rgba(46,111,218,.35);display:flex;align-items:center;justify-content:center}
.ch-title{font-family:var(--font-serif);font-size:17px;font-weight:700;color:white}
.ch-sub{font-size:10px;color:var(--text-nav-soft);letter-spacing:.08em;margin-top:1px}
.ch-acts{display:flex;gap:8px;position:relative;z-index:1}
.ch-btn{width:32px;height:32px;border-radius:8px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);color:var(--text-nav-soft);cursor:pointer;font-size:12px;display:flex;align-items:center;justify-content:center;transition:all .18s}
.ch-btn:hover{background:rgba(214,63,77,.2);border-color:rgba(214,63,77,.3);color:#ff8090}
.msgs{flex:1;overflow-y:auto;padding:28px;display:flex;flex-direction:column;gap:18px}
.welcome-wrap{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px 20px;text-align:center}
.welcome-svg{margin-bottom:20px;animation:floatRing 5s ease-in-out infinite}
@keyframes floatRing{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
.w-title{font-family:var(--font-serif);font-size:26px;font-weight:700;color:var(--text-dark)}
.w-sub{font-size:13px;color:var(--text-soft);max-width:320px;margin:8px auto 0}
.w-chips{display:flex;gap:8px;margin-top:20px;flex-wrap:wrap;justify-content:center}
.w-chip{padding:5px 12px;border-radius:100px;background:var(--surface);border:1px solid var(--border-light);font-size:10px;font-weight:600;color:var(--text-mid);letter-spacing:.06em;display:flex;align-items:center;gap:5px}
.w-chip i{color:var(--accent);font-size:9px}
.msg-row{display:flex;gap:10px;max-width:86%;animation:fadeUp .26s ease}
.msg-row.user{align-self:flex-end;flex-direction:row-reverse}
.msg-row.bot{align-self:flex-start}
.msg-av{width:32px;height:32px;border-radius:9px;flex-shrink:0;display:flex;align-items:center;justify-content:center}
.msg-av.user{background:var(--navy-900)}
.msg-av.bot{background:var(--surface);border:1px solid var(--border-light)}
.msg-bub{padding:12px 16px;border-radius:var(--radius);font-size:13.5px;line-height:1.7}
.msg-bub.user{background:var(--navy-900);color:white;border-radius:var(--radius) var(--radius) 4px var(--radius);box-shadow:0 4px 16px rgba(13,27,46,.2)}
.msg-bub.bot{background:var(--off-white);border:1px solid var(--border-light);color:var(--text-dark);border-radius:var(--radius) var(--radius) var(--radius) 4px}
.msg-bub strong{color:var(--accent);font-weight:600}
.msg-bub ul,.msg-bub ol{padding-left:18px;margin:6px 0}
.msg-bub li{margin-bottom:3px}
.msg-bub p{margin-bottom:8px}
.msg-bub p:last-child{margin-bottom:0}
.src-tag{display:inline-flex;align-items:center;gap:5px;margin-top:9px;padding:3px 10px;border-radius:100px;font-size:9px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}
.src-tag.doc{background:var(--success-dim);color:var(--success);border:1px solid rgba(26,158,106,.2)}
.src-tag.wiki{background:var(--accent-dim);color:var(--accent);border:1px solid rgba(46,111,218,.2)}
.typing-ind{display:flex;gap:4px;padding:4px 2px}
.typing-ind span{width:7px;height:7px;border-radius:50%;background:var(--text-muted);animation:tyBounce 1.1s ease-in-out infinite}
.typing-ind span:nth-child(2){animation-delay:.18s}
.typing-ind span:nth-child(3){animation-delay:.36s}
@keyframes tyBounce{0%,80%,100%{transform:translateY(0);opacity:.35}40%{transform:translateY(-6px);opacity:1}}
.chat-input-bar{padding:16px 24px 20px;background:var(--white);border-top:1px solid var(--border-light);flex-shrink:0}
.chat-field{display:flex;align-items:flex-end;gap:10px;background:var(--off-white);border:1.5px solid var(--border-light);border-radius:var(--radius-lg);padding:10px 12px;transition:all .2s}
.chat-field:focus-within{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-dim);background:white}
.chat-ta{flex:1;background:transparent;border:none;outline:none;color:var(--text-dark);font-family:var(--font-sans);font-size:13.5px;resize:none;line-height:1.6;min-height:22px;max-height:100px}
.chat-ta::placeholder{color:var(--text-muted)}
.chat-ta:disabled{cursor:not-allowed}
.send-btn{width:38px;height:38px;border-radius:10px;border:none;cursor:pointer;background:var(--navy-900);color:white;flex-shrink:0;display:flex;align-items:center;justify-content:center;transition:all .2s;box-shadow:0 2px 10px rgba(13,27,46,.2)}
.send-btn:hover:not(:disabled){background:var(--navy-700);transform:scale(1.05)}
.send-btn:disabled{opacity:.35;cursor:not-allowed;transform:none}
.input-hint{font-size:10px;color:var(--text-muted);text-align:center;margin-top:8px;letter-spacing:.04em}
.footer{background:var(--navy-900);padding:20px 48px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid rgba(255,255,255,.04)}
.ft-left{display:flex;align-items:center;gap:12px}
.ft-logo{font-family:var(--font-serif);font-size:15px;font-weight:700;color:white}
.ft-div{width:1px;height:16px;background:rgba(255,255,255,.1)}
.ft-copy{font-size:11px;color:var(--text-nav-soft)}
.ft-cred{font-size:11px;color:var(--text-nav-soft)}
.ft-cred strong{color:var(--accent-light);font-weight:600}
.toast-stack{position:fixed;bottom:24px;right:24px;z-index:999;display:flex;flex-direction:column;gap:8px}
.toast{display:flex;align-items:center;gap:10px;padding:11px 16px;border-radius:var(--radius);min-width:220px;font-size:12px;font-weight:600;border:1px solid transparent;animation:toastIn .28s ease;box-shadow:var(--shadow)}
@keyframes toastIn{from{opacity:0;transform:translateX(16px)}to{opacity:1;transform:translateX(0)}}
.toast.success{background:rgba(26,158,106,.95);color:white}
.toast.error{background:rgba(214,63,77,.95);color:white}
.toast.info{background:rgba(46,111,218,.95);color:white}
@media(max-width:1100px){.main-grid{grid-template-columns:1fr;padding:16px 20px}.hero-stats{display:none}.hdr-center{display:none}}
`

// SVG Components
const HdrBg = () => (
  <svg style={{position:'absolute',right:0,top:0,height:'100%',opacity:.07,pointerEvents:'none'}} viewBox="0 0 600 66" fill="none">
    <circle cx="550" cy="33" r="80" stroke="white" strokeWidth="0.5"/>
    <circle cx="550" cy="33" r="50" stroke="white" strokeWidth="0.5"/>
    <circle cx="550" cy="33" r="25" stroke="white" strokeWidth="0.5"/>
    {[...Array(12)].map((_,i)=>(
      <circle key={i} cx={410+(i%6)*32} cy={14+Math.floor(i/6)*24} r="1.5" fill="white"/>
    ))}
  </svg>
)

const HeroBgSVG = () => (
  <svg style={{position:'absolute',inset:0,width:'100%',height:'100%',pointerEvents:'none'}} viewBox="0 0 1200 120" preserveAspectRatio="xMaxYMid slice" fill="none">
    {[...Array(40)].map((_,i)=>(<circle key={i} cx={700+(i%10)*50} cy={15+Math.floor(i/10)*25} r="1.5" fill="white" opacity="0.25"/>))}
    <path d="M900 0 Q1100 60 900 120" stroke="white" strokeWidth="0.5" opacity="0.12"/>
    <path d="M980 0 Q1150 60 980 120" stroke="white" strokeWidth="0.5" opacity="0.08"/>
    <polygon points="1140,25 1165,12 1190,25 1190,52 1165,65 1140,52" stroke="white" strokeWidth="0.8" opacity="0.12"/>
  </svg>
)

const LpBgSVG = () => (
  <svg style={{position:'absolute',right:-10,bottom:-20,opacity:.06,pointerEvents:'none'}} width="140" height="120" viewBox="0 0 140 120" fill="none">
    {[...Array(20)].map((_,i)=>(<circle key={i} cx={(i%5)*22+10} cy={Math.floor(i/5)*22+10} r="2" fill="white"/>))}
    <polygon points="80,50 110,33 140,50 140,83 110,100 80,83" stroke="white" strokeWidth="0.8"/>
  </svg>
)

const ChtHdrBgSVG = () => (
  <svg style={{position:'absolute',right:0,top:0,height:'100%',opacity:.05,pointerEvents:'none'}} viewBox="0 0 500 72" fill="none">
    {[...Array(16)].map((_,i)=>(<circle key={i} cx={310+(i%8)*24} cy={12+Math.floor(i/8)*22} r="1.5" fill="white" opacity="0.5"/>))}
    <circle cx="455" cy="36" r="50" stroke="white" strokeWidth="0.6"/>
    <circle cx="455" cy="36" r="30" stroke="white" strokeWidth="0.6"/>
  </svg>
)

const DropSVG = () => (
  <svg width="58" height="58" viewBox="0 0 58 58" fill="none" style={{margin:'0 auto 14px',display:'block'}}>
    <circle cx="29" cy="29" r="27" stroke="var(--accent)" strokeWidth="1.5" strokeDasharray="5 4" opacity="0.3"/>
    <circle cx="29" cy="29" r="19" fill="var(--accent-dim)"/>
    <path d="M22 30 L29 22 L36 30" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <line x1="29" y1="22" x2="29" y2="39" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/>
    <line x1="23" y1="39" x2="35" y2="39" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" opacity="0.5"/>
  </svg>
)

const LogoSVG = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
    <rect x="2" y="2" width="7" height="9" rx="1.5" fill="white" opacity="0.9"/>
    <rect x="11" y="2" width="7" height="4" rx="1.5" fill="white" opacity="0.6"/>
    <rect x="11" y="8" width="7" height="5" rx="1.5" fill="white" opacity="0.6"/>
    <rect x="2" y="13" width="16" height="4" rx="1.5" fill="white" opacity="0.4"/>
  </svg>
)

const FileIconSVG = () => (
  <svg width="18" height="22" viewBox="0 0 18 22" fill="none">
    <path d="M2 2a1 1 0 011-1h8l5 5v14a1 1 0 01-1 1H3a1 1 0 01-1-1V2z" fill="rgba(46,111,218,0.2)" stroke="var(--accent-light)" strokeWidth="1.2"/>
    <path d="M11 1v5h5" stroke="var(--accent-light)" strokeWidth="1.2"/>
    <line x1="5" y1="11" x2="13" y2="11" stroke="var(--accent-light)" strokeWidth="1.2" strokeLinecap="round"/>
    <line x1="5" y1="14" x2="13" y2="14" stroke="var(--accent-light)" strokeWidth="1.2" strokeLinecap="round"/>
    <line x1="5" y1="17" x2="9" y2="17" stroke="var(--accent-light)" strokeWidth="1.2" strokeLinecap="round"/>
  </svg>
)

const LockSVG = () => (
  <svg width="30" height="30" viewBox="0 0 30 30" fill="none">
    <rect x="5" y="13" width="20" height="15" rx="3" fill="rgba(46,111,218,0.15)" stroke="var(--accent-light)" strokeWidth="1.5"/>
    <path d="M9 13V10Q9 4 15 4Q21 4 21 10V13" stroke="var(--accent-light)" strokeWidth="1.8" strokeLinecap="round"/>
    <circle cx="15" cy="20" r="2.5" fill="var(--accent-light)"/>
    <line x1="15" y1="22.5" x2="15" y2="25" stroke="var(--accent-light)" strokeWidth="1.5" strokeLinecap="round"/>
  </svg>
)

const CheckSVG = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
    <circle cx="9" cy="9" r="8" stroke="var(--success)" strokeWidth="1.5"/>
    <path d="M5 9 L8 12 L13 6" stroke="var(--success)" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
)

const ArrowSVG = () => (
  <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
    <path d="M1 6.5 L12 6.5 M7.5 2 L12 6.5 L7.5 11" stroke="white" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
)

const SendSVG = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <path d="M1 7 L13 7 M8 2 L13 7 L8 12" stroke="white" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
)

const ChatIconSVG = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
    <path d="M2 3a1 1 0 011-1h10a1 1 0 011 1v7a1 1 0 01-1 1H9l-3 3v-3H3a1 1 0 01-1-1V3z" fill="rgba(46,111,218,0.4)" stroke="var(--accent-light)" strokeWidth="1.2"/>
    <line x1="5" y1="6" x2="11" y2="6" stroke="var(--accent-light)" strokeWidth="1.1" strokeLinecap="round"/>
    <line x1="5" y1="8.5" x2="9" y2="8.5" stroke="var(--accent-light)" strokeWidth="1.1" strokeLinecap="round"/>
  </svg>
)

const BotSVG = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
    <rect x="3" y="5" width="10" height="8" rx="2" fill="var(--accent)" opacity="0.85"/>
    <rect x="5.5" y="2" width="5" height="2.5" rx="1.2" fill="var(--accent)" opacity="0.6"/>
    <line x1="8" y1="4.5" x2="8" y2="5" stroke="var(--accent)" strokeWidth="1.2"/>
    <circle cx="5.5" cy="8.5" r="1.2" fill="white"/>
    <circle cx="10.5" cy="8.5" r="1.2" fill="white"/>
    <rect x="5.5" y="10.5" width="5" height="1" rx="0.5" fill="white" opacity="0.7"/>
    <line x1="1" y1="9" x2="3" y2="9" stroke="var(--accent)" strokeWidth="1.2" strokeLinecap="round"/>
    <line x1="13" y1="9" x2="15" y2="9" stroke="var(--accent)" strokeWidth="1.2" strokeLinecap="round"/>
  </svg>
)

const UserSVG = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <circle cx="7" cy="4.5" r="2.5" fill="rgba(255,255,255,0.85)"/>
    <path d="M2 12 Q2 8.5 7 8.5 Q12 8.5 12 12" stroke="rgba(255,255,255,0.85)" strokeWidth="1.5" fill="none" strokeLinecap="round"/>
  </svg>
)

const WelcomeSVG = () => (
  <svg className="welcome-svg" width="92" height="92" viewBox="0 0 92 92" fill="none">
    <circle cx="46" cy="46" r="44" stroke="var(--border-light)" strokeWidth="1.5"/>
    <circle cx="46" cy="46" r="33" stroke="var(--accent)" strokeWidth="1.5" strokeDasharray="7 5" opacity="0.35"/>
    <circle cx="46" cy="46" r="21" fill="var(--accent-dim)"/>
    <path d="M46 30 L49 43 L46 46 L43 43 Z" fill="var(--accent)" opacity="0.75"/>
    <path d="M46 62 L49 49 L46 46 L43 49 Z" fill="var(--accent)" opacity="0.45"/>
    <path d="M30 46 L43 49 L46 46 L43 43 Z" fill="var(--accent)" opacity="0.45"/>
    <path d="M62 46 L49 49 L46 46 L49 43 Z" fill="var(--accent)" opacity="0.75"/>
    {[0,90,180,270].map((deg,i)=>{const r=(deg*Math.PI)/180;return <circle key={i} cx={46+43*Math.cos(r)} cy={46+43*Math.sin(r)} r="3.5" fill="var(--accent)" opacity="0.55"/>})}
  </svg>
)

export default function App() {
  const [tab, setTab] = useState('file')
  const [file, setFile] = useState(null)
  const [urlVal, setUrlVal] = useState('')
  const [textVal, setTextVal] = useState('')
  const [processing, setProcessing] = useState(false)
  const [ready, setReady] = useState(false)
  const [docSrc, setDocSrc] = useState(null)
  const [isDrag, setIsDrag] = useState(false)
  const [msgs, setMsgs] = useState([{type:'welcome'}])
  const [chatVal, setChatVal] = useState('')
  const [toasts, setToasts] = useState([])
  const fileRef = useRef(null)
  const msgsRef = useRef(null)
  const taRef = useRef(null)

  useEffect(()=>{if(ready && msgs[0]?.type==='welcome')setMsgs([{type:'bot',content:'Document indexed and ready. What would you like to know?',source:'rag'}])},[ready])
  useEffect(()=>{if(msgsRef.current)msgsRef.current.scrollTop=msgsRef.current.scrollHeight},[msgs])

  const toast=(msg,type='info')=>{const id=Date.now();setToasts(p=>[...p,{id,msg,type}]);setTimeout(()=>setToasts(p=>p.filter(t=>t.id!==id)),4000)}
  const validateFile=f=>{const ext='.'+f.name.split('.').pop().toLowerCase();if(!['.pdf','.docx','.txt'].includes(ext)){toast('Please upload PDF, DOCX, or TXT','error');return}setFile(f);setReady(false);setDocSrc(null);setMsgs([{type:'welcome'}])}
  const processDoc=async()=>{if(processing)return;if(tab==='file'&&!file){toast('Please select a file','error');return}if(tab==='url'){if(!urlVal){toast('Please enter a URL','error');return}try{new URL(urlVal)}catch{toast('Invalid URL','error');return}}if(tab==='text'&&textVal.length<50){toast('Please enter at least 50 characters','error');return}setProcessing(true);try{const fd=new FormData();fd.append('query','Initialize');fd.append('content_type',tab);if(tab==='file')fd.append('file',file);else if(tab==='url')fd.append('url',urlVal);else fd.append('text',textVal);const res=await fetch('/api/process',{method:'POST',body:fd});const data=await res.json();if(data.error)throw new Error(data.error);setReady(true);setDocSrc(tab);toast('Document processed successfully','success')}catch(e){toast(e.message||'Processing failed','error');setReady(false)}finally{setProcessing(false)}}
  const sendMsg=async()=>{if(!chatVal.trim()||!ready)return;const q=chatVal.trim();setMsgs(p=>[...p,{type:'user',content:q}]);setChatVal('');if(taRef.current)taRef.current.style.height='auto';const tid=Date.now();setMsgs(p=>[...p,{type:'typing',id:tid}]);try{const fd=new FormData();fd.append('query',q);fd.append('content_type',docSrc);if(docSrc==='file')fd.append('file',file);else if(docSrc==='url')fd.append('url',urlVal);else fd.append('text',textVal);const res=await fetch('/api/process',{method:'POST',body:fd});const data=await res.json();setMsgs(p=>p.filter(m=>m.id!==tid));setMsgs(p=>[...p,{type:'bot',content:data.error?`Error: ${data.error}`:data.answer,source:data.source}])}catch{setMsgs(p=>p.filter(m=>m.id!==tid));setMsgs(p=>[...p,{type:'bot',content:'Something went wrong. Please try again.'}])}}
  const clearChat=()=>setMsgs(ready?[{type:'bot',content:'Chat cleared. Ask me anything.',source:null}]:[{type:'welcome'}])
  const fmt=b=>b<1024?b+'B':b<1048576?(b/1024).toFixed(1)+'KB':(b/1048576).toFixed(1)+'MB'
  const md=t=>(typeof window!=='undefined'&&window.marked)?window.marked.parse(t):t.replace(/\n/g,'<br/>')
  const step1ok=file||(tab==='url'&&urlVal)||(tab==='text'&&textVal.length>=50)

  return (
    <>
      <style>{CSS}</style>
      <div className="shell">
        <header className="hdr">
          <HdrBg/>
          <div className="hdr-logo">
            <div className="logo-mark"><LogoSVG/></div>
            <div><div className="logo-name">DocMind</div><div className="logo-sub">AI Document Intelligence</div></div>
          </div>
          <div className="hdr-center">
            <span>Multi-Agent RAG</span><div className="hdr-sep"/><span>Semantic Search</span><div className="hdr-sep"/><span>Real-Time QA</span><div className="hdr-sep"/><span>PDF · DOCX · TXT</span>
          </div>
          <div className="hdr-badge"><div className="live-dot"/>System Active</div>
        </header>

        <div className="hero">
          <HeroBgSVG/>
          <div className="hero-content">
            <div className="hero-ey"><div className="hero-ey-line"/>Intelligent Document Analysis</div>
            <div className="hero-title">Ask anything about<br/><em>your documents.</em></div>
            <div className="hero-sub">Upload a PDF, paste a URL, or enter text — DocMind's multi-agent pipeline extracts precise answers instantly.</div>
            <div className="hero-stats">
              <div><div className="stat-num">98%</div><div className="stat-label">Accuracy</div></div>
              <div className="stat-div"/>
              <div><div className="stat-num">&lt;2s</div><div className="stat-label">Response</div></div>
              <div className="stat-div"/>
              <div><div className="stat-num">3</div><div className="stat-label">Input Formats</div></div>
            </div>
          </div>
        </div>

        <main className="main-grid">
          <aside className="left-panel">
            <div className="lp-top">
              <LpBgSVG/>
              <div className="lp-ey">Document Source</div>
              <div className="lp-title">Upload Content</div>
              <div className="lp-sub">Select a file, URL, or paste text</div>
              <div className="step-bar">
                <div style={{display:'flex',alignItems:'center',gap:6}}>
                  <div className={`s-num ${step1ok?'done':'active'}`}>{step1ok?'✓':'1'}</div>
                  <span className={`s-lbl ${!step1ok?'active':''}`}>Upload</span>
                </div>
                <div className="s-con"/>
                <div style={{display:'flex',alignItems:'center',gap:6}}>
                  <div className={`s-num ${ready?'done':processing?'active':'idle'}`}>{ready?'✓':'2'}</div>
                  <span className={`s-lbl ${processing?'active':''}`}>Process</span>
                </div>
                <div className="s-con"/>
                <div style={{display:'flex',alignItems:'center',gap:6}}>
                  <div className={`s-num ${ready?'active':'idle'}`}>3</div>
                  <span className={`s-lbl ${ready?'active':''}`}>Chat</span>
                </div>
              </div>
            </div>
            <div className="tab-bar">
              {[{id:'file',icon:'fa-file-pdf',label:'File'},{id:'url',icon:'fa-globe',label:'URL'},{id:'text',icon:'fa-align-left',label:'Text'}].map(t=>(
                <button key={t.id} onClick={()=>{setTab(t.id);setReady(false)}} className={`tab-btn ${tab===t.id?'active':''}`}>
                  <div className="tab-icon-box"><i className={`fas ${t.icon}`}/></div>{t.label}
                </button>
              ))}
            </div>
            <div className="upload-body">
              {tab==='file'&&(!file?(
                <div className={`drop-zone ${isDrag?'drag-over':''}`} onClick={()=>fileRef.current?.click()} onDragOver={e=>{e.preventDefault();setIsDrag(true)}} onDragLeave={()=>setIsDrag(false)} onDrop={e=>{e.preventDefault();setIsDrag(false);if(e.dataTransfer.files[0])validateFile(e.dataTransfer.files[0])}}>
                  <DropSVG/>
                  <div className="drop-title">Drop your file here</div>
                  <div className="drop-sub">or click to browse files</div>
                  <div className="type-pills">{['PDF','DOCX','TXT'].map(x=><span key={x} className="type-pill">{x}</span>)}</div>
                  <input type="file" ref={fileRef} onChange={e=>{if(e.target.files[0])validateFile(e.target.files[0])}} accept=".pdf,.docx,.txt" hidden/>
                </div>
              ):(
                <div className="file-card">
                  <div className="file-badge"><FileIconSVG/></div>
                  <div className="file-info"><div className="file-name">{file.name}</div><div className="file-meta">{fmt(file.size)} · {file.name.split('.').pop().toUpperCase()}</div></div>
                  <button className="file-del" onClick={()=>{setFile(null);if(fileRef.current)fileRef.current.value='';setReady(false)}}><i className="fas fa-times"/></button>
                </div>
              ))}
              {tab==='url'&&(<div className="field-wrap"><i className="fas fa-link field-icon"/><input type="url" value={urlVal} onChange={e=>setUrlVal(e.target.value)} placeholder="https://example.com/document" className="field-input"/></div>)}
              {tab==='text'&&(<textarea value={textVal} onChange={e=>setTextVal(e.target.value)} placeholder="Paste your text content here…" className="field-ta"/>)}
            </div>
            <div className="proc-sec">
              <div className="proc-sep"/>
              {!processing&&!ready&&(<button className="proc-btn" onClick={processDoc}><div className="btn-ring"><ArrowSVG/></div>Process Document</button>)}
              {processing&&(<div className="status-card"><div className="sc-ic proc"><div className="spinner"/></div><div><div className="sc-t">Processing Document</div><div className="sc-s">Building knowledge index…</div></div></div>)}
              {ready&&(<div className="status-card"><div className="sc-ic ready"><CheckSVG/></div><div><div className="sc-t">Ready to Chat</div><div className="sc-s">Document successfully indexed</div></div></div>)}
            </div>
          </aside>

          <section className="right-panel">
            {!ready&&(<div className="chat-overlay"><div className="overlay-box"><div className="ov-ic"><LockSVG/></div><div className="ov-title">Process a Document</div><div className="ov-sub">Upload and process your document on the left to unlock the AI chat interface.</div></div></div>)}
            <div className="chat-hdr">
              <ChtHdrBgSVG/>
              <div className="ch-info"><div className="ch-ic"><ChatIconSVG/></div><div><div className="ch-title">Document Chat</div><div className="ch-sub">Multi-Agent RAG · Semantic Retrieval</div></div></div>
              <div className="ch-acts"><button className="ch-btn" onClick={clearChat} title="Clear"><i className="fas fa-trash-alt"/></button></div>
            </div>
            <div className="msgs" ref={msgsRef}>
              {msgs.map((m,i)=>{
                if(m.type==='welcome')return(
                  <div key={i} className="welcome-wrap">
                    <WelcomeSVG/>
                    <div className="w-title">Welcome to DocMind</div>
                    <div className="w-sub">Upload a document using the panel on the left, then ask me anything about its content.</div>
                    <div className="w-chips">
                      {[{icon:'fa-search',label:'Semantic Search'},{icon:'fa-network-wired',label:'Multi-Agent RAG'},{icon:'fa-bolt',label:'Instant Answers'},{icon:'fa-shield-alt',label:'Accurate & Cited'}].map(c=>(<div key={c.label} className="w-chip"><i className={`fas ${c.icon}`}/>{c.label}</div>))}
                    </div>
                  </div>
                )
                if(m.type==='typing')return(<div key={i} className="msg-row bot"><div className="msg-av bot"><BotSVG/></div><div className="msg-bub bot"><div className="typing-ind"><span/><span/><span/></div></div></div>)
                const isUser=m.type==='user'
                return(
                  <div key={i} className={`msg-row ${isUser?'user':'bot'}`}>
                    <div className={`msg-av ${isUser?'user':'bot'}`}>{isUser?<UserSVG/>:<BotSVG/>}</div>
                    <div className={`msg-bub ${isUser?'user':'bot'}`}>
                      {isUser?m.content:(<><div dangerouslySetInnerHTML={{__html:md(m.content)}}/>{m.source&&(<div className={`src-tag ${m.source==='rag'?'doc':'wiki'}`}><i className={`fas ${m.source==='rag'?'fa-file-alt':'fa-globe'}`}/>{m.source==='rag'?'From Document':'From Wikipedia'}</div>)}</>)}
                    </div>
                  </div>
                )
              })}
            </div>
            <div className="chat-input-bar">
              <div className="chat-field">
                <textarea ref={taRef} value={chatVal} onChange={e=>setChatVal(e.target.value)} onKeyDown={e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMsg()}}} onInput={e=>{e.target.style.height='auto';e.target.style.height=Math.min(e.target.scrollHeight,100)+'px'}} disabled={!ready} placeholder="Ask a question about your document…" rows={1} className="chat-ta"/>
                <button onClick={sendMsg} disabled={!ready||!chatVal.trim()} className="send-btn"><SendSVG/></button>
              </div>
              <div className="input-hint">Enter to send · Shift+Enter for new line</div>
            </div>
          </section>
        </main>

        <footer className="footer">
          <div className="ft-left"><span className="ft-logo">DocMind</span><div className="ft-div"/><span className="ft-copy">© 2026 All rights reserved</span></div>
          <div className="ft-cred">Developed by <strong>Naman Nanda</strong></div>
        </footer>
      </div>
      <div className="toast-stack">
        {toasts.map(t=>(<div key={t.id} className={`toast ${t.type}`}><i className={`fas ${t.type==='success'?'fa-check-circle':t.type==='error'?'fa-exclamation-circle':'fa-info-circle'}`}/>{t.msg}</div>))}
      </div>
    </>
  )
}