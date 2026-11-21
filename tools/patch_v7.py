"""v7: çöpçü balığı + vatoz (dip balıkları), mizaç sistemi, avcılık (köpekbalığı, aslan balığı)."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'src', 'index.template.html')
s = open(P, encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    assert s.count(a) >= 1, 'bulunamadı: ' + a[:80]
    s = s.replace(a, b, n)

# ---------- türler ----------
rep("SPECIES.sort((a,b)=>a.lvl-b.lvl||a.cost-b.cost);",
"""SPECIES.push(
 {id:'pleco',name:'Çöpçü Balığı',lvl:2,cost:70,sell:150,bxp:3,sxp:12,grow:720,len:58,hb:.22,ped:.15,tail:'lunate',dors:15,anal:0,c1:'#5b4b33',c2:'#2c2318',c3:'#9a8a68',fin:'rgba(88,72,50,.9)',pat:null,speed:22,move:'bottom',role:'clean',eyeK:.034},
 {id:'ray',name:'Mavi Benekli Vatoz',lvl:9,cost:600,sell:1300,bxp:14,sxp:80,grow:9000,len:145,hb:.2,ped:.1,tail:'round',dors:0,anal:0,c1:'#c9a35c',c2:'#8a6a32',c3:'#f2e6cc',fin:'rgba(200,160,90,.6)',pat:null,speed:30,move:'bottom'});
SPECIES.sort((a,b)=>a.lvl-b.lvl||a.cost-b.cost);""")
rep("seahorse:'Pembe Deniz Atı',jelly:'Mavi Işıltı'};", "seahorse:'Pembe Deniz Atı',jelly:'Mavi Işıltı',pleco:'Albino Çöpçü',ray:'Motoro Vatoz'};")
rep("lion:90,puffer:120,shark:180};", "lion:90,puffer:120,shark:180,pleco:12,ray:150};")
rep("const hungerT=sp=>",
"""const TEMPER={neon:'calm',gold:'calm',clown:'semi',angel:'semi',tang:'semi',betta:'semi',discus:'calm',koi:'calm',lion:'pred',puffer:'semi',seahorse:'calm',jelly:'calm',shark:'pred',pleco:'clean',ray:'calm'};
const TEMPER_TXT={calm:['Barışçıl','#46D39A'],semi:['Yarı saldırgan','#FFB23F'],pred:['Avcı','#FF6B6B'],clean:['Temizlikçi','#4DA3FF']};
const TEMPER_INFO={pred:'Acıkınca kendinden küçük balıkları avlar. Tokluğunu %35 üstünde tut.',clean:'Dipte gezip kiri ve yere düşen yemi temizler. Zırhlıdır, yenmez.',semi:'Bölgesine yaklaşanı kovalar ama zarar vermez.'};
const temperOf=sp=>TEMPER[sp.id]||'calm';
const hungerT=sp=>""")

# ---------- dip balığı hareketi ----------
rep(" if(sp.move){updSpecial(f,dt,sz);fishExtras(f,dt,sz);return;}",
    " if(sp.move==='bottom'){updBottom(f,dt,sz);fishExtras(f,dt,sz);return;}\n if(sp.move){updSpecial(f,dt,sz);fishExtras(f,dt,sz);return;}")
rep("function updSpecial(f,dt,sz){",
"""function botY(f,sz){return floorY+(f.sp.id==='ray'?2:12)-f.sp.hb*f.sp.len*sz*.5;}
const cleanerK=()=>1-.2*Math.min(3,G.fish.filter(f=>!f.dead&&f.sp.role==='clean').length);
function cleanAround(f,amt){
 const R=95,x=f.x,y=f.y;let rem=0;
 const q0=Math.max(0,Math.floor((x-R)/CELL)),q1=Math.min(DCOL-1,Math.ceil((x+R)/CELL)),r0=Math.max(0,Math.floor((y-R*1.6)/CELL)),r1=Math.min(DROW-1,Math.ceil((y+R*.4)/CELL));
 for(let r=r0;r<=r1;r++)for(let q=q0;q<=q1;q++){const i=r*DCOL+q;if(!DM[i])continue;const b=G.dirt[i];if(b<.005)continue;G.dirt[i]=Math.max(0,b-amt*.035);rem+=b-G.dirt[i];}
 if(rem>0){dirtDirty=true;f.h=Math.min(1,f.h+rem*.6);if(Math.random()<.04)spawnBubble(x+f.face*f.sp.len*.4,y,1);}
}
function updBottom(f,dt,sz){
 const sp=f.sp;let food=null;
 if(f.h<.95&&foods.length){let bd=1e12;for(const fd of foods){if(fd.eaten||(fd.land<=0&&fd.y<floorY-90))continue;const d=Math.abs(fd.x-f.x);if(d<bd){bd=d;food=fd;}}if(bd>520)food=null;}
 const tx=food?food.x:f.tx,ty=botY(f,sz)+(f.dy||0),dx=tx-f.x,d=Math.abs(dx);
 let want=sp.speed*(.6+.5*sz)*(food?1.7:1);
 if(!food){
  if(f.idle>0){f.idle-=dt;want=0;}
  else if(d<18){f.idle=sp.role==='clean'?rnd(2,6):rnd(.4,1.8);f.tx=rnd(60,WW-60);f.dy=rnd(-3,24);}
  if(sp.role==='clean'&&want>0)want*=.35+.9*Math.max(0,Math.sin(T*2.4+f.seed%9));
 }
 if(f.flee>0){const p=fishBySeed(f.fleeFrom);if(p){want=sp.speed*1.8;f.tx=clamp(f.x+(f.x-p.x>0?1:-1)*240,60,WW-60);}}
 f.vx+=(Math.sign(dx)*Math.min(want,d*2.5)-f.vx)*Math.min(1,dt*2.2);
 f.vy+=((ty-f.y)*2.2-f.vy)*Math.min(1,dt*3);
 f.x+=f.vx*dt;f.y+=f.vy*dt;
 const m=sp.len*sz*.5;f.x=clamp(f.x,m,WW-m);
 if(Math.abs(f.vx)>3){const tf=f.vx>0?1:-1;f.face+=(tf-f.face)*Math.min(1,dt*3);}
 const spd=Math.abs(f.vx);
 f.ph+=dt*(sp.id==='ray'?1.5+spd/16:(spd>3?6+spd/5:.8));
 if(food&&Math.abs(food.x-f.x)<14+12*sz&&Math.abs(food.y-f.y)<70){food.eaten=true;feedFish(f);}
 if(sp.role==='clean'&&f.h>.05)cleanAround(f,dt*(.6+.5*sz));
}
function updSpecial(f,dt,sz){""")
# seahorse/jelly kaçış itmesi
rep(" f.x+=f.vx*dt;f.y+=f.vy*dt;\n const m=sp.len*sz*.4,",
    " if(f.flee>0){const p=fishBySeed(f.fleeFrom);if(p){const ax=f.x-p.x,ay=f.y-p.y,dd=Math.hypot(ax,ay)||1;f.vx+=ax/dd*dt*90;f.vy+=ay/dd*dt*60;}}\n f.x+=f.vx*dt;f.y+=f.vy*dt;\n const m=sp.len*sz*.4,")

# ---------- normal balık: av/kovala/kaç ----------
rep(" const dx=tx-(food?mx:f.x),dy=ty-f.y,d=Math.hypot(dx,dy)||1;\n let want=maxs;if(!food){if(f.idle>0){f.idle-=dt;want*=.12;}if(d<60)want*=d/60;}",
""" let hq=null;
 if(!food){const ch=chaseOf(f);if(ch){hq=ch.q;tx=hq.x;ty=hq.y;maxs*=ch.k;}}
 if(f.flee>0&&!food){const p=fishBySeed(f.fleeFrom);if(p){const ax=f.x-p.x,ay=f.y-p.y,dd=Math.hypot(ax,ay)||1;tx=f.x+ax/dd*220;ty=f.y+ay/dd*140;maxs*=1.75;f.idle=0;}}
 const dx=tx-(food||hq?mx:f.x),dy=ty-f.y,d=Math.hypot(dx,dy)||1;
 let want=maxs;if(!food&&!hq&&!(f.flee>0)){if(f.idle>0){f.idle-=dt;want*=.12;}if(d<60)want*=d/60;}""")
rep(" const k=Math.min(1,dt*(food?3:1.3));", " const k=Math.min(1,dt*(food||hq||f.flee>0?3:1.3));")

# ---------- avcılık + bölgesellik ----------
rep("/* ================= ÇİFTLEŞME / ÜREME ================= */",
"""/* ================= AVCILIK / BÖLGESELLİK ================= */
const PREDS={lion:1,shark:1};
const gsz=f=>.38+.62*Math.min(1,f.g);
const effLen=f=>f.sp.len*gsz(f);
function canEat(p,q){if(q===p||q.dead||q.sid==='pleco'||q.sid==='jelly'||q.sid==='ray'||PREDS[q.sid])return false;return effLen(q)<=effLen(p)*.75;}
const NIP_TXT={clown:'Burası benim!',betta:'Hıh!',puffer:'Çimdik!',angel:'Uzak dur!',tang:'Uzak dur!'};
const LONGFIN={gold:1,betta:1,angel:1};
function chaseOf(f){
 if(f.hunt){const q=fishBySeed(f.hunt.t);if(q){if(f.hunt.st==='stalk')return {q,k:.5};const base=f.sp.speed*(.6+.5*fs(f)),qs=q.sp.speed*(.6+.5*fs(q))*1.75;return {q,k:Math.max(2.3,qs*(f.hunt.esc?.8:1.3)/base)};}}
 if(f.nip){const q=fishBySeed(f.nip.t);if(q)return {q,k:1.9};}
 return null;
}
function catchPrey(p,q){
 p.hunt=null;
 if(q.sid==='puffer'){q.puffT=4;q.flee=2.5;q.fleeFrom=p.seed;p.huntCD=300;floater(q.x,q.y-44,'Şişti, tükürüldü!','#ffe066');snd('blip');return;}
 q.dead=true;q.dt=99;q.mate=0;
 spawnBubble(q.x,q.y,14,true);for(let i=0;i<16;i++)sparks.push({x:q.x+rnd(-22,22),y:q.y+rnd(-14,14),life:rnd(.4,.9)});
 p.h=1;p.huntCD=900;if(p.g<1)p.g=Math.min(1,p.g+.05);
 floater(p.x,p.y-48,'Hap!','#ff8a7a');snd('bad');
 toast(`${p.sid==='shark'?'🦈':'🦁'} ${fname(p)}, ${fname(q)} balığını yedi!`);
 if(selected===q)closeInfo();stat('eaten');save();
}
function updHunt(dt){
 for(const f of G.fish){if(f.flee>0)f.flee-=dt;if(f.huntCD>0)f.huntCD-=dt;if(f.nipCD>0)f.nipCD-=dt;
  if(f.nip){f.nip.tm+=dt;const q=fishBySeed(f.nip.t);if(!q||f.nip.tm>1.6||f.h<.2)f.nip=null;else{q.flee=.8;q.fleeFrom=f.seed;}}}
 // bölgesel kovalamaca (zararsız)
 for(const f of G.fish){if(f.dead||f.nip||f.hunt||temperOf(f.sp)!=='semi'||f.g<.5||f.mate&&(f.cd||0)<=0||(f.nipCD||0)>0)continue;
  if(Math.random()>dt*.08)continue;
  let best=null,bd=170*170;
  for(const q of G.fish){if(q===f||q.dead||q.sid===f.sid||q.sp.move==='bottom'||PREDS[q.sid]||q.sp.len*gsz(q)>f.sp.len*gsz(f)*1.35)continue;
   if(f.sid==='betta'&&!LONGFIN[q.sid])continue;
   const d=(q.x-f.x)**2+(q.y-f.y)**2;if(d<bd){bd=d;best=q;}}
  f.nipCD=rnd(25,55);
  if(best){f.nip={t:best.seed,tm:0};floater(f.x,f.y-34,NIP_TXT[f.sid]||'Uzak dur!','#ffd27a');}
 }
 if(G.noHunt){for(const f of G.fish)f.hunt=null;return;}
 for(const p of G.fish){if(!PREDS[p.sid]||p.dead)continue;
  if(p.hunt){const q=fishBySeed(p.hunt.t);
   if(!q||!canEat(p,q)){p.hunt=null;continue;}
   p.hunt.tm+=dt;
   if(p.h>.5){p.hunt=null;p.huntCD=120;floater(p.x,p.y-44,'Doydu, vazgeçti','#9af575');continue;}
   if(p.hunt.st==='stalk'){if(p.hunt.tm>=8){p.hunt.st='chase';p.hunt.tm=0;p.hunt.esc=Math.random()<.3;snd('bad');floater(p.x,p.y-48,'Saldırıyor!','#ff8a7a');}}
   else{q.flee=1;q.fleeFrom=p.seed;
    const mx=p.x+p.face*p.sp.len*.42*fs(p),d=Math.hypot(q.x-mx,q.y-p.y);
    if(d<10+q.sp.len*fs(q)*.35)catchPrey(p,q);
    else if(p.hunt.tm>6){p.hunt=null;p.huntCD=180;floater(q.x,q.y-38,'Kaçtı!','#9af575');}}
  } else if(p.g>=.6&&p.h<.35&&!((p.huntCD||0)>0)){
   let best=null,bd=1e12;for(const q of G.fish){if(!canEat(p,q))continue;const d=(q.x-p.x)**2+(q.y-p.y)**2;if(d<bd){bd=d;best=q;}}
   if(best){p.hunt={t:best.seed,st:'stalk',tm:0};p.nip=null;snd('bad');floater(p.x,p.y-48,'Acıktım!','#ff8a7a');
    toast(`⚠️ ${fname(p)} acıktı, ${fname(best)} balığına göz dikti! Hemen besle.`);}
   else p.huntCD=20;
  }
 }
}

/* ================= ÇİFTLEŞME / ÜREME ================= */""")
rep(" updPairs(dt);\n", " updPairs(dt);\n updHunt(dt);\n")

# ---------- kirlenme: çöpçü azaltır ----------
rep("const n=liveFish().length,add=(.5+.1*n)/600*dirtAcc*DMN;", "const n=liveFish().length,add=(.5+.1*n)/600*dirtAcc*DMN*cleanerK();")
rep("const n=liveFish().length,add=(.5+.1*n)/600*sec;", "const n=liveFish().length,add=(.5+.1*n)/600*sec*cleanerK();")

# ---------- çizim ----------
rep("ctx.fillStyle=`rgba(0,25,35,${.05+.15*hgt})`;ctx.beginPath();ctx.ellipse(f.x,floorY+6+f.z*30,f.sp.len*sz*.42*(1.4-hgt*.4),3+3*sz,0,0,TAU);ctx.fill();}",
    "const bot=f.sp.move==='bottom';ctx.fillStyle=`rgba(0,25,35,${bot?.3:.05+.15*hgt})`;ctx.beginPath();ctx.ellipse(f.x,bot?f.y+f.sp.hb*f.sp.len*sz*.55:floorY+6+f.z*30,f.sp.len*sz*(bot?.4:.42*(1.4-hgt*.4)),bot?4+4*sz:3+3*sz,0,0,TAU);ctx.fill();}\n"
    " for(const p of lf){if(!p.hunt||p.dead)continue;const q=fishBySeed(p.hunt.t);if(!q)continue;const st=p.hunt.st==='stalk';\n"
    "  ctx.save();ctx.strokeStyle=st?'rgba(255,90,90,.45)':'rgba(255,60,60,.8)';ctx.lineWidth=st?2:3;ctx.setLineDash([4,8]);ctx.lineCap='round';ctx.lineDashOffset=-T*40;ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(q.x,q.y);ctx.stroke();\n"
    "  ctx.setLineDash([]);ctx.strokeStyle=`rgba(255,80,80,${.35+.25*Math.sin(T*8)})`;ctx.lineWidth=2.5;ctx.beginPath();ctx.ellipse(q.x,q.y,q.sp.len*fs(q)*.7,q.sp.hb*q.sp.len*fs(q)*1.4+8,0,0,TAU);ctx.stroke();ctx.restore();}")
rep("  if(f.h<.3)drawBadge(f.x,y+bob,f.h<=0?'hungry':'food');",
    "  if(f.hunt)drawBadge(f.x,y+bob*2,'warn',f.hunt.st==='stalk'?Math.min(1,f.hunt.tm/8):undefined);\n  else if(f.h<.3)drawBadge(f.x,y+bob,f.h<=0?'hungry':'food');")
rep("heart:['#ff6f91','#c2416b'],", "heart:['#ff6f91','#c2416b'],warn:['#ff4d4d','#a3122a'],")
rep(" if(kind==='heart'){heartPath(ctx,0,0,6.2);ctx.fill();}",
    " if(kind==='heart'){heartPath(ctx,0,0,6.2);ctx.fill();}\n else if(kind==='warn'){rr(ctx,-1.9,-7.5,3.8,9.5,1.6);ctx.fill();ctx.beginPath();ctx.arc(0,5.3,2.1,0,TAU);ctx.fill();}")

# ---------- bilgi paneli / mağaza ----------
rep("e.innerHTML=`<h3>${fname(f)}${f.rare?'<span class=\"rtag\">✨ Nadir</span>':''} <small id=\"istg\"></small></h3>",
    "const tp=TEMPER_TXT[temperOf(f.sp)];\n e.innerHTML=`<h3>${fname(f)}${f.rare?'<span class=\"rtag\">✨ Nadir</span>':''}<span class=\"ttag\" style=\"--tc:${tp[1]}\">${tp[0]}</span> <small id=\"istg\"></small></h3>${TEMPER_INFO[temperOf(f.sp)]?`<div class=\"tinfo\">${TEMPER_INFO[temperOf(f.sp)]}</div>`:''}")
rep("  const meta=it.special?it.desc:shopTab==='fish'?`${fmtT(it.grow)} · satış ${it.sell}`:(it.desc||`+${it.xp} XP`);",
    "  const tpx=(!it.special&&shopTab==='fish')?TEMPER_TXT[temperOf(it)]:null;\n  const meta=(tpx?`<b style=\"color:${tpx[1]}\">${tpx[0]}</b> · `:'')+(it.special?it.desc:shopTab==='fish'?`${fmtT(it.grow)} · satış ${it.sell}`:(it.desc||`+${it.xp} XP`));")
rep("  $('shop').classList.add('hidden');toast(`${it.name} yumurtası akvaryuma bırakıldı 🥚`);",
    "  $('shop').classList.add('hidden');toast(PREDS[it.id]?`${it.name} yumurtası bırakıldı. Dikkat: avcıdır, aç kalırsa küçük balıkları yer!`:it.id==='pleco'?'Çöpçü balığı yumurtası bırakıldı: dipte gezip akvaryumu temiz tutacak':`${it.name} yumurtası akvaryuma bırakıldı 🥚`);")
rep(".rtag{", ".ttag{display:inline-block;background:color-mix(in srgb,var(--tc) 22%,transparent);color:var(--tc);border:1px solid color-mix(in srgb,var(--tc) 55%,transparent);border-radius:7px;font-size:10px;font-weight:600;padding:1px 6px;margin-left:5px;vertical-align:middle}\n.tinfo{font-size:11.5px;opacity:.85;margin:-2px 0 6px}\n.rtag{")

# ---------- ayarlar: avcılık aç/kapa ----------
rep('      <button class="row" id="saveB">',
    '      <button class="row" id="huntB"><i data-ic="fish"></i><span>Avcılar balık yesin<small>Köpekbalığı ve aslan balığı acıkınca küçük balıkları avlar</small></span><em class="tg"></em></button>\n      <button class="row" id="saveB">')
rep("$('mus').onclick=()=>{",
    "$('huntB').onclick=()=>{G.noHunt=!G.noHunt;$('huntB').classList.toggle('off',!!G.noHunt);toast(G.noHunt?'Avlanma kapalı: avcılar balık yemez':'Avlanma açık');save();};\n$('mus').onclick=()=>{")
rep("cdShell:G.cdShell||0,starsGot:", "cdShell:G.cdShell||0,noHunt:G.noHunt?1:0,starsGot:")
rep("cdShell:s.cdShell||0,starsGot:", "cdShell:s.cdShell||0,noHunt:!!s.noHunt,starsGot:")
rep(" muted=!!s.muted;musicOff=!!s.musicOff;seenHelp=seenHelp||!!s.seenHelp;",
    " muted=!!s.muted;musicOff=!!s.musicOff;seenHelp=seenHelp||!!s.seenHelp;$('huntB').classList.toggle('off',!!G.noHunt);")

# ---------- yardım ----------
rep("      <p><b>Hareketli süsler:</b>",
    "      <p><b>Avcılar:</b> Köpekbalığı ve aslan balığı acıkınca kendinden küçük bir balığa göz diker (başında kırmızı ünlem çıkar). O sırada beslersen vazgeçer. Ayarlardan kapatılabilir.</p>\n      <p><b>Dip balıkları:</b> Çöpçü balığı kumda gezip kiri temizler, vatoz dipte süzülüp yere düşen yemi toplar.</p>\n      <p><b>Hareketli süsler:</b>")

open(P, 'w', encoding='utf-8').write(s)
print('v7 yaması tamam', len(s))
