---
name: CodeByAbi Developer Game World
description: A playable developer workbench rendered as crisp animated game UI.
colors:
  void: "#080b13"
  panel: "#0d111f"
  panel-raised: "#111827"
  rule: "#303950"
  text: "#f4f7ff"
  text-muted: "#8491a8"
  phosphor-mint: "#7df9c2"
  electric-violet: "#b98cff"
  screen-amber: "#ffd166"
  alert-coral: "#ff7a8a"
typography:
  display:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    fontWeight: 700
    letterSpacing: "0.08em"
  body:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    fontWeight: 400
  label:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    fontWeight: 700
    letterSpacing: "0.16em"
rounded:
  panel: "18px"
  tile: "0px"
spacing:
  xs: "8px"
  sm: "16px"
  md: "28px"
  lg: "40px"
components:
  game-panel:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.text}"
    rounded: "{rounded.panel}"
    padding: "{spacing.lg}"
  portal:
    backgroundColor: "{colors.panel-raised}"
    textColor: "{colors.text}"
    rounded: "{rounded.tile}"
    height: "64px"
---

# Design System: CodeByAbi Developer Game World

## Overview

**Creative North Star: "The Playable Developer Workbench"**

The profile is one continuous developer game world rather than a stack of unrelated badges or generated banners. Every surface looks like part of the same late-night build session: crisp pixel geometry, terminal-like information density, small animated systems, and clear routes into real work.

The world is playful but useful. Visitors should understand Abi's role, projects, activity, and contact paths without decoding the theme. Motion communicates activity and progress; it never replaces readable content.

**Key Characteristics:**

- Ink-black layered surfaces with four sparse signal colors.
- Crisp one-pixel rules, pixel characters, and authored vector icons.
- Monospaced HUD typography with strong size and weight steps.
- Continuous game language across hero, portals, missions, data, and contribution history.
- GitHub-safe SVG motion with a complete reduced-motion fallback.

## Colors

The palette behaves like a dark game console: neutral space dominates while each signal color owns a clear system role.

### Primary

- **Phosphor Mint:** Identity, progress, success, live status, and primary paths.

### Secondary

- **Electric Violet:** Code, repositories, secondary progress, and navigation paths.

### Tertiary

- **Screen Amber:** Systems, security, attention, and measured energy.
- **Alert Coral:** Enemies, testing, message actions, and active warnings.

### Neutral

- **Void:** The deepest page and end-screen field.
- **Panel:** Large HUD and data surfaces.
- **Raised Panel:** Portals and mission tiles.
- **Rule:** Dividers, tracks, and panel outlines.
- **Console White:** Primary headings and values.
- **Muted Telemetry:** Supporting labels and metadata.

**The Signal Discipline Rule.** Signal colors label meaning; they do not become decorative gradients or full-surface washes.

## Typography

**Display Font:** UI monospace with SFMono, Menlo, and Consolas fallbacks

**Body Font:** UI monospace with the same platform fallbacks

**Label/Mono Font:** The same stack, tightened through scale and expanded tracking

**Character:** The single-family system feels like a coherent game HUD. Hierarchy comes from size, weight, case, spacing, and color rather than from mixing decorative typefaces.

### Hierarchy

- **Display:** Heavy uppercase statements for the hero and end screen.
- **Headline:** Bold uppercase titles for major game systems.
- **Title:** Compact mission and portal names.
- **Body:** Sentence-case project descriptions and plain-language context.
- **Label:** Small uppercase telemetry with generous tracking for categories and statuses.

**The HUD Legibility Rule.** Expanded tracking belongs to short labels only; project descriptions and actionable names stay compact enough to scan on mobile.

## Layout

The README is a single centered vertical route. Full-width 1200-unit SVG panels establish the main rhythm, while the four portals form a compact two-by-two control cluster. Major systems are separated with deliberate breathing room and remain in the same reading order on desktop and mobile.

Responsive behavior comes from fluid SVG view boxes and percentage widths, not separate compositions. Essential copy is embedded at sizes that remain legible when the profile narrows, and linked text below the mission board preserves accessible navigation even when the artwork is scaled down.

## Elevation & Depth

The system is intentionally flat. Depth comes from nested dark tones, thin rules, selective glows inside illustrated screens, and overlapping game objects—not from card shadows or glass blur.

**The Console Layer Rule.** Use tonal separation and one-pixel structure for hierarchy; do not add ambient card shadows or translucent glass.

## Shapes

Large system panels use gently curved 18px corners. Interactive portals and mission tiles use clipped lower-right corners and crisp polygonal outlines, which distinguishes actions from passive containers. Icons use authored geometric strokes with consistent visual weight; emoji and borrowed glyphs do not belong in the world.

## Components

### Game World Panel

The opening panel combines player HUD, role, current quest, animated desk hardware, avatar, enemies, and circuit terrain. It owns the strongest scale and the richest motion.

### Portals

Four linked controls use the same 220-by-64 geometry, a distinct signal color, a drawn icon, a small action verb, and a plain destination name. They stay in a two-column grid on narrow screens.

### Quest Map

The journey is a single animated path from idea through interface, systems, and test to ship. It communicates process without turning the page into a generic step-card sequence.

### Mission Select

Real repositories appear as four game missions. Each tile carries a drawn icon, truthful technology/category label, project name, short factual description, and state.

### Player Data and Commit Raid

Player Data shows a small verified public-profile snapshot and updates through the repository workflow. Commit Raid renders the annual contribution history as a battle matrix with its own legend, status HUD, and reduced-motion fallback.

## Do's and Don'ts

### Do:

- **Do** keep every new section inside the same developer-game vocabulary.
- **Do** use real repositories, verified public counts, and generated contribution data.
- **Do** author SVG icons and motion with readable static and reduced-motion states.
- **Do** preserve the direct route from project art to working GitHub links.

### Don't:

- **Don't** reintroduce badge walls, unrelated stats services, or standalone generated hero art.
- **Don't** mix glassmorphism, gradients, soft dashboard cards, or generic portfolio templates into the console world.
- **Don't** invent employers, awards, clients, metrics, or project outcomes.
- **Don't** let animation change an object's base coordinates or cover readable text.
