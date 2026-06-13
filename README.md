<div align="center">

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 280" width="900" height="280" role="img" aria-label="CodeByAbi animated ghost banner">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="50%" stop-color="#131022"/>
      <stop offset="100%" stop-color="#0d1117"/>
    </linearGradient>
    <linearGradient id="ghostGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8b5cf6"/>
      <stop offset="100%" stop-color="#6d28d9"/>
    </linearGradient>
    <radialGradient id="glowGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.7"/>
      <stop offset="60%" stop-color="#6d28d9" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#6d28d9" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <style>
    .float { animation: float 4s ease-in-out infinite; }
    .fade { animation: fade 6s ease-in-out infinite; }
    .blink-left { animation: blink 5s infinite; transform-origin: center; transform-box: fill-box; }
    .blink-right { animation: blink 5s infinite; transform-origin: center; transform-box: fill-box; }
    .pulse-glow { animation: pulseGlow 3s ease-in-out infinite; transform-origin: center; transform-box: fill-box; }
    .twinkle-a { animation: twinkle 2.5s ease-in-out infinite; }
    .twinkle-b { animation: twinkle 3s ease-in-out infinite 0.4s; }
    .twinkle-c { animation: twinkle 2s ease-in-out infinite 0.8s; }
    .twinkle-d { animation: twinkle 3.5s ease-in-out infinite 1.2s; }
    .twinkle-e { animation: twinkle 2.8s ease-in-out infinite 0.2s; }
    .twinkle-f { animation: twinkle 3.2s ease-in-out infinite 1.5s; }
    .badge-hide { animation: badgeHide 8s ease-in-out infinite; }
    .text-glow { animation: textGlow 4s ease-in-out infinite; }

    @keyframes float {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-10px); }
    }
    @keyframes fade {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.15; }
    }
    @keyframes blink {
      0%, 90%, 100% { transform: scaleY(1); }
      93%, 97% { transform: scaleY(0.1); }
    }
    @keyframes pulseGlow {
      0%, 100% { transform: scale(1); opacity: 0.4; }
      50% { transform: scale(1.3); opacity: 0.75; }
    }
    @keyframes twinkle {
      0%, 100% { opacity: 0.2; }
      50% { opacity: 1; }
    }
    @keyframes badgeHide {
      0%, 40% { transform: translateX(0); opacity: 1; }
      50%, 60% { transform: translateX(40px); opacity: 0; }
      70%, 100% { transform: translateX(0); opacity: 1; }
    }
    @keyframes textGlow {
      0%, 100% { filter: drop-shadow(0 0 4px #8b5cf6) drop-shadow(0 0 8px #6d28d9); }
      50% { filter: drop-shadow(0 0 12px #c084fc) drop-shadow(0 0 22px #8b5cf6); }
    }
  </style>

  <rect width="900" height="280" fill="url(#bgGrad)"/>

  <g fill="#a78bfa">
    <circle class="twinkle-a" cx="80" cy="50" r="1.5"/>
    <circle class="twinkle-b" cx="150" cy="30" r="1"/>
    <circle class="twinkle-c" cx="220" cy="80" r="1.5"/>
    <circle class="twinkle-d" cx="680" cy="40" r="1"/>
    <circle class="twinkle-e" cx="760" cy="70" r="1.5"/>
    <circle class="twinkle-f" cx="830" cy="50" r="1"/>
    <circle class="twinkle-a" cx="120" cy="200" r="1"/>
    <circle class="twinkle-c" cx="780" cy="180" r="1.5"/>
    <circle class="twinkle-b" cx="40" cy="120" r="1"/>
    <circle class="twinkle-d" cx="860" cy="120" r="1"/>
    <circle class="twinkle-e" cx="180" cy="150" r="1"/>
    <circle class="twinkle-f" cx="720" cy="200" r="1"/>
  </g>

  <text x="60" y="190" font-family="monospace" font-size="120" fill="#6d28d9" opacity="0.35" font-weight="bold">{</text>
  <text x="820" y="190" font-family="monospace" font-size="120" fill="#6d28d9" opacity="0.35" font-weight="bold">}</text>

  <text x="450" y="28" font-family="monospace" font-size="13" fill="#a78bfa" text-anchor="middle" opacity="0.8">while(true) { code() }</text>

  <g transform="translate(620, 80)">
    <g class="badge-hide">
      <rect x="0" y="0" width="120" height="30" rx="15" ry="15" fill="#0d1117" stroke="#8b5cf6" stroke-width="2"/>
      <text x="60" y="20" font-family="monospace" font-size="12" font-weight="bold" fill="#a78bfa" text-anchor="middle" letter-spacing="1.5">GHOST MODE</text>
    </g>
  </g>

  <g class="float">
    <ellipse class="pulse-glow" cx="450" cy="130" rx="90" ry="100" fill="url(#glowGrad)"/>

    <g class="fade">
      <text x="335" y="145" font-family="monospace" font-size="30" font-weight="bold" fill="#8b5cf6" text-anchor="middle" opacity="0.9">&lt;</text>
      <text x="565" y="145" font-family="monospace" font-size="30" font-weight="bold" fill="#8b5cf6" text-anchor="middle" opacity="0.9">/&gt;</text>

      <path d="M 390 110 A 60 60 0 0 1 510 110 L 510 180 Q 495 200 480 180 Q 465 200 450 180 Q 435 200 420 180 Q 405 200 390 180 Z" fill="url(#ghostGrad)" stroke="#a78bfa" stroke-width="1.5"/>

      <ellipse cx="410" cy="125" rx="9" ry="5" fill="#f0abfc" opacity="0.55"/>
      <ellipse cx="490" cy="125" rx="9" ry="5" fill="#f0abfc" opacity="0.55"/>

      <ellipse class="blink-left" cx="425" cy="100" rx="7" ry="11" fill="#0d1117"/>
      <ellipse class="blink-right" cx="475" cy="100" rx="7" ry="11" fill="#0d1117"/>

      <circle cx="422" cy="95" r="2" fill="#ffffff"/>
      <circle cx="472" cy="95" r="2" fill="#ffffff"/>

      <path d="M 435 130 Q 450 142 465 130" fill="none" stroke="#0d1117" stroke-width="2.5" stroke-linecap="round"/>
    </g>
  </g>

  <text class="text-glow" x="450" y="225" font-family="'Segoe UI', 'Helvetica Neue', Arial, sans-serif" font-size="36" font-weight="bold" fill="#ffffff" text-anchor="middle">CodeByAbi</text>

  <text x="450" y="252" font-family="'Segoe UI', 'Helvetica Neue', Arial, sans-serif" font-size="13" fill="#94a3b8" text-anchor="middle">Full-Stack Developer &amp; MERN Specialist</text>
</svg>

</div>

# 👻 SPECTRAL PRESENCE
**R.Abisheik** · CodeByAbi · Full-Stack Developer · MERN Specialist  
📍 Tamilnadu · 🕯️ Coding after midnight · ☕ Black coffee fuel

# 👻 THE HAUNTED STACK
### 👻 Frontend
TypeScript · React · Next.js · React Native · Tailwind · Redux
### 👻 Backend
Node.js · Python · Go · GraphQL · Prisma · PostgreSQL · MongoDB
### 👻 Infrastructure
Docker · AWS · Firebase · Auth0 · Git Actions · Cloudflare
### 👻 Tools
VS Code · Figma · Postman · Linux · Git · Biome

# 👻 GRAVEYARD PROJECTS
### 👻 [Fahh](https://github.com/Abi-de-jo/Fahh)
VS Code extension · Catch bugs by ear 🔊
`TypeScript`
### 👻 [Fitmachi](https://github.com/Abi-de-jo/Fitmachi)
Fitness tracking · Workout planning · Analytics 💪
`TypeScript`
### 👻 [AiMock Interview](https://github.com/Abi-de-jo/AiMock-Interview)
AI-powered mock interview · Real-time feedback 🎯
`JavaScript`
### 👻 [ReleaseNotePro](https://github.com/Abi-de-jo/ReleaseNotePro)
Multi-agent AI · Automated release notes 📝
`Multi-Agent AI`
### 👻 [Wedding Invitation](https://github.com/Abi-de-jo/Wedding-Invitation)
Interactive invites · RSVP · Gallery 💍
`TypeScript`
### 👻 [NailsByShmatko](https://github.com/Abi-de-jo/NailsByShmatko)
Salon booking · Portfolio platform 💅
`Next.js`
### 👻 [Freelance Photography](https://github.com/Abi-de-jo/Freelance-Photography)
Photography platform · Connect clients 📸
`TypeScript`
### 👻 [CodeByAbi Portfolio](https://github.com/Abi-de-jo/CodeByAbi-Portfolio)
Personal portfolio · Creative showcase 🎨
`HTML/CSS/JS/TS`

# 👻 UNDEAD STATS
<p align="center">
<img src="https://github-readme-stats.vercel.app/api?username=Abi-de-jo&show_icons=true&theme=midnight-purple&hide_border=true&bg_color=0d1117&title_color=a78bfa&icon_color=8b5cf6&text_color=e2e8f0" width="48%" />
<img src="https://github-readme-streak-stats.herokuapp.com/?user=Abi-de-jo&theme=midnight-purple&hide_border=true&background=0d1117&ring=a78bfa&fire=8b5cf6&currStreakLabel=e2e8f0" width="48%" />
</p>
<p align="center">
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=Abi-de-jo&layout=compact&theme=midnight-purple&hide_border=true&bg_color=0d1117&title_color=a78bfa&text_color=e2e8f0" width="40%" />
</p>

# 👻 HAUNTED CONTRIBUTIONS
<p align="center">
<img src="https://github-readme-activity-graph.vercel.app/graph?username=Abi-de-jo&bg_color=0d1117&color=a78bfa&line=8b5cf6&point=c084fc&area=true&area_color=6d28d9&hide_border=true" width="95%" />
</p>

# 👻 THE ORDER
Sree-Cognicoders // The Order 🏛️

> Teaching 50+ students · Shaping the next generation of full-stack engineers

# 👻 SUMMON ME
<p align="center">
<a href="https://www.youtube.com/channel/UCTEUF6w84xLXPRfs7AYkTXQ"><img src="https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube"/></a>
<a href="https://www.instagram.com/codebyabi"><img src="https://img.shields.io/badge/Instagram-%23E4405F.svg?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram"/></a>
<a href="https://github.com/Abi-de-jo"><img src="https://img.shields.io/badge/GitHub-%23121011.svg?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/></a>
</p>
<p align="center">
<img src="https://komarev.com/ghpvc/?username=Abi-de-jo&color=8b5cf6&style=flat-square&label=Ghost+Sightings" alt="Profile Views" />
</p>

---
<p align="center">
👻 Haunting production systems since 2020 · Senior Code Spirit at Sree-Cognicoders 👻
</p>
