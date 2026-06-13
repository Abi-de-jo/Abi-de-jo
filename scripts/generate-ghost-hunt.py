#!/usr/bin/env python3
"""Generate the Ghost Hunt game SVG statically (no JS needed)."""

import random, os, datetime

random.seed(42)

colors = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
WEEKS = 52
DAYS = 7
CELL = 13
GAP = 16
OFFSET_X = 20
OFFSET_Y = 55

def gen():
    lines = []
    a = lines.append
    
    a('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 320" width="900" height="320">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="#0d1117"/>
<stop offset="100%" stop-color="#161b22"/>
</linearGradient>
<style>
@keyframes ghostFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
@keyframes ghostGlow{0%,100%{filter:drop-shadow(0 0 3px #8b5cf6)}50%{filter:drop-shadow(0 0 10px #c084fc)}}
@keyframes twinkle{0%,100%{opacity:0.2}50%{opacity:1}}
.ghost{animation:ghostFloat 3s ease-in-out infinite,ghostGlow 2s ease-in-out infinite}
.s1{animation-delay:0s}.s2{animation-delay:0.3s}.s3{animation-delay:0.7s}
.s4{animation-delay:1s}.s5{animation-delay:1.3s}.s6{animation-delay:1.7s}
.s7{animation-delay:2s}.s8{animation-delay:2.3s}.s9{animation-delay:2.7s}
.s10{animation-delay:3s}.s11{animation-delay:3.3s}.s12{animation-delay:3.7s}
.star{animation:twinkle 3s ease-in-out infinite}
</style>
</defs>
<rect width="900" height="320" fill="url(#bg)" rx="12"/>''')
    
    # Title
    a('<text x="450" y="32" text-anchor="middle" font-family="system-ui,sans-serif" font-size="20" font-weight="800" fill="#c084fc">👻 GHOST HUNT</text>')
    a('<text x="450" y="48" text-anchor="middle" font-family="monospace" font-size="11" fill="#6b7280">Ghosts hide in contribution cells — keep committing to catch them!</text>')
    
    # Decorative stars
    star_positions = [(50,25),(150,20),(300,28),(500,22),(700,30),(830,18)]
    for i, (sx, sy) in enumerate(star_positions):
        a(f'<circle cx="{sx}" cy="{sy}" r="1.2" fill="#c084fc" class="star s{i+1}"/>')
    
    # Contribution grid
    ghost_cells = []
    total_cells = WEEKS * DAYS
    
    for w in range(WEEKS):
        for d in range(DAYS):
            x = OFFSET_X + w * GAP
            y = OFFSET_Y + d * GAP
            r = random.random()
            if r < 0.35:
                level = 0
            elif r < 0.6:
                level = 1
            elif r < 0.78:
                level = 2
            elif r < 0.9:
                level = 3
            else:
                level = 4
            
            a(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{colors[level]}"/>')
            
            # Ghosts appear on cells with level 3+
            if level >= 3 and random.random() < 0.15:
                ghost_cells.append((x, y))
    
    # Add ghost emojis with animations
    class_names = ["s1","s2","s3","s4","s5","s6","s7","s8","s9","s10","s11","s12"]
    for i, (gx, gy) in enumerate(ghost_cells):
        cn = class_names[i % len(class_names)]
        a(f'<text x="{gx + CELL//2}" y="{gy + CELL - 1}" text-anchor="middle" font-size="11" class="ghost {cn}">👻')
        dur = round(2 + random.random() * 3, 1)
        a(f'<animate attributeName="opacity" values="1;0;1" dur="{dur}s" repeatCount="indefinite"/>')
        a('</text>')
    
    # Stats bar
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    a(f'<rect x="20" y="235" width="860" height="35" rx="8" fill="#0d1117" stroke="#8b5cf6" stroke-width="1" opacity="0.8"/>')
    a(f'<text x="30" y="257" font-family="monospace" font-size="12" fill="#c4b5fd">👻 Ghosts Spotted: {len(ghost_cells)}  |  📦 Hunt Area: {total_cells} cells  |  🕐 {now} UTC</text>')
    
    # Footer
    a('<text x="450" y="305" text-anchor="middle" font-family="monospace" font-size="9" fill="#6b7280">👻 Ghosts hide in active contribution cells. Keep committing to hunt them all!</text>')
    
    a('</svg>')
    
    return '\n'.join(lines)

if __name__ == "__main__":
    svg = gen()
    path = os.path.join(os.path.dirname(__file__) or ".", "..", "assets", "ghost-hunt-game.svg")
    path = os.path.normpath(path)
    with open(path, "w") as f:
        f.write(svg)
    print(f"👻 Ghost Hunt game saved to {path}")
    print(f"   Ghosts spotted: {svg.count('👻') - 1}")
