"""v6: Blender tane tane kum zemini, süslerin kuma gömülmesi (arka tepecik + ön kum dudağı),
yakın süsler arası kum köprüleri, dokununca açılan sandık / dalgıç kaskı / istiridye."""
import os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'index.template.html')
s = open(P, encoding='utf-8').read()

def R(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:100]); s = s.replace(a, b)

# ---------- kum görseli ----------
R("const LOGO_SRC='/*LOGO*/';", """const LOGO_SRC='/*LOGO*/';
const SAND_SRC='/*SAND*/',SAND_IMG=new Image();let sandOK=false,sandTint=null,sandPat=null,sandSc=1,sandTop=0;
if(SAND_SRC.startsWith('data:')){SAND_IMG.onload=()=>{sandOK=true;if(VW){buildBG();}};SAND_IMG.src=SAND_SRC;}""")

# ---------- tema kum tonları ----------
R("ray:'200,240,255',mote:'230,250,255',vig:'0,18,35',far:'plants'},", "ray:'200,240,255',mote:'230,250,255',vig:'0,18,35',far:'plants',tint:null},")
R("ray:'235,255,205',mote:'230,255,220',vig:'5,25,15',far:'grass'},", "ray:'235,255,205',mote:'230,255,220',vig:'5,25,15',far:'grass',tint:['multiply','#8a6a44',.62]},")
R("ray:'225,255,255',mote:'255,255,255',vig:'0,30,50',far:'reef'},", "ray:'225,255,255',mote:'255,255,255',vig:'0,30,50',far:'reef',tint:['screen','#fff7ea',.42]},")
R("far:'plants',glow:true},", "far:'plants',glow:true,tint:['multiply','#5e6a8c',.72]},")

# ---------- zemin: Blender kumu ----------
R(""" c.save();c.clip();
 const cols=TH.peb;
 const n=Math.round(WW*(WH-floorY)/38);""", """ c.save();c.clip();
 if(sandOK){
  sandTop=floorY-30;sandSc=(WH-sandTop)/SAND_IMG.height;
  sandTint=document.createElement('canvas');sandTint.width=SAND_IMG.width;sandTint.height=SAND_IMG.height;
  const tc=sandTint.getContext('2d');tc.drawImage(SAND_IMG,0,0);
  if(TH.tint){tc.globalCompositeOperation=TH.tint[0];tc.globalAlpha=TH.tint[2];tc.fillStyle=TH.tint[1];tc.fillRect(0,0,sandTint.width,sandTint.height);tc.globalAlpha=1;tc.globalCompositeOperation='source-over';}
  const tw=SAND_IMG.width*sandSc;for(let x=0;x<WW;x+=tw)c.drawImage(sandTint,x,sandTop,tw,WH-sandTop);
  sandPat=null;
  g=c.createLinearGradient(0,sandTop,0,WH);g.addColorStop(0,'rgba(0,0,0,.12)');g.addColorStop(.35,'rgba(0,0,0,0)');g.addColorStop(1,'rgba(0,0,0,.18)');c.fillStyle=g;c.fillRect(0,sandTop,WW,WH-sandTop);
 }
 const cols=TH.peb;
 const n=sandOK?0:Math.round(WW*(WH-floorY)/38);""")

# eski canvas kum tepeciği: Blender kumu varken yeni sistem çiziyor
R("function sandMound(c,w){", "function sandMound(c,w){\n if(sandOK)return;")

# ---------- tepecik / köprü / dudak ----------
R("function decorPos(d){", r"""function sandFill(){
 if(!sandTint)return '#d9c38f';
 if(!sandPat){sandPat=ctx.createPattern(sandTint,'repeat');}
 if(sandPat.setTransform)sandPat.setTransform(new DOMMatrix().translateSelf(0,sandTop).scaleSelf(sandSc,sandSc));
 return sandPat;
}
function moundGeo(d){const def=DC_[d.t];const w=(def.w||60)*d.s;return {x:d.x,y:d.y,hw:w*.52+12,mh:5+Math.min(15,w*.075)};}
function shadeMound(top,bot,x0,x1){
 const g=ctx.createLinearGradient(0,top,0,bot);g.addColorStop(0,'rgba(255,248,225,.28)');g.addColorStop(.5,'rgba(255,248,225,0)');g.addColorStop(1,'rgba(60,40,20,.22)');
 ctx.fillStyle=g;ctx.fill();
}
function drawMoundsBack(ds){
 const fill=sandFill();
 // yakın süsler arası kum köprüleri
 for(let i=0;i<ds.length;i++)for(let j=i+1;j<ds.length;j++){
  const a=moundGeo(ds[i]),b=moundGeo(ds[j]);const L=a.x<b.x?a:b,Rr=a.x<b.x?b:a;
  if(Rr.x-L.x>L.hw+Rr.hw+55||Math.abs(a.y-b.y)>40)continue;
  const bh=Math.min(a.mh,b.mh)*.55,mx=(L.x+Rr.x)/2,my=(L.y+Rr.y)/2;
  ctx.beginPath();ctx.moveTo(L.x,L.y-L.mh*.6);ctx.quadraticCurveTo(mx,my-bh-2,Rr.x,Rr.y-Rr.mh*.6);ctx.lineTo(Rr.x,Rr.y+10);ctx.lineTo(L.x,L.y+10);ctx.closePath();
  ctx.fillStyle=fill;ctx.fill();shadeMound(my-bh,my+10);
  const rr=mulberry((ds[i].seed^ds[j].seed)>>>0);
  for(let k=0;k<9;k++){const t=.15+rr()*.7,x=L.x+(Rr.x-L.x)*t,y=L.y+(Rr.y-L.y)*t-bh*Math.sin(Math.PI*t)*.6+rr()*8,s=1.5+rr()*2.6;
   ctx.fillStyle='rgba(50,35,20,.35)';ctx.beginPath();ctx.ellipse(x+.7,y+.8,s,s*.6,0,0,TAU);ctx.fill();
   ctx.fillStyle=['#efe0b8','#b8a17c','#8a9aa0','#c9a07a','#f6ead0','#7d6a4a'][(rr()*6)|0];ctx.beginPath();ctx.ellipse(x,y,s,s*.6,rr(),0,TAU);ctx.fill();}
  const kind=(ds[i].seed+ds[j].seed)%3;
  if(kind===0){ctx.strokeStyle='#3f7a34';ctx.lineWidth=2;ctx.lineCap='round';for(let k=-2;k<=2;k++){ctx.beginPath();ctx.moveTo(mx+k*3,my-bh+4);ctx.quadraticCurveTo(mx+k*5,my-bh-8,mx+k*7+Math.sin(T+k)*2,my-bh-16-Math.abs(k)*-2);ctx.stroke();}}
  else if(kind===1){ctx.fillStyle='#f3d9c8';ctx.beginPath();ctx.moveTo(mx,my-bh+3);ctx.arc(mx,my-bh+3,7,Math.PI*1.1,Math.PI*1.9);ctx.closePath();ctx.fill();ctx.strokeStyle='rgba(150,90,70,.5)';ctx.lineWidth=.8;ctx.beginPath();for(let k=0;k<5;k++){const an=Math.PI*(1.15+k*.17);ctx.moveTo(mx,my-bh+3);ctx.lineTo(mx+Math.cos(an)*7,my-bh+3+Math.sin(an)*7);}ctx.stroke();}
 }
 // her süsün arka tepeciği
 for(const d of ds){const m=moundGeo(d);
  ctx.beginPath();ctx.moveTo(m.x-m.hw-12,m.y+9);ctx.bezierCurveTo(m.x-m.hw*.62,m.y+9,m.x-m.hw*.55,m.y-m.mh,m.x,m.y-m.mh);ctx.bezierCurveTo(m.x+m.hw*.55,m.y-m.mh,m.x+m.hw*.62,m.y+9,m.x+m.hw+12,m.y+9);ctx.lineTo(m.x+m.hw+12,m.y+12);ctx.lineTo(m.x-m.hw-12,m.y+12);ctx.closePath();
  ctx.fillStyle=fill;ctx.fill();shadeMound(m.y-m.mh,m.y+12);}
}
function drawLip(d){
 const m=moundGeo(d),hw=m.hw*.86,fill=sandFill();
 ctx.beginPath();ctx.moveTo(m.x-hw,m.y-1);ctx.quadraticCurveTo(m.x,m.y+3,m.x+hw,m.y-1);ctx.lineTo(m.x+hw*1.08,m.y+7);ctx.quadraticCurveTo(m.x,m.y+15,m.x-hw*1.08,m.y+7);ctx.closePath();
 ctx.fillStyle=fill;ctx.fill();
 const g=ctx.createLinearGradient(0,m.y-2,0,m.y+14);g.addColorStop(0,'rgba(255,250,235,.32)');g.addColorStop(.45,'rgba(255,250,235,0)');g.addColorStop(1,'rgba(50,32,15,.2)');ctx.fillStyle=g;ctx.fill();
 const rr=mulberry((d.seed>>>0)+3);
 for(let k=0;k<10;k++){const x=m.x+(rr()-.5)*hw*1.9,y=m.y+rr()*4,s=1.2+rr()*1.8;ctx.fillStyle=['#efe0b8','#c2a46e','#9c8152','#f6ead0'][(rr()*4)|0];ctx.beginPath();ctx.ellipse(x,y,s,s*.6,0,0,TAU);ctx.fill();}
}
function decorPos(d){""")
R(" for(const d of ds)drawDecorAt(ctx,d,T,d.x,d.y,d.s);", " drawMoundsBack(ds);\n for(const d of ds){drawDecorAt(ctx,d,T,d.x,d.y,d.s);drawLip(d);}")

# ---------- hareketli süsler: kare seçimi ----------
R("  if(d.t==='shell'){const op=Math.pow(Math.max(0,Math.sin(t*.35+(d.ph||0))),.6);fr=Math.min(ds_.n-1,Math.round(op*(ds_.n-1)));}",
  "  if(ds_.n>1)fr=Math.min(ds_.n-1,Math.round((d.op||0)*(ds_.n-1)));")
R("  if(d.t==='volcano'||d.t==='chest'){c.shadowBlur=0;const p=.6+.4*Math.sin(t*2+(d.ph||0)),",
  "  if(d.t==='volcano'||(d.t==='chest'&&(d.op||0)>.05)){c.shadowBlur=0;const p=(.6+.4*Math.sin(t*2+(d.ph||0)))*(d.t==='chest'?d.op:1),")

# ---------- hareketli süsler: güncelleme ----------
R("  if(d.t==='chest'){d.bt-=dt;if(d.bt<=0){d.bt=rnd(3,6);spawnBubble(d.x,d.y-55*d.s,6,true);}}\n  if(d.t==='shell'){const op=Math.sin(T*.35+d.ph);if(op>.98&&Math.random()<dt*3)spawnBubble(d.x,d.y-30*d.s,2,true);}",
  "  if(d.t==='chest'&&(d.op||0)<.05){d.bt-=dt;if(d.bt<=0){d.bt=rnd(4,8);spawnBubble(d.x+rnd(-14,14)*d.s,d.y-42*d.s,2);}}\n  updInteract(d,dt);")
R("function update(dt){", r"""/* ---- dokununca açılan süsler ---- */
const INTER={chest:{hold:4.5,spd:1.6},diver:{hold:4,spd:1.8},shell:{hold:3.2,spd:1.4}};
function interact(d){
 const it=INTER[d.t];if(!it)return false;
 if(d.ot===1){d.ot=0;d.hold=0;}else{d.ot=1;d.hold=it.hold;d.man=1;}
 snd(d.t==='chest'?'creak':'blip');return true;
}
function updInteract(d,dt){
 const it=INTER[d.t];if(!it)return;
 if(d.op===undefined){d.op=0;d.ot=0;d.hold=0;}
 const prev=d.op;
 if(d.t==='shell'&&!d.man){d.op=Math.pow(Math.max(0,Math.sin(T*.35+(d.ph||0))),.6);if(d.op>.97&&Math.random()<dt*3)spawnBubble(d.x,d.y-30*d.s,2,true);return;}
 d.op+=Math.sign(d.ot-d.op)*Math.min(Math.abs(d.ot-d.op),dt*it.spd);
 if(d.ot===1&&d.op>=1){d.hold-=dt;if(d.hold<=0)d.ot=0;}
 if(d.ot===1&&prev<.8&&d.op>=.8)openBurst(d);
 if(d.t==='diver'&&d.op>.6&&Math.random()<dt*9)spawnBubble(d.x+(2+rnd(-6,6))*d.s,d.y-108*d.s,1,Math.random()<.5);
 if(d.op<.02&&d.ot===0){d.man=0;}
}
function openBurst(d){
 const now=Date.now();
 if(d.t==='chest'){
  spawnBubble(d.x,d.y-52*d.s,22,true);for(let i=0;i<24;i++)sparks.push({x:d.x+rnd(-36,36)*d.s,y:d.y+rnd(-70,-35)*d.s,life:rnd(.5,1.2)});
  if(now>(G.cdChest||0)){const c=12+G.level*3;G.coins+=c;G.cdChest=now+30*60e3;floater(d.x,d.y-90*d.s,`+${c}`,'#ffe066');toast(`Sandıktan ${c} altın çıktı!`);snd('coin');save();updHUD();}
  else floater(d.x,d.y-90*d.s,`Boş · ${fmtT((G.cdChest-now)/1000)}`,'#cfe9f7');
 } else if(d.t==='diver'){
  spawnBubble(d.x+2*d.s,d.y-106*d.s,16,true);floater(d.x,d.y-140*d.s,'Merhaba!','#ffffff');
 } else if(d.t==='shell'){
  for(let i=0;i<18;i++)sparks.push({x:d.x+rnd(-20,20)*d.s,y:d.y+rnd(-40,-10)*d.s,life:rnd(.5,1.1),pink:1});spawnBubble(d.x,d.y-24*d.s,8,true);
  if(now>(G.cdShell||0)){G.pearls=(G.pearls||0)+1;G.cdShell=now+12*3600e3;floater(d.x,d.y-60*d.s,'+1 inci','#e6dcff');toast('İstiridyeden bir inci çıktı!');snd('lvl');save();updHUD();}
  else floater(d.x,d.y-60*d.s,`İnci ${fmtT((G.cdShell-now)/1000)} sonra`,'#cfe9f7');
 }
}
function update(dt){""")
R(" case 'bad':tone(300,0,.2,'sawtooth',.05,150);break;",
  " case 'bad':tone(300,0,.2,'sawtooth',.05,150);break;\n case 'creak':tone(140,0,.35,'sawtooth',.03,90);tone(220,.05,.25,'triangle',.05,160);break;")

# ---------- dokunma: kısa dokunuş = aç/kapat ----------
R("const up=()=>{pointer.down=false;if(dragging){dragging=null;save();}",
  "const up=()=>{pointer.down=false;if(dragging){const d=dragging;dragging=null;if(dragMoved<8&&INTER[d.t])interact(d);save();}")
R("e.innerHTML=`<h3>${def.name}</h3><div class=\"bar\">Taşımak için sürükle.</div>",
  "e.innerHTML=`<h3>${def.name}</h3><div class=\"bar\">${INTER[d.t]?'Dokun: açılır. ':''}Taşımak için sürükle. Yakındaki süslerle kumla birleşir.</div>")
R(" {id:'shell',name:'İnci İstiridyesi',lvl:3,cost:130,xp:4,w:95,h:50,draw:dShell,desc:'Açılıp kapanır'},",
  " {id:'shell',name:'İnci İstiridyesi',lvl:3,cost:130,xp:4,w:95,h:50,draw:dShell,desc:'Dokun: günde 2 inci'},")
R(" {id:'diver',name:'Dalgıç',lvl:5,cost:220,xp:6,w:60,h:120,draw:dDiver,desc:'Kabarcık çıkarır'},",
  " {id:'diver',name:'Dalgıç',lvl:5,cost:220,xp:6,w:60,h:120,draw:dDiver,desc:'Dokun: kaskı açılır'},")
R(" {id:'chest',name:'Hazine Sandığı',lvl:6,cost:300,xp:8,w:95,h:85,draw:dChest,desc:'Kabarcık çıkarır'},",
  " {id:'chest',name:'Hazine Sandığı',lvl:6,cost:300,xp:8,w:95,h:85,draw:dChest,desc:'Dokun: açılır, altın verir'},")

# ---------- kayıt ----------
R("  pearls:G.pearls||0,starsGot:G.starsGot||0,", "  pearls:G.pearls||0,cdChest:G.cdChest||0,cdShell:G.cdShell||0,starsGot:G.starsGot||0,")
R("  pearls:s.pearls??5,starsGot:s.starsGot||0,", "  pearls:s.pearls??5,cdChest:s.cdChest||0,cdShell:s.cdShell||0,starsGot:s.starsGot||0,")
R("      <p><b>Güzellik ve inci:</b>", "      <p><b>Hareketli süsler:</b> Hazine sandığına, dalgıca ve inci istiridyesine dokun: açılırlar. Sandık yarım saatte bir altın, istiridye günde iki inci verir.</p>\n      <p><b>Güzellik ve inci:</b>")

open(P, 'w', encoding='utf-8').write(s)
print('v6 yaması tamam', len(s))
