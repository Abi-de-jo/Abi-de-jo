<div align="center">

<!-- â•â•â•â•â•â•â•â•â•â•â• ANIMATED PAC-MAN EATING GHOSTS â•â•â•â•â•â•â•â•â•â•â• -->

<style>
.pac-scene {
  position: relative;
  width: 100%;
  max-width: 760px;
  height: 300px;
  background: radial-gradient(ellipse at center, #050509 0%, #000 100%);
  border: 2px solid #1e3a8a;
  border-radius: 14px;
  margin: 16px auto;
  overflow: hidden;
  box-shadow: 0 0 30px rgba(168, 85, 247, 0.35), inset 0 0 60px rgba(30, 58, 138, 0.2);
  font-family: 'Courier New', 'Consolas', monospace;
}

/* â”€â”€â”€ BACKGROUND NAME â€” "Codebyabi" reveals as ghosts are eaten â”€â”€â”€ */
.pac-name {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  font-family: 'Courier New', 'Consolas', monospace;
  font-size: 56px;
  font-weight: 900;
  letter-spacing: 6px;
  color: #fde047;
  text-shadow: 0 0 30px #fde047, 0 0 60px rgba(253, 224, 71, 0.5);
  z-index: 0;
  pointer-events: none;
  white-space: nowrap;
  opacity: 0.06;
  animation: name-reveal 10s linear infinite;
}
@keyframes name-reveal {
  0%   { opacity: 0.06; transform: translate(-50%, -50%) scale(1); }
  12%  { opacity: 0.06; }                                                    /* before eat 1 */
  13%  { opacity: 0.4;  transform: translate(-50%, -50%) scale(1.02); }       /* eat 1 */
  24%  { opacity: 0.4; }
  25%  { opacity: 0.6;  transform: translate(-50%, -50%) scale(1.05); }       /* eat 2 */
  36%  { opacity: 0.6; }
  37%  { opacity: 0.8;  transform: translate(-50%, -50%) scale(1.08); }       /* eat 3 */
  49%  { opacity: 0.8; }
  50%  { opacity: 1.0;  transform: translate(-50%, -50%) scale(1.18); }       /* eat 4 - PEAK */
  85%  { opacity: 1.0;  transform: translate(-50%, -50%) scale(1.15); }       /* hold */
  95%  { opacity: 0.4;  transform: translate(-50%, -50%) scale(1.0); }
  100% { opacity: 0.06; transform: translate(-50%, -50%) scale(1); }
}

/* â”€â”€â”€ HUD â”€â”€â”€ */
.pac-hud {
  position: absolute; top: 0; left: 0; right: 0;
  height: 30px;
  background: linear-gradient(180deg, #0a0a0f 0%, #050509 100%);
  border-bottom: 1px solid #1e3a8a;
  display: flex; justify-content: space-between; align-items: center;
  padding: 0 16px; font-size: 12px; letter-spacing: 2px;
  z-index: 10;
}
.pac-hud-score { color: #22d3ee; }
.pac-hud-score b { color: #fde047; font-size: 14px; }
.pac-hud-title { color: #a855f7; font-weight: bold; }
.pac-hud-lives  { color: #fde047; }

/* â”€â”€â”€ Maze walls â”€â”€â”€ */
.pac-wall {
  position: absolute;
  background: linear-gradient(180deg, #3b82f6 0%, #1e3a8a 100%);
  box-shadow: 0 0 8px #3b82f6;
  border-radius: 2px;
  z-index: 2;
}
.mh { height: 4px; }
.mv { width: 4px; }

/* â”€â”€â”€ Pac-Man â€” glides from left to right across ghosts â”€â”€â”€ */
@keyframes pm-glide {
  0%   { left: 5%;  transform: scaleX(1); }
  50%  { left: 80%; transform: scaleX(1); }
  85%  { left: 80%; transform: scaleX(1); }
  92%  { left: 80%; transform: scaleX(1); opacity: 1; }
  95%  { left: 80%; transform: scaleX(1); opacity: 0; }
  100% { left: 5%;  transform: scaleX(1); opacity: 0; }
}
@keyframes pm-chomp {
  0%, 100% { clip-path: polygon(50% 50%, 100% 8%, 100% 92%); }
  50%      { clip-path: polygon(50% 50%, 100% 50%, 100% 50%); }
}
@keyframes pm-bob {
  0%, 100% { bottom: 50px; }
  50%      { bottom: 56px; }
}
@keyframes pm-burst {
  0%, 12%   { filter: drop-shadow(0 0 0 transparent); }
  12.5%     { filter: drop-shadow(0 0 24px #fde047) drop-shadow(0 0 48px #fde047); }
  13%       { filter: drop-shadow(0 0 0 transparent); }
  24%       { filter: drop-shadow(0 0 0 transparent); }
  24.5%     { filter: drop-shadow(0 0 24px #fde047) drop-shadow(0 0 48px #fde047); }
  25%       { filter: drop-shadow(0 0 0 transparent); }
  36%       { filter: drop-shadow(0 0 0 transparent); }
  36.5%     { filter: drop-shadow(0 0 24px #fde047) drop-shadow(0 0 48px #fde047); }
  37%       { filter: drop-shadow(0 0 0 transparent); }
  49%       { filter: drop-shadow(0 0 0 transparent); }
  50%       { filter: drop-shadow(0 0 30px #fde047) drop-shadow(0 0 60px #fde047) drop-shadow(0 0 90px #fde047); }
  52%       { filter: drop-shadow(0 0 0 transparent); }
  100%      { filter: drop-shadow(0 0 0 transparent); }
}
.pac-pm {
  position: absolute;
  width: 40px; height: 40px;
  background: #fde047;
  border-radius: 50%;
  box-shadow: 0 0 20px #fde047, 0 0 40px rgba(253, 224, 71, 0.4);
  z-index: 6;
  animation:
    pm-glide 10s linear infinite,
    pm-bob 0.6s ease-in-out infinite,
    pm-burst 10s linear infinite;
}
.pac-pm::after {
  content: ''; position: absolute; inset: 0;
  background: #fde047;
  border-radius: 50%;
  animation: pm-chomp 0.25s linear infinite;
}
.pac-pm-eye {
  position: absolute;
  width: 5px; height: 5px;
  background: #000;
  border-radius: 50%;
  top: 8px;
  z-index: 7;
}

/* â”€â”€â”€ Ghosts â€” wrapper handles position+hover, inner handles eat â”€â”€â”€ */
.ghost-wrap {
  position: absolute;
  z-index: 4;
  display: inline-block;
}
.gw-1 { left: 24%; top: 100px; animation: hover-up 1.5s ease-in-out infinite; }
.gw-2 { left: 43%; top: 180px; animation: hover-side 2s ease-in-out infinite; }
.gw-3 { left: 61%; top: 130px; animation: hover-float 2.5s ease-in-out infinite; }
.gw-4 { left: 80%; top: 200px; animation: hover-tilt 1.8s ease-in-out infinite; }

@keyframes hover-up   { 0%,100%{transform:translateY(0);}          50%{transform:translateY(-8px);} }
@keyframes hover-side { 0%,100%{transform:translate(0,0);}        50%{transform:translate(12px,-6px);} }
@keyframes hover-float{ 0%,100%{transform:translate(0,0);} 33%{transform:translate(-10px,-10px);} 66%{transform:translate(8px,-4px);} }
@keyframes hover-tilt { 0%,100%{transform:translateY(0) rotate(-3deg);} 50%{transform:translateY(-12px) rotate(3deg);} }

.pac-ghost {
  position: relative;
  display: inline-block;
  font-size: 30px;
  filter: drop-shadow(0 0 8px currentColor);
  transform-origin: 50% 50%;
}
.g-1 { color: #ef4444; animation: eat-1 10s linear infinite; }
.g-2 { color: #f472b6; animation: eat-2 10s linear infinite; }
.g-3 { color: #22d3ee; animation: eat-3 10s linear infinite; }
.g-4 { color: #fb923c; animation: eat-4 10s linear infinite; }

/* Each ghost's eat moment matches Pac-Man reaching its x position:
   Pac-Man at left:5% (t=0) â†’ left:80% (t=5s), linear.
   Ghost 1 at 24% â†’ caught at t=1.25s (12.5%)
   Ghost 2 at 43% â†’ caught at t=2.5s  (25%)
   Ghost 3 at 61% â†’ caught at t=3.75s (37.5%)
   Ghost 4 at 80% â†’ caught at t=5s    (50%)  */
@keyframes eat-1 {
  0%, 12%   { opacity: 1; transform: scale(1);   filter: drop-shadow(0 0 8px #ef4444); }
  12.5%     { opacity: 1; transform: scale(1.4); filter: drop-shadow(0 0 24px #ef4444) brightness(2); }   /* caught */
  13%       { opacity: 0.5; transform: scale(0.6); }
  13.5%     { opacity: 0; transform: scale(0); }                                                       /* eaten */
  99%       { opacity: 0; transform: scale(0); }
  100%      { opacity: 1; transform: scale(1); }                                                       /* respawn */
}
@keyframes eat-2 {
  0%, 24%   { opacity: 1; transform: scale(1);   filter: drop-shadow(0 0 8px #f472b6); }
  24.5%     { opacity: 1; transform: scale(1.4); filter: drop-shadow(0 0 24px #f472b6) brightness(2); }
  25%       { opacity: 0.5; transform: scale(0.6); }
  25.5%     { opacity: 0; transform: scale(0); }
  99%       { opacity: 0; transform: scale(0); }
  100%      { opacity: 1; transform: scale(1); }
}
@keyframes eat-3 {
  0%, 36%   { opacity: 1; transform: scale(1);   filter: drop-shadow(0 0 8px #22d3ee); }
  36.5%     { opacity: 1; transform: scale(1.4); filter: drop-shadow(0 0 24px #22d3ee) brightness(2); }
  37%       { opacity: 0.5; transform: scale(0.6); }
  37.5%     { opacity: 0; transform: scale(0); }
  99%       { opacity: 0; transform: scale(0); }
  100%      { opacity: 1; transform: scale(1); }
}
@keyframes eat-4 {
  0%, 49%   { opacity: 1; transform: scale(1);   filter: drop-shadow(0 0 8px #fb923c); }
  49.5%     { opacity: 1; transform: scale(1.5); filter: drop-shadow(0 0 30px #fb923c) brightness(2.5); }   /* CLIMAX */
  50%       { opacity: 0.5; transform: scale(0.6); }
  50.5%     { opacity: 0; transform: scale(0); }
  99%       { opacity: 0; transform: scale(0); }
  100%      { opacity: 1; transform: scale(1); }
}

/* â”€â”€â”€ Eat burst particles (âœ¦) at each ghost's x position â”€â”€â”€ */
.pac-eat {
  position: absolute;
  font-size: 24px;
  color: #fde047;
  z-index: 5;
  pointer-events: none;
  opacity: 0;
}
.eat-1 { left: 24%; top: 130px; animation: burst 10s linear infinite; }
.eat-2 { left: 43%; top: 210px; animation: burst 10s linear infinite; animation-delay: 0s; }
.eat-3 { left: 61%; top: 160px; animation: burst 10s linear infinite; animation-delay: 0s; }
.eat-4 { left: 80%; top: 230px; animation: burst 10s linear infinite; animation-delay: 0s; }

@keyframes burst {
  0%, 12%    { opacity: 0; transform: scale(0) rotate(0deg); }
  12.5%      { opacity: 1; transform: scale(1.5) rotate(180deg); }
  16%        { opacity: 0; transform: scale(2.5) rotate(360deg); }
  100%       { opacity: 0; }
}
.eat-2 { animation-name: burst-2; }
.eat-3 { animation-name: burst-3; }
.eat-4 { animation-name: burst-4; }
@keyframes burst-2 {
  0%, 24%    { opacity: 0; transform: scale(0) rotate(0deg); }
  24.5%      { opacity: 1; transform: scale(1.5) rotate(180deg); }
  28%        { opacity: 0; transform: scale(2.5) rotate(360deg); }
  100%       { opacity: 0; }
}
@keyframes burst-3 {
  0%, 36%    { opacity: 0; transform: scale(0) rotate(0deg); }
  36.5%      { opacity: 1; transform: scale(1.5) rotate(180deg); }
  40%        { opacity: 0; transform: scale(2.5) rotate(360deg); }
  100%       { opacity: 0; }
}
@keyframes burst-4 {
  0%, 49%    { opacity: 0; transform: scale(0) rotate(0deg); }
  49.5%      { opacity: 1; transform: scale(2) rotate(180deg); }
  55%        { opacity: 0; transform: scale(3) rotate(540deg); }
  100%       { opacity: 0; }
}

/* â”€â”€â”€ Static yellow dots (no sparkle) â”€â”€â”€ */
.pac-dot {
  position: absolute;
  width: 6px; height: 6px;
  background: #fde047;
  border-radius: 50%;
  z-index: 3;
  /* No animation - plain yellow dots */
}

/* â”€â”€â”€ Power pellets (keep pulsing) â”€â”€â”€ */
@keyframes pellet-pulse {
  0%, 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 16px #fde047; }
  50%      { opacity: 0.4; transform: scale(0.65); box-shadow: 0 0 6px #fde047; }
}
.pac-pellet {
  position: absolute;
  width: 16px; height: 16px;
  background: #fde047;
  border-radius: 50%;
  animation: pellet-pulse 0.9s ease-in-out infinite;
  z-index: 3;
}

/* â”€â”€â”€ Title block â”€â”€â”€ */
.pac-title {
  text-align: center;
  font-family: 'Courier New', monospace;
  font-size: 32px;
  font-weight: 900;
  letter-spacing: 6px;
  margin: 18px 0 6px 0;
  color: #fde047;
  text-shadow: 0 0 12px rgba(253, 224, 71, 0.6);
}
.pac-sub {
  text-align: center;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  letter-spacing: 4px;
  color: #a855f7;
  margin-bottom: 12px;
}
.pac-sub em { color: #22d3ee; font-style: normal; }
</style>

<!-- Title (outside scene) -->
<a href="https://github.com/Abi-de-jo" style="text-decoration:none;">
  <div class="pac-title">ðŸŸ¡ C O D E B Y A B I ðŸ’</div>
</a>
<div class="pac-sub">â–¸ FULL-STACK DEVELOPER Â· MERN SPECIALIST Â· <em>CODING IN THE GRAVEYARD</em> â—‚</div>

<!-- Game scene -->
<div class="pac-scene">

  <!-- Big background name â€” appears as ghosts are eaten -->
  <div class="pac-name">Codebyabi</div>

  <!-- HUD -->
  <div class="pac-hud">
    <span class="pac-hud-score">1UP&nbsp; <b>024680</b></span>
    <span class="pac-hud-title">â—€ PAC-MAN â–¶</span>
    <span class="pac-hud-lives">â™¥â™¥â™¥</span>
  </div>

  <!-- Maze walls -->
  <div class="pac-wall mh" style="top: 60px;  left: 8%;  right: 8%;"></div>
  <div class="pac-wall mh" style="top: 250px; left: 8%;  right: 8%;"></div>
  <div class="pac-wall mv" style="left: 8%;  top: 60px; height: 190px;"></div>
  <div class="pac-wall mv" style="right: 8%; top: 60px; height: 190px;"></div>
  <div class="pac-wall mv" style="left: 48%; top: 65px; height: 60px;"></div>
  <div class="pac-wall mv" style="right: 48%; top: 185px; height: 60px;"></div>
  <div class="pac-wall mh" style="top: 140px; left: 20%; width: 100px;"></div>
  <div class="pac-wall mh" style="top: 140px; right: 20%; width: 100px;"></div>

  <!-- Static yellow dots (no animation, no sparkle) -->
  <!-- Top row (y=95) -->
  <div class="pac-dot" style="top:95px;  left:12%;"></div>
  <div class="pac-dot" style="top:95px;  left:18%;"></div>
  <div class="pac-dot" style="top:95px;  left:24%;"></div>
  <div class="pac-dot" style="top:95px;  left:30%;"></div>
  <div class="pac-dot" style="top:95px;  left:36%;"></div>
  <div class="pac-dot" style="top:95px;  left:54%;"></div>
  <div class="pac-dot" style="top:95px;  left:60%;"></div>
  <div class="pac-dot" style="top:95px;  left:66%;"></div>
  <div class="pac-dot" style="top:95px;  left:72%;"></div>
  <div class="pac-dot" style="top:95px;  left:78%;"></div>
  <div class="pac-dot" style="top:95px;  left:84%;"></div>

  <!-- Mid row (y=170) -->
  <div class="pac-dot" style="top:170px; left:12%;"></div>
  <div class="pac-dot" style="top:170px; left:18%;"></div>
  <div class="pac-dot" style="top:170px; left:36%;"></div>
  <div class="pac-dot" style="top:170px; left:42%;"></div>
  <div class="pac-dot" style="top:170px; left:58%;"></div>
  <div class="pac-dot" style="top:170px; left:64%;"></div>
  <div class="pac-dot" style="top:170px; left:82%;"></div>
  <div class="pac-dot" style="top:170px; left:88%;"></div>

  <!-- Bottom row (y=220) -->
  <div class="pac-dot" style="top:220px; left:12%;"></div>
  <div class="pac-dot" style="top:220px; left:18%;"></div>
  <div class="pac-dot" style="top:220px; left:24%;"></div>
  <div class="pac-dot" style="top:220px; left:30%;"></div>
  <div class="pac-dot" style="top:220px; left:36%;"></div>
  <div class="pac-dot" style="top:220px; left:42%;"></div>
  <div class="pac-dot" style="top:220px; left:48%;"></div>
  <div class="pac-dot" style="top:220px; left:54%;"></div>
  <div class="pac-dot" style="top:220px; left:60%;"></div>
  <div class="pac-dot" style="top:220px; left:66%;"></div>
  <div class="pac-dot" style="top:220px; left:72%;"></div>
  <div class="pac-dot" style="top:220px; left:78%;"></div>
  <div class="pac-dot" style="top:220px; left:84%;"></div>

  <!-- Power pellets (still pulsing) -->
  <div class="pac-pellet" style="top:165px; left:11%;"></div>
  <div class="pac-pellet" style="top:165px; right:11%;"></div>

  <!-- Eat burst particles (âœ¦ at each ghost's x position) -->
  <div class="pac-eat eat-1">âœ¦</div>
  <div class="pac-eat eat-2">âœ¦</div>
  <div class="pac-eat eat-3">âœ¦</div>
  <div class="pac-eat eat-4">âœ¦</div>

  <!-- Pac-Man with eye -->
  <div class="pac-pm">
    <div class="pac-pm-eye" style="right: 8px;"></div>
  </div>

  <!-- 4 ghosts â€” wrapper handles position+hover, inner ghost handles eat effect -->
  <div class="ghost-wrap gw-1">
    <div class="pac-ghost g-1">ðŸ‘»</div>
  </div>
  <div class="ghost-wrap gw-2">
    <div class="pac-ghost g-2">ðŸ‘»</div>
  </div>
  <div class="ghost-wrap gw-3">
    <div class="pac-ghost g-3">ðŸ‘»</div>
  </div>
  <div class="ghost-wrap gw-4">
    <div class="pac-ghost g-4">ðŸ‘»</div>
  </div>

</div>

<br>

<!-- Typing banner -->
<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=FDE047&center=true&vCenter=true&width=600&lines=Eating+bugs+for+breakfast;Chasing+ghosts+daily;Power+pellet+mode+ON;Waka+waka+waka;Full-Stack+Developer" alt="Typing SVG" />
</a>

<br><br>

<!-- Social badges -->
<a href="https://github.com/Abi-de-jo">
  <img src="https://api.visitorbadge.io/api/visitors?path=Abi-de-jo&label=visitors&countColor=%23a855f7&style=flat-square&labelStyle=upper" />
</a>
&nbsp;
<a href="https://discord.com/users/Abi-de-jo">
  <img src="https://img.shields.io/badge/Discord-@Abi__de__jo-5865F2?style=flat-square&logo=discord&logoColor=white" />
</a>
&nbsp;
<a href="https://linkedin.com/in/Abi-de-jo">
  <img src="https://img.shields.io/badge/LinkedIn-Abi--de--jo-0A66C2?style=flat-square&logo=linkedin&logoColor=white" />
</a>
&nbsp;
<a href="mailto:contact@codebyabi.dev">
  <img src="https://img.shields.io/badge/Email-contact-8b5cf7?style=flat-square&logo=minutemailer&logoColor=white" />
</a>

</div>

---

<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• ABOUT + MAZE PANEL â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->

<table>
<tr>
<td width="50%" valign="top" style="padding-right:20px;">

## ðŸ‘¨â€ðŸ’» About Me

```yaml
name: R.Abisheik
handle: Abi-de-jo
location: Chennai, TamilNadu
company: Sree-Cognicoders
blog: codebyabi.dev
joined: 2023
philosophy: "Clean code over clever code â€” always."
```

<br>

### <span style="color:#22d3ee">ðŸŽ¨ Frontend</span>
**React Â· TypeScript Â· Next.js**

### <span style="color:#22c55e">âš™ï¸ Backend</span>
**Node.js Â· Express Â· MongoDB**

### <span style="color:#fb923c">ðŸŽ¯ Styling</span>
**HTML5 Â· CSS3 Â· Tailwind**

### <span style="color:#a855f7">ðŸš€ Focus</span>
**Production-grade web applications**

</td>
<td width="50%" valign="top" style="padding-left:20px;">

<div align="center">

### ðŸ‘» The Stack â€” *Waka Waka Edition*

<br>

```
   Â· Â· Â· Â· Â· Â· ðŸŸ¦ðŸŸ¦ðŸŸ¦ðŸŸ¦ðŸŸ¦ Â· Â· Â· ðŸŸ¦ðŸŸ¦ðŸŸ¦ðŸŸ¦ðŸŸ¦ Â· Â· Â· Â· Â· Â·
   Â·     ðŸŸ¦     ðŸŸ¦              ðŸŸ¦     ðŸŸ¦
   ðŸŸ¡    ðŸŸ¦     [âš›ï¸ React]  [TS]     ðŸŸ¦    Â·    ðŸ‘»
   Â·     ðŸŸ¦     ðŸŸ¦              ðŸŸ¦     ðŸŸ¦
   Â· Â· Â· Â· Â· Â· ðŸŸ¦ðŸŸ¦ðŸŸ¦ðŸŸ¦ðŸŸ¦ Â· Â· Â· ðŸŸ¦ðŸŸ¦ðŸŸ¦ðŸŸ¦ðŸŸ¦ Â· Â· Â· Â· Â· Â·
                  ðŸŸ¦                ðŸŸ¦
   [ðŸŸ¢ Node] [ex Express] [N Next]  ðŸŸ¦
   ðŸŸ¡        ðŸŸ¦         ðŸŸ¦         ðŸŸ¦    ðŸŸ¡
   Â· Â· Â· Â· Â·ðŸŸ¦ðŸŸ¦ðŸŸ¦Â· Â· Â· Â· Â· Â· Â· Â·ðŸŸ¦ðŸŸ¦ðŸŸ¦Â· Â· Â· Â· Â·
                  [ðŸƒ Mongo]
```

*ðŸŸ¡ = power-pellet ready Â· chasing down bugs daily*

</div>

</td>
</tr>
</table>

---

<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• QUOTE â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->

<div align="center">

> ### ðŸ† *"Clean code over clever code â€” always."*

</div>

---

<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• TECH STACK BADGES â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->

## ðŸ› ï¸ Tech Stack

<div align="center">

<img src="https://skillicons.dev/icons?i=js,ts,react,nextjs,nodejs,express,mongodb,html,css,tailwind,git,github,vscode,postman,linux&theme=dark&perline=8" alt="Tech Stack" />

</div>

---

<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• GITHUB STATS â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->

## ðŸ“Š GitHub Statistics

<div align="center">

<table>
  <tr>
    <td width="50%">
      <img src="https://github-readme-stats.vercel.app/api?username=Abi-de-jo&show_icons=true&theme=midnight-purple&hide_border=true&bg_color=0a0a0f&title_color=fde047&icon_color=fde047&text_color=e2e8f0&border_color=1e1b4b&include_all_commits=true&count_private=true" width="100%" />
    </td>
    <td width="50%">
      <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=Abi-de-jo&layout=compact&theme=midnight-purple&hide_border=true&bg_color=0a0a0f&title_color=fde047&text_color=e2e8f0&border_color=1e1b4b" width="100%" />
    </td>
  </tr>
</table>

<br>

<img src="https://github-readme-streak-stats.herokuapp.com/?user=Abi-de-jo&theme=midnight-purple&hide_border=true&background=0a0a0f&stroke=fde047&ring=fde047&fire=c084fc&currStreakNum=e2e8f0&sideNums=e2e8f0&currStreakLabel=fde047&sideLabels=fde047&dates=6b7280" width="70%" />

</div>

---

<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• ACTIVITY GRAPH â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->

## ðŸ“ˆ Contribution Activity

<div align="center">

<img src="https://github-readme-activity-graph.vercel.app/graph?username=Abi-de-jo&bg_color=0a0a0f&color=fde047&line=a855f7&point=c084fc&area=true&hide_border=true&radius=8" width="95%" />

</div>

---

<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• TROPHIES â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->

## ðŸ† Achievements

<div align="center">

<img src="https://github-profile-trophy-tawny.vercel.app/?username=Abi-de-jo&theme=discord&no-frame=true&no-bg=true&column=8&margin-w=10&margin-h=10&title_color=fde047" alt="Trophies" />

<br><br>
<sub><i>Trophies auto-refresh via the GitHub Trophy API</i></sub>

</div>

---

<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• PAC-MAN CONTRIBUTION GRAPH â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->

## ðŸ‘» Pac-Man Contribution Graph

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Abi-de-jo/Abi-de-jo/output/pacman-contribution-graph-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Abi-de-jo/Abi-de-jo/output/pacman-contribution-graph.svg" />
  <img alt="Pac-Man Contribution Graph" src="https://raw.githubusercontent.com/Abi-de-jo/Abi-de-jo/output/pacman-contribution-graph-dark.svg" width="100%" />
</picture>

<br>
<sub><i>ðŸ‘» Pac-Man chases your contributions â€” auto-updated every 12 hours</i></sub>

</div>

---

<!-- â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• TYPING BANNER â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• -->

<div align="center">

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=FDE047&center=true&vCenter=true&width=600&lines=Eating+bugs+for+breakfast;Chasing+ghosts+daily;Power+pellet+mode+ON;Waka+waka+waka;Full-Stack+Developer" alt="Typing SVG" />
</a>

<br><br>

<sub>ðŸŸ¡ <b>WAKA WAKA</b> Â· built with â¤ï¸ in Chennai Â· Â© R.Abisheik</sub>

</div>
