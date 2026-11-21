"""v8: ince kum, 3D bitki süsleri (animasyonlu sprite), süslerin üstünde su ışığı, toz bulutu ve fırça."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'src', 'index.template.html')
s = open(P, encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    assert s.count(a) >= 1, 'bulunamadı: ' + a[:90]
    s = s.replace(a, b, n)

# ---------- maske sprite'ları ----------
rep("const DSPR={};", "const DSPR={},DMASK={};")
rep(" if(id.startsWith('d_'))DSPR[id.slice(2)]=mkSpr(m);",
    " if(id.startsWith('d_'))DSPR[id.slice(2)]=mkSpr(m);\n else if(id.startsWith('m_'))DMASK[id.slice(2)]=mkSpr(m);")

# ---------- kare seçimi: bitkiler sürekli dalgalanır ----------
rep("function decorPos(d){",
"""const ANIM={weed:.2,redweed:.24,kelp:.14,anem:.3,fan:.18};
function decorFrame(d,t,s_){if(s_.n<=1)return 0;const a=ANIM[d.t];if(a)return Math.floor((((t*a+(d.ph||0)/TAU)%1)+1)%1*s_.n)%s_.n;return Math.min(s_.n-1,Math.round((d.op||0)*(s_.n-1)));}
function decorPos(d){""")
rep("  const k=100/ds_.ppu;let fr=0;\n  if(ds_.n>1)fr=Math.min(ds_.n-1,Math.round((d.op||0)*(ds_.n-1)));",
    "  const k=100/ds_.ppu,fr=decorFrame(d,t,ds_);")
# kristal parıltısı (sprite olunca da)
rep("  if(d.t==='volcano'||(d.t==='chest'&&(d.op||0)>.05)){",
    "  if(d.t==='crystal'){c.shadowBlur=0;const p=.6+.4*Math.sin(t*1.6+(d.ph||0)),g=c.createRadialGradient(0,-50,4,0,-50,80);g.addColorStop(0,`rgba(170,215,255,${.38*p})`);g.addColorStop(1,'rgba(170,215,255,0)');c.globalCompositeOperation='lighter';c.fillStyle=g;c.fillRect(-80,-130,160,140);c.globalCompositeOperation='source-over';}\n  if(d.t==='volcano'||(d.t==='chest'&&(d.op||0)>.05)){")

# ---------- süs ışığı + toz ----------
rep("function drawFishWorld(f){",
"""/* süslerin üst yüzeylerinde hareketli su ışığı: maskeler arkadan öne, öndeki süs arkadakini örter */
let litCv=null,litCx=null,litPat=null,caCv=null,caCx=null;
function drawDecorLight(ds){
 const sc=.5,w=Math.ceil(WW*sc),h=Math.ceil(WH*sc);
 if(!litCv||litCv.width!==w||litCv.height!==h){litCv=document.createElement('canvas');litCv.width=w;litCv.height=h;litCx=litCv.getContext('2d');litPat=null;}
 const c=litCx;c.setTransform(1,0,0,1,0,0);c.globalCompositeOperation='source-over';c.globalAlpha=1;c.clearRect(0,0,w,h);c.setTransform(sc,0,0,sc,0,0);
 let any=false;
 for(const d of ds){const s_=DSPR[d.t],m_=DMASK[d.t];if(!s_||!s_.ok)continue;
  const k=100/s_.ppu*d.s,fr=decorFrame(d,T,s_),x=d.x-s_.ox*k,y=d.y-s_.oy*k,W_=s_.fw*k,H_=s_.fh*k;
  c.globalCompositeOperation='destination-out';c.drawImage(s_.img,fr*s_.fw,0,s_.fw,s_.fh,x,y,W_,H_);
  if(m_&&m_.ok){c.globalCompositeOperation='source-over';c.drawImage(m_.img,fr*m_.fw,0,m_.fw,m_.fh,x,y,W_,H_);any=true;}}
 if(!any)return;
 if(!caCv||caCv.width!==w||caCv.height!==h){caCv=document.createElement('canvas');caCv.width=w;caCv.height=h;caCx=caCv.getContext('2d');litPat=null;}
 const cc=caCx;if(!litPat)litPat=cc.createPattern(CAUSTIC,'repeat');if(!litPat.setTransform)return;
 cc.setTransform(1,0,0,1,0,0);cc.globalCompositeOperation='source-over';cc.globalAlpha=1;cc.clearRect(0,0,w,h);cc.setTransform(sc,0,0,sc,0,0);cc.fillStyle=litPat;
 litPat.setTransform(new DOMMatrix().translateSelf(T*9,floorY+T*2).scaleSelf(1.3,.75));cc.fillRect(0,0,WW,WH);
 cc.globalCompositeOperation='lighter';litPat.setTransform(new DOMMatrix().translateSelf(-T*6,floorY-T*3).scaleSelf(1.05,.6));cc.globalAlpha=.7;cc.fillRect(0,0,WW,WH);
 c.setTransform(1,0,0,1,0,0);c.globalCompositeOperation='source-in';c.drawImage(caCv,0,0);
 ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=(THM().glow?.38:.55);ctx.drawImage(litCv,0,0,WW,WH);ctx.restore();
}
/* toz: süs kuma konunca kalkar, yukarı bakan yüzeylere çöker, fırçayla temizlenir */
let dusts=[];
const DUSTPAT=(()=>{const N=96,c=document.createElement('canvas');c.width=c.height=N;const x=c.getContext('2d');x.fillStyle='rgba(214,190,142,.96)';x.fillRect(0,0,N,N);
 const r=mulberry(77);for(let i=0;i<520;i++){const v=r();x.fillStyle=v<.45?'rgba(245,228,190,.9)':v<.8?'rgba(176,150,105,.85)':'rgba(120,104,82,.8)';const s=.6+r()*1.6;x.fillRect(r()*N,r()*N,s,s);}return c;})();
let dustPatObj=null,dustCv=null,dustCx=null;
function dustCanvas(w,h){if(!dustCv||dustCv.width<w||dustCv.height<h){dustCv=document.createElement('canvas');dustCv.width=Math.max(w,dustCv?dustCv.width:0);dustCv.height=Math.max(h,dustCv?dustCv.height:0);dustCx=dustCv.getContext('2d');dustPatObj=dustCx.createPattern(DUSTPAT,'repeat');}return dustCx;}
function drawDust(d){
 if(!(d.dust>.02))return;const s_=DSPR[d.t],m_=DMASK[d.t];if(!s_||!s_.ok||!m_||!m_.ok)return;
 const k=100/s_.ppu*d.s,fr=decorFrame(d,T,s_),W_=Math.ceil(s_.fw*k),H_=Math.ceil(s_.fh*k),c=dustCanvas(W_,H_);
 c.globalCompositeOperation='source-over';c.globalAlpha=1;c.clearRect(0,0,dustCv.width,dustCv.height);
 c.drawImage(m_.img,fr*m_.fw,0,m_.fw,m_.fh,0,0,W_,H_);
 c.globalCompositeOperation='destination-in';c.drawImage(m_.img,fr*m_.fw,0,m_.fw,m_.fh,0,0,W_,H_);
 c.globalCompositeOperation='source-in';c.fillStyle=dustPatObj;c.fillRect(0,0,W_,H_);
 ctx.save();ctx.globalAlpha=Math.min(1,d.dust*1.15);ctx.drawImage(dustCv,0,0,W_,H_,d.x-s_.ox*k,d.y-s_.oy*k,W_,H_);ctx.restore();
}
function dustPuff(x,y,n,spread,up,big){
 for(let i=0;i<n;i++){const a=Math.random()*Math.PI,sp=rnd(.3,1)*spread;dusts.push({x:x+rnd(-12,12),y:y+rnd(-4,4),vx:Math.cos(a)*sp*(Math.random()<.5?-1:1),vy:-rnd(.3,1)*up,r:rnd(7,big?24:11),life:rnd(2,3.8),max:3.8,a:rnd(.42,.72)});}
}
function raiseDust(d){
 const def=DC_[d.t],w=(def?def.w:80)*d.s;
 dustPuff(d.x,d.y,48,w*1.1,85,true);
 d.dust=d.dust||0;d.dustT=.9;d.dustDelay=1.2;
 for(const o of G.decor){if(o===d)continue;const dd=Math.abs(o.x-d.x);if(dd<w*.5+170){o.dustT=Math.min(1,Math.max(o.dustT||o.dust||0,(o.dust||0)+.45*(1-dd/(w*.5+170))));o.dustDelay=1.6;}}
 dustHintAt=T+3;
}
let dustHintAt=0,dustHinted=0;
function updDust(dt){
 for(const p of dusts){p.life-=dt;p.x+=p.vx*dt;p.y+=p.vy*dt;p.vx*=Math.pow(.25,dt);p.vy=p.vy*Math.pow(.3,dt)+dt*14;p.r+=dt*6;}
 dusts=dusts.filter(p=>p.life>0);if(dusts.length>260)dusts.splice(0,dusts.length-260);
 for(const d of G.decor){if(d.dustT===undefined)continue;if(d.dustDelay>0){d.dustDelay-=dt;continue;}
  const cur=d.dust||0;if(cur<d.dustT){d.dust=Math.min(d.dustT,cur+dt*.45);}else d.dustT=undefined;}
 if(dustHintAt&&T>dustHintAt){dustHintAt=0;if(dustHinted<3&&G.decor.some(d=>(d.dust||0)>.3)){dustHinted++;toast('Süslerin üstüne kum tozu çöktü: Temizle modunda fırçayla sil, güzellik puanı geri gelsin');}}
}
function drawDusts(){
 for(const p of dusts){const a=p.a*Math.min(1,p.life/1.2)*Math.min(1,(p.max-p.life)*3+.3);if(a<=.01)continue;
  const g=ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,p.r);g.addColorStop(0,`rgba(222,200,155,${a})`);g.addColorStop(1,'rgba(222,200,155,0)');ctx.fillStyle=g;ctx.fillRect(p.x-p.r,p.y-p.r,p.r*2,p.r*2);}
}
let brushAcc=0;
function brushDecor(d,x,y,amt){
 const b=d.dust||0;d.dust=Math.max(0,b-amt*.13);d.dustT=undefined;const rem=b-d.dust;
 if(rem>.002&&Math.random()<.5)dustPuff(x,y,2,40,30,false);
 if(Math.random()<.25)snd('scrub');
 brushAcc+=rem;if(brushAcc>=.34){brushAcc-=.34;G.xp+=1;G.coins+=1;floater(x,y-36,'+1 XP  +1','#e9d7a8');checkLevel();}
 if(b>0&&d.dust<=0.02){d.dust=0;floater(d.x,d.y-70*d.s,'Tertemiz!','#c6ff8f');snd('blip');updBeauty();save();}
}
function hitDusty(x,y){const s=[...G.decor].sort((a,b)=>b.y-a.y);for(const d of s){if(!((d.dust||0)>.02))continue;const def=DC_[d.t];if(Math.abs(x-d.x)<def.w*d.s/2&&y<d.y+10&&y>d.y-def.h*d.s)return d;}return null;}
function cleanAt(x,y,amt){const d=hitDusty(x,y);if(d)brushDecor(d,x,y,amt);else scrub(x,y,amt);}
function drawBrush(x,y){
 ctx.save();ctx.translate(x,y);ctx.rotate(-.5+Math.sin(T*22)*(pointer.down?.16:0));ctx.scale(1.5,1.5);
 ctx.fillStyle='#8a5a2b';rr(ctx,-4,-46,8,30,3);ctx.fill();ctx.fillStyle='#c7c9cc';rr(ctx,-7,-18,14,7,2);ctx.fill();
 const g=ctx.createLinearGradient(0,-12,0,6);g.addColorStop(0,'#f2dfa6');g.addColorStop(1,'#c9a565');ctx.fillStyle=g;ctx.beginPath();ctx.moveTo(-8,-11);ctx.lineTo(8,-11);ctx.lineTo(10,6);ctx.lineTo(-10,6);ctx.closePath();ctx.fill();
 ctx.strokeStyle='rgba(120,90,40,.5)';ctx.lineWidth=.8;for(let i=-8;i<=8;i+=2.5){ctx.beginPath();ctx.moveTo(i*.85,-10);ctx.lineTo(i,6);ctx.stroke();}
 ctx.restore();
}
function drawFishWorld(f){""")

# render döngüsü
rep(" drawMoundsBack(ds);\n for(const d of ds){drawDecorAt(ctx,d,T,d.x,d.y,d.s);drawLip(d);}",
    " drawMoundsBack(ds);\n for(const d of ds){drawDecorAt(ctx,d,T,d.x,d.y,d.s);drawDust(d);drawLip(d);}\n drawDecorLight(ds);\n drawDusts();")
rep(" if(mode==='clean'&&(pointer.in||pointer.down))drawSponge(pointer.x,pointer.y);",
    " if(mode==='clean'&&(pointer.in||pointer.down)){const hd=hitDusty(pointer.x,pointer.y);if(hd)drawBrush(pointer.x,pointer.y);else drawSponge(pointer.x,pointer.y);}")
rep(" else if(mode==='clean')scrub(p.x,p.y,.25);", " else if(mode==='clean')cleanAt(p.x,p.y,.25);")
rep(" if(mode==='clean')scrub(p.x,p.y,Math.min(.55,dist/70));", " if(mode==='clean')cleanAt(p.x,p.y,Math.min(.55,dist/70));")
rep(" updHunt(dt);\n", " updHunt(dt);\n updDust(dt);\n")

# yerleştirince toz
rep("G.decor.push(d);decorPos(d);\n floater(d.x,d.y-60,", "G.decor.push(d);decorPos(d);raiseDust(d);\n floater(d.x,d.y-60,")
# taşıyınca da biraz toz
rep("const up=()=>{pointer.down=false;if(dragging){const d=dragging;dragging=null;",
    "const up=()=>{pointer.down=false;if(dragging){const d=dragging;dragging=null;if(dragMoved>=30){dustPuff(d.x,d.y,14,60,45,false);d.dustT=Math.min(1,(d.dust||0)+.25);d.dustDelay=.8;}")

# vatoz kumu eşeler
rep(" if(food&&Math.abs(food.x-f.x)<14+12*sz&&Math.abs(food.y-f.y)<70){food.eaten=true;feedFish(f);}",
    " if(food&&Math.abs(food.x-f.x)<14+12*sz&&Math.abs(food.y-f.y)<70){food.eaten=true;feedFish(f);}\n if(sp.id==='ray'&&spd>10){f.stir=(f.stir||0)+dt;if(f.stir>.5){f.stir=0;dustPuff(f.x-f.face*sp.len*.25*sz,f.y+8,2,30,22,false);for(const o of G.decor)if(Math.abs(o.x-f.x)<70&&Math.random()<.3){o.dustT=Math.min(1,(o.dust||0)+.04);}}}")

# güzellik: tozlu süs yarı puan
rep("for(const d of G.decor){const def=DC_[d.t];if(def)b+=decorBeauty(def);}",
    "for(const d of G.decor){const def=DC_[d.t];if(def)b+=decorBeauty(def)*(1-.5*Math.min(1,d.dust||0));}")

# kayıt
rep("decor:G.decor.map(d=>({t:d.t,xf:+d.xf.toFixed(4),dy:+d.dy.toFixed(1),seed:d.seed})),",
    "decor:G.decor.map(d=>({t:d.t,xf:+d.xf.toFixed(4),dy:+d.dy.toFixed(1),seed:d.seed,du:+Math.max(d.dust||0,d.dustT||0).toFixed(2)})),")
rep("G.decor=(s.decor||[]).filter(o=>DC_[o.t]).map(o=>prepDecor({t:o.t,xf:o.xf,dy:o.dy,seed:o.seed}));",
    "G.decor=(s.decor||[]).filter(o=>DC_[o.t]).map(o=>{const d=prepDecor({t:o.t,xf:o.xf,dy:o.dy,seed:o.seed});d.dust=o.du||0;return d;});")

# süs bilgi paneli
rep("<div class=\"bar\">${INTER[d.t]?'Dokun: açılır. ':''}Taşımak için sürükle. Yakındaki süslerle kumla birleşir.</div>",
    "<div class=\"bar\">${INTER[d.t]?'Dokun: açılır. ':''}Taşımak için sürükle. Yakındaki süslerle kumla birleşir.${(d.dust||0)>.05?` <b style=\"color:#e9d7a8\">Tozlu (%${Math.round(d.dust*100)}): Temizle modunda fırçala.</b>`:''}</div>")

# yardım
rep("      <p><b>Hareketli süsler:</b>",
    "      <p><b>Toz ve fırça:</b> Kuma yeni süs koyunca toz kalkar ve süslerin üstüne çöker. Tozlu süs yarım güzellik puanı verir. Temizle modunda süsün üstünde fırça çıkar; sürterek tozu al.</p>\n      <p><b>Hareketli süsler:</b>")

open(P, 'w', encoding='utf-8').write(s)
print('v8 yaması tamam', len(s))
