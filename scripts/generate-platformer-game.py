#!/usr/bin/env python3
"""
🎮 GHOST RUNNER — Animated Platformer Game SVG Generator
=======================================================
Fetches real GitHub contributions and generates a stunning game-like
visualization where commit activity builds the world terrain.

The output is a pure SVG with CSS + SMIL animations (zero JS) —
it works beautifully when embedded in GitHub README.

Usage:
  python generate-platformer-game.py --username Abi-de-jo --output assets/ghost-runner.svg
"""

from __future__ import annotations

import json
import math
import os
import random
import sys
import xml.sax.saxutils as saxutils
from datetime import datetime, timezone, timedelta

# ─── Constants ───────────────────────────────────────────────────────────────

CANVAS_W = 900
CANVAS_H = 420

GRID_LEFT = 40
GRID_TOP = 170
CELL_SIZE = 10
CELL_GAP = 3
STEP = CELL_SIZE + CELL_GAP
ROWS = 7
COLS = 52

GROUND_Y = GRID_TOP + ROWS * STEP + 4
TERRAIN_BASE = GROUND_Y - 10

PURPLE = "#8b5cf6"
PURPLE_LIGHT = "#a78bfa"
PURPLE_DIM = "#6d28d9"
GREEN_LEVELS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
CYAN = "#22d3ee"
PINK = "#f472b6"
GOLD = "#fbbf24"
WHITE = "#ffffff"

GRAPHQL_QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            contributionLevel
            date
            weekday
          }
        }
      }
    }
  }
}
"""


# ─── Data Fetching ───────────────────────────────────────────────────────────

def fetch_contributions(username: str, token: str | None = None) -> dict:
    """Fetch real contribution data via GitHub GraphQL."""
    token = token or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print("::warning::No GitHub token — using mock data", file=sys.stderr)
        return _mock_data()

    import urllib.request
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    body = json.dumps({"query": GRAPHQL_QUERY, "variables": {"login": username}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=body, headers=headers, method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        if "errors" in data:
            print(f"::warning::GraphQL errors: {data['errors']}", file=sys.stderr)
            return _mock_data()
        return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    except Exception as e:
        print(f"::warning::Fetch failed: {e} — using mock data", file=sys.stderr)
        return _mock_data()


def _mock_data() -> dict:
    """Generate realistic-looking mock contribution data."""
    weeks = []
    today = datetime.now(timezone.utc)
    for w in range(52):
        days = []
        for d in range(7):
            date = today - timedelta(weeks=52 - w, days=6 - d)
            count = max(0, int(random.gauss(3, 4)))
            days.append({
                "contributionCount": count,
                "contributionLevel": _level_name(count),
                "date": date.strftime("%Y-%m-%d"),
                "weekday": d,
            })
        weeks.append({"contributionDays": days})
    total = sum(sum(d["contributionCount"] for d in w["contributionDays"]) for w in weeks)
    return {"totalContributions": total, "weeks": weeks}


def _level_name(count: int) -> str:
    if count == 0:
        return "NONE"
    if count <= 3:
        return "FIRST_QUARTILE"
    if count <= 6:
        return "SECOND_QUARTILE"
    if count <= 9:
        return "THIRD_QUARTILE"
    return "FOURTH_QUARTILE"


# ─── SVG Generation ──────────────────────────────────────────────────────────

def esc(text: str) -> str:
    """XML-escape text."""
    return saxutils.escape(text)


def generate_game(calendar: dict, username: str) -> str:
    """Generate the complete platformer game SVG."""
    weeks_data = calendar["weeks"]
    total_commits = calendar["totalContributions"]
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Pre-compute weekly totals and max height
    weekly_totals = []
    max_weekly = 1
    for week in weeks_data:
        wt = sum(d["contributionCount"] for d in week["contributionDays"])
        weekly_totals.append(wt)
        max_weekly = max(max_weekly, wt)

    # Grid cells lookup
    all_cells = []
    for col, week in enumerate(weeks_data):
        col_cells = []
        for row, day in enumerate(week["contributionDays"]):
            lvl = _level_name(day["contributionCount"])
            lvl_idx = ["NONE", "FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"].index(lvl)
            col_cells.append({
                "count": day["contributionCount"],
                "level": lvl_idx,
                "x": GRID_LEFT + col * STEP,
                "y": GRID_TOP + row * STEP,
            })
        all_cells.append(col_cells)

    # Terrain heights (column top positions based on weekly total)
    terrain_tops = []
    for col in range(COLS):
        if col < len(weekly_totals):
            ratio = weekly_totals[col] / max_weekly if max_weekly > 0 else 0
            column_height = int(ratio * 60)  # max 60px terrain height
        else:
            column_height = 0
        top = TERRAIN_BASE - column_height
        terrain_tops.append(top)

    # Ghost/coin positions
    ghost_positions = []
    coin_positions = []
    sparkle_positions = []
    for col, week in enumerate(weeks_data):
        for row, day in enumerate(week["contributionDays"]):
            if day["contributionCount"] == 0:
                continue
            cx = GRID_LEFT + col * STEP + CELL_SIZE / 2
            cy = GRID_TOP + row * STEP + CELL_SIZE / 2
            # Ghosts on active cells
            if day["contributionCount"] >= 5 and random.random() < 0.2:
                ghost_positions.append((cx, cy - 4, random.uniform(0, 3), random.uniform(2.5, 4.5)))
            # Coins on high-commit days
            if day["contributionCount"] >= 8:
                coin_positions.append((cx, cy - 8, random.uniform(0, 2)))
            # Sparkles on very active
            if day["contributionCount"] >= 10:
                sparkle_positions.append((cx, cy - 12))

    lines: list[str] = []
    a = lines.append

    # ── SVG HEADER ──
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
      f'width="{CANVAS_W}" height="{CANVAS_H}">')

    # ── STYLES ──
    a("""<defs>
<style>
/* ── Background ── */
.sky { fill: url(#skyGrad); }
.ground-fill { fill: #0d1117; }
.ground-line { fill: none; stroke: #8b5cf6; stroke-width: 1.5; stroke-dasharray: 4,4; }

/* ── Stars ── */
.star { fill: #c4b5fd; }

/* ── Terrain Cells ── */
.cell-0 { fill: #161b22; }
.cell-1 { fill: #0e4429; rx: 1; }
.cell-2 { fill: #006d32; rx: 1; }
.cell-3 { fill: #26a641; rx: 1; }
.cell-4 { fill: #39d353; rx: 1; }

@keyframes cellPulse {
  0%, 100% { opacity: 0.7; }
  50% { opacity: 1; }
}
.cell-active { animation: cellPulse 2s ease-in-out infinite; }

/* ── Ghost Float ── */
@keyframes ghostFloat {
  0%, 100% { transform: translateY(0); opacity: 0.9; }
  50% { transform: translateY(-6px); opacity: 0.4; }
}
.ghost { animation: ghostFloat 3s ease-in-out infinite; }

/* ── Coin Spin ── */
@keyframes coinSpin {
  0%, 100% { transform: scaleY(1); opacity: 1; }
  25% { transform: scaleY(0.3); opacity: 0.6; }
  50% { transform: scaleY(1); opacity: 0.8; }
  75% { transform: scaleY(0.3); opacity: 0.6; }
}
.coin { animation: coinSpin 1.5s ease-in-out infinite; }

/* ── Sparkle ── */
@keyframes sparkle {
  0%, 100% { opacity: 0; transform: scale(0.3); }
  50% { opacity: 1; transform: scale(1.2); }
}
.sparkle { animation: sparkle 1.2s ease-in-out infinite; }

/* ── Character Running ── */
@keyframes charWalk {
  0%, 100% { transform: translateY(0); }
  25% { transform: translateY(-3px); }
  50% { transform: translateY(0); }
  75% { transform: translateY(-2px); }
}
.char-walk { animation: charWalk 0.6s ease-in-out infinite; }

@keyframes charRun {
  0% { transform: translateX(-60px); }
  100% { transform: translateX(920px); }
}
.char-run { animation: charRun 20s linear infinite; }

/* ── Clouds ── */
@keyframes cloudDrift {
  0% { transform: translateX(0); }
  100% { transform: translateX(-120px); }
}
.cloud { animation: cloudDrift 40s linear infinite; }
.cloud-fast { animation: cloudDrift 25s linear infinite; }

/* ── Fog ── */
@keyframes fogDrift {
  0% { transform: translateX(0); opacity: 0.08; }
  50% { opacity: 0.15; }
  100% { transform: translateX(-200px); opacity: 0.08; }
}
.fog { animation: fogDrift 30s linear infinite; }

/* ── Moon Glow ── */
@keyframes moonGlow {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}
.moon-glow { animation: moonGlow 4s ease-in-out infinite; }

/* ── Title Pulse ── */
@keyframes titlePulse {
  0%, 100% { opacity: 0.9; }
  50% { opacity: 1; text-shadow: 0 0 20px #8b5cf6; }
}
.title-pulse { animation: titlePulse 2.5s ease-in-out infinite; }

/* ── HUD Pulse ── */
@keyframes hudPulse {
  0%, 100% { opacity: 0.8; }
  50% { opacity: 1; }
}
.hud-pulse { animation: hudPulse 1.5s ease-in-out infinite; }

/* ── Terrain glow ── */
@keyframes terrainGlow {
  0%, 100% { stop-opacity: 0.3; }
  50% { stop-opacity: 0.7; }
}
.terrain-glow { animation: terrainGlow 3s ease-in-out infinite; }
</style>

<!-- Gradients -->
<linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#0d1117"/>
  <stop offset="40%" stop-color="#131022"/>
  <stop offset="100%" stop-color="#0d1117"/>
</linearGradient>

<radialGradient id="moonGlow" cx="50%" cy="50%" r="50%">
  <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.4"/>
  <stop offset="60%" stop-color="#6d28d9" stop-opacity="0.15"/>
  <stop offset="100%" stop-color="#6d28d9" stop-opacity="0"/>
</radialGradient>

<linearGradient id="groundGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#1a0b2e"/>
  <stop offset="100%" stop-color="#0d1117"/>
</linearGradient>

<!-- Character Sprite (Ghost Hunter) -->
<g id="ghost-hunter">
  <!-- Body -->
  <rect x="-6" y="0" width="12" height="14" rx="3" fill="#8b5cf6"/>
  <rect x="-6" y="0" width="12" height="14" rx="3" fill="none" stroke="#a78bfa" stroke-width="0.5"/>
  <!-- Head -->
  <circle cx="0" cy="-8" r="7" fill="#c4b5fd"/>
  <circle cx="0" cy="-8" r="7" fill="none" stroke="#a78bfa" stroke-width="0.5"/>
  <!-- Hat -->
  <path d="M-10,-12 L10,-12 L12,-18 L-12,-18 Z" fill="#6d28d9"/>
  <rect x="-8" y="-19" width="16" height="3" rx="1" fill="#8b5cf6"/>
  <!-- Eyes -->
  <circle cx="-3" cy="-9" r="1.5" fill="#0d1117"/>
  <circle cx="3" cy="-9" r="1.5" fill="#0d1117"/>
  <!-- Eye shine -->
  <circle cx="-2" cy="-10" r="0.5" fill="#ffffff"/>
  <circle cx="4" cy="-10" r="0.5" fill="#ffffff"/>
  <!-- Legs -->
  <rect x="-5" y="14" width="4" height="5" rx="1" fill="#6d28d9"/>
  <rect x="1" y="14" width="4" height="5" rx="1" fill="#6d28d9"/>
  <!-- Net/Gun -->
  <line x1="8" y1="-4" x2="18" y2="-2" stroke="#a78bfa" stroke-width="1.5"/>
  <circle cx="20" cy="-1" r="3" fill="none" stroke="#fbbf24" stroke-width="1" opacity="0.8"/>
</g>

<!-- Ghost Enemy -->
<g id="ghost-enemy">
  <text text-anchor="middle" dominant-baseline="central" font-size="14">👻</text>
</g>

<!-- Coin -->
<g id="coin-item">
  <text text-anchor="middle" dominant-baseline="central" font-size="10">⭐</text>
</g>

</defs>""")

    # ── LAYER 0: SKY ──
    a(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" class="sky"/>')

    # ── MOON ──
    a(f'<circle cx="780" cy="60" r="50" fill="url(#moonGlow)" class="moon-glow"/>')
    a(f'<circle cx="780" cy="60" r="18" fill="#c4b5fd" opacity="0.9"/>')
    a(f'<circle cx="775" cy="55" r="18" fill="#0d1117" opacity="0.3"/>')  # crescent

    # ── STARS ──
    random.seed(42)
    for i in range(35):
        sx = random.randint(10, CANVAS_W - 10)
        sy = random.randint(5, GRID_TOP - 20)
        sr = random.uniform(0.5, 1.5)
        dur = random.uniform(2, 5)
        delay = random.uniform(0, 3)
        a(f'<circle cx="{sx}" cy="{sy}" r="{sr:.1f}" class="star">'
          f'<animate attributeName="opacity" values="0.15;0.9;0.15" '
          f'dur="{dur:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/>'
          f'</circle>')

    # ── LAYER 1: CLOUDS ──
    cloud_data = [
        (80, 50, 1.0, "cloud"), (250, 35, 0.7, "cloud-fast"),
        (450, 55, 0.8, "cloud"), (650, 30, 0.6, "cloud-fast"),
        (820, 45, 0.9, "cloud"),
    ]
    for cx, cy, scale, cls in cloud_data:
        a(f'<g class="{cls}" transform="scale({scale})" opacity="0.12">'
          f'<circle cx="{cx}" cy="{cy}" r="18" fill="#c4b5fd"/>'
          f'<circle cx="{cx+20}" cy="{cy-5}" r="14" fill="#c4b5fd"/>'
          f'<circle cx="{cx+38}" cy="{cy+2}" r="16" fill="#c4b5fd"/>'
          f'<circle cx="{cx+15}" cy="{cy+5}" r="12" fill="#c4b5fd"/>'
          f'</g>')

    # ── LAYER 2: DISTANT MOUNTAINS ──
    mountains = [
        (0, 100, 1.0), (120, 70, 0.8), (260, 90, 0.9),
        (380, 60, 0.7), (500, 85, 0.8), (620, 50, 0.6),
        (730, 75, 0.7), (840, 95, 0.9),
    ]
    a(f'<g opacity="0.06">')
    for mx, mh, mw in mountains:
        a(f'<polygon points="{mx},{GROUND_Y} {mx+mw*40},{GROUND_Y-mh} {mx+mw*80},{GROUND_Y}" fill="#8b5cf6"/>')
    a(f'</g>')

    # ── LAYER 3: FOG ──
    a(f'<rect x="0" y="{GROUND_Y-20}" width="{CANVAS_W}" height="25" fill="#8b5cf6" class="fog"/>')
    a(f'<rect x="0" y="{GROUND_Y-5}" width="{CANVAS_W}" height="15" fill="#8b5cf6" class="fog" '
      f'style="animation-delay: -10s; animation-duration: 25s;"/>')

    # ── LAYER 4: CONTRIBUTION TERRAIN ──
    # Ground base
    a(f'<rect x="0" y="{GROUND_Y}" width="{CANVAS_W}" height="{CANVAS_H-GROUND_Y}" fill="url(#groundGrad)"/>')
    a(f'<line x1="0" y1="{GROUND_Y}" x2="{CANVAS_W}" y2="{GROUND_Y}" class="ground-line"/>')

    # Draw the contribution grid as terrain columns
    for col in range(min(COLS, len(all_cells))):
        col_cells = all_cells[col]
        terrain_top = terrain_tops[col] if col < len(terrain_tops) else TERRAIN_BASE

        # Draw each cell in column
        for cell in col_cells:
            lvl = min(cell["level"], 4)
            cls = f"cell-{lvl}"
            if cell["count"] >= 8:
                cls += " cell-active"
            a(f'<rect x="{cell["x"]}" y="{cell["y"]}" width="{CELL_SIZE}" '
              f'height="{CELL_SIZE}" class="{cls}"/>')

        # Draw terrain column fill (weeks with high contributions get taller columns)
        if weekly_totals[col] > 0:
            col_height = TERRAIN_BASE - terrain_top
            col_x = GRID_LEFT + col * STEP
            # Decorative side line for the column
            alpha = min(0.3, weekly_totals[col] / max_weekly * 0.3)
            a(f'<line x1="{col_x}" y1="{terrain_top}" x2="{col_x}" y2="{TERRAIN_BASE}" '
              f'stroke="#8b5cf6" stroke-width="1" opacity="{alpha:.2f}"/>')

    # ── LAYER 5: GAME ELEMENTS ──

    # Ghosts (👻) floating above active cells
    for gx, gy, delay, dur in ghost_positions:
        a(f'<g class="ghost" style="animation-delay: {delay:.1f}s; animation-duration: {dur:.1f}s">'
          f'<use href="#ghost-enemy" x="{gx}" y="{gy}"/>'
          f'</g>')

    # Coins (⭐) on high-commit days
    for cx, cy, delay in coin_positions:
        a(f'<g class="coin" style="animation-delay: {delay:.1f}s">'
          f'<use href="#coin-item" x="{cx}" y="{cy}"/>'
          f'</g>')

    # Sparkles
    for sx, sy in sparkle_positions:
        delay = random.uniform(0, 2)
        a(f'<circle cx="{sx}" cy="{sy}" r="2" fill="{GOLD}" class="sparkle" '
          f'style="animation-delay: {delay:.1f}s"/>')
        a(f'<circle cx="{sx-4}" cy="{sy-3}" r="1.5" fill="{CYAN}" class="sparkle" '
          f'style="animation-delay: {delay+0.3:.1f}s"/>')

    # ── CHARACTER ──
    # The character runs along the terrain using animateMotion
    path_parts = []
    for col in range(min(COLS, len(terrain_tops))):
        x = GRID_LEFT + col * STEP + CELL_SIZE / 2
        y = terrain_tops[col] - 25  # character stands on top of terrain
        path_parts.append(f"{x},{y}")
    # Add end position beyond last column
    last_x = GRID_LEFT + min(COLS, len(terrain_tops)) * STEP
    path_parts.append(f"{last_x + 30},{terrain_tops[-1] - 25 if terrain_tops else GROUND_Y - 25}")

    path_d = "M " + " L ".join(path_parts)

    a(f'<path id="char-path" d="{path_d}" fill="none" stroke="none"/>')
    a(f'<g class="char-run">'
      f'<g class="char-walk">'
      f'<use href="#ghost-hunter">'
      f'<animateMotion dur="18s" repeatCount="indefinite">'
      f'<mpath href="#char-path"/>'
      f'</animateMotion>'
      f'</use>'
      f'</g>'
      f'</g>')

    # ── HUD (top overlay) ──

    # Title bar
    a(f'<rect x="20" y="8" width="{CANVAS_W-40}" height="36" rx="8" fill="#0d1117" '
      f'stroke="#8b5cf6" stroke-width="1.5" opacity="0.85"/>')

    a(f'<text x="40" y="31" font-family="system-ui, sans-serif" font-size="16" '
      f'font-weight="900" fill="{PURPLE_LIGHT}" letter-spacing="2" class="title-pulse">'
      f'🎮 GHOST RUNNER</text>')

    # Score display
    a(f'<text x="{CANVAS_W-40}" y="21" font-family="monospace" font-size="11" '
      f'fill="#c4b5fd" text-anchor="end" class="hud-pulse">'
      f'SCORE: {total_commits:,}</text>')

    # Stats bar
    streak = _calculate_streak(weeks_data)
    a(f'<text x="{CANVAS_W-40}" y="35" font-family="monospace" font-size="9" '
      f'fill="{PURPLE_DIM}" text-anchor="end">'
      f'📅 {len(weeks_data)}w · 🔥 {streak}d streak · 👻 {len(ghost_positions)} ghosts</text>')

    # Month labels along the top of the grid
    a(f'<g font-family="monospace" font-size="7" fill="#6b7280">')
    month_labels = _get_month_labels(weeks_data)
    for col_idx, label in month_labels:
        x = GRID_LEFT + col_idx * STEP
        a(f'<text x="{x}" y="{GRID_TOP - 8}">{esc(label)}</text>')
    a(f'</g>')

    # Day labels on the left
    day_labels = ["Mon", "", "Wed", "", "Fri", "", "Sun"]
    for i, label in enumerate(day_labels):
        if label:
            a(f'<text x="{GRID_LEFT - 5}" y="{GRID_TOP + i * STEP + 8}" '
              f'text-anchor="end" font-family="monospace" font-size="7" fill="#6b7280">'
              f'{label}</text>')

    # ── LEGEND ──
    legend_y = GROUND_Y + 18
    a(f'<g font-family="monospace" font-size="8" fill="#6b7280">')
    a(f'<text x="{GRID_LEFT}" y="{legend_y}">Contribution Level:</text>')
    for i in range(5):
        lx = GRID_LEFT + 120 + i * 50
        a(f'<rect x="{lx}" y="{legend_y-7}" width="8" height="8" class="cell-{i}"/>')
        labels = ["None", "Low", "Med", "High", "Max"]
        a(f'<text x="{lx+11}" y="{legend_y}">{labels[i]}</text>')
    a(f'</g>')

    # ── FOOTER ──
    a(f'<text x="{CANVAS_W//2}" y="{CANVAS_H-8}" text-anchor="middle" '
      f'font-family="monospace" font-size="8" fill="#374151">'
      f'github.com/{esc(username)} · Updated {esc(now_str)}</text>')

    a("</svg>")
    return "\n".join(lines)


def _calculate_streak(weeks_data: list) -> int:
    """Calculate current contribution streak (consecutive days with commits)."""
    streak = 0
    for week in reversed(weeks_data):
        for day in reversed(week["contributionDays"]):
            if day["contributionCount"] > 0:
                streak += 1
            elif streak > 1:
                return streak
            else:
                streak = 0
    return streak


def _get_month_labels(weeks_data: list) -> list[tuple[int, str]]:
    """Extract month labels for the x-axis."""
    labels: list[tuple[int, str]] = []
    prev_month = ""
    for col, week in enumerate(weeks_data):
        if not week["contributionDays"]:
            continue
        date_str = week["contributionDays"][0]["date"]
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            month = dt.strftime("%b")
            if month != prev_month:
                labels.append((col, month))
                prev_month = month
        except ValueError:
            pass
    return labels


# ─── Main ────────────────────────────────────────────────────────────────────

def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Generate Ghost Runner platformer game SVG")
    parser.add_argument("--username", default="Abi-de-jo", help="GitHub username")
    parser.add_argument("--output", default="assets/ghost-runner.svg", help="Output SVG path")
    parser.add_argument("--token", default=None, help="GitHub token")
    args = parser.parse_args()

    print(f":: Fetching contributions for {args.username} ...", file=sys.stderr)
    calendar = fetch_contributions(args.username, args.token)
    total = calendar["totalContributions"]
    print(f":: {total:,} total contributions found", file=sys.stderr)

    print(":: Generating Ghost Runner game SVG ...", file=sys.stderr)
    svg = generate_game(calendar, args.username)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg)
    size = os.path.getsize(args.output)
    print(f":: Written to {args.output} ({size:,} bytes)", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
