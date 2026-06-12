#!/usr/bin/env python3
"""
OPERATION: GRID STRIKE — Military Game SVG Generator
Generates an animated military-themed contribution grid game SVG.

Usage:
    python generate-game.py --username Abi-de-jo [--output dist/game.svg] [--token ghp_xxx]

The output SVG shows the contribution grid as a battlefield with:
  - A tactical HUD overlay (military command center style)
  - Contribution cells rendered as captured territory / military assets
  - Animated "troop advance" line sweeping across the grid
  - Pulsing objectives and marching soldier markers
  - Dark night-vision / tactical green aesthetic
"""

import json
import os
import sys
import argparse
from datetime import datetime, timezone
from xml.sax.saxutils import escape as xml_escape

# ─── GitHub API ──────────────────────────────────────────────────────────────

GRAPHQL_QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            date
            color
            weekday
          }
        }
      }
    }
  }
}
"""


def fetch_contributions(username: str, token: str | None = None) -> dict:
    """Fetch contribution calendar data from GitHub GraphQL API."""
    token = token or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print("::warning::No GitHub token found. Using mock data for preview.", file=sys.stderr)
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
        print(f"::warning::Failed to fetch contributions: {e}", file=sys.stderr)
        return _mock_data()


def _mock_data() -> dict:
    """Generate mock contribution data for local preview."""
    from random import randint
    from datetime import timedelta

    weeks = []
    today = datetime.now(timezone.utc)
    # Generate 52 weeks
    for w in range(52):
        days = []
        for d in range(7):
            date = today - timedelta(weeks=52 - w, days=6 - d)
            count = randint(0, 12)
            days.append({
                "contributionCount": count,
                "date": date.strftime("%Y-%m-%d"),
                "color": _level_color(count),
                "weekday": d,
            })
        weeks.append({"contributionDays": days})
    return {"totalContributions": 1276, "weeks": weeks}


def _level_color(count: int) -> str:
    if count == 0:
        return "#161b22"
    if count <= 3:
        return "#0e4429"
    if count <= 6:
        return "#006d32"
    if count <= 9:
        return "#26a641"
    return "#39d353"


# ─── SVG Generator ───────────────────────────────────────────────────────────

# Layout constants
CELL_SIZE = 13
CELL_GAP = 3
GRID_LEFT = 100
GRID_TOP = 110
ROWS = 7
WEEKS_MAX = 53
SVG_WIDTH = GRID_LEFT + WEEKS_MAX * (CELL_SIZE + CELL_GAP) + 40
SVG_HEIGHT = 380

MONTHS = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAYS = ["", "Mon", "", "Wed", "", "Fri", ""]


def generate_game_svg(calendar: dict, username: str) -> str:
    """Generate the military-themed game SVG from contribution data."""
    weeks_data = calendar["weeks"]
    total_commits = calendar["totalContributions"]

    # Calculate max contribution for normalization
    all_counts = [
        d["contributionCount"]
        for w in weeks_data
        for d in w["contributionDays"]
    ]
    max_count = max(all_counts) if all_counts else 1

    # Collect month labels (first week of each month)
    month_labels = []
    for i, w in enumerate(weeks_data):
        first_day = w["contributionDays"][0]
        month_num = int(first_day["date"][5:7])
        day_num = int(first_day["date"][8:10])
        if day_num <= 7:
            month_labels.append((i, MONTHS[month_num]))

    # SVG parts
    cells = []
    soldier_animations = []
    explosions = []

    total_committed = 0
    week_totals = []

    for wi, w in enumerate(weeks_data):
        if wi >= WEEKS_MAX:
            break
        week_sum = 0
        for di, d in enumerate(w["contributionDays"]):
            count = d["contributionCount"]
            level = min(count // 3 + (1 if count > 0 else 0), 4)
            x = GRID_LEFT + wi * (CELL_SIZE + CELL_GAP)
            y = GRID_TOP + di * (CELL_SIZE + CELL_GAP)

            # Cell background with military-style fill
            fill = "#161b22"
            if level >= 1:
                fill = "#1a4a1a"
            if level >= 2:
                fill = "#0d5e0d"
            if level >= 3:
                fill = "#0a7a0a"
            if level >= 4:
                fill = "#05a805"

            # Cell rectangle
            rx = 2
            if level > 0:
                cells.append(
                    f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" '
                    f'rx="{rx}" fill="{fill}" '
                    f'class="cell cell-l{level}" '
                    f'data-count="{count}" data-date="{d["date"]}" />'
                )
                # Inner glow for active cells
                if level >= 2:
                    cells.append(
                        f'<rect x="{x + 2}" y="{y + 2}" width="{CELL_SIZE - 4}" height="{CELL_SIZE - 4}" '
                        f'rx="1" fill="none" stroke="#4aff4a" stroke-width="0.5" '
                        f'stroke-opacity="0.4" class="glow-{level}" />'
                    )

                # Soldiers / military markers on high-contribution cells
                if level >= 3:
                    cx = x + CELL_SIZE // 2
                    cy = y + CELL_SIZE // 2
                    # Small soldier icon (simplified)
                    cells.append(
                        f'<circle cx="{cx}" cy="{cy - 1}" r="1.5" fill="#aaffaa" '
                        f'class="soldier soldier-w{wi}" opacity="0.9" />'
                    )
                if level >= 4:
                    cx = x + CELL_SIZE // 2
                    cy = y + CELL_SIZE // 2
                    # Star / objective marker
                    cells.append(
                        f'<text x="{cx}" y="{cy + 1.5}" text-anchor="middle" '
                        f'fill="#ffff4a" font-size="7" font-family="monospace" '
                        f'class="objective obj-w{wi}">&#9733;</text>'
                    )
            else:
                cells.append(
                    f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" '
                    f'rx="{rx}" fill="{fill}" class="cell cell-0" />'
                )

            week_sum += count
            total_committed += count

        week_totals.append(week_sum)

    # Month labels
    month_svg = ""
    for wi, label in month_labels:
        x = GRID_LEFT + wi * (CELL_SIZE + CELL_GAP)
        month_svg += f'<text x="{x}" y="{GRID_TOP - 15}" fill="#8b949e" font-size="9" font-family="monospace">{xml_escape(label)}</text>'

    # Day labels
    day_svg = ""
    day_labels_short = ["", "Mon", "", "Wed", "", "Fri", ""]
    for di, label in enumerate(day_labels_short):
        if label:
            y = GRID_TOP + di * (CELL_SIZE + CELL_GAP) + CELL_SIZE - 2
            day_svg += f'<text x="{GRID_LEFT - 25}" y="{y}" fill="#8b949e" font-size="9" font-family="monospace">{label}</text>'

    # The animated "front line" sweep
    scan_line = f'''
    <rect x="{GRID_LEFT - 5}" y="{GRID_TOP - 5}" width="3" height="{ROWS * (CELL_SIZE + CELL_GAP) + 5}"
          fill="#4aff4a" opacity="0.15" class="scan-line" rx="1" />
    '''

    # Military HUD Header
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d %H:%M UTC")

    hud_header = f'''
    <g font-family="monospace">
      <rect x="15" y="15" width="{SVG_WIDTH - 30}" height="50" rx="4" fill="#0a0e14" stroke="#1a4a1a" stroke-width="1" opacity="0.9" />
      <text x="30" y="38" fill="#4aff4a" font-size="11" font-weight="bold" letter-spacing="2">OPERATION: GRID STRIKE</text>
      <text x="30" y="54" fill="#8b949e" font-size="9">CLASSIFIED // TACTICAL COMMIT ANALYSIS</text>
      <text x="{SVG_WIDTH - 200}" y="38" fill="#4aff4a" font-size="9" text-anchor="end">AGENT: {xml_escape(username)}</text>
      <text x="{SVG_WIDTH - 200}" y="54" fill="#8b949e" font-size="8" text-anchor="end">STATUS: ACTIVE // {date_str}</text>
    </g>
    '''

    # Stats bar
    streak = _calculate_streak(weeks_data)
    avg_weekly = total_commits // max(len(weeks_data), 1)

    stats_bar = f'''
    <g font-family="monospace">
      <rect x="15" y="72" width="{SVG_WIDTH - 30}" height="24" rx="2" fill="#0d1117" stroke="#1a4a1a" stroke-width="0.5" opacity="0.9" />
      <text x="25" y="87" fill="#4aff4a" font-size="9">&#9654; TOTAL COMMITS: {total_commits:,}</text>
      <text x="250" y="87" fill="#4aff4a" font-size="9">&#9654; AVG/WEEK: {avg_weekly}</text>
      <text x="450" y="87" fill="#4aff4a" font-size="9">&#9654; STREAK: {streak}d</text>
      <text x="620" y="87" fill="#4aff4a" font-size="9">&#9654; THEATER: CONTRIBUTION GRID</text>
    </g>
    '''

    # Footer
    footer = f'''
    <g font-family="monospace">
      <text x="{SVG_WIDTH // 2}" y="{SVG_HEIGHT - 15}" fill="#30363d" font-size="8" text-anchor="middle">
        GENERATED BY COMMAND // github.com/{xml_escape(username)}/{xml_escape(username)}
      </text>
    </g>
    '''

    # Legend
    legend = f'''
    <g font-family="monospace" transform="translate(15, {GRID_TOP + ROWS * (CELL_SIZE + CELL_GAP) + 25})">
      <text x="0" y="0" fill="#8b949e" font-size="9">LEGEND:</text>
      <rect x="60" y="-8" width="10" height="10" rx="1" fill="#161b22" /><text x="75" y="1" fill="#8b949e" font-size="8">DARK</text>
      <rect x="120" y="-8" width="10" height="10" rx="1" fill="#1a4a1a" /><text x="135" y="1" fill="#8b949e" font-size="8">OUTPOST</text>
      <rect x="195" y="-8" width="10" height="10" rx="1" fill="#0d5e0d" /><text x="210" y="1" fill="#8b949e" font-size="8">GARRISON</text>
      <rect x="275" y="-8" width="10" height="10" rx="1" fill="#0a7a0a" /><text x="290" y="1" fill="#8b949e" font-size="8">FORTRESS</text>
      <rect x="355" y="-8" width="10" height="10" rx="1" fill="#05a805" /><text x="370" y="1" fill="#8b949e" font-size="8">HQ</text>
      <text x="430" y="1" fill="#8b949e" font-size="8">|</text>
      <circle cx="455" cy="-3" r="3" fill="#aaffaa" /><text x="462" y="1" fill="#8b949e" font-size="8">TROOPS</text>
      <text x="515" y="1" fill="#ffff4a" font-size="8">&#9733; OBJECTIVE</text>
    </g>
    '''

    # CSS Animations
    css = '''
    <style>
      @keyframes scanSweep {
        0% { transform: translateX(0px); opacity: 0.1; }
        50% { opacity: 0.25; }
        100% { transform: translateX(700px); opacity: 0.05; }
      }
      @keyframes pulse {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 1; }
      }
      @keyframes march {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-1.5px); }
        100% { transform: translateY(0px); }
      }
      @keyframes glow {
        0%, 100% { stroke-opacity: 0.2; }
        50% { stroke-opacity: 0.7; }
      }
      .scan-line {
        animation: scanSweep 8s ease-in-out infinite;
      }
      .cell { transition: fill 0.3s; }
      .soldier {
        animation: march 1.2s ease-in-out infinite;
        mix-blend-mode: screen;
      }
      .objective {
        animation: pulse 2s ease-in-out infinite;
      }
      .glow-3 { animation: glow 2.5s ease-in-out infinite; }
      .glow-4 { animation: glow 1.8s ease-in-out infinite; }
    </style>
    '''

    # Background
    background = f'<rect width="{SVG_WIDTH}" height="{SVG_HEIGHT}" fill="#0d1117" />'

    # Grid background
    grid_bg = f'''
    <rect x="{GRID_LEFT - 8}" y="{GRID_TOP - 8}"
          width="{WEEKS_MAX * (CELL_SIZE + CELL_GAP) + 16}"
          height="{ROWS * (CELL_SIZE + CELL_GAP) + 16}"
          rx="4" fill="#0a0e14" stroke="#1a4a1a" stroke-width="0.5" />
    '''

    # Compose SVG
    svg = f'''<svg width="{SVG_WIDTH}" height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}"
     xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="Operation Grid Strike - Military contribution game for {username}">
  <desc>Military-themed contribution grid game showing {total_commits:,} commits across the contribution calendar as a tactical battlefield map.</desc>
{css}
{background}
{grid_bg}
{hud_header}
{stats_bar}
{month_svg}
{day_svg}
{"".join(cells)}
{scan_line}
{legend}
{footer}
</svg>'''

    return svg


def _calculate_streak(weeks_data: list) -> int:
    """Calculate current contribution streak (consecutive days with >0 commits)."""
    streak = 0
    for w in reversed(weeks_data):
        for d in reversed(w["contributionDays"]):
            if d["contributionCount"] > 0:
                streak += 1
            else:
                return streak
    return streak


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate military contribution game SVG")
    parser.add_argument("--username", default="Abi-de-jo", help="GitHub username")
    parser.add_argument("--output", default="dist/game.svg", help="Output SVG path")
    parser.add_argument("--token", default=None, help="GitHub token")
    args = parser.parse_args()

    print(f":: Fetching contributions for {args.username} ...", file=sys.stderr)
    calendar = fetch_contributions(args.username, args.token)

    print(f":: Generating military game SVG ({calendar['totalContributions']:,} commits) ...", file=sys.stderr)
    svg = generate_game_svg(calendar, args.username)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f":: Written to {args.output} ({os.path.getsize(args.output):,} bytes)", file=sys.stderr)
    print(f":: SVG_WIDTH={SVG_WIDTH} SVG_HEIGHT={SVG_HEIGHT}", file=sys.stderr)


if __name__ == "__main__":
    main()
