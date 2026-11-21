"""v5: yeni arayüz (derin deniz camı), SVG ikonlar, açılış ekranı, ayarlar, inci ekonomisi, sergi geliri,
güzellik puanı, çiftleşme/üreme, grafik iyileştirmeleri."""
import os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'index.template.html')
s = open(P, encoding='utf-8').read()

def R(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:100]); s = s.replace(a, b)

# ============================== CSS ==============================
CSS = r"""
/*FONTS*/
:root{--glass:rgba(10,34,62,.78);--glass2:rgba(14,44,78,.94);--line:rgba(140,230,255,.22);--cyan:#5EE6E0;--coral:#FF6F91;--pearl:#F4FBFF;--gold:#FFC94A;--kelp:#46D39A;--navy:#0E2A47}
html,body{font-family:'Fredoka','Trebuchet MS',system-ui,sans-serif}
button,textarea{font-family:inherit}
i[data-ic]{display:inline-flex;width:22px;height:22px;flex:none;align-items:center;justify-content:center}
i[data-ic] svg{width:100%;height:100%;display:block}
#hud{gap:8px;padding:calc(8px + env(safe-area-inset-top)) 12px 4px;align-items:flex-start;flex-wrap:nowrap}
.player{display:flex;align-items:center;gap:9px;background:var(--glass);border:1px solid var(--line);border-radius:30px 18px 18px 30px;padding:3px 14px 3px 3px;backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);box-shadow:0 6px 18px rgba(0,10,30,.35)}
.port{position:relative;width:46px;height:46px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#4fd6ff,#0d5a9a 72%);display:grid;place-items:center;box-shadow:inset 0 0 0 3px rgba(184,244,255,.35),inset 0 -6px 10px rgba(0,0,0,.35)}
.port b{font-size:19px;font-weight:700;color:#fff;text-shadow:0 2px 0 #0a3a66;position:relative;z-index:1}
.port .ring{position:absolute;left:-4px;top:-4px;width:54px;height:54px;transform:rotate(-90deg)}
.ring circle{fill:none;stroke-width:4}
.ring .rt{stroke:rgba(255,255,255,.14)}
.ring .rf{stroke:var(--gold);stroke-linecap:round;stroke-dasharray:157;stroke-dashoffset:157;transition:stroke-dashoffset .5s}
.pname{font-weight:600;font-size:14px;color:var(--pearl);line-height:1.15}
.pxp{font-size:12px;color:#9fd8ee;font-weight:500}
.cur{display:flex;align-items:center;gap:6px;height:36px;margin-top:5px;background:var(--glass);border:1px solid var(--line);border-radius:18px;padding:0 12px 0 5px;color:#fff;font-weight:600;font-size:16px;backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);cursor:pointer}
.cur b{font-variant-numeric:tabular-nums}
.cur i[data-ic]{width:26px;height:26px}
.cur .plus{width:20px;height:20px;border-radius:50%;background:var(--coral);display:grid;place-items:center;font-size:15px;line-height:1;margin-left:2px;box-shadow:0 2px 0 #c2416b;color:#fff}
.stat{display:flex;align-items:center;gap:5px;height:32px;margin-top:7px;background:rgba(10,34,62,.58);border:1px solid var(--line);border-radius:16px;padding:0 10px 0 6px;color:#dff6ff;font-weight:600;font-size:14px;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);white-space:nowrap}
.stat.bad{background:rgba(130,24,48,.82);border-color:#ff8fa0;animation:pulse 1s infinite alternate}
.stat.feeder{border-color:var(--kelp)}
.stars{display:flex;gap:1px;margin-left:1px}
.stars i[data-ic]{width:12px;height:12px;opacity:.25;filter:grayscale(1)}
.stars i[data-ic].on{opacity:1;filter:none}
.ib{position:relative;width:42px;height:42px;margin-top:2px;border-radius:50%;border:1px solid var(--line);background:var(--glass);display:grid;place-items:center;cursor:pointer;backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);flex:none}
.ib i[data-ic]{width:22px;height:22px}
.ib:focus-visible,#tools button:focus-visible,.row:focus-visible,.btn:focus-visible{outline:3px solid var(--cyan);outline-offset:2px}
#tools{background:rgba(10,34,62,.62);border:1px solid var(--line);border-radius:34px;padding:7px 10px;gap:10px;box-shadow:0 10px 28px rgba(0,10,30,.45)}
#tools button{width:64px;height:64px;border-radius:50%;border:none;background:radial-gradient(circle at 35% 28%,#66dcff,#1a6fb8 62%,#0f4f8c);box-shadow:inset 0 2px 0 rgba(255,255,255,.45),inset 0 -5px 10px rgba(0,20,60,.45),0 4px 10px rgba(0,10,30,.4);gap:0;padding-top:3px;color:#fff;font-weight:600;font-size:11px;text-shadow:0 1px 2px rgba(0,30,60,.6);position:relative;overflow:hidden}
#tools button::after{content:"";position:absolute;left:13px;top:7px;width:20px;height:9px;border-radius:50%;background:rgba(255,255,255,.32);transform:rotate(-25deg);pointer-events:none}
#tools button i[data-ic]{width:28px;height:28px}
#tools button span{font-size:11px;line-height:1.15}
#tools button.on{background:radial-gradient(circle at 35% 28%,#ffc0d0,#ff6f91 60%,#d4436b);box-shadow:inset 0 2px 0 rgba(255,255,255,.5),inset 0 -5px 10px rgba(110,10,40,.35),0 0 0 3px rgba(255,111,145,.35),0 0 18px rgba(255,111,145,.55);color:#fff}
#tools button.green{background:radial-gradient(circle at 35% 28%,#fff0b0,#f2b52c 60%,#c98a0b);color:#4a2e00;text-shadow:none}
#tools button:active{transform:scale(.93)}
.modal{background:rgba(2,14,32,.62);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px)}
.mbox{background:linear-gradient(180deg,#123a66 0%,#0b2748 100%);color:var(--pearl);border:1px solid rgba(140,230,255,.3);border-radius:26px;box-shadow:0 24px 60px rgba(0,0,0,.55),inset 0 1px 0 rgba(255,255,255,.12)}
.mbox.sm{max-width:420px}
.mhead{background:none;border-bottom:1px solid var(--line);padding:12px 14px}
.mhead .ttl{color:#fff;text-shadow:none;font-weight:700;font-size:21px;display:flex;align-items:center;gap:8px}
.mhead .ttl i[data-ic]{width:26px;height:26px}
.tabs button,.btabs button{border:1px solid var(--line);background:rgba(255,255,255,.06);color:#bfe9f7;border-radius:14px;font-weight:600;font-size:14px}
.tabs button.on,.btabs button.on{background:var(--cyan);color:#06304a;border-color:var(--cyan)}
.x{background:rgba(255,255,255,.1);border:1px solid var(--line);box-shadow:none;display:grid;place-items:center;padding:0}
.x i[data-ic]{width:16px;height:16px}
.mbody{color:#dcefff}
.mbody b{color:var(--cyan)}
.card{background:linear-gradient(180deg,rgba(255,255,255,.1),rgba(255,255,255,.035));border:1px solid rgba(140,230,255,.16);border-top:3px solid var(--rc,#9fb4c8);box-shadow:none;border-radius:18px;color:var(--pearl);padding:8px}
.card .cn{color:#fff;font-weight:600}
.card .cm{color:#9fd0e4;font-weight:500}
.card canvas{background:radial-gradient(ellipse at 50% 15%,#2f9fd6,#0d4f80 70%,#08375c)}
.card .rar{font-size:11px;font-weight:600;color:var(--rc,#9fb4c8);margin-top:-2px}
.card .lock{top:34px}
.btn{font-weight:600;font-size:14px;border:none;border-radius:14px}
.btn.g{background:linear-gradient(#6be6ad,#2fb874);box-shadow:0 3px 0 #1f8a55;color:#053a24}
.btn.y{background:linear-gradient(#ffe08a,#f2b52c);box-shadow:0 3px 0 #b8800b;color:#4a2e00}
.btn.r{background:linear-gradient(#ff9fb5,#ff6f91);box-shadow:0 3px 0 #c2416b;color:#fff}
.btn.p{background:linear-gradient(#ece3ff,#b9a6f5);box-shadow:0 3px 0 #7d67c9;color:#2e2366}
.card .btn{background:linear-gradient(#ffe08a,#f2b52c);color:#4a2e00;box-shadow:0 3px 0 #b8800b}
.card .btn.p{background:linear-gradient(#ece3ff,#b9a6f5);color:#2e2366;box-shadow:0 3px 0 #7d67c9}
.card .btn.sel{background:rgba(255,255,255,.12);color:#bfe9f7;box-shadow:none}
.card .btn:disabled{filter:grayscale(.7);opacity:.5}
.coin,.pearlc{display:inline-block;width:22px;height:22px;background:center/contain no-repeat;border:none;box-shadow:none;border-radius:0;vertical-align:middle;flex:none}
#info{background:linear-gradient(180deg,#123a66,#0b2748);color:var(--pearl);border:1px solid rgba(140,230,255,.3)}
#info h3{color:#fff}
#info h3 small{background:var(--cyan);color:#06304a}
.bar{color:#9fd0e4}.bar .b{background:rgba(255,255,255,.1);box-shadow:none}
.irow{flex-wrap:wrap}
.mate{margin-top:8px;padding:7px 10px;border-radius:12px;background:rgba(255,111,145,.14);border:1px solid rgba(255,111,145,.45);color:#ffd2de;font-weight:600;font-size:13px;display:flex;align-items:center;gap:8px}
.mate i[data-ic]{width:18px;height:18px}
.mate .mb{flex:1;height:8px;border-radius:6px;background:rgba(255,255,255,.12);overflow:hidden}
.mate .mb i{display:block;height:100%;background:linear-gradient(90deg,#ff9fb5,#ff6f91)}
.login{background:linear-gradient(180deg,rgba(255,201,74,.2),rgba(255,201,74,.06));border:1px solid rgba(255,201,74,.45);box-shadow:none;color:#ffe9b0}
.days div{background:rgba(255,255,255,.08);border-color:rgba(255,201,74,.3);color:#ffe9b0}
.days div.got{background:var(--kelp);color:#053a24;border-color:var(--kelp)}
.q,.ach{background:rgba(255,255,255,.06);box-shadow:none;border:1px solid rgba(140,230,255,.15)}
.q .qr,.ach .ad,.qnote,.albh{color:#9fd0e4}
.q .qb{background:rgba(255,255,255,.1)}
.alb .card.unk canvas{background:radial-gradient(ellipse at 50% 20%,#1e4a68,#0a2236 70%)}
#toast{background:rgba(8,30,56,.94);border:1px solid var(--line);font-weight:600}
#placebar,#cleanBar{background:var(--glass2);color:#fff;border:1px solid var(--line)}
#cleanBar .cbt small{color:#9fd0e4}
#cleanBar .cbb{background:rgba(255,255,255,.12)}
#saveM textarea{background:rgba(0,0,0,.25);color:#dff6ff;border-color:var(--line)}
.setl{display:flex;flex-direction:column;gap:8px}
.row{display:flex;align-items:center;gap:12px;width:100%;padding:12px 14px;border-radius:16px;border:1px solid var(--line);background:rgba(255,255,255,.06);color:#fff;font-weight:600;font-size:16px;cursor:pointer;text-align:left}
.row i[data-ic]{width:24px;height:24px}
.row span{flex:1}
.row small{color:#9fd0e4;font-weight:500;font-size:12px;display:block}
.tg{width:46px;height:26px;border-radius:13px;background:var(--kelp);position:relative;transition:background .2s;flex:none}
.tg::after{content:"";position:absolute;top:3px;left:23px;width:20px;height:20px;border-radius:50%;background:#fff;transition:left .2s}
.row.off .tg{background:rgba(255,255,255,.2)}.row.off .tg::after{left:3px}
.row:disabled{opacity:.45}
#collectM{position:absolute;left:50%;transform:translateX(-50%);bottom:calc(98px + env(safe-area-inset-bottom));width:min(360px,92%);z-index:7;background:var(--glass2);border:1px solid var(--line);border-radius:22px;padding:10px;display:flex;flex-direction:column;gap:8px;box-shadow:0 14px 34px rgba(0,0,0,.5)}
.plist{display:flex;flex-direction:column;gap:8px;margin-top:6px}
.plist div{display:flex;align-items:center;gap:10px;padding:9px 12px;border-radius:14px;background:rgba(255,255,255,.06);border:1px solid var(--line);font-weight:500}
.plist div b{margin-left:auto;color:#d9ccff}
#splash{position:absolute;inset:0;z-index:30;display:flex;align-items:center;justify-content:center;background:linear-gradient(180deg,rgba(6,44,79,.35),rgba(4,24,48,.82));backdrop-filter:blur(3px);-webkit-backdrop-filter:blur(3px);cursor:pointer;transition:opacity .5s}
#splash.hide{opacity:0;pointer-events:none}
.spl-in{text-align:center;padding:20px}
#splLogo{width:min(600px,78vw);max-height:44vh;object-fit:contain;filter:drop-shadow(0 12px 26px rgba(0,20,50,.55));animation:float 4s ease-in-out infinite}
.spl-tap{margin-top:16px;font-weight:600;font-size:21px;color:#fff;animation:breathe 1.6s ease-in-out infinite}
.spl-sub{margin-top:6px;font-size:13px;color:#9fd8ee}
@keyframes float{50%{transform:translateY(-8px)}}
@keyframes breathe{50%{opacity:.45}}
@media (prefers-reduced-motion:reduce){#splLogo,.spl-tap{animation:none}}
body.small #hud{padding-top:5px;gap:6px}
body.small .port{width:38px;height:38px}
body.small .port .ring{width:46px;height:46px}
body.small .port b{font-size:16px}
body.small .pname{font-size:12px}
body.small .pxp{font-size:10px}
body.small .cur{height:30px;font-size:14px;margin-top:4px}
body.small .cur i[data-ic]{width:22px;height:22px}
body.small .stat{height:28px;font-size:12px;margin-top:5px;padding:0 8px 0 5px}
body.small .stat i[data-ic]{width:18px;height:18px}
body.small .ib{width:36px;height:36px}
body.small #tools{gap:7px;padding:5px 8px;bottom:6px}
body.small #tools button{width:54px;height:54px}
body.small #tools button i[data-ic]{width:24px;height:24px}
body.small #tools button span{font-size:10px}
body.small #tools button::after{left:10px;top:5px;width:16px;height:7px}
body.small #collectM{bottom:72px}
</style>"""
R("</style>", CSS)

# ============================== HTML ==============================
a = s.index('<div id="hud">'); b = s.index('<div id="tools">')
s = s[:a] + '''<div id="hud">
  <div class="player" title="Seviye">
    <div class="port"><svg class="ring" viewBox="0 0 54 54"><circle cx="27" cy="27" r="25" class="rt"/><circle cx="27" cy="27" r="25" class="rf" id="xpring"/></svg><b id="lvl">1</b></div>
    <div class="pinfo"><div class="pname">Akvaryumum</div><div class="pxp" id="xpt">0/40 XP</div></div>
  </div>
  <div class="cur" id="coinChip" title="Altın"><i data-ic="coin"></i><b id="coins">0</b></div>
  <div class="cur" id="pearlChip" title="İnci"><i data-ic="pearl"></i><b id="pearls">0</b><span class="plus">+</span></div>
  <div class="sp"></div>
  <div class="stat" id="beautyChip" title="Güzellik puanı"><i data-ic="star"></i><b id="beauty">0</b><span class="stars" id="stars"><i data-ic="star"></i><i data-ic="star"></i><i data-ic="star"></i></span></div>
  <div class="stat" id="fishChip" title="Balık sayısı"><i data-ic="fish"></i><b id="fc">0/10</b></div>
  <div class="stat" id="clp" title="Temizlik"><i data-ic="drop"></i><b id="cl">100%</b></div>
  <button class="ib" id="bookB" title="Defter" aria-label="Defter"><i data-ic="book"></i><span class="badge hidden" id="bookBadge">!</span></button>
  <button class="ib" id="setB" title="Ayarlar" aria-label="Ayarlar"><i data-ic="gear"></i></button>
</div>

''' + s[b:]
R('''  <button data-m="select" class="on"><span>👆</span>Seç</button>
  <button data-m="feed"><span>🍤</span>Yem</button>
  <button data-m="clean"><span>🧽</span>Temizle</button>
  <button id="sellAll" class="green"><span>💰</span>Topla</button>
  <button id="shopB"><span>🛒</span>Mağaza</button>''',
'''  <button data-m="select" class="on"><i data-ic="hand"></i><span>Seç</span></button>
  <button data-m="feed"><i data-ic="food"></i><span>Yem</span></button>
  <button data-m="clean"><i data-ic="sponge"></i><span>Temizle</span></button>
  <button id="sellAll" class="green"><i data-ic="bag"></i><span>Topla</span></button>
  <button id="shopB"><i data-ic="shop"></i><span>Mağaza</span></button>''')
R('<div id="help" class="modal hidden">', '''<div id="collectM" class="hidden">
  <button class="row" id="colInc"><i data-ic="bag"></i><span id="colIncT">Gelirleri topla</span></button>
  <button class="row" id="colSell"><i data-ic="star"></i><span id="colSellT">Olgun balıkları sat</span></button>
</div>
<div id="setM" class="modal hidden">
  <div class="mbox sm">
    <div class="mhead"><div class="ttl"><i data-ic="gear"></i>Ayarlar</div><button class="x" id="setX" aria-label="Kapat"><i data-ic="close"></i></button></div>
    <div class="mbody setl">
      <button class="row" id="mus"><i data-ic="music"></i><span>Müzik</span><em class="tg"></em></button>
      <button class="row" id="snd"><i data-ic="sound"></i><span>Ses efektleri ve ortam sesi</span><em class="tg"></em></button>
      <button class="row" id="saveB"><i data-ic="save"></i><span>Kayıt ve yedek kod<small>İlerlemeni sakla veya başka cihaza taşı</small></span></button>
      <button class="row" id="hlp"><i data-ic="help"></i><span>Nasıl oynanır</span></button>
    </div>
  </div>
</div>
<div id="pearlM" class="modal hidden">
  <div class="mbox sm">
    <div class="mhead"><div class="ttl"><i data-ic="pearl"></i>İnci</div><button class="x" id="pearlX" aria-label="Kapat"><i data-ic="close"></i></button></div>
    <div class="mbody">
      <p>İnci, akvaryumun değerli parasıdır. Beklemeyi atlamak, nadir yumurta ve özel süsler almak için kullanılır.</p>
      <div class="plist">
        <div><i data-ic="star"></i>Seviye atlamak<b>+2</b></div>
        <div><i data-ic="book"></i>Başarım rozetleri<b>+2 / +5 / +15</b></div>
        <div><i data-ic="heart"></i>Günlük girişin 3. ve 7. günü<b>+1 / +5</b></div>
        <div><i data-ic="star"></i>Akvaryum yıldızları (güzellik)<b>+3 / +5 / +10</b></div>
        <div><i data-ic="book"></i>Her günün 3. görevi<b>+1</b></div>
      </div>
    </div>
  </div>
</div>
<div id="splash"><div class="spl-in"><img id="splLogo" alt="Mercan Akvaryum"><div class="spl-tap">Dokun ve başla</div><div class="spl-sub">Sesi açmayı unutma</div></div></div>

<div id="help" class="modal hidden">''')
R("<p>Kendi akvaryumuna hoş geldin! Balık yumurtası al, balıklarını besle, büyüt ve sat.</p>",
  "<p>Kendi akvaryumuna hoş geldin! Balık yumurtası al, balıklarını besle, büyüt; ister sat, ister sergile.</p>\n"
  "      <p><b>Sergi geliri:</b> Olgun balıklar akvaryumda kaldıkça altın biriktirir. Balığın üstünde kese çıkınca dokun ya da <b>Topla</b>'ya bas.</p>\n"
  "      <p><b>Çiftleşme:</b> Aynı türden iki yetişkin balık kendiliğinden eşleşir, kalpli rozet alır, bir süre flört eder ve yumurta bırakır. Eşleşmiş balıkları satarsan çift ayrılır.</p>\n"
  "      <p><b>Güzellik ve inci:</b> Her süs güzellik puanı verir, puan arttıkça sergi geliri artar. İnci ile beklemeyi atlayabilir, nadir yumurta ve özel süsler alabilirsin.</p>")

# ============================== JS: ikonlar ==============================
ICONS = r"""
/* ================= SVG İKON SETİ ================= */
const ICON={
coin:'<svg viewBox="0 0 32 32"><circle cx="16" cy="16.5" r="14" fill="#B57A06"/><circle cx="16" cy="15.2" r="13.2" fill="#FFC94A"/><circle cx="16" cy="15.2" r="9.4" fill="none" stroke="#E8A21C" stroke-width="2"/><path d="M10.2 15.4c2.2-3 5.6-3.9 8.6-2.6l2.6-2v8.6l-2.6-2c-3 1.3-6.4.4-8.6-2z" fill="#D49413"/><ellipse cx="11.2" cy="9.4" rx="4" ry="2.1" fill="#FFF3C0" opacity=".85" transform="rotate(-32 11.2 9.4)"/></svg>',
pearl:'<svg viewBox="0 0 32 32"><defs><radialGradient id="pgr" cx=".38" cy=".32" r=".78"><stop offset="0" stop-color="#fff"/><stop offset=".45" stop-color="#EEF5FF"/><stop offset=".8" stop-color="#CDBDF3"/><stop offset="1" stop-color="#8F7FD0"/></radialGradient></defs><circle cx="16" cy="16" r="13" fill="url(#pgr)"/><ellipse cx="11.3" cy="10.6" rx="4.2" ry="2.6" fill="#fff" transform="rotate(-35 11.3 10.6)"/><circle cx="21.5" cy="22" r="2" fill="#fff" opacity=".5"/></svg>',
star:'<svg viewBox="0 0 32 32"><path d="M16 3l3.9 8.2 9 1.1-6.6 6.2 1.7 8.9L16 23l-8 4.4 1.7-8.9-6.6-6.2 9-1.1z" fill="#FFC94A" stroke="#C98A0B" stroke-width="1.6" stroke-linejoin="round"/><path d="M11.8 12l2.6-.4" stroke="#FFF3C0" stroke-width="2" stroke-linecap="round"/></svg>',
fish:'<svg viewBox="0 0 32 32"><path d="M7 16c3-5 8-7 13-6.5 3.5.4 6 2.8 7 6.5-1 3.7-3.5 6.1-7 6.5-5 .5-10-1.5-13-6.5z" fill="#5EE6E0"/><path d="M8.5 16L2.5 10.5v11z" fill="#3CC9C3"/><circle cx="22" cy="14.6" r="1.7" fill="#0E2A47"/><path d="M17.5 11.8c.9 2.6.9 5.8 0 8.4" stroke="#2BB8B2" stroke-width="1.6" fill="none" stroke-linecap="round"/></svg>',
drop:'<svg viewBox="0 0 32 32"><path d="M16 3c5 7 9 11.5 9 16a9 9 0 0 1-18 0c0-4.5 4-9 9-16z" fill="#7FD3FF"/><path d="M11.5 19.5a4.5 4.5 0 0 0 3.5 4.4" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round"/></svg>',
book:'<svg viewBox="0 0 32 32" fill="none" stroke="#fff" stroke-width="2.4" stroke-linejoin="round"><path d="M16 8.5c-3-2-7-2.5-11-2v18c4-.5 8 0 11 2 3-2 7-2.5 11-2v-18c-4-.5-8 0-11 2z"/><path d="M16 8.5v18"/></svg>',
gear:'<svg viewBox="0 0 24 24"><path fill="#fff" fill-rule="evenodd" d="M19.4 13a7.6 7.6 0 0 0 0-2l2.1-1.6-2-3.5-2.5 1a7.4 7.4 0 0 0-1.7-1L15 3.3h-4l-.4 2.6a7.4 7.4 0 0 0-1.7 1l-2.5-1-2 3.5L6.6 11a7.6 7.6 0 0 0 0 2l-2.1 1.6 2 3.5 2.5-1a7.4 7.4 0 0 0 1.7 1l.3 2.6h4l.4-2.6a7.4 7.4 0 0 0 1.7-1l2.5 1 2-3.5zM12 15.4a3.4 3.4 0 1 1 0-6.8 3.4 3.4 0 0 1 0 6.8z"/></svg>',
hand:'<svg viewBox="0 0 32 32"><path d="M13 6a2.5 2.5 0 0 1 5 0v8.3l5.1 1c1.9.4 3.1 2.2 2.8 4l-1 6.4A4 4 0 0 1 21 29h-6a4 4 0 0 1-3.2-1.6l-5.3-6.9a2.3 2.3 0 0 1 3.4-3.1L13 20z" fill="#fff"/><path d="M9.6 7a6.3 6.3 0 0 1 11.8 0" stroke="#fff" stroke-width="2" fill="none" opacity=".6" stroke-linecap="round"/></svg>',
food:'<svg viewBox="0 0 32 32"><rect x="8" y="10" width="16" height="18" rx="3" fill="#FF8A3D"/><rect x="7" y="7" width="18" height="5" rx="2" fill="#FFD27A"/><rect x="11" y="16" width="10" height="7" rx="2" fill="#fff" opacity=".85"/><circle cx="12.5" cy="4" r="1.5" fill="#FFB347"/><circle cx="17" cy="2.8" r="1.3" fill="#E07B2A"/><circle cx="21" cy="4.5" r="1.2" fill="#FFB347"/></svg>',
sponge:'<svg viewBox="0 0 32 32"><rect x="4" y="10" width="24" height="7" rx="3" fill="#2F9E5A"/><rect x="4" y="15" width="24" height="12" rx="3.5" fill="#FFD84A"/><circle cx="10" cy="20" r="1.5" fill="#D9A21C"/><circle cx="16" cy="23" r="1.3" fill="#D9A21C"/><circle cx="22" cy="19.5" r="1.6" fill="#D9A21C"/><circle cx="24" cy="5.5" r="2.3" fill="none" stroke="#DFF8FF" stroke-width="1.5"/><circle cx="18.6" cy="4.2" r="1.3" fill="none" stroke="#DFF8FF" stroke-width="1.2"/></svg>',
bag:'<svg viewBox="0 0 32 32"><path d="M11.5 9h9l-2.2-4.2h-4.6z" fill="#B57A06"/><path d="M12 9c-5 4-8 9-7 13 1 4.5 5 6 11 6s10-1.5 11-6c1-4-2-9-7-13z" fill="#E8A21C"/><rect x="11" y="8" width="10" height="3" rx="1.5" fill="#8A5A08"/><circle cx="16" cy="19.5" r="5.2" fill="#FFD25E"/><path d="M13.2 19.6c1.2-1.6 3-2 4.6-1.4l1.4-1v4.8l-1.4-1c-1.6.6-3.4.2-4.6-1.4z" fill="#C98A0B"/></svg>',
shop:'<svg viewBox="0 0 32 32"><path d="M7 11h18l-1.5 15a2.5 2.5 0 0 1-2.5 2.2H11A2.5 2.5 0 0 1 8.5 26z" fill="#fff"/><path d="M12 13V9.2a4 4 0 0 1 8 0V13" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round"/><path d="M12.2 18.5c1.6 2.2 6 2.2 7.6 0" stroke="#1a6fb8" stroke-width="2" fill="none" stroke-linecap="round"/></svg>',
music:'<svg viewBox="0 0 24 24"><path fill="#fff" d="M9 17.2A2.8 2.8 0 1 1 7.2 14.6V5.2L19 3v12.3a2.8 2.8 0 1 1-1.8-2.6V7.4l-8.2 1.5z"/></svg>',
sound:'<svg viewBox="0 0 24 24"><path d="M4 9h4l5-4v14l-5-4H4z" fill="#fff"/><path d="M16 8.5a5 5 0 0 1 0 7M18.5 6a8.5 8.5 0 0 1 0 12" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg>',
save:'<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round"><path d="M5 4h11l3 3v13H5z"/><path d="M8 4v5h7V4M8 20v-6h8v6"/></svg>',
help:'<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.6 2.6 0 0 1 5 .9c0 1.8-2.5 2.2-2.5 3.6"/><circle cx="12" cy="17" r=".7" fill="#fff"/></svg>',
close:'<svg viewBox="0 0 24 24" stroke="#fff" stroke-width="3" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>',
heart:'<svg viewBox="0 0 24 24"><path d="M12 21s-7.5-4.6-9.3-9.3C1.4 8.2 3.6 4.5 7.2 4.5c2 0 3.6 1.1 4.8 2.8 1.2-1.7 2.8-2.8 4.8-2.8 3.6 0 5.8 3.7 4.5 7.2C19.5 16.4 12 21 12 21z" fill="#FF6F91"/><path d="M6.5 8.5c.6-1 1.4-1.4 2.4-1.4" stroke="#ffd2de" stroke-width="1.6" fill="none" stroke-linecap="round"/></svg>',
bolt:'<svg viewBox="0 0 24 24"><path d="M13 2L4 14h7l-1 8 9-12h-7z" fill="#FFC94A" stroke="#C98A0B" stroke-width="1.2" stroke-linejoin="round"/></svg>',
egg:'<svg viewBox="0 0 24 24"><ellipse cx="12" cy="13" rx="7" ry="9" fill="#fff4e0"/><path d="M8 9c.8-2 2-3 3.4-3.2" stroke="#fff" stroke-width="1.6" fill="none" stroke-linecap="round"/><circle cx="14" cy="11" r="1.4" fill="#d9b0ff"/><circle cx="10" cy="15.5" r="1.1" fill="#d9b0ff"/></svg>',
};
function paintIcons(root){(root||document).querySelectorAll('i[data-ic]').forEach(e=>{if(e.dataset.p!==e.dataset.ic){e.innerHTML=ICON[e.dataset.ic]||'';e.dataset.p=e.dataset.ic;}});}
(function(){const st=document.createElement('style');const u=k=>`url("data:image/svg+xml;charset=utf-8,${encodeURIComponent(ICON[k])}")`;
 st.textContent=`.coin{background-image:${u('coin')}}.pearlc{background-image:${u('pearl')}}`;document.head.appendChild(st);
 new MutationObserver(()=>paintIcons()).observe(document.getElementById('app'),{childList:true,subtree:true});paintIcons();})();
const LOGO_SRC='/*LOGO*/';
if(LOGO_SRC.startsWith('data:'))document.getElementById('splLogo').src=LOGO_SRC;else document.getElementById('splLogo').replaceWith(Object.assign(document.createElement('div'),{textContent:'Mercan Akvaryum',style:'font-size:46px;font-weight:700;color:#ff6f91;text-shadow:0 4px 0 #0b2140'}));
"""
R("/* ================= BALIK TÜRLERİ ================= */", ICONS + "\n/* ================= BALIK TÜRLERİ ================= */")

# ============================== EKONOMİ ==============================
R("const fname=f=>f.rare?(RARE[f.sid]||f.sp.name):f.sp.name;",
"""const fname=f=>f.rare?(RARE[f.sid]||f.sp.name):f.sp.name;
/* --- v5 ekonomi: büyüme süreleri (dk), satış ve XP formülü --- */
const GROW_MIN={neon:3,gold:6,clown:10,angel:14,seahorse:18,tang:22,betta:30,discus:40,jelly:50,koi:60,lion:90,puffer:120,shark:180};
for(const sp of SPECIES){const m=GROW_MIN[sp.id];if(m){sp.grow=m*60;sp.sell=Math.round(sp.cost*1.6+m*3);sp.sxp=Math.round(4+m*.9);}}
const hungerT=sp=>Math.min(7200,Math.max(600,sp.grow*.5));
const RAR=[{n:'Yaygın',c:'#9fb4c8'},{n:'Sıradışı',c:'#46D39A'},{n:'Nadir',c:'#4DA3FF'},{n:'Destansı',c:'#B07CFF'},{n:'Efsanevi',c:'#FFB23F'}];
const rarity=l=>RAR[Math.min(4,Math.floor((l-1)/2))];
const fmtT=sec=>{sec=Math.max(0,Math.round(sec));if(sec<60)return sec+' sn';const m=Math.round(sec/60);return m<60?m+' dk':Math.floor(m/60)+' sa'+(m%60?' '+m%60+' dk':'');};
const THEME_BEAUTY={ocean:0,fresh:15,reef:30,night:40};
let beautyCache=0;
const beautyMult=()=>1+Math.min(1.5,beautyCache/400);
const incomeRate=f=>f.sp.sell*.006*(f.rare?3:1)*beautyMult(); // altın / dakika
const feederOn=()=>!!G.feederUntil&&Date.now()<G.feederUntil;
const courtT=sp=>Math.min(1800,Math.max(150,sp.grow*.6));
const breedCD=sp=>courtT(sp)*1.5;""")
R(" f.h=Math.max(0,f.h-dt/HUNGER);", " f.h=feederOn()?Math.max(f.h,.75):Math.max(0,f.h-dt/hungerT(sp));")
R(" if(f.h<=0){f.hp-=dt/90;", " if(f.h>0&&f.g>=1){const r=incomeRate(f);f.bank=Math.min((f.bank||0)+r*dt/60,r*240);}\n if(f.h<=0){f.hp-=dt/(hungerT(sp)*.5);")
s = s.replace(" for(const f of liveFish()){const fed=Math.max(0,Math.min(sec,(f.h-.12)*HUNGER));",
 " const feedS=G.feederUntil?clamp((G.feederUntil-(Date.now()-sec*1000))/1000,0,sec):0;\n"
 " for(const f of liveFish()){const HT=hungerT(f.sp),h0=feedS>0?Math.max(f.h,.75):f.h,fed=Math.max(0,Math.min(sec,feedS+Math.max(0,(h0-.12)*HT)));\n"
 "  if(f.g>=1||f.g+fed/f.sp.grow>=1){const r=incomeRate(f);f.bank=Math.min((f.bank||0)+r*Math.min(fed,8*3600)/60,r*240);}\n"
 "  if(f.mate&&(f.cd||0)<=0)f.bond=(f.bond||0)+fed;else if(f.cd>0)f.cd=Math.max(0,f.cd-sec);\n ")
R("f.h=Math.max(0,f.h-sec/HUNGER);}", "f.h=feedS>=sec?h0:Math.max(0,h0-(sec-feedS)/HT);}")
R("const HUNGER=160; // sn: tok -> aç", "")
R("let G={coins:300,xp:0,level:1,fish:[],decor:[],dirt:[]};", "let G={coins:300,pearls:5,xp:0,level:1,fish:[],decor:[],dirt:[]};")

# satış değeri ve kayıtta yeni alanlar
R("fish:liveFish().map(f=>({s:f.sid,r:f.rare?1:0,g:+f.g.toFixed(4),",
  "fish:liveFish().map(f=>({s:f.sid,r:f.rare?1:0,m:f.mate||0,bd:+(f.bond||0).toFixed(1),cd:+(f.cd||0).toFixed(1),bk:+(f.bank||0).toFixed(2),g:+f.g.toFixed(4),")
R("theme:G.theme||'ocean',themes:G.themes||['ocean'],capBonus:G.capBonus||0,quests:G.quests||null,",
  "pearls:G.pearls||0,starsGot:G.starsGot||0,feederUntil:G.feederUntil||0,theme:G.theme||'ocean',themes:G.themes||['ocean'],capBonus:G.capBonus||0,quests:G.quests||null,")
R("  theme:s.theme||'ocean',themes:s.themes||['ocean'],capBonus:s.capBonus||0,quests:s.quests||null,",
  "  pearls:s.pearls??5,starsGot:s.starsGot||0,feederUntil:s.feederUntil||0,theme:s.theme||'ocean',themes:s.themes||['ocean'],capBonus:s.capBonus||0,quests:s.quests||null,")
R("z:o.z,seed:o.seed,rare:!!o.r})", "z:o.z,seed:o.seed,rare:!!o.r,mate:o.m||0,bond:o.bd||0,cd:o.cd||0,bank:o.bk||0})")
R(" f.rare=!!o.rare;f.pts=genPts(sp,f.seed);", " f.rare=!!o.rare;f.mate=o.mate||0;f.bond=o.bond||0;f.cd=o.cd||0;f.bank=o.bank||0;f.pts=genPts(sp,f.seed);")
R("  G={coins:300,xp:0,level:1,fish:[],decor:[],dirt:[],_last:0,", "  G={coins:300,pearls:5,xp:0,level:1,fish:[],decor:[],dirt:[],_last:0,")

# seviye: inci ödülü
R(" while(G.xp>=need(G.level)){G.xp-=need(G.level);G.level++;up=true;}",
  " let pg=0;while(G.xp>=need(G.level)){G.xp-=need(G.level);G.level++;up=true;const p=G.level%5===0?3:2;G.pearls=(G.pearls||0)+p;pg+=p;}")
R("`Akvaryum kapasitesi: ${capacity()}`].filter(Boolean).join('<br>');",
  "`Akvaryum kapasitesi: ${capacity()}`,pg?`Ödül: +${pg} inci`:''].filter(Boolean).join('<br>');")
# başarım: inci
R("const c=[60,300,1200][cur-1],x=[10,40,120][cur-1];G.coins+=c;G.xp+=x;got=true;achQ.push({a,cur,c,x});",
  "const c=[60,300,1200][cur-1],x=[10,40,120][cur-1],pp=[2,5,15][cur-1];G.coins+=c;G.xp+=x;G.pearls=(G.pearls||0)+pp;got=true;achQ.push({a,cur,c,x,pp});")
R("const {a,cur,c,x}=achQ.shift(),el=$('achBan');", "const {a,cur,c,x,pp}=achQ.shift(),el=$('achBan');")
R("${a.d(a.t[cur-1])} · +${c} altın · +${x} XP</small>", "${a.d(a.t[cur-1])} · +${c} altın · +${x} XP · +${pp} inci</small>")
# günlük giriş: 3. ve 7. gün inci
R("function loginReward(){const d=((G.login.streak-1)%7)+1;return {d,c:25*d+G.level*5,x:d===7?20:0};}",
  "function loginReward(){const d=((G.login.streak-1)%7)+1;return {d,c:25*d+G.level*5,x:d===7?20:0,p:d===7?5:d===3?1:0};}")
R("G.login.cl=true;G.coins+=lr.c;G.xp+=lr.x;", "G.login.cl=true;G.coins+=lr.c;G.xp+=lr.x;G.pearls=(G.pearls||0)+lr.p;")
R("`<button class=\"btn y\" id=\"lgClaim\">Al: +${lr.c} altın${lr.x?` +${lr.x} XP`:''}</button>`",
  "`<button class=\"btn y\" id=\"lgClaim\">Al: +${lr.c} altın${lr.x?` +${lr.x} XP`:''}${lr.p?` +${lr.p} inci`:''}</button>`")
# 3. görev inci
R("q.cl=true;G.coins+=q.c;G.xp+=q.x;", "q.cl=true;G.coins+=q.c;G.xp+=q.x;if(+b.dataset.q===2)G.pearls=(G.pearls||0)+1;")
R("<div class=\"qr\">${q.p}/${q.n} · Ödül: ${q.c} altın + ${q.x} XP</div>", "<div class=\"qr\">${q.p}/${q.n} · Ödül: ${q.c} altın + ${q.x} XP${i===2?' + 1 inci':''}</div>")
# yeni görev / başarım türleri
R(" {t:'decor',txt:n=>`${n} süs yerleştir`,n:[1,2,3]},",
  " {t:'decor',txt:n=>`${n} süs yerleştir`,n:[1,2,3]},\n {t:'breed',txt:n=>`${n} yavru yap`,n:[1,1,2]},\n {t:'income',txt:n=>`Sergi gelirinden ${n} altın topla`,n:[80,250,700]},")
R(" {id:'feed',name:'Cömert Besleyici',",
  " {id:'breed',name:'Aile Kurucu',ic:'💕',d:n=>`${n} yavru yap`,t:[1,10,50],st:'bred'},\n {id:'income',name:'Sergi Ustası',ic:'🎟️',d:n=>`Sergi gelirinden ${n.toLocaleString('tr-TR')} altın topla`,t:[500,5000,50000],st:'income'},\n {id:'feed',name:'Cömert Besleyici',")

# ============================== İNCİ ALIŞVERİŞİ ==============================
R("function buy(it){\n unlockAudio();\n if(G.coins<it.cost){toast('Yeterli paran yok');snd('bad');return;}",
"""function spendPearls(n){if((G.pearls||0)<n){toast('Yeterli incin yok');snd('bad');$('pearlM').classList.remove('hidden');return false;}G.pearls-=n;return true;}
function buy(it){
 unlockAudio();
 if(it.special==='rareEgg'){
  if(liveFish().length+eggs.length>=capacity()){toast(`Akvaryum dolu (${capacity()}).`);snd('bad');return;}
  if(!spendPearls(8))return;const pool=SPECIES.filter(x=>x.lvl<=G.level),sp=pool[(Math.random()*pool.length)|0];
  const x=rnd(80,WW-80);eggs.push({sid:sp.id,x,y:topY,vy:0,ly:floorY+rnd(0,30),t:0,p:rnd(0,TAU),forceRare:1});
  snd('buy');save();$('shop').classList.add('hidden');toast('Nadir yumurta bırakıldı, içinden ne çıkacak?');updHUD();return;}
 if(it.special==='feeder'){if(!spendPearls(6))return;G.feederUntil=Math.max(Date.now(),G.feederUntil||0)+24*3600e3;for(const f of liveFish())f.h=Math.max(f.h,.75);snd('buy');save();renderShop();updHUD();toast('Otomatik yemlik açık: balıklar 24 saat aç kalmaz');return;}
 if(it.pearl){placing=it;$('shop').classList.add('hidden');setMode('place');$('placeTxt').textContent=`${it.name}: kumun üstüne dokun`;return;}
 if(G.coins<it.cost){toast('Yeterli paran yok');snd('bad');return;}""")
R(" const it=placing;if(!it)return;\n if(G.coins<it.cost){toast('Yeterli paran yok');setMode('select');return;}\n G.coins-=it.cost;G.xp+=it.xp;",
  " const it=placing;if(!it)return;\n if(it.pearl){if(!spendPearls(it.pearl)){setMode('select');return;}}\n else{if(G.coins<it.cost){toast('Yeterli paran yok');setMode('select');return;}G.coins-=it.cost;}\n G.xp+=it.xp;")
R(" floater(d.x,d.y-60,`-${it.cost}`,'#ffb3a7');spawnBubble(d.x,d.y-20,8,true);snd('buy');stat('placed');",
  " floater(d.x,d.y-60,it.pearl?`-${it.pearl} inci`:`-${it.cost}`,'#ffb3a7');floater(d.x,d.y-82,`+${decorBeauty(it)} güzellik`,'#ffe066');spawnBubble(d.x,d.y-20,8,true);snd('buy');stat('placed');")

# mağaza kartları: nadirlik, güzellik, inci fiyatı, özel kartlar
R(" const list=shopTab==='fish'?SPECIES:DECOR;\n for(const it of list){\n  const locked=G.level<it.lvl,card=document.createElement('div');card.className='card'+(locked?' locked':'');\n  const meta=shopTab==='fish'?`⏱ ${it.grow>=60?Math.round(it.grow/60)+' dk':it.grow+' sn'} · Satış ${it.sell}`:(it.desc||`+${it.xp} XP`);\n  card.innerHTML=`<canvas></canvas>${locked?`<div class=\"lock\">🔒 Seviye ${it.lvl}</div>`:''}<div class=\"cn\">${it.name}</div><div class=\"cm\">${meta}</div><button class=\"btn g\" ${locked||G.coins<it.cost?'disabled':''}><span class=\"coin\" style=\"width:18px;height:18px\"></span>${it.cost}</button>`;",
""" const list=shopTab==='fish'?[...SPECIAL,...SPECIES]:DECOR;
 for(const it of list){
  const locked=G.level<it.lvl,card=document.createElement('div');card.className='card'+(locked?' locked':'');
  const rr=it.special?{n:'İnci',c:'#B9A6F5'}:shopTab==='fish'?rarity(it.lvl):{n:`+${decorBeauty(it)} güzellik`,c:it.pearl?'#B9A6F5':'#FFC94A'};card.style.setProperty('--rc',rr.c);
  const meta=it.special?it.desc:shopTab==='fish'?`${fmtT(it.grow)} · satış ${it.sell}`:(it.desc||`+${it.xp} XP`);
  const pc_=it.pearl||it.pc,canB=pc_?(G.pearls||0)>=pc_:G.coins>=it.cost;
  const price=pc_?`<span class="pearlc" style="width:18px;height:18px"></span>${pc_}`:`<span class="coin" style="width:18px;height:18px"></span>${it.cost}`;
  card.innerHTML=`<canvas></canvas>${locked?`<div class="lock">Seviye ${it.lvl}</div>`:''}<div class="cn">${it.name}</div><div class="rar">${rr.n}</div><div class="cm">${meta}</div><button class="btn ${pc_?'p':''}" ${locked||!canB?'disabled':''}>${price}</button>`;""")
R("function drawPreview(pc,it){\n const w=pc.clientWidth||130,h=pc.clientHeight||86,dpr=Math.min(2,window.devicePixelRatio||1);\n pc.width=w*dpr;pc.height=h*dpr;const c=pc.getContext('2d');c.setTransform(dpr,0,0,dpr,0,0);",
"""const SPECIAL=[
 {id:'_rareEgg',special:'rareEgg',name:'Nadir Yumurta',lvl:1,pc:8,desc:'İçinden kesin nadir renk çıkar'},
 {id:'_feeder',special:'feeder',name:'Otomatik Yemlik',lvl:1,pc:6,desc:'24 saat balıklar aç kalmaz'}];
function drawPreview(pc,it){
 const w=pc.clientWidth||130,h=pc.clientHeight||86,dpr=Math.min(2,window.devicePixelRatio||1);
 pc.width=w*dpr;pc.height=h*dpr;const c=pc.getContext('2d');c.setTransform(dpr,0,0,dpr,0,0);
 if(it.special){const img=new Image();img.onload=()=>{const k=Math.min(w,h)*.62;c.drawImage(img,(w-k)/2,(h-k)/2,k,k);};img.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(ICON[it.special==='rareEgg'?'egg':'food']);
  if(it.special==='feeder'&&feederOn()){c.fillStyle='#46D39A';c.font='600 12px Fredoka,sans-serif';c.textAlign='center';c.fillText('Kalan '+fmtT((G.feederUntil-Date.now())/1000),w/2,h-8);}return;}""")

# ============================== GÜZELLİK ==============================
R("function stat(k,n=1){", """function decorBeauty(def){return def.beauty??Math.round((def.pearl?def.pearl*14:def.cost)/8)+2;}
function calcBeauty(){let b=THEME_BEAUTY[G.theme||'ocean']||0;for(const d of G.decor){const def=DC_[d.t];if(def)b+=decorBeauty(def);}return b;}
function updBeauty(){beautyCache=calcBeauty();const st=[50,150,400].filter(v=>beautyCache>=v).length;G.starsGot=G.starsGot||0;
 while(G.starsGot<st){G.starsGot++;const p=[3,5,10][G.starsGot-1];G.pearls=(G.pearls||0)+p;toast(`Akvaryumun ${G.starsGot}. yıldıza ulaştı! +${p} inci`);snd('lvl');save();}}
function stat(k,n=1){""")

# ============================== HUD ==============================
R(" $('lvl').textContent=G.level;const nd=need(G.level);$('xpt').textContent=`${G.xp}/${nd}`;$('xpf').style.width=Math.min(100,G.xp/nd*100)+'%';",
""" updBeauty();
 $('lvl').textContent=G.level;const nd=need(G.level);$('xpt').textContent=`${G.xp}/${nd} XP`;$('xpring').style.strokeDashoffset=157*(1-Math.min(1,G.xp/nd));
 $('pearls').textContent=(G.pearls||0).toLocaleString('tr-TR');$('beauty').textContent=beautyCache;
 $('stars').querySelectorAll('i').forEach((e,i)=>e.classList.toggle('on',i<(G.starsGot||0)));
 $('beautyChip').title=`Güzellik ${beautyCache} · sergi geliri ×${beautyMult().toFixed(2)}`;
 $('fishChip').classList.toggle('feeder',feederOn());""")
R("function setMusic(off){musicOff=off;if(MUS)MUS.gain.setTargetAtTime(off?0:.32,AC.currentTime,.4);$('mus').classList.toggle('off',off);}",
  "function setMusic(off){musicOff=off;if(MUS)MUS.gain.setTargetAtTime(off?0:.32,AC.currentTime,.4);$('mus').classList.toggle('off',off);}")
R("$('snd').textContent=m?'🔇':'🔊';$('snd').classList.toggle('off',m);}", "$('snd').classList.toggle('off',m);}")

# ============================== BİLGİ PANELİ: gelir, hızlandırma, eş ==============================
R(" <div class=\"irow\"><div class=\"val\"><span class=\"coin\"></span><span id=\"iv\"></span></div><button class=\"btn y\" id=\"ifeed\">🍤 Besle</button><button class=\"btn g\" id=\"isell\">Sat</button><button class=\"btn r\" id=\"ix\">✕</button></div>`;",
""" <div id="imate"></div>
 <div class="irow"><div class="val"><span class="coin"></span><span id="iv"></span></div><button class="btn y" id="ifeed">Besle</button><button class="btn p" id="ibolt"></button><button class="btn g" id="isell">Sat</button><button class="btn r" id="ix" aria-label="Kapat">✕</button></div>`;
 let sellArm=0;
 $('ibolt').onclick=()=>{const f=selected;if(!f||f.g>=1)return;const n=boltCost(f);if(!spendPearls(n))return;f.g=1;floater(f.x,f.y-30,'Olgunlaştı!','#ffe066');snd('lvl');for(let i=0;i<20;i++)sparks.push({x:f.x+rnd(-30,30),y:f.y+rnd(-20,20),life:rnd(.5,1)});save();updInfo();updHUD();};""")
R(" $('isell').onclick=()=>{if(selected&&!selected.dead)sellFish(selected);};",
  " $('isell').onclick=()=>{const f=selected;if(!f||f.dead)return;if(f.mate&&Date.now()-sellArm>2500){sellArm=Date.now();$('isell').textContent='Çift ayrılacak, emin misin?';setTimeout(()=>{if($('isell'))$('isell').textContent='Sat';},2500);return;}sellFish(f);};")
R(" $('iv').textContent=sellValue(f)+(f.g<1?' (yarım değer)':'');",
""" $('iv').textContent=sellValue(f)+(f.g<1?' (yarım değer)':` · +${incomeRate(f).toFixed(1)}/dk`);
 const bb=$('ibolt');if(f.g<1){bb.style.display='';bb.innerHTML=`<i data-ic="bolt"></i>Büyüt ${boltCost(f)}<span class="pearlc" style="width:16px;height:16px"></span>`;}else bb.style.display='none';
 const m=mateOf(f),im=$('imate');
 if(m){const ct=courtT(f.sp),rest=(f.cd||0)>0;im.innerHTML=`<div class="mate"><i data-ic="heart"></i><span>${rest?'Eşiyle dinleniyor · '+fmtT(f.cd):'Eşiyle flört ediyor'}</span><span class="mb"><i style="width:${rest?100:Math.min(100,(f.bond||0)/ct*100)}%"></i></span></div>`;}
 else im.innerHTML=f.g>=1?'<div class="mate" style="opacity:.75"><i data-ic="heart"></i><span>Aynı türden bir eş bekliyor</span></div>':'';""")
R("function stageName(g){", "const boltCost=f=>Math.max(1,Math.ceil((1-f.g)*f.sp.grow/600));\nfunction stageName(g){")

# ============================== SERGİ GELİRİ TOPLAMA ==============================
R("function sellFish(f){", """function collectFish(f,quiet){const c=Math.floor(f.bank||0);if(c<1)return 0;f.bank-=c;G.coins+=c;stat('income',c);quest('income',c);if(!quiet){floater(f.x,f.y-36,`+${c}`,'#ffe066');snd('coin');}return c;}
function openCollect(){
 const el=$('collectM');if(!el.classList.contains('hidden')){el.classList.add('hidden');return;}
 const inc=liveFish().reduce((a,f)=>a+Math.floor(f.bank||0),0),ready=liveFish().filter(f=>f.g>=1&&!f.mate),paired=liveFish().filter(f=>f.g>=1&&f.mate).length;
 $('colIncT').innerHTML=inc?`Sergi gelirini topla <b style="color:#ffe066">+${inc}</b>`:'Toplanacak gelir yok';$('colInc').disabled=!inc;
 $('colSellT').innerHTML=ready.length?`${ready.length} olgun balığı sat <b style="color:#ffe066">+${ready.reduce((a,f)=>a+sellValue(f),0)}</b>${paired?`<small>${paired} eşleşmiş balık satılmaz</small>`:''}`:(paired?`Satılacak balık yok<small>${paired} eşleşmiş balık korunuyor</small>`:'Satılacak olgun balık yok');$('colSell').disabled=!ready.length;
 el.classList.remove('hidden');
}
function sellFish(f){""")
R("$('sellAll').onclick=()=>{", "$('sellAll').onclick=()=>{unlockAudio();openCollect();};\nconst _oldSellAll=()=>{")
R("  const f=hitFish(p.x,p.y);if(f){selectFish(f);return;}", "  const f=hitFish(p.x,p.y);if(f){collectFish(f);selectFish(f);return;}")

# ============================== ÇİFTLEŞME ==============================
BREED = r"""
/* ================= ÇİFTLEŞME / ÜREME ================= */
let hearts=[],pairT=0;
function fishBySeed(sd){return G.fish.find(f=>f.seed===sd&&!f.dead);}
function mateOf(f){return f&&f.mate?fishBySeed(f.mate):null;}
function heartP(x,y,big){hearts.push({x,y,vx:rnd(-6,6),vy:rnd(-26,-16),s:big?rnd(6,9):rnd(3.5,5.5),life:big?1.6:1.3,max:big?1.6:1.3});}
function canPair(f){return !f.dead&&f.g>=1&&!f.mate&&f.h>.25;}
function updPairs(dt){
 for(const f of G.fish){if(f.mate){const m=mateOf(f);if(!m||m.mate!==f.seed){f.mate=0;f.bond=0;}}if(f.cd>0)f.cd=Math.max(0,f.cd-dt);}
 pairT-=dt;
 if(pairT<=0){pairT=3;const gr={};for(const f of G.fish)if(canPair(f))(gr[f.sid]=gr[f.sid]||[]).push(f);
  for(const k in gr){const a=gr[k];while(a.length>=2){const x=a.shift(),y=a.shift();x.mate=y.seed;y.mate=x.seed;x.bond=y.bond=0;x.cd=y.cd=0;
   const mx=(x.x+y.x)/2,my=(x.y+y.y)/2;floater(mx,my-34,'Eşleştiler!','#ff9ec0');for(let i=0;i<8;i++)heartP(mx+rnd(-20,20),my+rnd(-10,10),true);
   toast(`İki ${x.sp.name} eşleşti! Bir süre flört edip yumurta bırakacaklar.`);snd('blip');}}}
 for(const f of G.fish){const m=mateOf(f);if(!m||f.seed>m.seed||f.dead)continue;
  if((f.cd||0)>0){m.cd=f.cd;continue;}
  const ok=f.h>.2&&m.h>.2&&clean>=.3;if(ok){f.bond=(f.bond||0)+dt;m.bond=f.bond;}
  if(Math.random()<dt*.8)heartP((f.x+m.x)/2+rnd(-12,12),(f.y+m.y)/2-8);
  const ct=courtT(f.sp);
  if(f.bond>=ct){
   if(liveFish().length+eggs.length<capacity()){layEgg(f,m);f.bond=m.bond=0;f.cd=m.cd=breedCD(f.sp);f.fullW=0;}
   else{f.bond=m.bond=ct;if(!f.fullW){f.fullW=1;toast('Akvaryum dolu: yeni yumurta için yer aç');}}}
 }
}
function courtSteer(f){const m=mateOf(f);if(!m||(f.cd||0)>0)return false;const lead=f.seed<m.seed,ct=courtT(f.sp);
 if((f.bond||0)>ct-10){const mx=(f.x+m.x)/2,my=(f.y+m.y)/2,a=T*2.4+(lead?0:Math.PI),r=f.sp.len*.5;f.tx=mx+Math.cos(a)*r;f.ty=my+Math.sin(a)*r*.45;f.idle=0;return true;}
 if(!lead){f.tx=m.x-(m.face>=0?1:-1)*m.sp.len*.9;f.ty=m.y+10;f.idle=0;return true;}return false;}
function layEgg(f,m){const x=(f.x+m.x)/2,y=(f.y+m.y)/2;
 eggs.push({sid:f.sid,x,y,vy:0,ly:floorY+rnd(0,30),t:0,p:rnd(0,TAU),rp:(f.rare?.25:0)+(m.rare?.25:0)});
 for(let i=0;i<16;i++)heartP(x+rnd(-26,26),y+rnd(-16,16),true);floater(x,y-36,'Yeni yumurta!','#ff9ec0');snd('hatch');stat('bred');quest('breed',1);
 toast(`${f.sp.name} çifti yumurta bıraktı!`);}
"""
R("function hatch(e){", BREED + "function hatch(e){")
R(" const sp=SP[e.sid],rare=!!sp.sprR&&Math.random()<RARE_P;", " const sp=SP[e.sid],rare=!!sp.sprR&&(e.forceRare||Math.random()<RARE_P+(e.rp||0));")
R(" const sz=fs(f);\n if(sp.move){updSpecial(f,dt,sz);fishExtras(f,dt,sz);return;}",
  " const sz=fs(f);\n courtSteer(f);\n if(sp.move){updSpecial(f,dt,sz);fishExtras(f,dt,sz);return;}")
R(" G.fish=G.fish.filter(f=>!(f.dead&&f.dt>6));", " G.fish=G.fish.filter(f=>!(f.dead&&f.dt>6));\n updPairs(dt);\n for(const h of hearts){h.life-=dt;h.x+=h.vx*dt;h.y+=h.vy*dt;h.vx*=.98;}hearts=hearts.filter(h=>h.life>0);\n for(const b of bokeh){b.y-=b.v*dt;b.x+=Math.sin(T*.2+b.p)*dt*6;if(b.y<-40){b.y=WH+40;b.x=rnd(0,WW);}}")

# ============================== ÇİZİM: ikonlar, kalpler, eş bağı, bokeh ==============================
R("function drawIcon(x,y,em,bgc){", r"""function heartPath(c,x,y,s){c.beginPath();c.moveTo(x,y+s*.9);c.bezierCurveTo(x-s*1.6,y-s*.1,x-s*.9,y-s*1.3,x,y-s*.45);c.bezierCurveTo(x+s*.9,y-s*1.3,x+s*1.6,y-s*.1,x,y+s*.9);c.closePath();}
function drawBadge(x,y,kind,prog){
 const col={food:['#ff9f1a','#c96a00'],hungry:['#ff5a5a','#b81f2e'],heart:['#ff6f91','#c2416b'],coin:['#ffc94a','#b57a06'],star:['#46D39A','#1f8a55']}[kind];
 ctx.save();ctx.translate(x,y);
 ctx.fillStyle='rgba(0,20,40,.25)';ctx.beginPath();ctx.ellipse(0,15,8,2.5,0,0,TAU);ctx.fill();
 const g=ctx.createRadialGradient(-4,-5,1,0,0,13);g.addColorStop(0,'#fff');g.addColorStop(.25,col[0]);g.addColorStop(1,col[1]);
 ctx.fillStyle=g;ctx.beginPath();ctx.arc(0,0,12,0,TAU);ctx.fill();
 ctx.beginPath();ctx.moveTo(-4,10);ctx.lineTo(0,16);ctx.lineTo(4,10);ctx.fill();
 ctx.lineWidth=2;ctx.strokeStyle='rgba(255,255,255,.9)';ctx.beginPath();ctx.arc(0,0,12,0,TAU);ctx.stroke();
 if(prog!==undefined){ctx.strokeStyle='#fff';ctx.lineWidth=3;ctx.lineCap='round';ctx.beginPath();ctx.arc(0,0,15.5,-Math.PI/2,-Math.PI/2+TAU*Math.min(1,prog));ctx.stroke();}
 ctx.fillStyle='#fff';
 if(kind==='heart'){heartPath(ctx,0,0,6.2);ctx.fill();}
 else if(kind==='coin'){ctx.beginPath();ctx.arc(0,0,6,0,TAU);ctx.fill();ctx.fillStyle=col[1];ctx.beginPath();ctx.moveTo(-3.4,0);ctx.quadraticCurveTo(0,-3.4,3,-.6);ctx.lineTo(4.4,-2);ctx.lineTo(4.4,2);ctx.lineTo(3,.6);ctx.quadraticCurveTo(0,3.4,-3.4,0);ctx.fill();}
 else if(kind==='star'){ctx.beginPath();for(let i=0;i<10;i++){const a=-Math.PI/2+i*Math.PI/5,r=i%2?3:7;ctx.lineTo(Math.cos(a)*r,Math.sin(a)*r);}ctx.closePath();ctx.fill();}
 else{for(const [a,b,r] of [[-3,-2,2],[2.5,-3,1.7],[0,2.5,2.2],[3.5,2,1.4],[-3.5,3,1.3]]){ctx.beginPath();ctx.arc(a,b,r,0,TAU);ctx.fill();}}
 ctx.restore();
}
function drawIcon(x,y,em,bgc){""")
R("  if(f.h<.3)drawIcon(f.x,y+Math.sin(T*4)*2,'🍤',f.h<=0?'#e53935':'#ff9f1a');else if(f.g>=1)drawIcon(f.x,y+Math.sin(T*3)*2,'⭐','#2fa84f');}",
"""  const m=mateOf(f),bob=Math.sin(T*3+f.seed)*2;
  if(f.h<.3)drawBadge(f.x,y+bob,f.h<=0?'hungry':'food');
  else if(m)drawBadge(f.x,y+bob,'heart',(f.cd||0)>0?undefined:Math.min(1,(f.bond||0)/courtT(f.sp)));
  else if((f.bank||0)>=Math.max(3,incomeRate(f)*1.5))drawBadge(f.x,y+bob,'coin');
  else if(f.g>=1)drawBadge(f.x,y+bob,'star');}
 for(const h of hearts){const a=Math.min(1,h.life/h.max*1.6);ctx.save();ctx.globalAlpha=a;ctx.fillStyle='#ff6f91';heartPath(ctx,h.x,h.y,h.s);ctx.fill();ctx.fillStyle='rgba(255,255,255,.55)';ctx.beginPath();ctx.arc(h.x-h.s*.45,h.y-h.s*.4,h.s*.22,0,TAU);ctx.fill();ctx.restore();}""")
R(" const sorted=[...lf].sort((a,b)=>a.z-b.z);",
""" for(const f of lf){const m=mateOf(f);if(!m||f.seed>m.seed||f.dead)continue;const court=(f.cd||0)<=0;
  ctx.save();ctx.strokeStyle=court?'rgba(255,140,175,.55)':'rgba(255,140,175,.25)';ctx.lineWidth=2;ctx.setLineDash([2,7]);ctx.lineCap='round';ctx.lineDashOffset=-T*14;
  const mx=(f.x+m.x)/2,my=Math.min(f.y,m.y)-28;ctx.beginPath();ctx.moveTo(f.x,f.y-6);ctx.quadraticCurveTo(mx,my,m.x,m.y-6);ctx.stroke();ctx.restore();}
 const sorted=[...lf].sort((a,b)=>a.z-b.z);""")
R("ctx.font='bold 17px \"Trebuchet MS\",sans-serif';", "ctx.font='600 17px Fredoka,\"Trebuchet MS\",sans-serif';")
R(" ctx.setTransform(1,0,0,1,0,0);ctx.drawImage(fg,0,0);ctx.setTransform(DPR*S,0,0,DPR*S,0,0);\n // ikonlar",
""" ctx.save();ctx.globalCompositeOperation='lighter';
 for(const b of bokeh){const g=ctx.createRadialGradient(b.x,b.y,0,b.x,b.y,b.r);g.addColorStop(0,`rgba(${TH.mote},${b.a})`);g.addColorStop(.7,`rgba(${TH.mote},${b.a*.4})`);g.addColorStop(1,`rgba(${TH.mote},0)`);ctx.fillStyle=g;ctx.fillRect(b.x-b.r,b.y-b.r,b.r*2,b.r*2);}
 ctx.restore();
 ctx.setTransform(1,0,0,1,0,0);ctx.drawImage(fg,0,0);ctx.setTransform(DPR*S,0,0,DPR*S,0,0);
 // ikonlar""")
R("let eggs=[],foods=[],bubbles=[],floaters=[],motes=[],sparks=[];", "let eggs=[],foods=[],bubbles=[],floaters=[],motes=[],sparks=[],bokeh=[];")
R(" motes=[];for(let i=0;i<Math.round(WW*WH/9000);i++)",
  " bokeh=[];for(let i=0;i<9;i++)bokeh.push({x:rnd(0,WW),y:rnd(0,WH),r:rnd(14,34),v:rnd(3,9),p:rnd(0,TAU),a:rnd(.04,.09)});\n motes=[];for(let i=0;i<Math.round(WW*WH/9000);i++)")

# ============================== GRAFİK: caustics + bulanık uzak katman ==============================
R(" // kum üstünde ışık desenleri\n ctx.beginPath();ctx.rect(0,floorY-25,WW,WH-floorY+25);ctx.clip();",
""" // kum üstünde hareketli ışık ağı (caustics)
 ctx.beginPath();ctx.rect(0,floorY-25,WW,WH-floorY+25);ctx.clip();
 if(!causticPat)causticPat=ctx.createPattern(CAUSTIC,'repeat');
 if(causticPat.setTransform){ctx.fillStyle=causticPat;
  causticPat.setTransform(new DOMMatrix().translateSelf(t*9,floorY+t*2).scaleSelf(1.5,.55));ctx.globalAlpha=.42;ctx.fillRect(0,floorY-25,WW,WH-floorY+25);
  causticPat.setTransform(new DOMMatrix().translateSelf(-t*6,floorY-t*3).scaleSelf(1.15,.45));ctx.globalAlpha=.3;ctx.fillRect(0,floorY-25,WW,WH-floorY+25);ctx.globalAlpha=1;}""")
R("function drawRays(t){", r"""const CAUSTIC=(()=>{const N=192,c=document.createElement('canvas');c.width=c.height=N;const x=c.getContext('2d'),im=x.createImageData(N,N);
 for(let j=0;j<N;j++)for(let i=0;i<N;i++){const u=i/N*TAU,v=j/N*TAU;const s=Math.sin(u*2+Math.sin(v*3)*1.2)+Math.sin(v*2+Math.sin(u*3+1)*1.3)+Math.sin((u+v)*3+Math.sin(u-v)*1.1)*.7;
  const val=Math.pow(1-Math.min(1,Math.abs(s)*.65),7),k=(j*N+i)*4;im.data[k]=255;im.data[k+1]=250;im.data[k+2]=225;im.data[k+3]=val*200;}
 x.putImageData(im,0,0);return c;})();
let causticPat=null;
function drawRays(t){""")
R(" ridge(floorY-40,60,TH.r1,40);", " c.filter='blur(2.2px)';\n ridge(floorY-40,60,TH.r1,40);")
R(" ridge(floorY-10,30,TH.r2,30);", " ridge(floorY-10,30,TH.r2,30);\n c.filter='none';")
R(" initDirt();buildBG();buildFG();scalePat=null;", " initDirt();buildBG();buildFG();scalePat=null;causticPat=null;")

# ============================== İNCİ SÜSLERİ ==============================
R("const DECOR=[", r"""function dCrystal(c,t,d){
 contactShadow(c,40);const p=.6+.4*Math.sin(t*1.6+(d.ph||0));
 let g=c.createRadialGradient(0,-45,4,0,-45,70);g.addColorStop(0,`rgba(180,230,255,${.35*p})`);g.addColorStop(1,'rgba(180,230,255,0)');c.save();c.globalCompositeOperation='lighter';c.fillStyle=g;c.fillRect(-70,-115,140,120);c.restore();
 const cols=[['#d6f8ff','#5bc8f5','#2b8fc4'],['#efe0ff','#a77bff','#6a43c9'],['#d9fff3','#43d8b4','#1f9a7c']];
 for(const [x,w,h,a,ci] of [[-24,15,60,-.28,1],[24,13,64,.24,2],[0,19,92,0,0],[-11,10,40,-.55,2],[13,9,38,.55,1]]){
  const [c0,c1,c2]=cols[ci];c.save();c.translate(x,0);c.rotate(a);
  g=c.createLinearGradient(-w/2,0,w/2,0);g.addColorStop(0,c2);g.addColorStop(.45,c1);g.addColorStop(.55,c0);g.addColorStop(1,c1);
  c.fillStyle=g;c.beginPath();c.moveTo(-w/2,2);c.lineTo(-w/2,-h*.74);c.lineTo(0,-h);c.lineTo(w/2,-h*.74);c.lineTo(w/2,2);c.closePath();c.fill();
  c.strokeStyle='rgba(255,255,255,.55)';c.lineWidth=1.2;c.beginPath();c.moveTo(0,-h);c.lineTo(0,0);c.moveTo(-w/2,-h*.74);c.lineTo(0,-h*.6);c.lineTo(w/2,-h*.74);c.stroke();
  c.fillStyle=`rgba(255,255,255,${.5*p})`;c.beginPath();c.arc(-w*.18,-h*.8,1.8,0,TAU);c.fill();c.restore();}
 sandMound(c,40);
}
function dArch(c,t,d){
 contactShadow(c,74);
 const g=c.createLinearGradient(0,-100,0,0);g.addColorStop(0,'#ff9cbc');g.addColorStop(.5,'#ff6f91');g.addColorStop(1,'#b8355c');
 c.fillStyle=g;c.beginPath();c.ellipse(0,2,72,98,0,Math.PI,TAU);c.ellipse(0,2,44,68,0,TAU,Math.PI,true);c.closePath();c.fill();
 c.save();c.clip();c.fillStyle='rgba(255,230,240,.55)';for(let i=0;i<90;i++){const a=Math.PI+(i*2.399)%Math.PI,r=46+((i*37)%25);c.beginPath();c.arc(Math.cos(a)*r*1.05,2+Math.sin(a)*r*1.42,1.6,0,TAU);c.fill();}
 c.fillStyle='rgba(90,0,30,.25)';c.beginPath();c.ellipse(0,2,72,98,0,Math.PI,TAU);c.ellipse(0,6,60,86,0,TAU,Math.PI,true);c.fill();c.restore();
 c.strokeStyle='#ff8fb0';c.lineCap='round';
 for(const [x,y,a,l] of [[-50,-70,-1.1,22],[-20,-95,-1.4,18],[22,-94,-1.7,20],[52,-68,-2,24]]){c.lineWidth=5;c.beginPath();c.moveTo(x,y);c.lineTo(x+Math.cos(a)*l,y+Math.sin(a)*l);c.stroke();c.lineWidth=3;c.beginPath();c.moveTo(x+Math.cos(a)*l*.6,y+Math.sin(a)*l*.6);c.lineTo(x+Math.cos(a+.6)*l*.9,y+Math.sin(a+.6)*l*.9);c.stroke();}
 c.fillStyle='#4a7330';for(const [x,w] of [[-58,12],[58,12]]){c.beginPath();c.ellipse(x,0,w,4,0,0,TAU);c.fill();}
 sandMound(c,74);
}
const DECOR=[""")
R(" {id:'castle',name:'Batık Kale',lvl:7,cost:450,xp:10,w:145,h:180,draw:dCastle},",
  " {id:'castle',name:'Batık Kale',lvl:7,cost:450,xp:10,w:145,h:180,draw:dCastle},\n"
  " {id:'crystal',name:'Kristal Kümesi',lvl:3,cost:0,pearl:20,xp:8,w:90,h:100,draw:dCrystal,desc:'Işıldar, inci süsü'},\n"
  " {id:'arch',name:'Mercan Kemeri',lvl:5,cost:0,pearl:15,xp:8,w:150,h:105,draw:dArch,desc:'Balıklar altından geçer'},")

# ============================== AYARLAR / İNCİ / AÇILIŞ ==============================
R("$('bookB').onclick=()=>{unlockAudio();openBook();};",
"""$('bookB').onclick=()=>{unlockAudio();openBook();};
$('setB').onclick=()=>{unlockAudio();$('setM').classList.remove('hidden');};
$('setX').onclick=()=>$('setM').classList.add('hidden');
$('setM').addEventListener('pointerdown',e=>{if(e.target.id==='setM')$('setM').classList.add('hidden');});
$('pearlChip').onclick=()=>$('pearlM').classList.remove('hidden');
$('coinChip').onclick=()=>{shopTab='fish';openShop();};
$('pearlX').onclick=()=>$('pearlM').classList.add('hidden');
$('pearlM').addEventListener('pointerdown',e=>{if(e.target.id==='pearlM')$('pearlM').classList.add('hidden');});
$('colInc').onclick=()=>{let t=0;for(const f of liveFish())t+=collectFish(f,true);if(t){snd('coin');toast(`Sergi geliri toplandı: +${t} altın`);for(const f of liveFish())if(f.g>=1)sparks.push({x:f.x,y:f.y,life:.8});}$('collectM').classList.add('hidden');save();updHUD();};
$('colSell').onclick=()=>{const r=liveFish().filter(f=>f.g>=1&&!f.mate);let tot=0;r.forEach(f=>{tot+=sellValue(f);sellFish(f);});if(r.length)toast(`${r.length} balık satıldı: +${tot} altın`);$('collectM').classList.add('hidden');};
const hideSplash=()=>{const sp=$('splash');if(sp.classList.contains('hide'))return;sp.classList.add('hide');unlockAudio();setTimeout(()=>{sp.style.display='none';if(!seenHelp)$('help').classList.remove('hidden');},500);};
$('splash').addEventListener('click',hideSplash);""")
R(" if(!seenHelp)$('help').classList.remove('hidden');\n}", "}")
R("$('saveB').onclick=()=>{", "$('saveB').onclick=()=>{$('setM').classList.add('hidden');")
R("$('hlp').onclick=()=>$('help').classList.remove('hidden');", "$('hlp').onclick=()=>{$('setM').classList.add('hidden');$('help').classList.remove('hidden');};")
R("cv.addEventListener('pointerdown',e=>{", "cv.addEventListener('pointerdown',e=>{$('collectM').classList.add('hidden');")

for _k in ('id="shopX"','id="helpX"','id="bookX"','id="saveX"'):
    s = s.replace(_k+'>✕</button>', _k+' aria-label="Kapat"><i data-ic="close"></i></button>')
open(P, 'w', encoding='utf-8').write(s)
print('v5 yaması tamam', len(s))
