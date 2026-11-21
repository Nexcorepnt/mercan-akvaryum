"""Oyun v3: yeni türler, nadir varyantlar, koleksiyon, görevler, başarımlar, temalar, 3D süs sprite desteği."""
import os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'index.template.html')
s = open(P, encoding='utf-8').read()

def R(a, b, cnt=1):
    global s
    n = s.count(a)
    assert n == cnt, (n, a[:90])
    s = s.replace(a, b)

# ======================= CSS =======================
R("@keyframes pop{from{transform:scale(.3);opacity:0}}",
"""@keyframes pop{from{transform:scale(.3);opacity:0}}
.rbtn{position:relative}
.badge{position:absolute;top:-3px;right:-3px;min-width:16px;height:16px;border-radius:9px;background:#ff3b30;border:2px solid #fff;font-size:10px;line-height:12px;color:#fff;font-weight:800;padding:0 3px}
.btabs{display:flex;gap:6px}
.btabs button{border:2px solid #fff;border-radius:12px;padding:6px 12px;font:700 14px inherit;font-family:inherit;background:#ffffff40;color:#fff;cursor:pointer}
.btabs button.on{background:#fff;color:#1667a8}
#bookBody{overflow:auto;padding:12px;-webkit-overflow-scrolling:touch;touch-action:auto}
.login{background:linear-gradient(#fff6d6,#ffe39a);border:3px solid #fff;border-radius:16px;padding:10px 12px;box-shadow:0 3px 0 #e0b84a;margin-bottom:12px}
.login .lt{font-weight:800;display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap}
.days{display:flex;gap:6px;margin-top:8px}
.days div{flex:1;background:#fff;border-radius:10px;text-align:center;font-size:11px;font-weight:800;padding:5px 2px;color:#8a6a10;border:2px solid #f2d27a}
.days div.got{background:#8ee66a;color:#fff;border-color:#5fbf3f}
.days div.now{border-color:#ff8a00;box-shadow:0 0 0 2px #ff8a0055}
.q{background:#fff;border-radius:14px;padding:10px 12px;margin-bottom:8px;box-shadow:0 3px 0 #9cc3dd;display:flex;align-items:center;gap:10px}
.q .qm{flex:1}
.q .qt{font-weight:800;font-size:14px}
.q .qb{height:10px;background:#cfe2ef;border-radius:8px;overflow:hidden;margin:5px 0 3px}
.q .qb i{display:block;height:100%;background:linear-gradient(90deg,#7fd3ff,#3fb52a);border-radius:8px}
.q .qr{font-size:12px;color:#4a7a9c;font-weight:700}
.q.done{opacity:.6}
.qnote{text-align:center;font-size:12px;color:#4a7a9c;margin-top:6px}
.achs{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px}
.ach{background:#fff;border-radius:14px;padding:10px;box-shadow:0 3px 0 #9cc3dd;display:flex;gap:10px;align-items:center}
.ach .ai{font-size:30px;width:42px;text-align:center}
.ach .an{font-weight:800}
.ach .ad{font-size:12px;color:#4a7a9c}
.ach .am{font-size:16px;letter-spacing:2px;margin-top:2px}
.ach .am span{opacity:.22;filter:grayscale(1)}
.ach .am span.on{opacity:1;filter:none}
.alb{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:8px}
.alb .card canvas{height:70px}
.alb .card.unk canvas{background:radial-gradient(ellipse at 50% 20%,#2b5a78,#0d2c44 70%)}
.rtag{display:inline-block;background:linear-gradient(#ffb3ff,#d45fd4);color:#fff;border-radius:7px;font-size:10px;padding:1px 6px;margin-left:4px;vertical-align:middle}
.albh{font-weight:800;margin-bottom:8px;display:flex;justify-content:space-between}
#achBan{position:absolute;left:50%;top:64px;transform:translate(-50%,-140%);z-index:16;background:linear-gradient(#fff3b0,#ffc933);color:#5a3300;border:3px solid #fff;border-radius:16px;padding:8px 16px;font-weight:800;box-shadow:0 8px 24px #0007;transition:transform .45s cubic-bezier(.2,1.4,.4,1);text-align:center;pointer-events:none;max-width:90%}
#achBan.show{transform:translate(-50%,0)}
#achBan small{display:block;font-weight:700;font-size:12px;color:#7a5200}
.tcard canvas{background:none!important}
.card .btn.sel{background:linear-gradient(#cfe2ef,#a9c9df);color:#2a5f86;box-shadow:0 3px 0 #7fa6c2}""")

# ======================= HTML =======================
R('<button class="rbtn" id="saveB" title="Kayıt">💾</button>',
  '<button class="rbtn" id="bookB" title="Görevler">📋<span class="badge hidden" id="bookBadge">!</span></button>\n  <button class="rbtn" id="saveB" title="Kayıt">💾</button>')
R('<div class="tabs"><button data-t="fish" class="on">🐠 Balıklar</button><button data-t="decor">🪸 Süsler</button></div>',
  '<div class="tabs"><button data-t="fish" class="on">🐠 Balıklar</button><button data-t="decor">🪸 Süsler</button><button data-t="theme">🎨 Temalar</button></div>')
R('<div id="saveM" class="modal hidden">',
  '''<div id="book" class="modal hidden">
  <div class="mbox">
    <div class="mhead"><div class="ttl">📋 Defter</div>
      <div class="btabs"><button data-b="quest" class="on">Görevler</button><button data-b="ach">Başarımlar</button><button data-b="album">Koleksiyon</button></div>
      <button class="x" id="bookX">✕</button></div>
    <div id="bookBody"></div>
  </div>
</div>
<div id="achBan"></div>

<div id="saveM" class="modal hidden">''')
R("<p>Satış ve alışverişten XP kazanırsın. Seviye atladıkça yeni balıklar, yeni süsler açılır ve akvaryumun büyür. Oyun otomatik kaydedilir.</p>",
  "<p><b>✨ Nadir balıklar:</b> Her yumurtadan küçük bir ihtimalle farklı renkte nadir balık çıkar, 3 kat değerlidir. Hepsini <b>📋 Defter → Koleksiyon</b>'da topla.</p>\n"
  "      <p><b>📋 Görevler:</b> Her gün 3 yeni görev ve günlük giriş ödülü var. Başarımlar rozet ve altın kazandırır.</p>\n"
  "      <p><b>🎨 Temalar:</b> Mağazadan Tatlı Su, Mercan Resifi ve Gece temalarını alabilir, akvaryumu büyütebilirsin.</p>\n"
  "      <p>Satış ve alışverişten XP kazanırsın. Seviye atladıkça yeni balıklar, yeni süsler açılır ve akvaryumun büyür. Oyun otomatik kaydedilir.</p>")

# ======================= TÜRLER + SPRITE =======================
R("const SP={};SPECIES.forEach(s=>SP[s.id]=s);",
"""SPECIES.push(
 {id:'seahorse',name:'Deniz Atı',lvl:4,cost:150,sell:340,bxp:5,sxp:22,grow:270,len:70,hb:.45,ped:.2,tail:'round',dors:0,anal:0,c1:'#f2b134',c2:'#b4650f',c3:'#ffe39a',fin:'rgba(255,220,120,.55)',pat:'gold',speed:14,move:'seahorse'},
 {id:'jelly',name:'Denizanası',lvl:7,cost:340,sell:780,bxp:9,sxp:44,grow:450,len:60,hb:.45,ped:.2,tail:'round',dors:0,anal:0,c1:'#ffb3d9',c2:'#ff5fa2',c3:'#fff0f7',fin:'rgba(255,180,220,.5)',pat:'gold',speed:10,move:'jelly'},
 {id:'shark',name:'Köpekbalığı Yavrusu',lvl:10,cost:650,sell:1500,bxp:15,sxp:90,grow:600,len:100,hb:.2,ped:.09,tail:'fork',dors:14,anal:4,c1:'#8796a5',c2:'#55636f',c3:'#f2f5f7',fin:'rgba(115,130,145,.95)',pat:null,speed:66,eyeK:.035,eye:'#1e2328'});
SPECIES.sort((a,b)=>a.lvl-b.lvl||a.cost-b.cost);
const SP={};SPECIES.forEach(s=>SP[s.id]=s);
const RARE={neon:'Altın Neon',gold:'İnci Japon',clown:'Gece Palyaçosu',angel:'Kara Melek',tang:'Sarı Cerrah',betta:'Kraliyet Beta',discus:'Mavi Diskus',koi:'Altın Koi',lion:'Kara Aslan',puffer:'Yeşil Balon',shark:'Albino Köpekbalığı',seahorse:'Pembe Deniz Atı',jelly:'Mavi Işıltı'};
const RARE_P=.07;
const fname=f=>f.rare?(RARE[f.sid]||f.sp.name):f.sp.name;""")
start = s.index("for(const id in SPRITE_DATA){const m=SPRITE_DATA[id],sp=SP[id];")
end = s.index("\n", start)
s = s[:start]+("const DSPR={};\n"
 "function mkSpr(m){const img=new Image(),o={fw:m.fw,fh:m.fh,n:m.n,ppu:m.ppu,ox:m.ox,oy:m.oy,img,ok:false};"
 "img.onload=()=>{o.ok=true;sprRefresh();};img.src=m.src;return o;}\n"
 "let sprRT=0;function sprRefresh(){clearTimeout(sprRT);sprRT=setTimeout(()=>{const sh=document.getElementById('shop');if(sh&&!sh.classList.contains('hidden'))renderShop();const bk=document.getElementById('book');if(bk&&!bk.classList.contains('hidden'))renderBook();},120);}\n"
 "for(const id in SPRITE_DATA){const m=SPRITE_DATA[id];\n"
 " if(id.startsWith('d_'))DSPR[id.slice(2)]=mkSpr(m);\n"
 " else if(id.endsWith('_r')){const sp=SP[id.slice(0,-2)];if(sp)sp.sprR=mkSpr(m);}\n"
 " else if(SP[id])SP[id].spr=mkSpr(m);}")+s[end:]
R("function drawFishAny(c,sp,ph,f){const s=sp.spr;if(s&&s.ok)",
  "function drawFishAny(c,sp,ph,f){const s=(f&&f.rare&&sp.sprR&&sp.sprR.ok)?sp.sprR:sp.spr;if(s&&s.ok)")

# ======================= SÜS SPRITE =======================
R(" if(selDecor===d){c.shadowColor='#fff8a0';c.shadowBlur=14;}\n DC_[d.t].draw(c,t,d);c.restore();",
""" if(selDecor===d){c.shadowColor='#fff8a0';c.shadowBlur=14;}
 const ds_=DSPR[d.t];
 if(ds_&&ds_.ok){
  const k=100/ds_.ppu;let fr=0;
  if(d.t==='shell'){const op=Math.pow(Math.max(0,Math.sin(t*.35+(d.ph||0))),.6);fr=Math.min(ds_.n-1,Math.round(op*(ds_.n-1)));}
  c.drawImage(ds_.img,fr*ds_.fw,0,ds_.fw,ds_.fh,-ds_.ox*k,-ds_.oy*k,ds_.fw*k,ds_.fh*k);
  if(d.t==='volcano'||d.t==='chest'){c.shadowBlur=0;const p=.6+.4*Math.sin(t*2+(d.ph||0)),yy=d.t==='volcano'?-97:-44,rr_=d.t==='volcano'?42:36;
   const g=c.createRadialGradient(0,yy,2,0,yy,rr_);g.addColorStop(0,d.t==='volcano'?`rgba(255,150,50,${.55*p})`:`rgba(255,225,120,${.45*p})`);g.addColorStop(1,'rgba(255,150,50,0)');
   c.globalCompositeOperation='lighter';c.fillStyle=g;c.fillRect(-rr_,yy-rr_,rr_*2,rr_*2);}
 } else DC_[d.t].draw(c,t,d);
 c.restore();""")
R("  const d=prepDecor({t:it.id,seed:7}),k=Math.min((w-14)/it.w,(h-14)/it.h,1.3);",
  "  const ds_=DSPR[it.id];if(ds_&&ds_.ok){const k=Math.min((w-10)/ds_.fw,(h-8)/ds_.fh,1.4);c.imageSmoothingQuality='high';c.drawImage(ds_.img,0,0,ds_.fw,ds_.fh,(w-ds_.fw*k)/2,(h-ds_.fh*k)/2,ds_.fw*k,ds_.fh*k);return;}\n"
  "  const d=prepDecor({t:it.id,seed:7}),k=Math.min((w-14)/it.w,(h-14)/it.h,1.3);")

# ======================= BALIK DAVRANIŞI =======================
R(" f.pts=genPts(sp,f.seed);newTarget(f);return f;", " f.rare=!!o.rare;f.pts=genPts(sp,f.seed);newTarget(f);return f;")
R(" const sz=fs(f);\n let tx=f.tx,ty=f.ty,maxs=sp.speed*(.6+.5*sz),food=null;",
  " const sz=fs(f);\n if(sp.move){updSpecial(f,dt,sz);fishExtras(f,dt,sz);return;}\n let tx=f.tx,ty=f.ty,maxs=sp.speed*(.6+.5*sz),food=null;")
R(" if(food&&Math.hypot(food.x-mx,food.y-f.y)<7+9*sz){food.eaten=true;f.h=Math.min(1,f.h+.24);spawnBubble(mx,f.y,2);}",
  " if(food&&Math.hypot(food.x-mx,food.y-f.y)<7+9*sz){food.eaten=true;feedFish(f,mx);}")
R(" if(Math.random()<dt*.08)spawnBubble(mx,f.y-2,1);\n if(f.g>=1&&Math.random()<dt*1.2)sparks.push({x:f.x+rnd(-20,20)*sz,y:f.y+rnd(-14,14)*sz,life:.8});\n}",
""" if(Math.random()<dt*.08)spawnBubble(mx,f.y-2,1);
 fishExtras(f,dt,sz,true);
}
function fishExtras(f,dt,sz,noz){
 if(!noz){f.z+=(f.tz-f.z)*dt*.1;if(Math.random()<dt*.05)f.tz=Math.random();}
 if(f.g>=1&&Math.random()<dt*1.2)sparks.push({x:f.x+rnd(-20,20)*sz,y:f.y+rnd(-14,14)*sz,life:.8});
 if(f.rare&&Math.random()<dt*2.2)sparks.push({x:f.x+rnd(-26,26)*sz,y:f.y+rnd(-18,18)*sz,life:.9,pink:1});
}
function feedFish(f,x){f.h=Math.min(1,f.h+.24);spawnBubble(x??f.x,f.y,2);stat('fed');quest('feed',1);}
function updSpecial(f,dt,sz){
 const sp=f.sp;let food=null,tx=f.tx,ty=f.ty;
 if(f.h<.92&&foods.length){let bd=1e12;for(const fd of foods){if(fd.eaten)continue;const d=(fd.x-f.x)**2+(fd.y-f.y)**2;if(d<bd){bd=d;food=fd;}}if(food&&bd<420*420){tx=food.x;ty=food.y;}else food=null;}
 const dx=tx-f.x,dy=ty-f.y,d=Math.hypot(dx,dy)||1;
 if(sp.move==='jelly'){
  f.ph+=dt*(food?3.2:2.2);const pulse=Math.max(0,Math.sin(f.ph)),v=(food?30:14)*(.6+.5*sz);
  f.vx+=(dx/d*v*.6-f.vx)*dt*.8;
  f.vy+=((dy/d)*v*.5-pulse*16*(dy<0?1.5:.5)+6-f.vy)*dt*1.2;f.face=1;
 } else {
  f.ph+=dt*(food?7:4.5);let want=(food?32:sp.speed)*(.6+.5*sz);
  if(!food&&f.idle>0){f.idle-=dt;want*=.1;}if(!food&&d<50)want*=d/50;
  f.vx+=(dx/d*want-f.vx)*dt*1.2;f.vy+=(dy/d*want*.8+Math.sin(T*1.5+f.seed)*4-f.vy)*dt*1.2;
  if(Math.abs(f.vx)>2){const tf=f.vx>0?1:-1;f.face+=(tf-f.face)*Math.min(1,dt*3);}
 }
 f.x+=f.vx*dt;f.y+=f.vy*dt;
 const m=sp.len*sz*.4,hh=sp.hb*sp.len*sz;f.x=clamp(f.x,m,WW-m);f.y=clamp(f.y,topY+hh,floorY-10-hh*(sp.move==='jelly'?1.7:1));
 if(!food&&d<30){if(f.idle<=0&&Math.random()<.5)f.idle=rnd(1,3);newTarget(f);}
 if(food&&d<10+12*sz){food.eaten=true;feedFish(f);}
}""")
R(" ctx.rotate(clamp(Math.atan2(f.vy,Math.abs(f.vx)+10),-.45,.45)*(f.face>=0?1:-1));",
  " if(!sp.move)ctx.rotate(clamp(Math.atan2(f.vy,Math.abs(f.vx)+10),-.45,.45)*(f.face>=0?1:-1));")
R("ctx.fillStyle=`rgba(255,240,150,${a})`;ctx.beginPath();for(let i=0;i<4;i++)",
  "ctx.fillStyle=s.pink?`rgba(255,190,255,${Math.min(1,a)})`:`rgba(255,240,150,${Math.min(1,a)})`;ctx.beginPath();for(let i=0;i<4;i++)")

# yumurtadan çıkış
R("else{e.t+=dt;if(e.t>4.5){e.done=true;const f=makeFish(e.sid,0,{x:e.x,y:e.y-25,h:.7});G.fish.push(f);spawnBubble(e.x,e.y-8,10,true);floater(e.x,e.y-30,'Yumurtadan çıktı!','#bff');snd('hatch');}}",
  "else{e.t+=dt;if(e.t>4.5){e.done=true;hatch(e);}}")
R("function update(dt){",
"""function hatch(e){
 const sp=SP[e.sid],rare=!!sp.sprR&&Math.random()<RARE_P;
 const f=makeFish(e.sid,0,{x:e.x,y:e.y-25,h:.7,rare});G.fish.push(f);spawnBubble(e.x,e.y-8,10,true);
 if(rare){floater(e.x,e.y-40,'✨ NADİR! '+RARE[e.sid],'#ffb3ff');toast(`✨ Nadir balık çıktı: ${RARE[e.sid]}! Değeri 3 kat.`);snd('lvl');for(let i=0;i<30;i++)sparks.push({x:e.x+rnd(-50,50),y:e.y-25+rnd(-40,30),life:rnd(.6,1.3),pink:1});}
 else{floater(e.x,e.y-30,'Yumurtadan çıktı!','#bff');snd('hatch');}
 albumAdd(e.sid+(rare?'_r':''));stat('hatch');if(rare)stat('rare');quest('hatch',1);
}
function update(dt){""")

# satış / satın alma / süs / temizlik hook'ları
R("function sellValue(f){return f.g>=1?f.sp.sell:Math.floor(f.sp.sell*f.g*.5);}",
  "function sellValue(f){return (f.g>=1?f.sp.sell:Math.floor(f.sp.sell*f.g*.5))*(f.rare?3:1);}")
R(" const v=sellValue(f),xp=f.g>=1?f.sp.sxp:Math.round(f.sp.sxp*f.g*.4);\n G.coins+=v;G.xp+=xp;G.fish=G.fish.filter(x=>x!==f);",
  " const v=sellValue(f),xp=(f.g>=1?f.sp.sxp:Math.round(f.sp.sxp*f.g*.4))*(f.rare?2:1);\n G.coins+=v;G.xp+=xp;G.fish=G.fish.filter(x=>x!==f);stat('earned',v);stat('sold');quest('sell',1);quest('earn',v);")
R(" e.innerHTML=`<h3>${f.sp.name} <small id=\"istg\"></small></h3>",
  " e.innerHTML=`<h3>${fname(f)}${f.rare?'<span class=\"rtag\">✨ Nadir</span>':''} <small id=\"istg\"></small></h3>")
R("  G.coins-=it.cost;G.xp+=it.bxp;\n", "  G.coins-=it.cost;G.xp+=it.bxp;stat('bought');quest('buy',1);\n")
R(" floater(d.x,d.y-60,`-${it.cost}`,'#ffb3a7');spawnBubble(d.x,d.y-20,8,true);snd('buy');checkLevel();save();setMode('select');",
  " floater(d.x,d.y-60,`-${it.cost}`,'#ffb3a7');spawnBubble(d.x,d.y-20,8,true);snd('buy');stat('placed');quest('decor',1);checkLevel();save();setMode('select');")
R(" const c=5+G.level*3,x=3+G.level;G.coins+=c;G.xp+=x;\n", " const c=5+G.level*3,x=3+G.level;G.coins+=c;G.xp+=x;stat('cleans');quest('clean',1);\n")
R("  for(let i=0;i<40;i++)spawnBubble(rnd(0,WW),floorY,1,true);\n }\n}",
  "  for(let i=0;i<40;i++)spawnBubble(rnd(0,WW),floorY,1,true);\n  checkAch();\n }\n}")
R("const capacity=()=>Math.min(30,8+G.level*2);", "const capacity=()=>Math.min(30,8+G.level*2)+(G.capBonus||0);")

# ======================= TEMALAR =======================
R("function buildBG(){",
"""const THEMES=[
 {id:'ocean',name:'Okyanus',cost:0,lvl:1,water:['#35b4e0','#1a86ba','#0c5d8a','#073b5c'],haze:'170,235,255',r1:'rgba(14,78,115,.55)',r2:'rgba(10,58,88,.6)',plant:[25,95,100],sand:['#bfa673','#d9c38f','#8c7046'],peb:['#efe0b8','#c2a46e','#9c8152','#dccca3','#7d6a4a','#f6ead0','#a9967a','#cbb9a2','#8a9aa0','#c9a07a'],ray:'200,240,255',mote:'230,250,255',vig:'0,18,35',far:'plants'},
 {id:'fresh',name:'Tatlı Su',cost:400,lvl:3,water:['#7cc9a6','#3f9a78','#22684c','#123d2c'],haze:'210,255,215',r1:'rgba(28,85,52,.55)',r2:'rgba(18,58,36,.62)',plant:[40,125,48],sand:['#7d6a4a','#9a8458','#4f3f28'],peb:['#6b5a3e','#8a7552','#4e4030','#a08a62','#3e3426','#b8a27a','#5e5444','#7a6a50'],ray:'235,255,205',mote:'230,255,220',vig:'5,25,15',far:'grass'},
 {id:'reef',name:'Mercan Resifi',cost:900,lvl:5,water:['#66e3f2','#22b6d6','#1189b2','#0a5b82'],haze:'210,255,255',r1:'rgba(30,125,155,.42)',r2:'rgba(20,95,125,.5)',plant:[60,150,160],sand:['#efe6cf','#fbf4e2','#c9b88f'],peb:['#ffffff','#f4ead2','#e8d9b5','#fff7e6','#d9c7a0','#ffd9d0','#f0e0ff'],ray:'225,255,255',mote:'255,255,255',vig:'0,30,50',far:'reef'},
 {id:'night',name:'Gece',cost:1500,lvl:7,water:['#1d3f78','#122a62','#0a1a44','#050c24'],haze:'120,160,255',r1:'rgba(10,25,62,.6)',r2:'rgba(6,16,42,.7)',plant:[20,60,95],sand:['#5d6478','#757d94','#3a3f50'],peb:['#8a90a8','#6a7088','#a8b0c8','#50566c','#c0c8e0'],ray:'150,185,255',mote:'140,255,230',vig:'0,0,15',over:'rgba(5,12,45,.30)',far:'plants',glow:true},
];
const THM=()=>THEMES.find(x=>x.id===(G.theme||'ocean'))||THEMES[0];
function buildBG(){""")
R(" let g=c.createLinearGradient(0,0,0,WH);g.addColorStop(0,'#35b4e0');g.addColorStop(.3,'#1a86ba');g.addColorStop(.7,'#0c5d8a');g.addColorStop(1,'#073b5c');",
  " const TH=THM();let g=c.createLinearGradient(0,0,0,WH);g.addColorStop(0,TH.water[0]);g.addColorStop(.3,TH.water[1]);g.addColorStop(.7,TH.water[2]);g.addColorStop(1,TH.water[3]);")
R("g.addColorStop(0,'rgba(170,235,255,.4)');g.addColorStop(1,'rgba(170,235,255,0)');c.fillStyle=g;c.fillRect(0,0,WW,WH);\n const r=mulberry(77);",
  "g.addColorStop(0,`rgba(${TH.haze},.4)`);g.addColorStop(1,`rgba(${TH.haze},0)`);c.fillStyle=g;c.fillRect(0,0,WW,WH);\n const r=mulberry(77);")
R(" ridge(floorY-40,60,'rgba(14,78,115,.55)',40);\n for(let i=0;i<WW/22;i++){const x=r()*WW,h=40+r()*110;c.strokeStyle=`rgba(25,${95+r()*30|0},100,${.25+r()*.2})`;c.lineWidth=2+r()*3;c.lineCap='round';c.beginPath();c.moveTo(x,floorY-20);c.quadraticCurveTo(x+(r()-.5)*30,floorY-20-h*.5,x+(r()-.5)*20,floorY-20-h);c.stroke();}\n ridge(floorY-10,30,'rgba(10,58,88,.6)',30);",
""" ridge(floorY-40,60,TH.r1,40);
 const [pr,pg,pb]=TH.plant;
 if(TH.far==='reef'){
  const cc=['255,120,150','255,175,90','175,125,255','90,205,185','255,225,120'];
  for(let i=0;i<WW/45;i++){const x=r()*WW,y=floorY-22-r()*25,col=cc[(r()*cc.length)|0],a=.22+r()*.18,sc=.6+r()*.9;
   c.fillStyle=`rgba(${col},${a})`;c.strokeStyle=`rgba(${col},${a})`;c.lineCap='round';
   if(r()<.5){for(let k=0;k<7;k++){c.beginPath();c.arc(x+(r()-.5)*40*sc,y-r()*40*sc,(8+r()*14)*sc,0,TAU);c.fill();}}
   else{c.lineWidth=5*sc;for(let k=0;k<6;k++){const a2=-Math.PI/2+(r()-.5)*1.6,L=(30+r()*50)*sc;c.beginPath();c.moveTo(x,y);c.quadraticCurveTo(x+Math.cos(a2)*L*.5,y+Math.sin(a2)*L*.6,x+Math.cos(a2)*L,y+Math.sin(a2)*L);c.stroke();}}}
 } else {
  const n=TH.far==='grass'?WW/9:WW/22;
  for(let i=0;i<n;i++){const x=r()*WW,h=(TH.far==='grass'?60:40)+r()*(TH.far==='grass'?150:110);c.strokeStyle=`rgba(${pr},${pg+r()*30|0},${pb},${.25+r()*.2})`;c.lineWidth=2+r()*3;c.lineCap='round';c.beginPath();c.moveTo(x,floorY-20);c.quadraticCurveTo(x+(r()-.5)*30,floorY-20-h*.5,x+(r()-.5)*20,floorY-20-h);c.stroke();}
  if(TH.far==='grass')for(let i=0;i<4;i++){const x=r()*WW;c.strokeStyle='rgba(40,28,15,.45)';c.lineWidth=7+r()*5;c.beginPath();c.moveTo(x,floorY-15);c.quadraticCurveTo(x+30,floorY-70-r()*40,x+60+r()*40,floorY-120-r()*60);c.stroke();}
 }
 ridge(floorY-10,30,TH.r2,30);""")
R(" g=c.createLinearGradient(0,floorY-30,0,WH);g.addColorStop(0,'#bfa673');g.addColorStop(.18,'#d9c38f');g.addColorStop(1,'#8c7046');c.fillStyle=g;c.fill();",
  " g=c.createLinearGradient(0,floorY-30,0,WH);g.addColorStop(0,TH.sand[0]);g.addColorStop(.18,TH.sand[1]);g.addColorStop(1,TH.sand[2]);c.fillStyle=g;c.fill();")
R(" const cols=['#efe0b8','#c2a46e','#9c8152','#dccca3','#7d6a4a','#f6ead0','#a9967a','#cbb9a2','#8a9aa0','#c9a07a'];", " const cols=TH.peb;")
R("g.addColorStop(1,'rgba(0,18,35,.6)');", "g.addColorStop(1,`rgba(${THM().vig},.6)`);")
R("g.addColorStop(0,`rgba(200,240,255,${a})`);g.addColorStop(1,'rgba(200,240,255,0)');",
  "g.addColorStop(0,`rgba(${THM().ray},${a})`);g.addColorStop(1,`rgba(${THM().ray},0)`);")
R(" for(const m of motes){ctx.fillStyle=`rgba(230,250,255,${.25+.2*Math.sin(T+m.p)})`;ctx.beginPath();ctx.arc(m.x,m.y,m.r,0,TAU);ctx.fill();}",
  " const TH=THM();\n for(const m of motes){ctx.fillStyle=`rgba(${TH.mote},${.25+.2*Math.sin(T+m.p)})`;ctx.beginPath();ctx.arc(m.x,m.y,m.r,0,TAU);ctx.fill();}")
R(" ctx.filter='none';ctx.globalAlpha=1;\n // kabarcıklar",
""" ctx.filter='none';ctx.globalAlpha=1;
 if(TH.over){ctx.fillStyle=TH.over;ctx.fillRect(0,0,WW,WH);}
 if(TH.glow){ctx.save();ctx.globalCompositeOperation='lighter';
  for(const m of motes){const a=.25+.25*Math.sin(T*1.3+m.p*3);const g=ctx.createRadialGradient(m.x,m.y,0,m.x,m.y,m.r*5);g.addColorStop(0,`rgba(${TH.mote},${a})`);g.addColorStop(1,`rgba(${TH.mote},0)`);ctx.fillStyle=g;ctx.fillRect(m.x-m.r*5,m.y-m.r*5,m.r*10,m.r*10);}
  for(const f of G.fish){if(f.dead||f.sp.move!=='jelly')continue;const sz=fs(f),R_=50*sz;const g=ctx.createRadialGradient(f.x,f.y,0,f.x,f.y,R_);g.addColorStop(0,f.rare?'rgba(120,210,255,.35)':'rgba(255,150,210,.35)');g.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=g;ctx.fillRect(f.x-R_,f.y-R_,R_*2,R_*2);}
  ctx.restore();}
 // kabarcıklar""")

# ======================= MAĞAZA: TEMALAR =======================
R(" const grid=$('grid');grid.innerHTML='';\n const list=shopTab==='fish'?SPECIES:DECOR;",
  " const grid=$('grid');grid.innerHTML='';\n if(shopTab==='theme'){renderThemes(grid);return;}\n const list=shopTab==='fish'?SPECIES:DECOR;")
R("function drawPreview(pc,it){",
"""function renderThemes(grid){
 G.themes=G.themes||['ocean'];
 for(const th of THEMES){
  const own=G.themes.includes(th.id),cur=(G.theme||'ocean')===th.id,locked=!own&&G.level<th.lvl;
  const card=document.createElement('div');card.className='card tcard'+(locked?' locked':'');
  card.innerHTML=`<canvas></canvas>${locked?`<div class="lock">🔒 Seviye ${th.lvl}</div>`:''}<div class="cn">${th.name}</div><div class="cm">${own?(cur?'Kullanılıyor':'Sahipsin'):'Akvaryum teması'}</div>`+
   (own?`<button class="btn ${cur?'sel':'g'}" ${cur?'disabled':''}>${cur?'✓ Seçili':'Kullan'}</button>`:`<button class="btn g" ${locked||G.coins<th.cost?'disabled':''}><span class="coin" style="width:18px;height:18px"></span>${th.cost}</button>`);
  grid.appendChild(card);
  const pc=card.querySelector('canvas');requestAnimationFrame(()=>{const w=pc.clientWidth||130,h=pc.clientHeight||86,dpr=Math.min(2,devicePixelRatio||1);pc.width=w*dpr;pc.height=h*dpr;const c=pc.getContext('2d');c.setTransform(dpr,0,0,dpr,0,0);
   let g=c.createLinearGradient(0,0,0,h);th.water.forEach((cl,i)=>g.addColorStop(i/3,cl));c.fillStyle=g;rr(c,0,0,w,h,11);c.fill();
   c.fillStyle=th.sand[1];c.beginPath();c.moveTo(0,h*.78);for(let x=0;x<=w;x+=8)c.lineTo(x,h*.76+Math.sin(x*.08)*3);c.lineTo(w,h);c.lineTo(0,h);c.fill();
   c.fillStyle=`rgba(${th.ray},.25)`;for(let i=0;i<3;i++){c.beginPath();c.moveTo(w*(.2+i*.3),0);c.lineTo(w*(.28+i*.3),0);c.lineTo(w*(.36+i*.3),h*.75);c.lineTo(w*(.18+i*.3),h*.75);c.fill();}
   if(th.far==='reef'){['255,120,150','255,175,90','175,125,255'].forEach((cl,i)=>{c.fillStyle=`rgba(${cl},.7)`;c.beginPath();c.arc(w*(.2+i*.3),h*.72,9,0,TAU);c.arc(w*(.25+i*.3),h*.66,7,0,TAU);c.fill();});}
   if(th.glow){for(let i=0;i<14;i++){c.fillStyle=`rgba(${th.mote},.8)`;c.beginPath();c.arc((i*37)%w,(i*23)%(h*.7),1.6,0,TAU);c.fill();}}});
  card.querySelector('button').onclick=()=>{
   if(own){G.theme=th.id;buildBG();buildFG();save();renderShop();toast(`🎨 ${th.name} teması`);return;}
   if(G.coins<th.cost){toast('Yeterli paran yok');return;}
   G.coins-=th.cost;G.themes.push(th.id);G.theme=th.id;buildBG();buildFG();snd('buy');save();renderShop();toast(`🎨 ${th.name} teması açıldı!`);updHUD();};
 }
 const nb=(G.capBonus||0)/2,cost=300*(nb+1),max=nb>=5;
 const card=document.createElement('div');card.className='card';
 card.innerHTML=`<canvas></canvas><div class="cn">Akvaryumu Büyüt</div><div class="cm">${max?'En büyük boyut':`+2 balık yeri (${capacity()} → ${capacity()+2})`}</div><button class="btn g" ${max||G.coins<cost?'disabled':''}>${max?'Tamam':`<span class="coin" style="width:18px;height:18px"></span>${cost}`}</button>`;
 grid.appendChild(card);
 const pc=card.querySelector('canvas');requestAnimationFrame(()=>{const w=pc.clientWidth||130,h=pc.clientHeight||86,dpr=Math.min(2,devicePixelRatio||1);pc.width=w*dpr;pc.height=h*dpr;const c=pc.getContext('2d');c.setTransform(dpr,0,0,dpr,0,0);
  c.font='34px "Segoe UI Emoji","Apple Color Emoji",sans-serif';c.textAlign='center';c.textBaseline='middle';c.fillText('🐟↔️',w/2,h/2);});
 card.querySelector('button').onclick=()=>{if(max)return;if(G.coins<cost){toast('Yeterli paran yok');return;}G.coins-=cost;G.capBonus=(G.capBonus||0)+2;snd('buy');save();renderShop();updHUD();toast(`Akvaryum büyüdü! Kapasite: ${capacity()}`);};
}
function drawPreview(pc,it){""")

# ======================= DEFTER: GÖREV / BAŞARIM / KOLEKSİYON =======================
R("function setMode(m){",
r"""/* ---- istatistik, görev, başarım, koleksiyon ---- */
function stat(k,n=1){G.stats=G.stats||{};G.stats[k]=(G.stats[k]||0)+n;checkAch();}
const QUEST_T=[
 {t:'feed',txt:n=>`Balıklarına ${n} kez yem yedir`,n:[15,25,40]},
 {t:'sell',txt:n=>`${n} balık sat`,n:[3,5,8]},
 {t:'earn',txt:n=>`Satışlardan ${n} altın kazan`,n:[300,900,2500]},
 {t:'buy',txt:n=>`${n} yumurta al`,n:[3,5,8]},
 {t:'hatch',txt:n=>`${n} yumurta çatlat`,n:[3,5,8]},
 {t:'clean',txt:n=>`Akvaryumu ${n} kez tamamen temizle`,n:[1,1,2]},
 {t:'decor',txt:n=>`${n} süs yerleştir`,n:[1,2,3]},
];
function dayStr(ms){const d=new Date(ms??Date.now());return d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate();}
function hashStr(s){let h=2166136261;for(const ch of s){h^=ch.charCodeAt(0);h=Math.imul(h,16777619);}return h>>>0;}
function ensureDaily(){
 const td=dayStr();
 if(!G.quests||G.quests.date!==td){
  const r=mulberry(hashStr(td)),pool=[...QUEST_T],picks=[];
  while(picks.length<3){picks.push(pool.splice((r()*pool.length)|0,1)[0]);}
  const ti=G.level<4?0:G.level<8?1:2;
  G.quests={date:td,list:picks.map((q,i)=>({t:q.t,n:q.n[ti],p:0,cl:false,c:Math.round((40+G.level*15)*(1+i*.5)),x:5+G.level*2+i*4}))};
 }
 if(!G.login||G.login.last!==td){
  const ys=dayStr(Date.now()-864e5),st=(G.login&&G.login.last===ys)?G.login.streak+1:1;
  G.login={last:td,streak:st,cl:false,best:Math.max(st,(G.login&&G.login.best)||0)};
 }
 updBadge();
}
function qText(q){return QUEST_T.find(x=>x.t===q.t).txt(q.n);}
function quest(t,n){
 if(!G.quests)return;
 for(const q of G.quests.list){if(q.t!==t||q.p>=q.n)continue;q.p=Math.min(q.n,q.p+n);if(q.p>=q.n){toast(`📋 Görev tamamlandı: ${qText(q)}`);snd('blip');}}
 updBadge();if(!$('book').classList.contains('hidden')&&bookTab==='quest')renderBook();
}
function claimable(){let n=0;if(G.login&&!G.login.cl)n++;if(G.quests)for(const q of G.quests.list)if(q.p>=q.n&&!q.cl)n++;return n;}
function updBadge(){const n=claimable(),b=$('bookBadge');b.textContent=n;b.classList.toggle('hidden',!n);}
function loginReward(){const d=((G.login.streak-1)%7)+1;return {d,c:25*d+G.level*5,x:d===7?20:0};}
const ACH=[
 {id:'hatch',name:'Balık Sever',ic:'🐣',d:n=>`${n} balık yumurtadan çıkar`,t:[10,50,200],st:'hatch'},
 {id:'earn',name:'Tüccar',ic:'💰',d:n=>`Satışlardan toplam ${n.toLocaleString('tr-TR')} altın kazan`,t:[1000,10000,100000],st:'earned'},
 {id:'clean',name:'Temizlik Uzmanı',ic:'🧽',d:n=>`Akvaryumu ${n} kez tamamen temizle`,t:[1,10,50],st:'cleans'},
 {id:'decor',name:'Dekoratör',ic:'🪸',d:n=>`${n} süs yerleştir`,t:[5,20,50],st:'placed'},
 {id:'album',name:'Koleksiyoncu',ic:'📖',d:n=>`Koleksiyonda ${n} tür keşfet`,t:[5,13,26],st:'album'},
 {id:'rare',name:'Nadir Avcısı',ic:'✨',d:n=>`${n} nadir balık çıkar`,t:[1,5,15],st:'rare'},
 {id:'streak',name:'Sadık Bakıcı',ic:'📅',d:n=>`${n} gün üst üste oyuna gir`,t:[3,7,30],st:'streak'},
 {id:'level',name:'Usta Akvaryumcu',ic:'⭐',d:n=>`Seviye ${n}'e ulaş`,t:[5,10,15],st:'level'},
 {id:'feed',name:'Cömert Besleyici',ic:'🍤',d:n=>`Balıklarına ${n} kez yem yedir`,t:[50,500,3000],st:'fed'},
];
const MED=['🥉','🥈','🥇'],TIERN=['Bronz','Gümüş','Altın'];
function statVal(st){if(st==='album')return Object.keys(G.album||{}).length;if(st==='streak')return G.login?(G.login.best||G.login.streak):0;if(st==='level')return G.level;return (G.stats||{})[st]||0;}
let achQ=[],achShowing=false;
function checkAch(){
 G.ach=G.ach||{};let got=false;
 for(const a of ACH){let cur=G.ach[a.id]||0;
  while(cur<3&&statVal(a.st)>=a.t[cur]){cur++;G.ach[a.id]=cur;const c=[60,300,1200][cur-1],x=[10,40,120][cur-1];G.coins+=c;G.xp+=x;got=true;achQ.push({a,cur,c,x});}}
 if(got){showAchQ();checkLevel();}
}
function showAchQ(){
 if(achShowing||!achQ.length)return;achShowing=true;const {a,cur,c,x}=achQ.shift(),el=$('achBan');
 el.innerHTML=`🏆 ${a.ic} ${a.name} ${MED[cur-1]} ${TIERN[cur-1]}<small>${a.d(a.t[cur-1])} · +${c} altın · +${x} XP</small>`;
 el.classList.add('show');snd('lvl');setTimeout(()=>{el.classList.remove('show');setTimeout(()=>{achShowing=false;showAchQ();},500);},3200);
}
function albumAdd(key){G.album=G.album||{};if(G.album[key])return;G.album[key]=1;
 const id=key.replace(/_r$/,''),nm=key.endsWith('_r')?RARE[id]:SP[id].name;setTimeout(()=>toast(`📖 Koleksiyona eklendi: ${nm}`),key.endsWith('_r')?2500:300);checkAch();}
let bookTab='quest';
function openBook(){ensureDaily();$('book').classList.remove('hidden');renderBook();snd('blip');}
function renderBook(){
 document.querySelectorAll('.btabs button').forEach(b=>b.classList.toggle('on',b.dataset.b===bookTab));
 const B=$('bookBody');B.innerHTML='';
 if(bookTab==='quest'){
  const lr=loginReward();let days='';for(let i=1;i<=7;i++)days+=`<div class="${i<lr.d||(i===lr.d&&G.login.cl)?'got':''} ${i===lr.d?'now':''}">Gün ${i}<br>${i===7?'🎁':'🪙'}</div>`;
  B.insertAdjacentHTML('beforeend',`<div class="login"><div class="lt"><span>🎁 Günlük giriş · ${G.login.streak} gün seri</span>${G.login.cl?'<span>✓ Bugün alındı</span>':`<button class="btn y" id="lgClaim">Al: +${lr.c} altın${lr.x?` +${lr.x} XP`:''}</button>`}</div><div class="days">${days}</div></div>`);
  if(!G.login.cl)$('lgClaim').onclick=()=>{G.login.cl=true;G.coins+=lr.c;G.xp+=lr.x;snd('coin');checkLevel();checkAch();save();updBadge();renderBook();updHUD();toast(`🎁 +${lr.c} altın`);};
  G.quests.list.forEach((q,i)=>{const done=q.p>=q.n;
   B.insertAdjacentHTML('beforeend',`<div class="q ${q.cl?'done':''}"><div class="qm"><div class="qt">${qText(q)}</div><div class="qb"><i style="width:${q.p/q.n*100}%"></i></div><div class="qr">${q.p}/${q.n} · Ödül: ${q.c} altın + ${q.x} XP</div></div>${q.cl?'<b>✓</b>':`<button class="btn ${done?'g':''}" data-q="${i}" ${done?'':'disabled'}>Al</button>`}</div>`);});
  B.querySelectorAll('[data-q]').forEach(b=>b.onclick=()=>{const q=G.quests.list[+b.dataset.q];if(q.cl||q.p<q.n)return;q.cl=true;G.coins+=q.c;G.xp+=q.x;snd('coin');checkLevel();save();updBadge();renderBook();updHUD();toast(`📋 +${q.c} altın +${q.x} XP`);});
  B.insertAdjacentHTML('beforeend','<div class="qnote">Görevler her gün yenilenir.</div>');
 } else if(bookTab==='ach'){
  let h='<div class="achs">';
  for(const a of ACH){const cur=(G.ach||{})[a.id]||0,nx=Math.min(2,cur),v=statVal(a.st);
   h+=`<div class="ach"><div class="ai">${a.ic}</div><div style="flex:1"><div class="an">${a.name}</div><div class="ad">${cur>=3?'Tamamlandı!':a.d(a.t[nx])+` (${Math.min(v,a.t[nx]).toLocaleString('tr-TR')}/${a.t[nx].toLocaleString('tr-TR')})`}</div><div class="am">${MED.map((m,i)=>`<span class="${i<cur?'on':''}">${m}</span>`).join('')}</div></div></div>`;}
  B.innerHTML=h+'</div>';
 } else {
  const keys=[];for(const sp of SPECIES){keys.push(sp.id);keys.push(sp.id+'_r');}
  const n=keys.filter(k=>(G.album||{})[k]).length;
  B.insertAdjacentHTML('beforeend',`<div class="albh"><span>📖 Koleksiyon</span><span>${n}/${keys.length}</span></div>`);
  const g=document.createElement('div');g.className='alb';B.appendChild(g);
  for(const k of keys){const id=k.replace(/_r$/,''),rare=k.endsWith('_r'),sp=SP[id],has=(G.album||{})[k];
   const card=document.createElement('div');card.className='card'+(has?'':' unk');
   card.innerHTML=`<canvas></canvas><div class="cn" style="font-size:12px">${has?(rare?RARE[id]:sp.name):'???'}${rare?'<span class="rtag">✨</span>':''}</div>`;g.appendChild(card);
   const pc=card.querySelector('canvas');requestAnimationFrame(()=>{const w=pc.clientWidth||100,h=pc.clientHeight||70,dpr=Math.min(2,devicePixelRatio||1);pc.width=w*dpr;pc.height=h*dpr;const c=pc.getContext('2d');c.setTransform(dpr,0,0,dpr,0,0);
    const s=rare?sp.sprR:sp.spr;if(!s||!s.ok)return;const kk=Math.min((w-8)/s.fw,(h-6)/s.fh);
    if(!has){c.filter='brightness(0)';c.globalAlpha=.45;}
    c.drawImage(s.img,0,0,s.fw,s.fh,(w-s.fw*kk)/2,(h-s.fh*kk)/2,s.fw*kk,s.fh*kk);});}
 }
}
$('bookB').onclick=()=>{unlockAudio();openBook();};
$('bookX').onclick=()=>$('book').classList.add('hidden');
$('book').addEventListener('pointerdown',e=>{if(e.target.id==='book')$('book').classList.add('hidden');});
document.querySelectorAll('.btabs button').forEach(b=>b.onclick=()=>{bookTab=b.dataset.b;renderBook();});
function setMode(m){""")

# ======================= KAYIT =======================
R("  dirt:+(1-clean).toFixed(3),last:Date.now(),muted,seenHelp};",
  "  dirt:+(1-clean).toFixed(3),last:Date.now(),muted,seenHelp,\n  theme:G.theme||'ocean',themes:G.themes||['ocean'],capBonus:G.capBonus||0,quests:G.quests||null,login:G.login||null,stats:G.stats||{},ach:G.ach||{},album:G.album||{}};")
R("fish:liveFish().map(f=>({s:f.sid,g:+f.g.toFixed(4),", "fish:liveFish().map(f=>({s:f.sid,r:f.rare?1:0,g:+f.g.toFixed(4),")
R(" G={coins:s.coins|0,xp:s.xp|0,level:Math.max(1,s.level|0),fish:[],decor:[],dirt:[],_dirtAvg:s.dirt||0,_last:s.last||0};",
  " G={coins:s.coins|0,xp:s.xp|0,level:Math.max(1,s.level|0),fish:[],decor:[],dirt:[],_dirtAvg:s.dirt||0,_last:s.last||0,\n  theme:s.theme||'ocean',themes:s.themes||['ocean'],capBonus:s.capBonus||0,quests:s.quests||null,login:s.login||null,stats:s.stats||{},ach:s.ach||{},album:s.album||{}};")
R("makeFish(o.s,o.g,{h:o.h,hp:o.hp,x:clamp(o.xf*WW,40,WW-40),y:clamp(o.yf*WH,topY+20,floorY-20),z:o.z,seed:o.seed})",
  "makeFish(o.s,o.g,{h:o.h,hp:o.hp,x:clamp(o.xf*WW,40,WW-40),y:clamp(o.yf*WH,topY+20,floorY-20),z:o.z,seed:o.seed,rare:!!o.r})")
R(" initDirt();renderDirt();\n const el=(Date.now()-(s.last||Date.now()))/1000;applyElapsed(el);",
  " for(const f of G.fish)G.album[f.sid+(f.rare?'_r':'')]=1;\n buildBG();buildFG();initDirt();renderDirt();ensureDaily();\n const el=(Date.now()-(s.last||Date.now()))/1000;applyElapsed(el);")
R("  G={coins:300,xp:0,level:1,fish:[],decor:[],dirt:[],_last:0};",
  "  G={coins:300,xp:0,level:1,fish:[],decor:[],dirt:[],_last:0,theme:'ocean',themes:['ocean'],capBonus:0,quests:null,login:null,stats:{},ach:{},album:{gold:1,neon:1}};")
R("  initDirt();\n }\n $('snd').textContent=muted?'🔇':'🔊';",
  "  buildBG();buildFG();initDirt();ensureDaily();\n }\n $('snd').textContent=muted?'🔇':'🔊';")
R("resize();load();resize();renderDirt();updHUD();save();initCloud();",
  "resize();load();resize();renderDirt();updHUD();save();initCloud();\n"
  "setTimeout(()=>{if(G.login&&!G.login.cl)toast('🎁 Günlük ödülün hazır! 📋 Defter\\'e bak');},1500);\n"
  "setInterval(()=>{if(G.quests&&G.quests.date!==dayStr()){ensureDaily();toast('📋 Yeni günlük görevler geldi!');}},60000);")

open(P, 'w', encoding='utf-8').write(s)
print('oyun v3 yaması tamam', len(s))
