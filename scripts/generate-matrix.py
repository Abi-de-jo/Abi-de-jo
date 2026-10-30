#!/usr/bin/env python3
import json
import os
import sys
from datetime import date, timedelta

# Baseline verified from Abi's profile (including private/org contributions)
BASELINE_COMMITS = 2328
BASELINE_GRID = [
  [-1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 2, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [-1, -1, -1, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 2, 0, 3, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 3, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [-1, -1, -1, -1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 3, 1, 3, 1, 1, 4, 1, 1, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [-1, -1, -1, -1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 2, 1, 1, 0, 2, 0, 0, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, -1],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 0, 1, 0, 2, 1, 0, 1, 0, 0, 0, 1, 1, 2, 0, 0, 1, 2, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1]
]

OUTPUT_PATH = "assets/contribution-matrix.svg"


def build_svg(grid=BASELINE_GRID, total_commits=BASELINE_COMMITS):
    start_x = 88
    start_y = 138
    tile_size = 14
    gap = 5
    step = tile_size + gap

    start_sunday = date(2025, 12, 28)
    month_cols = {
        'JAN': 0, 'FEB': 5, 'MAR': 9, 'APR': 13, 'MAY': 17, 'JUN': 22,
        'JUL': 26, 'AUG': 30, 'SEP': 35, 'OCT': 39, 'NOV': 44, 'DEC': 48
    }

    months_svg = []
    for m_name, col_idx in month_cols.items():
        mx = start_x + col_idx * step
        months_svg.append(f'<text x="{mx}" y="{start_y - 12}" fill="#8290a8" class="m tiny">{m_name}</text>')

    days_svg = [
        f'<text x="{start_x - 14}" y="{start_y + 1 * step + 11}" text-anchor="end" fill="#64748b" class="m tiny">MON</text>',
        f'<text x="{start_x - 14}" y="{start_y + 3 * step + 11}" text-anchor="end" fill="#64748b" class="m tiny">WED</text>',
        f'<text x="{start_x - 14}" y="{start_y + 5 * step + 11}" text-anchor="end" fill="#64748b" class="m tiny">FRI</text>',
    ]

    level_styles = {
        0: 'fill="#131826" stroke="#1f293d"',
        1: 'fill="#1b4d3e" stroke="#2dd4bf" stroke-opacity=".5"',
        2: 'fill="#237a57" stroke="#7df9c2" stroke-opacity=".8"',
        3: 'fill="#7df9c2" stroke="#a7f3d0" class="lvl3"',
        4: 'fill="#ffd166" stroke="#fff" class="lvl4"'
    }

    tiles_svg = []
    for col in range(53):
        for row in range(7):
            lvl = grid[row][col]
            if lvl < 0:
                continue
            tx = start_x + col * step
            ty = start_y + row * step
            style = level_styles.get(lvl, level_styles[0])
            dt = start_sunday + timedelta(days=col * 7 + row)
            date_str = dt.strftime('%Y-%m-%d')
            tiles_svg.append(f'<rect x="{tx}" y="{ty}" width="{tile_size}" height="{tile_size}" rx="2" {style}><title>{date_str} (Level {lvl})</title></rect>')

    months_str = "\n  ".join(months_svg)
    days_str = "\n  ".join(days_svg)
    tiles_str = "\n  ".join(tiles_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 460" role="img" aria-labelledby="title desc">
  <title id="title">Commit Raid: 365-Day Battle Matrix</title>
  <desc id="desc">An animated game arena visualizing Abi's {total_commits:,} annual GitHub contributions in 2026 across 53 weeks with health bars, combo streaks, and combat drone patrol.</desc>
  <defs>
    <linearGradient id="arena-bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0b0f1a"/>
      <stop offset="100%" stop-color="#080c15"/>
    </linearGradient>
    <linearGradient id="beam-grad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#7df9c2" stop-opacity="0"/>
      <stop offset="50%" stop-color="#7df9c2" stop-opacity=".35"/>
      <stop offset="100%" stop-color="#7df9c2" stop-opacity="0"/>
    </linearGradient>
    <style>
      .m{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
      .cap{{font-size:11px;letter-spacing:2px}}
      .tiny{{font-size:10px;letter-spacing:1px}}
      .dot{{animation:blink 1.4s steps(1) infinite}}
      .pulse{{animation:pulse 2s ease-in-out infinite}}
      .drone{{animation:patrol 9s ease-in-out infinite}}
      .wheel{{animation:spin .5s linear infinite;transform-box:fill-box;transform-origin:center}}
      .eye{{animation:blink 3s steps(1) infinite}}
      .scanbeam{{animation:sweep 8s linear infinite}}
      .lvl3{{filter:drop-shadow(0 0 4px #7df9c2)}}
      .lvl4{{filter:drop-shadow(0 0 6px #ffd166);animation:pulse 2s ease-in-out infinite}}
      @keyframes blink{{50%{{opacity:.2}}}}
      @keyframes pulse{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}
      @keyframes spin{{to{{transform:rotate(360deg)}}}}
      @keyframes patrol{{
        0%,100%{{transform:translate(140px,96px)}}
        25%{{transform:translate(460px,88px)}}
        50%{{transform:translate(880px,98px)}}
        75%{{transform:translate(540px,92px)}}
      }}
      @keyframes sweep{{
        0%{{transform:translateX(0);opacity:0}}
        5%{{opacity:1}}
        95%{{opacity:1}}
        100%{{transform:translateX(1005px);opacity:0}}
      }}
      @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
    </style>
  </defs>

  <!-- Chassis Frame -->
  <rect width="1200" height="460" rx="18" fill="url(#arena-bg)"/>
  <rect x="1" y="1" width="1198" height="458" rx="17" fill="none" stroke="#2a354d"/>

  <!-- Corner Tech Brackets -->
  <path d="M18 36V18h18M1182 36V18h-18M18 424v18h18M1182 424v-18h-18" fill="none" stroke="#7df9c2" stroke-width="2" opacity=".6"/>

  <!-- Top Header Bar -->
  <circle cx="45" cy="44" r="7" fill="#7df9c2" class="dot"/>
  <text x="68" y="42" fill="#f4f7ff" class="m" font-size="22" font-weight="700" letter-spacing="2">COMMIT RAID // SECTOR 365</text>
  <text x="68" y="60" fill="#7df9c2" class="m cap">2026 EXPEDITION · {total_commits:,} COMMITS LOGGED</text>

  <!-- Player Status / Health Bars -->
  <g transform="translate(635 28)">
    <rect x="0" y="0" width="165" height="38" rx="6" fill="#121828" stroke="#28344c"/>
    <text x="12" y="15" fill="#8491a8" class="m tiny">HP // CODE HEALTH</text>
    <rect x="12" y="21" width="141" height="8" rx="2" fill="#1e293b"/>
    <rect x="12" y="21" width="141" height="8" rx="2" fill="#7df9c2"/>
  </g>

  <g transform="translate(815 28)">
    <rect x="0" y="0" width="165" height="38" rx="6" fill="#121828" stroke="#28344c"/>
    <text x="12" y="15" fill="#8491a8" class="m tiny">EXP // {total_commits:,} POWER</text>
    <rect x="12" y="21" width="141" height="8" rx="2" fill="#1e293b"/>
    <rect x="12" y="21" width="138" height="8" rx="2" fill="#b98cff"/>
  </g>

  <!-- Boss Clear Badge -->
  <g transform="translate(995 28)">
    <rect x="0" y="0" width="160" height="38" rx="6" fill="#121828" stroke="#7df9c2" stroke-width="1.5"/>
    <circle cx="20" cy="19" r="6" fill="#7df9c2" class="pulse"/>
    <text x="34" y="24" fill="#f4f7ff" class="m tiny" font-weight="700">BOSS: CLEARED</text>
    <text x="135" y="24" fill="#ffd166" class="m tiny">★ 74</text>
  </g>

  <path d="M40 82h1120" stroke="#222c42"/>

  <!-- Matrix Months & Days -->
  <g>
  {months_str}
  {days_str}
  </g>

  <!-- Matrix Grid -->
  <g>
  {tiles_str}
  </g>

  <!-- Sweeping Laser Beam -->
  <rect class="scanbeam" x="{start_x}" y="{start_y - 4}" width="32" height="136" fill="url(#beam-grad)" pointer-events="none"/>

  <!-- Combat Drone Patrol Companion -->
  <g class="drone" pointer-events="none">
    <path d="M0 16h10M46 16h10" stroke="#7df9c2" stroke-width="3"/>
    <rect x="10" y="4" width="36" height="24" rx="4" fill="#162035" stroke="#7df9c2" stroke-width="1.5"/>
    <circle cx="21" cy="16" r="3" fill="#7df9c2" class="eye"/>
    <circle cx="35" cy="16" r="3" fill="#7df9c2" class="eye"/>
    <circle cx="5" cy="16" r="4" fill="none" stroke="#b98cff" stroke-width="1.5" class="wheel"/>
    <circle cx="51" cy="16" r="4" fill="none" stroke="#b98cff" stroke-width="1.5" class="wheel"/>
    <path d="M28 28v18" stroke="#7df9c2" stroke-width="1" stroke-dasharray="2 2" opacity=".7"/>
  </g>

  <!-- Bottom Divider -->
  <path d="M40 310h1120" stroke="#222c42"/>

  <!-- Bottom Game Deck -->
  <g transform="translate(45 330)">
    <text fill="#8491a8" class="m tiny">CONTROLS</text>
    <g transform="translate(0 14)">
      <rect x="0" y="0" width="28" height="28" rx="4" fill="#151c2e" stroke="#2f3b54"/>
      <text x="14" y="18" text-anchor="middle" fill="#7df9c2" class="m tiny">◄</text>
      <rect x="34" y="0" width="28" height="28" rx="4" fill="#151c2e" stroke="#2f3b54"/>
      <text x="48" y="18" text-anchor="middle" fill="#7df9c2" class="m tiny">▲</text>
      <rect x="68" y="0" width="28" height="28" rx="4" fill="#151c2e" stroke="#2f3b54"/>
      <text x="82" y="18" text-anchor="middle" fill="#7df9c2" class="m tiny">▼</text>
      <rect x="102" y="0" width="28" height="28" rx="4" fill="#151c2e" stroke="#2f3b54"/>
      <text x="116" y="18" text-anchor="middle" fill="#7df9c2" class="m tiny">►</text>
      <rect x="148" y="0" width="82" height="28" rx="4" fill="#151c2e" stroke="#2f3b54"/>
      <text x="189" y="18" text-anchor="middle" fill="#f4f7ff" class="m tiny">[A] COMMIT</text>
      <rect x="236" y="0" width="70" height="28" rx="4" fill="#151c2e" stroke="#2f3b54"/>
      <text x="271" y="18" text-anchor="middle" fill="#f4f7ff" class="m tiny">[B] PUSH</text>
    </g>
  </g>

  <!-- Legend -->
  <g transform="translate(690 330)">
    <text fill="#8491a8" class="m tiny">MATRIX CHARGE LEVEL</text>
    <g transform="translate(0 18)">
      <rect x="0" y="0" width="14" height="14" rx="2" fill="#131826" stroke="#1f293d"/>
      <text x="20" y="11" fill="#8491a8" class="m tiny">IDLE</text>

      <rect x="70" y="0" width="14" height="14" rx="2" fill="#1b4d3e" stroke="#2dd4bf" stroke-opacity=".5"/>
      <text x="90" y="11" fill="#8491a8" class="m tiny">1-9</text>

      <rect x="135" y="0" width="14" height="14" rx="2" fill="#237a57" stroke="#7df9c2" stroke-opacity=".8"/>
      <text x="155" y="11" fill="#8491a8" class="m tiny">10-19</text>

      <rect x="215" y="0" width="14" height="14" rx="2" fill="#7df9c2" stroke="#a7f3d0" class="lvl3"/>
      <text x="235" y="11" fill="#8491a8" class="m tiny">20-29</text>

      <rect x="295" y="0" width="14" height="14" rx="2" fill="#ffd166" stroke="#fff" class="lvl4"/>
      <text x="315" y="11" fill="#8491a8" class="m tiny">30+ HYPER</text>
    </g>
  </g>

  <!-- Bottom Ticker -->
  <text x="45" y="420" fill="#64748b" class="m tiny">SECTOR STATUS: 2,328 COMMITS LOGGED ACROSS 2026 · 151 ACTIVE COMBAT DAYS · LEVEL 74 BUILDER</text>
  <text x="1155" y="420" text-anchor="end" fill="#7df9c2" class="m cap">SYSTEM ARMED <tspan class="dot">█</tspan></text>
</svg>
"""
    return svg


def main():
    svg = build_svg()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Successfully generated {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
