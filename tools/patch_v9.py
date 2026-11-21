"""v9: balık–süs etkileşimi (yuvalar, saklanma), gece ve gündüz, nadir misafirler, renk genetiği ve 7 Efsane Balık."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'src', 'index.template.html')
s = open(P, encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    assert s.count(a) >= 1, 'bulunamadı: ' + a[:90]
    s = s.replace(a, b, n)

# ================= sprite yükleme =================
rep("const DSPR={},DMASK={};", "const DSPR={},DMASK={},VSPR={};")
rep(" else if(id.startsWith('m_'))DMASK[id.slice(2)]=mkSpr(m);",
    " else if(id.startsWith('m_'))DMASK[id.slice(2)]=mkSpr(m);\n else if(id.startsWith('v_'))VSPR[id.slice(2)]=mkSpr(m);\n else if(id.endsWith('_l')){const sp=SP[id.slice(0,-2)];if(sp)sp.sprL=mkSpr(m);}")

# ================= genetik + efsaneler: veri =================
rep("const fname=f=>f.rare?(RARE[f.sid]||f.sp.name):f.sp.name;",
"""const LEG={
 koi:{name:'Ejder Koi',hint:"İki Altın Koi'nin yavrusu efsanevi olabilir.",ok:(f,m)=>f.rare&&m.rare},
 neon:{name:'Gökkuşağı Neon',hint:'Renkleri birbirinden çok farklı iki neon çiftleşirse...',ok:(f,m)=>hueDist(f.hu||0,m.hu||0)>=120},
 jelly:{name:'Ay Işığı Denizanası',hint:'Gece yumurtlayan denizanalarının yavrusu...',ok:()=>NK>.6},
 angel:{name:'Kraliyet Meleği',hint:'Uzun bitkilerle dolu, çok güzel bir akvaryumda melekler...',ok:()=>G.decor.filter(d=>['kelp','fan','weed'].includes(d.t)).length>=3&&beautyCache>=300},
 discus:{name:'Kristal Diskus',hint:'Tertemiz suda, bir kristalin ışığında diskuslar...',ok:()=>G.decor.some(d=>d.t==='crystal')&&clean>=.9},
 shark:{name:'Hayalet Köpekbalığı',hint:'İki albino köpekbalığının yavrusu...',ok:(f,m)=>f.rare&&m.rare},
 seahorse:{name:'Altın Deniz Atı',hint:'Dev yosunlu bir akvaryumda pembe bir deniz atı...',ok:(f,m)=>(f.rare||m.rare)&&G.decor.some(d=>d.t==='kelp')}};
const fname=f=>f.leg?(LEG[f.sid]?LEG[f.sid].name:f.sp.name):f.rare?(RARE[f.sid]||f.sp.name):f.sp.name;
const hueDist=(a,b)=>{const d=Math.abs(((a-b)%360+540)%360-180);return d;};
const snapHue=h=>((Math.round(h/15)*15)%360+540)%360-180;
const gauss=()=>{const u=1-Math.random(),v=Math.random();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v);};
function circMean(a,b){const r=Math.PI/180,x=Math.cos(a*r)+Math.cos(b*r),y=Math.sin(a*r)+Math.sin(b*r);return Math.atan2(y,x)/r;}
function childHue(f,m){if(Math.random()<.06)return snapHue(Math.floor(Math.random()*24)*15);return snapHue(circMean(f.hu||0,m.hu||0)+gauss()*14);}
const buyHue=()=>Math.random()<.15?(Math.random()<.5?-1:1)*(Math.random()<.5?15:30):0;
function legRoll(f,m){if(f.leg&&m.leg)return Math.random()<.5?1:0;const L=LEG[f.sid];return L&&L.ok(f,m)&&Math.random()<.3?1:0;}
const hueTxt=h=>!h?'Doğal renk':`${h>0?'+':''}${h}°`;""")
rep("f.rare=!!o.rare;f.mate=o.mate||0;", "f.rare=!!o.rare;f.leg=!!o.leg;f.hu=o.hu||0;f.mate=o.mate||0;")
rep("const incomeRate=f=>f.sp.sell*.006*(f.rare?3:1)*beautyMult();",
    "const incomeRate=f=>f.sp.sell*.006*(f.leg?5:f.rare?3:1)*beautyMult()*(homeOf(f)?1.15:1);")
rep("function sellValue(f){return (f.g>=1?f.sp.sell:Math.floor(f.sp.sell*f.g*.5))*(f.rare?3:1);}",
    "function sellValue(f){return (f.g>=1?f.sp.sell:Math.floor(f.sp.sell*f.g*.5))*(f.leg?8:f.rare?3:1);}")
# çizim: efsane sprite'ı + renk geni (ton kaydırma, önbellekli)
rep("function drawFishAny(c,sp,ph,f){const s=(f&&f.rare&&sp.sprR&&sp.sprR.ok)?sp.sprR:sp.spr;",
    """function tinted(s,hu){s.tc=s.tc||{};let t=s.tc[hu];if(t)return t;const c=document.createElement('canvas');c.width=s.img.naturalWidth||s.fw*s.n;c.height=s.img.naturalHeight||s.fh;const x=c.getContext('2d');
 if('filter' in x)x.filter=`hue-rotate(${hu}deg) saturate(1.12)`;x.drawImage(s.img,0,0);t=s.tc[hu]={fw:s.fw,fh:s.fh,n:s.n,ppu:s.ppu,ox:s.ox,oy:s.oy,img:c,ok:true};return t;}
function drawFishAny(c,sp,ph,f){let s=(f&&f.leg&&sp.sprL&&sp.sprL.ok)?sp.sprL:(f&&f.rare&&sp.sprR&&sp.sprR.ok)?sp.sprR:sp.spr;if(s&&s.ok&&f&&f.hu&&!f.leg)s=tinted(s,f.hu);""")
rep(" if(f.rare&&Math.random()<dt*2.2)sparks.push({x:f.x+rnd(-26,26)*sz,y:f.y+rnd(-18,18)*sz,life:.9,pink:1});",
    " if(f.rare&&Math.random()<dt*2.2)sparks.push({x:f.x+rnd(-26,26)*sz,y:f.y+rnd(-18,18)*sz,life:.9,pink:1});\n if(f.leg&&Math.random()<dt*3.5)sparks.push({x:f.x+rnd(-30,30)*sz,y:f.y+rnd(-20,20)*sz,life:1});")
# kalıtım
rep("rp:(f.rare?.25:0)+(m.rare?.25:0)});", "rp:(f.rare?.25:0)+(m.rare?.25:0),hu:childHue(f,m),leg:legRoll(f,m)});")
rep(" const sp=SP[e.sid],rare=!!sp.sprR&&(e.forceRare||Math.random()<RARE_P+(e.rp||0));\n const f=makeFish(e.sid,0,{x:e.x,y:e.y-25,h:.7,rare});",
    " const sp=SP[e.sid],leg=!!e.leg&&!!LEG[e.sid],rare=!leg&&!!sp.sprR&&(e.forceRare||Math.random()<RARE_P+(e.rp||0));\n const f=makeFish(e.sid,0,{x:e.x,y:e.y-25,h:.7,rare,leg,hu:leg?0:(e.hu||0)});\n G.hues=G.hues||{};{const hl=G.hues[e.sid]=G.hues[e.sid]||[];if(!hl.includes(f.hu))hl.push(f.hu);}")
rep(" if(rare){floater(e.x,e.y-40,'✨ NADİR! '+RARE[e.sid]", " if(leg){legendHatch(f,e);}\n else if(rare){floater(e.x,e.y-40,'✨ NADİR! '+RARE[e.sid]")
rep("/* ---- dokununca açılan süsler ---- */",
"""function legendHatch(f,e){const L=LEG[f.sid];G.legs=G.legs||{};const first=!G.legs[f.sid];G.legs[f.sid]=1;
 floater(e.x,e.y-46,'🌟 EFSANEVİ! '+L.name,'#ffe27a');for(let i=0;i<50;i++)sparks.push({x:e.x+rnd(-70,70),y:e.y-25+rnd(-50,40),life:rnd(.7,1.6)});snd('lvl');
 if(first){G.pearls=(G.pearls||0)+10;toast(`🌟 Efsane keşfedildi: ${L.name}! +10 inci. Defterde yerini aldı.`);}else toast(`🌟 Yine bir efsane doğdu: ${L.name}!`);
 stat('legend');save();updHUD();}
/* ---- dokununca açılan süsler ---- */""")
rep("eggs.push({sid:it.id,x,y:topY,vy:0,ly:floorY+rnd(0,30),t:0,p:rnd(0,TAU)});", "eggs.push({sid:it.id,x,y:topY,vy:0,ly:floorY+rnd(0,30),t:0,p:rnd(0,TAU),hu:buyHue()});")

# ================= yuvalar ve saklanma =================
rep("function newTarget(f){f.tx=rnd(60,WW-60);f.ty=rnd(topY+30,floorY-30);}",
"""const HOME={clown:['anem'],neon:['weed','redweed','kelp'],betta:['weed','redweed'],seahorse:['kelp','weed','fan'],angel:['kelp','fan'],discus:['arch','log','rock'],puffer:['rock','coral','brain'],tang:['coral','rock','arch'],lion:['ship','castle','arch'],pleco:['log','rock']};
const ANCH={anem:-36,weed:-90,redweed:-60,kelp:-150,fan:-80,arch:-38,log:-26,rock:-50,coral:-70,brain:-40,castle:-36,ship:-75,amph:-52,column:-85};
const SHELTER=['castle','ship','arch','log','amph','rock','kelp','weed','coral','column','fan','redweed'];
function homeOf(f){const L=HOME[f.sid];if(!L||f.dead||!G.decor)return null;
 if(f.home&&G.decor.includes(f.home))return f.home;
 let b=null,bd=1e12;for(const d of G.decor){if(!L.includes(d.t))continue;const dd=Math.abs(d.x-f.x);if(dd<bd){bd=dd;b=d;}}f.home=b;return b;}
const anchorOf=d=>({x:d.x,y:d.y+(ANCH[d.t]||-40)*(d.s||1)});
function shelterNear(f){let b=null,bd=280;for(const d of G.decor){if(!SHELTER.includes(d.t))continue;const a=anchorOf(d),dd=Math.hypot(a.x-f.x,a.y-f.y);if(dd<bd){bd=dd;b=d;}}return b;}
function homeLine(f){const L=HOME[f.sid];if(!L)return f.sp.move==='bottom'&&f.sid!=='pleco'?'Dipte dolaşır.':'Açık suyu sever, yuvaya ihtiyacı yok.';const h=homeOf(f);
 return h?`🏠 Yuvası: ${DC_[h.t].name} (+%15 gelir)`:`Sevdiği süs: ${L.map(t=>DC_[t].name).join(' / ')} (akvaryumda yok)`;}
function homeFans(id){const n=Object.keys(HOME).filter(k=>HOME[k].includes(id)).map(k=>SP[k]&&SP[k].name).filter(Boolean);return n.length?` · Yuva: ${n.slice(0,2).join(', ')}`:'';}
function newTarget(f){const h=(f.sp&&!f.dead)?homeOf(f):null;
 if(h&&(Math.random()<.55||NK>.6)){const a=anchorOf(h),r=f.sid==='clown'?20:45;f.tx=clamp(a.x+rnd(-r,r)*1.4,60,WW-60);f.ty=clamp(a.y+rnd(-r,r)*.6,topY+30,floorY-20);f.atHome=1;return;}
 f.atHome=0;f.tx=rnd(60,WW-60);f.ty=NK>.6?rnd(floorY-190,floorY-40):rnd(topY+30,floorY-30);}""")
rep("function canEat(p,q){if(q===p||q.dead||", "function canEat(p,q){if(q===p||q.dead||q.hid>0||")
# kaçarken saklanma
rep(" if(f.flee>0&&!food){const p=fishBySeed(f.fleeFrom);if(p){const ax=f.x-p.x,ay=f.y-p.y,dd=Math.hypot(ax,ay)||1;tx=f.x+ax/dd*220;ty=f.y+ay/dd*140;maxs*=1.75;f.idle=0;}}",
    " if(f.flee>0&&!food){const p=fishBySeed(f.fleeFrom);if(p){const sh=shelterNear(f);if(sh){const a=anchorOf(sh);tx=a.x;ty=a.y;if(Math.hypot(a.x-f.x,a.y-f.y)<38)f.hid=2.5;}else{const ax=f.x-p.x,ay=f.y-p.y,dd=Math.hypot(ax,ay)||1;tx=f.x+ax/dd*220;ty=f.y+ay/dd*140;}maxs*=1.75;f.idle=0;}}")
rep(" let tx=f.tx,ty=f.ty,maxs=sp.speed*(.6+.5*sz),food=null;",
    " let tx=f.tx,ty=f.ty,maxs=sp.speed*(.6+.5*sz),food=null;\n if(f.hid>0)f.hid-=dt;\n const sleepy=NK>.6&&!PREDS[f.sid]&&!f.hunt;if(sleepy)maxs*=.35;\n if(sleepy&&f.idle>0&&Math.random()<dt*.05)floater(f.x+f.face*12,f.y-16,'z','#cfe0ff');\n if(f.sid==='clown'&&f.atHome&&f.idle>0&&Math.random()<dt*.25)spawnBubble(f.x,f.y-6,1);")
rep(" if(!food&&d<25){if(f.idle<=0&&Math.random()<.4)f.idle=rnd(.5,2.5);newTarget(f);}",
    " if(!food&&d<25){if(f.idle<=0&&Math.random()<.4)f.idle=f.atHome?rnd(2,6)*(NK>.6?2:1):rnd(.5,2.5);newTarget(f);}")
rep(" f.ph+=dt*(3+Math.hypot(f.vx,f.vy)/sp.len*5);", " f.ph+=dt*(3+Math.hypot(f.vx,f.vy)/sp.len*5)*(sleepy?.5:1);")
rep(" if(!food&&d<30){if(f.idle<=0&&Math.random()<.5)f.idle=rnd(1,3);newTarget(f);}",
    " if(!food&&d<30){if(f.idle<=0&&Math.random()<.5)f.idle=f.atHome?rnd(3,8):rnd(1,3);newTarget(f);}")
rep(" let a=.72+.28*f.z;", " let a=.72+.28*f.z;if(f.hid>0)a*=.45;")
# dip balıkları gece daha hareketli
rep(" let want=sp.speed*(.6+.5*sz)*(food?1.7:1);", " let want=sp.speed*(.6+.5*sz)*(food?1.7:1)*(1+.5*NK);")

# ================= gece ve gündüz =================
rep("let eggs=[],foods=[]", "let NK=0;\nfunction nightK(){const m=(typeof G!=='undefined'&&G&&G.dayMode)||'auto';if(m==='day')return 0;if(m==='night')return 1;const d=new Date(),h=d.getHours()+d.getMinutes()/60;\n if(h>=21||h<5.5)return 1;if(h>=19)return (h-19)/2;if(h<7.5)return 1-(h-5.5)/2;return 0;}\nlet eggs=[],foods=[]")
rep(" updDust(dt);\n", " updDust(dt);\n NK+=(nightK()-NK)*Math.min(1,dt*.8);\n updVisitor(dt);\n")
rep(" if(TH.over){ctx.fillStyle=TH.over;ctx.fillRect(0,0,WW,WH);}",
    " drawVisitor();\n if(TH.over){ctx.fillStyle=TH.over;ctx.fillRect(0,0,WW,WH);}\n if(NK>.01)drawNight();")
rep("function drawFishWorld(f){",
"""function drawNight(){
 const k=NK;ctx.save();ctx.globalCompositeOperation='multiply';
 ctx.fillStyle=`rgb(${Math.round(255-205*k)},${Math.round(255-178*k)},${Math.round(255-118*k)})`;ctx.fillRect(0,0,WW,WH);
 ctx.globalCompositeOperation='lighter';
 const g=ctx.createLinearGradient(0,0,0,floorY);g.addColorStop(0,`rgba(120,150,230,${.16*k})`);g.addColorStop(1,'rgba(120,150,230,0)');ctx.fillStyle=g;ctx.beginPath();ctx.moveTo(WW*.6,0);ctx.lineTo(WW*.72,0);ctx.lineTo(WW*.84,floorY);ctx.lineTo(WW*.5,floorY);ctx.fill();
 const glow=(x,y,R,col,a)=>{const gg=ctx.createRadialGradient(x,y,0,x,y,R);gg.addColorStop(0,`rgba(${col},${a})`);gg.addColorStop(1,`rgba(${col},0)`);ctx.fillStyle=gg;ctx.fillRect(x-R,y-R,R*2,R*2);};
 for(const m of motes){const a=(.28+.28*Math.sin(T*1.7+m.p*5))*k;if(a>.05)glow(m.x,m.y,m.r*4,'120,255,220',a);}
 for(const f of G.fish){if(f.dead)continue;const sz=fs(f);
  if(f.sp.move==='jelly')glow(f.x,f.y,70*sz,f.leg?'190,200,255':f.rare?'120,210,255':'255,150,210',.45*k);
  else if(f.leg)glow(f.x,f.y,58*sz,'255,225,120',.4*k);}
 for(const d of G.decor){const p=.75+.25*Math.sin(T*1.5+(d.ph||0));
  if(d.t==='crystal')glow(d.x,d.y-50*d.s,110*d.s,'150,210,255',.5*k*p);else if(d.t==='volcano')glow(d.x,d.y-95*d.s,120*d.s,'255,140,60',.5*k*p);else if(d.t==='anem')glow(d.x,d.y-25*d.s,48*d.s,'230,140,255',.35*k*p);}
 const V=G.vis;if(V&&V.id==='angler'){const v=VIS_.angler;glow(V.x+V.face*v.len*.66,V.y-v.len*.3,60,'120,255,190',(.55+.25*Math.sin(T*3))*(.4+.6*k));}
 ctx.restore();
}
/* ================= nadir misafirler ================= */
const VIS=[
 {id:'turtle',emo:'🐢',name:'Deniz Kaplumbağası',len:170,move:'swim',spd:24,gift:{p:3},stay:[40,90],hint:'Bol yosunlu ve güzel bir akvaryumu sever.',desc:'Uzun yolculuğunda dinlenecek yeşil bir akvaryum arıyor.',cond:()=>G.decor.filter(d=>['weed','redweed','kelp','fan'].includes(d.t)).length>=2&&beautyCache>=120},
 {id:'octo',emo:'🐙',name:'Ahtapot',len:105,move:'perch',spd:16,gift:{p:2,c:150},stay:[30,80],hint:'Saklanacak bir batık gemi, testi ya da sandık arar.',desc:'Zeki ve meraklı; batıkların arasında dolaşmayı sever.',cond:()=>G.decor.some(d=>['ship','amph','chest'].includes(d.t))},
 {id:'crab',emo:'🦀',name:'Keşiş Yengeci',len:62,move:'walk',spd:15,gift:{c:120},stay:[30,70],hint:'Kumda kabuk, çakıl ya da deniz yıldızı arar.',desc:'Evini sırtında taşır; büyüdükçe daha büyük bir kabuğa taşınır.',cond:()=>G.decor.some(d=>['shell','pebble','star'].includes(d.t))},
 {id:'nudi',emo:'🐌',name:'Renkli Deniz Salyangozu',len:58,move:'walk',spd:7,gift:{p:2},stay:[30,70],hint:'Mercan ve anemon olan akvaryumlarda dolaşır.',desc:'Nudibranş: denizin en renkli canlılarından biri.',cond:()=>G.decor.some(d=>['coral','brain','fan'].includes(d.t))&&G.decor.some(d=>d.t==='anem')},
 {id:'angler',emo:'🏮',name:'Fener Balığı',len:92,move:'deep',spd:13,gift:{p:5},stay:[25,60],night:1,hint:'Yalnızca geceleri, ışıldayan bir süsün yanına gelir.',desc:'Derin denizden geldi; başındaki ışıkla yolunu buluyor.',cond:()=>NK>.6&&G.decor.some(d=>['crystal','volcano'].includes(d.t))}];
const VIS_={};VIS.forEach(v=>VIS_[v.id]=v);
let visT=25;
const visEligible=()=>VIS.filter(v=>{try{return !!v.cond();}catch(_){return false;}});
function visY(v){return v.move==='swim'?rnd(topY+90,floorY-170):v.move==='deep'?floorY-75:v.move==='perch'?floorY-20:floorY+22;}
function visPerch(){const d=G.decor.find(x=>['ship','amph','chest'].includes(x.t));if(!d)return null;return {x:d.x+(d.t==='ship'?25:0)*d.s,y:d.y+({ship:-128,amph:-92,chest:-74}[d.t])*d.s};}
function spawnVisitor(quiet,force){const el=force?[VIS_[force]]:visEligible();if(!el.length||!el[0])return false;
 const w=el.map(v=>((G.vbook||{})[v.id]?1:2.5)*(G.lastVis===v.id?.3:1));let r=Math.random()*w.reduce((a,b)=>a+b,0),v=el[0];for(let i=0;i<el.length;i++){r-=w[i];if(r<=0){v=el[i];break;}}
 const fromL=Math.random()<.5;G.vis={id:v.id,until:Date.now()+rnd(v.stay[0],v.stay[1])*60e3,x:fromL?-90:WW+90,y:visY(v),face:fromL?1:-1,ph:0,seen:0,tx:rnd(160,WW-160),wait:0};G.lastVis=v.id;
 if(!quiet){toast(`${v.emo} Akvaryumuna bir misafir geldi: ${v.name}! Dokunup deftere ekle.`);snd('blip');}
 save();return true;}
function updVisitor(dt){
 visT-=dt;const V=G.vis;
 if(!V){if(visT<=0){visT=45;if(Math.random()<.2)spawnVisitor();}return;}
 const v=VIS_[V.id];if(!v){G.vis=null;return;}
 const leave=Date.now()>V.until||(v.night&&NK<.35)||(v.move==='perch'&&!visPerch());
 let tx=V.tx,ty=V.y,sp=v.spd;
 if(leave){tx=V.face>=0?WW+140:-140;if(V.x<-120||V.x>WW+120){if(!V.seen)toast(`${v.emo} ${v.name} ayrıldı. Bir dahaki sefere dokunup deftere eklemeyi unutma!`);G.vis=null;save();return;}V.leaving=1;}
 else if(v.move==='perch'){const p=visPerch();if(p){tx=p.x;ty=p.y;}}
 else if(v.move==='swim'||v.move==='deep'){if(Math.abs(V.x-V.tx)<30){V.tx=rnd(120,WW-120);if(v.move==='swim')V.ty=rnd(topY+90,floorY-170);}ty=V.ty||V.y;}
 else{if(V.wait>0){V.wait-=dt;sp=0;}else if(Math.abs(V.x-V.tx)<10){V.wait=rnd(2,6);V.tx=rnd(80,WW-80);}}
 const dx=tx-V.x,dy=ty-V.y,d=Math.hypot(dx,dy);
 if(d>2&&sp>0){const m=Math.min(d,sp*dt*(leave?2.2:1));V.x+=dx/d*m;V.y+=dy/d*m;if(Math.abs(dx)>3)V.face=dx>0?1:-1;V.ph+=dt*(v.move==='walk'?5:2.4);}
 else V.ph+=dt*.8;
 if(v.move==='swim'||v.move==='deep')V.y+=Math.sin(T*1.2)*dt*4;
}
function drawVisitor(){const V=G.vis;if(!V)return;const v=VIS_[V.id],s=VSPR[V.id];if(!v||!s||!s.ok)return;
 const k=v.len/s.ppu,n=s.n,fi=Math.floor((((V.ph%TAU)+TAU)%TAU)/TAU*n)%n;
 if(v.move==='walk'||v.move==='perch'){ctx.fillStyle='rgba(0,25,35,.25)';ctx.beginPath();ctx.ellipse(V.x,V.y+6,v.len*.4,6,0,0,TAU);ctx.fill();}
 ctx.save();ctx.translate(V.x,V.y);ctx.scale(V.face>=0?1:-1,1);ctx.drawImage(s.img,fi*s.fw,0,s.fw,s.fh,-s.ox*k,-s.oy*k,s.fw*k,s.fh*k);ctx.restore();
 if(V.id==='angler'&&NK<.01){ctx.save();ctx.globalCompositeOperation='lighter';const x=V.x+V.face*v.len*.66,y=V.y-v.len*.3,g=ctx.createRadialGradient(x,y,0,x,y,40);g.addColorStop(0,'rgba(120,255,190,.5)');g.addColorStop(1,'rgba(120,255,190,0)');ctx.fillStyle=g;ctx.fillRect(x-40,y-40,80,80);ctx.restore();}
}
function hitVisitor(x,y){const V=G.vis;if(!V)return null;const v=VIS_[V.id];return Math.abs(x-V.x)<v.len*.5&&Math.abs(y-V.y)<v.len*.38?V:null;}
function tapVisitor(){const V=G.vis,v=VIS_[V.id];
 if(!V.seen){V.seen=1;G.vbook=G.vbook||{};const first=!G.vbook[v.id];G.vbook[v.id]=(G.vbook[v.id]||0)+1;
  let g=[];if(v.gift.p){G.pearls=(G.pearls||0)+v.gift.p;g.push(`+${v.gift.p} inci`);}if(v.gift.c){G.coins+=v.gift.c;g.push(`+${v.gift.c} altın`);}
  floater(V.x,V.y-v.len*.45,g.join('  '),'#e6dcff');for(let i=0;i<24;i++)sparks.push({x:V.x+rnd(-40,40),y:V.y+rnd(-30,20),life:rnd(.5,1.1)});snd('lvl');
  toast(`${v.emo} ${v.name} ${first?'deftere eklendi':'yine geldi'}! Hediye: ${g.join(', ')}`);stat('visitor');save();updHUD();}
 selDecor=null;selected=null;const e=$('info');e.classList.remove('hidden');
 e.innerHTML=`<h3>${v.emo} ${v.name}<span class="ttag" style="--tc:#4DA3FF">Misafir</span></h3><div class="tinfo">${v.desc}</div><div class="bar">Daha ${fmtT((V.until-Date.now())/1000)} kalacak · Deftere ${(G.vbook||{})[v.id]||0}. ziyaret olarak işlendi.</div><div class="irow"><button class="btn" id="ix">Tamam</button></div>`;
 $('ix').onclick=closeInfo;}
function albDraw(pc,s,has){const w=pc.clientWidth||100,h=pc.clientHeight||70,dpr=Math.min(2,devicePixelRatio||1);pc.width=w*dpr;pc.height=h*dpr;const c=pc.getContext('2d');c.setTransform(dpr,0,0,dpr,0,0);
 if(!s||!s.ok)return;const kk=Math.min((w-8)/s.fw,(h-6)/s.fh);if(!has){c.filter='brightness(0)';c.globalAlpha=.45;}c.drawImage(s.img,0,0,s.fw,s.fh,(w-s.fw*kk)/2,(h-s.fh*kk)/2,s.fw*kk,s.fh*kk);}
function renderExtraAlbum(B){
 const L=Object.keys(LEG),nl=L.filter(k=>(G.legs||{})[k]).length;
 B.insertAdjacentHTML('beforeend',`<div class="albh"><span>🌟 Efsanevi balıklar</span><span>${nl}/${L.length}</span></div>`);
 let g=document.createElement('div');g.className='alb';B.appendChild(g);
 for(const k of L){const has=(G.legs||{})[k],sp=SP[k],card=document.createElement('div');card.className='card'+(has?'':' unk');
  card.innerHTML=`<canvas></canvas><div class="cn" style="font-size:12px">${has?LEG[k].name:'???'}</div><div class="cm" style="font-size:10.5px;line-height:1.25">${has?sp.name+' efsanesi':LEG[k].hint}</div>`;g.appendChild(card);
  const pc=card.querySelector('canvas');requestAnimationFrame(()=>albDraw(pc,sp.sprL&&sp.sprL.ok?sp.sprL:sp.spr,has));}
 const nv=VIS.filter(v=>(G.vbook||{})[v.id]).length;
 B.insertAdjacentHTML('beforeend',`<div class="albh"><span>🐾 Misafirler</span><span>${nv}/${VIS.length}</span></div>`);
 g=document.createElement('div');g.className='alb';B.appendChild(g);
 for(const v of VIS){const has=(G.vbook||{})[v.id],card=document.createElement('div');card.className='card'+(has?'':' unk');
  card.innerHTML=`<canvas></canvas><div class="cn" style="font-size:12px">${has?v.name:'???'}</div><div class="cm" style="font-size:10.5px;line-height:1.25">${has?has+' kez geldi':v.hint}</div>`;g.appendChild(card);
  const pc=card.querySelector('canvas');requestAnimationFrame(()=>albDraw(pc,VSPR[v.id],has));}
 B.insertAdjacentHTML('beforeend',`<div class="albh"><span>🐠 Türler</span><span></span></div>`);
}
function drawFishWorld(f){""")
# tıklama: önce misafir
rep("  const f=hitFish(p.x,p.y);if(f){collectFish(f);selectFish(f);return;}",
    "  if(hitVisitor(p.x,p.y)){tapVisitor();return;}\n  const f=hitFish(p.x,p.y);if(f){collectFish(f);selectFish(f);return;}")
# defter
rep("const g=document.createElement('div');g.className='alb';B.appendChild(g);\n  for(const k of keys){",
    "renderExtraAlbum(B);\n  const g=document.createElement('div');g.className='alb';B.appendChild(g);\n  for(const k of keys){")
rep("card.innerHTML=`<canvas></canvas><div class=\"cn\" style=\"font-size:12px\">${has?(rare?RARE[id]:sp.name):'???'}${rare?'<span class=\"rtag\">✨</span>':''}</div>`;",
    "card.innerHTML=`<canvas></canvas><div class=\"cn\" style=\"font-size:12px\">${has?(rare?RARE[id]:sp.name):'???'}${rare?'<span class=\"rtag\">✨</span>':''}</div>${has&&!rare&&((G.hues||{})[id]||[]).length>1?`<div class=\"cm\" style=\"font-size:10.5px\">🎨 ${(G.hues[id]).length} renk</div>`:''}`;")

# ================= bilgi paneli =================
rep("<span class=\"ttag\" style=\"--tc:${tp[1]}\">${tp[0]}</span> <small id=\"istg\"></small></h3>",
    "${f.leg?'<span class=\"rtag\" style=\"background:linear-gradient(#ffe27a,#e0a000)\">🌟 Efsanevi</span>':''}<span class=\"ttag\" style=\"--tc:${tp[1]}\">${tp[0]}</span> <small id=\"istg\"></small></h3>")
rep("${TEMPER_INFO[temperOf(f.sp)]?`<div class=\"tinfo\">${TEMPER_INFO[temperOf(f.sp)]}</div>`:''}",
    "${TEMPER_INFO[temperOf(f.sp)]?`<div class=\"tinfo\">${TEMPER_INFO[temperOf(f.sp)]}</div>`:''}<div class=\"tinfo\">${homeLine(f)}${f.leg?'':` · <span class=\"hsw\" style=\"--h:${f.hu||0}deg\"></span> Renk geni: ${hueTxt(f.hu)}`}</div>")
rep(".tinfo{", ".hsw{display:inline-block;width:11px;height:11px;border-radius:50%;vertical-align:-1px;background:conic-gradient(from 0deg,#f55,#fd5,#5f8,#5df,#86f,#f5c,#f55);filter:hue-rotate(var(--h));border:1px solid rgba(255,255,255,.6)}\n.tinfo{")
# mağaza: süsü yuva yapan türler
rep("(it.special?it.desc:shopTab==='fish'?`${fmtT(it.grow)} · satış ${it.sell}`:(it.desc||`+${it.xp} XP`));",
    "(it.special?it.desc:shopTab==='fish'?`${fmtT(it.grow)} · satış ${it.sell}`:(it.desc||`+${it.xp} XP`)+homeFans(it.id));")

# ================= ayarlar =================
rep('      <button class="row" id="huntB">',
    '      <button class="row" id="dayB"><i data-ic="star"></i><span>Gece ve gündüz<small id="dayTxt">Otomatik: telefonun saatine göre</small></span></button>\n      <button class="row" id="huntB">')
rep("$('huntB').onclick=()=>{",
    "const DAYTXT={auto:'Otomatik: telefonun saatine göre',night:'Hep gece',day:'Hep gündüz'};\nfunction updDayTxt(){$('dayTxt').textContent=DAYTXT[G.dayMode||'auto'];}\n$('dayB').onclick=()=>{const o=['auto','night','day'];G.dayMode=o[(o.indexOf(G.dayMode||'auto')+1)%3];updDayTxt();toast('🌙 Gece ve gündüz: '+DAYTXT[G.dayMode]);save();};\n$('huntB').onclick=()=>{")

# ================= kayıt =================
rep("z:+f.z.toFixed(2),seed:f.seed}))", "z:+f.z.toFixed(2),seed:f.seed,hu:f.hu||0,lg:f.leg?1:0}))")
rep("seed:(Math.random()*1e9)|0})))", "seed:(Math.random()*1e9)|0,hu:e.hu||0,lg:e.leg?1:0})))")
rep("cdShell:G.cdShell||0,noHunt:G.noHunt?1:0,", "cdShell:G.cdShell||0,noHunt:G.noHunt?1:0,vis:G.vis||null,vbook:G.vbook||{},lastVis:G.lastVis||'',legs:G.legs||{},hues:G.hues||{},dayMode:G.dayMode||'auto',")
rep("cdShell:s.cdShell||0,noHunt:!!s.noHunt,", "cdShell:s.cdShell||0,noHunt:!!s.noHunt,vis:s.vis||null,vbook:s.vbook||{},lastVis:s.lastVis||'',legs:s.legs||{},hues:s.hues||{},dayMode:s.dayMode||'auto',")
rep("seed:o.seed,rare:!!o.r,mate:o.m||0,", "seed:o.seed,rare:!!o.r,leg:!!o.lg,hu:o.hu||0,mate:o.m||0,")
rep(" muted=!!s.muted;musicOff=!!s.musicOff;seenHelp=seenHelp||!!s.seenHelp;$('huntB').classList.toggle('off',!!G.noHunt);",
    " muted=!!s.muted;musicOff=!!s.musicOff;seenHelp=seenHelp||!!s.seenHelp;$('huntB').classList.toggle('off',!!G.noHunt);updDayTxt();NK=nightK();\n setTimeout(()=>{try{if(!G.vis&&s.last&&Date.now()-s.last>20*60e3&&Math.random()<.4){updBeauty();if(spawnVisitor(true)){G.vis.x=G.vis.tx;toast('👀 Sen yokken akvaryumuna bir misafir geldi! Bul ve dokun.');}}}catch(_){}} ,1800);")

# ================= yardım =================
rep("      <p><b>Toz ve fırça:</b>",
    "      <p><b>Yuvalar:</b> Bazı balıklar belirli süsleri yuva yapar: palyaço anemonu, neon ve beta yosunları, deniz atı dev yosunu sever. Yuvası olan balık %15 fazla kazandırır, tehlikede yuvasına saklanır.</p>\n      <p><b>Gece ve gündüz:</b> Akvaryum telefonunun saatine göre kararır. Gece balıklar uyur, denizanası ve kristal parlar. Ayarlardan değiştirilebilir.</p>\n      <p><b>Misafirler:</b> Doğru süsleri koyarsan akvaryuma kaplumbağa, ahtapot, yengeç gibi misafirler gelir. Dokun, deftere işlensin ve hediyeni al.</p>\n      <p><b>Renk genleri ve efsaneler:</b> Yavrular anne babasının rengini karıştırarak alır, bazen yeni renk çıkar. Gizli koşullarda 7 Efsane Balık doğabilir; ipuçları defterde.</p>\n      <p><b>Toz ve fırça:</b>")

rep(" update(dt);render();\n if(mode==='clean')", " try{update(dt);render();}catch(err){if(!window.__ferr){window.__ferr=1;console.error(err);}}\n if(mode==='clean')")

open(P, 'w', encoding='utf-8').write(s)
print('v9 yaması tamam', len(s))
