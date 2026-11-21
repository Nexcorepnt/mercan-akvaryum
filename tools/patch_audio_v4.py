"""v4: başarım kutusu gizleme düzeltmesi + yeni ses motoru (müzik, ortam sesi, efektler, mobil kilit açma)."""
import os
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src', 'index.template.html')
s = open(P, encoding='utf-8').read()

def R(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:90]); s = s.replace(a, b)

# --- sarı boş kutu: gizliyken tamamen görünmez olsun
R("transition:transform .45s cubic-bezier(.2,1.4,.4,1);text-align:center;pointer-events:none;max-width:90%}\n#achBan.show{transform:translate(-50%,0)}",
  "transition:transform .45s cubic-bezier(.2,1.4,.4,1),opacity .3s,visibility 0s .45s;text-align:center;pointer-events:none;max-width:90%;opacity:0;visibility:hidden}\n"
  "#achBan.show{transform:translate(-50%,0);opacity:1;visibility:visible;transition:transform .45s cubic-bezier(.2,1.4,.4,1),opacity .2s,visibility 0s}")

# --- müzik düğmesi
R('<button class="rbtn" id="snd" title="Ses">🔊</button>',
  '<button class="rbtn" id="mus" title="Müzik">🎵</button>\n  <button class="rbtn" id="snd" title="Ses efektleri">🔊</button>')
R(".rbtn{position:relative}", ".rbtn{position:relative}\n.rbtn.off{filter:grayscale(1);opacity:.65}")

# --- ses motoru
start = s.index("let AC=null;")
end = s.index("function snd(k){")
ENGINE = r"""/* ================= SES MOTORU ================= */
let AC=null,MASTER=null,SFX=null,MUS=null,AMB=null,REV=null,audioOn=false,musicOff=false;
const SILENT_WAV='data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAIA+AAACABAAZGF0YQAAAAA=';
let silentEl=null;
function buildAudio(){
 AC=new(window.AudioContext||window.webkitAudioContext)();
 const comp=AC.createDynamicsCompressor();comp.threshold.value=-14;comp.ratio.value=4;comp.connect(AC.destination);
 MASTER=AC.createGain();MASTER.gain.value=.95;MASTER.connect(comp);
 SFX=AC.createGain();SFX.gain.value=1.6;SFX.connect(MASTER);
 // su altı yankısı
 REV=AC.createConvolver();const len=AC.sampleRate*2.6,ir=AC.createBuffer(2,len,AC.sampleRate);
 for(let ch=0;ch<2;ch++){const d=ir.getChannelData(ch);for(let i=0;i<len;i++)d[i]=(Math.random()*2-1)*Math.pow(1-i/len,2.4);}
 REV.buffer=ir;const revG=AC.createGain();revG.gain.value=.55;REV.connect(revG);revG.connect(MASTER);
 MUS=AC.createGain();MUS.gain.value=musicOff?0:.32;MUS.connect(MASTER);MUS.connect(REV);
 AMB=AC.createGain();AMB.gain.value=muted?0:.22;AMB.connect(MASTER);
 startAmbient();startMusic();
}
function unlockAudio(){
 try{
  if(navigator.audioSession)try{navigator.audioSession.type='playback';}catch(_){}
  if(!AC)buildAudio();
  if(AC.state!=='running')AC.resume().then(()=>{audioOn=true;}).catch(()=>{});else audioOn=true;
  // iPhone sessiz modunda da çalabilmesi için sessiz bir medya öğesi oynat
  if(!silentEl){silentEl=new Audio(SILENT_WAV);silentEl.loop=true;silentEl.volume=.01;silentEl.setAttribute('playsinline','');}
  silentEl.play().catch(()=>{});
  // boş tampon çal (eski iOS kilidi)
  const b=AC.createBuffer(1,1,22050),src=AC.createBufferSource();src.buffer=b;src.connect(AC.destination);src.start(0);
 }catch(e){}
}
['pointerup','touchend','click','keydown'].forEach(ev=>document.addEventListener(ev,unlockAudio,{capture:true,passive:true}));
function tone(f,st,dur,type,vol,f2){
 if(muted||!AC||AC.state!=='running')return;
 const t=AC.currentTime+st,o=AC.createOscillator(),g=AC.createGain();o.type=type;o.frequency.setValueAtTime(f,t);
 if(f2)o.frequency.exponentialRampToValueAtTime(f2,t+dur);
 g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(vol,t+.01);g.gain.exponentialRampToValueAtTime(.0005,t+dur);
 o.connect(g);g.connect(SFX);if(type==='sine'||type==='triangle'){const s2=AC.createGain();s2.gain.value=.25;g.connect(s2);s2.connect(REV);}
 o.start(t);o.stop(t+dur+.05);
}
/* --- ortam: su altı uğultusu + rastgele kabarcık sesleri --- */
function startAmbient(){
 const len=AC.sampleRate*4,buf=AC.createBuffer(1,len,AC.sampleRate),d=buf.getChannelData(0);let last=0;
 for(let i=0;i<len;i++){last=(last+.02*(Math.random()*2-1))/1.02;d[i]=last*3.2;}
 const src=AC.createBufferSource();src.buffer=buf;src.loop=true;
 const lp=AC.createBiquadFilter();lp.type='lowpass';lp.frequency.value=420;lp.Q.value=.7;
 const wave=AC.createGain();wave.gain.value=.7;const lfo=AC.createOscillator(),lfoG=AC.createGain();lfo.frequency.value=.09;lfoG.gain.value=.3;
 lfo.connect(lfoG);lfoG.connect(wave.gain);src.connect(lp);lp.connect(wave);wave.connect(AMB);src.start();lfo.start();
 (function bub(){setTimeout(()=>{if(AC&&AC.state==='running'&&!muted&&!document.hidden){const t=AC.currentTime,n=1+((Math.random()*3)|0);
   for(let i=0;i<n;i++){const o=AC.createOscillator(),g=AC.createGain(),f=rnd(380,900),tt=t+i*rnd(.05,.14);o.type='sine';o.frequency.setValueAtTime(f,tt);o.frequency.exponentialRampToValueAtTime(f*rnd(1.8,2.6),tt+.07);
    g.gain.setValueAtTime(0,tt);g.gain.linearRampToValueAtTime(rnd(.05,.12),tt+.008);g.gain.exponentialRampToValueAtTime(.0005,tt+.09);o.connect(g);g.connect(AMB);const r=AC.createGain();r.gain.value=.5;g.connect(r);r.connect(REV);o.start(tt);o.stop(tt+.12);}}
  bub();},rnd(900,3200));})();
}
/* --- arka plan müziği: yumuşak, su altı havasında prosedürel parça --- */
const NOTE=n=>440*Math.pow(2,(n-69)/12);
const CHORDS=[[48,55,64,71],[45,52,60,67],[41,48,57,64],[43,50,59,62],[48,55,64,67],[45,52,60,64],[41,48,55,64],[43,50,55,62]];
const SCALE=[72,74,76,79,81,84,86,88];
let musStep=0,musNext=0;
function padChord(ch,t,dur){
 const f=AC.createBiquadFilter();f.type='lowpass';f.frequency.setValueAtTime(700,t);f.frequency.linearRampToValueAtTime(1300,t+dur*.5);f.frequency.linearRampToValueAtTime(600,t+dur);
 const g=AC.createGain();g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(.09,t+1.2);g.gain.setValueAtTime(.09,t+dur-1.2);g.gain.linearRampToValueAtTime(0,t+dur+.4);
 f.connect(g);g.connect(MUS);
 for(const n of ch.slice(1)){for(const det of [-6,6]){const o=AC.createOscillator();o.type='triangle';o.frequency.value=NOTE(n);o.detune.value=det;o.connect(f);o.start(t);o.stop(t+dur+.5);}}
 const b=AC.createOscillator(),bg=AC.createGain();b.type='sine';b.frequency.value=NOTE(ch[0]-12);bg.gain.setValueAtTime(0,t);bg.gain.linearRampToValueAtTime(.16,t+.3);bg.gain.exponentialRampToValueAtTime(.01,t+dur);b.connect(bg);bg.connect(MUS);b.start(t);b.stop(t+dur+.1);
}
function pluck(n,t,v){
 const o=AC.createOscillator(),o2=AC.createOscillator(),g=AC.createGain();o.type='sine';o2.type='triangle';o.frequency.value=NOTE(n);o2.frequency.value=NOTE(n)*2.01;
 const g2=AC.createGain();g2.gain.value=.18;o2.connect(g2);g2.connect(g);o.connect(g);
 g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(v,t+.006);g.gain.exponentialRampToValueAtTime(.0008,t+1.6);g.connect(MUS);
 o.start(t);o2.start(t);o.stop(t+1.7);o2.stop(t+1.7);
}
function startMusic(){
 const beat=60/68/2; // sekizlik
 musNext=AC.currentTime+.3;
 setInterval(()=>{
  if(!AC||AC.state!=='running'||document.hidden){if(AC)musNext=Math.max(musNext,AC.currentTime+.2);return;}
  while(musNext<AC.currentTime+.6){
   const bar=Math.floor(musStep/16),ch=CHORDS[bar%CHORDS.length],pos=musStep%16;
   if(!musicOff){
    if(pos===0)padChord(ch,musNext,beat*16);
    const r=Math.random();
    if(pos%2===0?r<.55:r<.18){const pool=SCALE.filter(n=>ch.some(c=>(n-c)%12===0)||Math.random()<.25);pluck(pool[(Math.random()*pool.length)|0],musNext,pos%4===0?.11:.07);}
    if(pos===12&&Math.random()<.4)pluck(SCALE[(Math.random()*SCALE.length)|0]+12,musNext,.04);
   }
   musStep++;musNext+=beat;
  }
 },120);
}
function setMusic(off){musicOff=off;if(MUS)MUS.gain.setTargetAtTime(off?0:.32,AC.currentTime,.4);$('mus').classList.toggle('off',off);}
function setMuted(m){muted=m;if(AMB)AMB.gain.setTargetAtTime(m?0:.22,AC.currentTime,.3);$('snd').textContent=m?'🔇':'🔊';$('snd').classList.toggle('off',m);}
document.addEventListener('visibilitychange',()=>{if(!AC)return;if(document.hidden)AC.suspend().catch(()=>{});else if(audioOn)AC.resume().catch(()=>{});});
"""
s = s[:start]+ENGINE+s[end:]

R("$('snd').onclick=()=>{muted=!muted;$('snd').textContent=muted?'🔇':'🔊';save();};",
  "$('snd').onclick=()=>{unlockAudio();setMuted(!muted);if(!muted)snd('blip');save();};\n"
  "$('mus').onclick=()=>{unlockAudio();setMusic(!musicOff);toast(musicOff?'🎵 Müzik kapalı':'🎵 Müzik açık');save();};")
R("  dirt:+(1-clean).toFixed(3),last:Date.now(),muted,seenHelp,", "  dirt:+(1-clean).toFixed(3),last:Date.now(),muted,musicOff,seenHelp,")
R(" muted=!!s.muted;seenHelp=seenHelp||!!s.seenHelp;", " muted=!!s.muted;musicOff=!!s.musicOff;seenHelp=seenHelp||!!s.seenHelp;")
R(" $('snd').textContent=muted?'🔇':'🔊';updHUD();", " setMuted(muted);setMusic(musicOff);updHUD();")
R(" $('snd').textContent=muted?'🔇':'🔊';\n", " setMuted(muted);setMusic(musicOff);\n")
open(P, 'w', encoding='utf-8').write(s)
print('ok')
