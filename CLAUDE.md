# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Gas City Hall website (gascityhall.com) — the community hub for Gas City, a customizable AI agent orchestration platform. Art Deco Phase 3 aesthetic (1920s-1930s: chrome, glass, neon, warm amber undertones). Evolved from the Gas Town Hall site (gastownhall.ai).

## Commands

- `npm run dev` — start dev server
- `npm run build` — typecheck + build to `./deploy/`
- `npm run preview` — preview production build locally

## Architecture

**Astro 5 static site** deployed to Cloudflare Pages. No client-side framework — pages are static HTML with one client-side script (leaderboard fetch).

### Key files

- `site.config.json` — all site metadata, social links, analytics config, and blog post entries. Components import this directly. To add a blog post, add an entry here.
- `astro.config.mjs` — Astro config. Build output goes to `./deploy/`.
- `src/layouts/BaseLayout.astro` — single layout wrapping all pages. Contains the full CSS design system (custom properties, global styles), header, footer, Google Fonts, Plausible analytics, and OG/Twitter meta tags.
- `src/components/` — Hero, WastelandLeaderboard, CityWire (blog), Community sections.
- `src/pages/` — index, about, faq, privacy, terms.

### Design system

All CSS custom properties live in `BaseLayout.astro` under `:root`. The palette (`--gc-gold`, `--gc-chrome`, `--gc-blue`, etc.), fonts (`--font-display: Poiret One`, `--font-body: Raleway`), and shared classes (`.glass-panel`, `.deco-divider`, `.section-title`, `.container`) are defined there. Components use scoped `<style>` blocks.

### Dynamic content

The Wasteland Leaderboard fetches from `https://wasteland.gastownhall.ai/api/scoreboard` client-side. It builds DOM nodes programmatically (no innerHTML) and shows table on desktop, cards on mobile.

### Images

Static images in `public/images/`. Web-optimized source images come from the gas-city-inc repo. The `.claude/skills/web-image-optimize/` skill handles batch optimization from source PNGs via a JSON spec file.

Blog thumbnails are in `public/images/blog/` and referenced by path in `site.config.json`.
