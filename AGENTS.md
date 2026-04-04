# Shared Agent Guide

This file is the canonical shared project instructions for Codex, Claude Code, and Gemini CLI.

Keep project-wide guidance here. Keep tool-specific leftovers in `CLAUDE.md` or `GEMINI.md` only when they should not apply to the other agents.

## Migration Notes

This file was expanded during migration so no existing guidance was lost. Review the imported sections below and move any truly tool-specific leftovers back into `CLAUDE.md` or `GEMINI.md` only after the shared rules are stable.

## Project Guidance

This guidance was carried forward from the previous `CLAUDE.md` so the shared guide starts with the repository's existing conventions.

## Project Overview

Gas City Hall website (gascityhall.com) — the community hub for Gas City, a customizable AI agent orchestration platform. Art Deco Phase 3 aesthetic (1920s-1930s: chrome, glass, neon, warm amber undertones). Evolved from the Gas Town Hall site (gastownhall.ai).

## Commands

- `npm run dev` — start dev server
- `npm run build` — typecheck + build to `./deploy/`
- `npm run preview` — preview production build locally
- `npm run deploy` — build + deploy to Cloudflare Pages via wrangler

## Architecture

**Astro 5 static site** deployed to Cloudflare Pages. No client-side framework — pages are static HTML with one client-side script (leaderboard fetch).

### Deployment

Pushing to `main` triggers an automatic build and deploy to gascityhall.com via Cloudflare Pages (GitHub integration). Manual deploy is also available via `npm run deploy` (requires `wrangler login` first). The Cloudflare Pages project name is `gch-website`.

### Key files

- `site.config.json` — all site metadata, social links, analytics config, and blog post entries. Components import this directly. To add a blog post, add an entry here.
- `astro.config.mjs` — Astro config. Build output goes to `./deploy/`.
- `src/layouts/BaseLayout.astro` — single layout wrapping all pages. Contains the full CSS design system (custom properties, global styles), header, footer, Google Fonts, Plausible analytics, OG/Twitter meta tags, JSON-LD structured data, and SEO meta tags.
- `src/components/` — Hero, WastelandLeaderboard, CityWire (blog), Community sections.
- `src/pages/` — index, about, privacy, terms, rss.xml.
- `public/_headers` — Cloudflare Pages security headers and cache control.
- `public/robots.txt` — search engine crawling directives.

### Design system

All CSS is centralized in `BaseLayout.astro`. The `<style is:global>` block contains:

- **Custom properties** (`:root`) — palette (`--gc-gold`, `--gc-chrome`, `--gc-blue`, etc.), fonts (`--font-display: Cinzel`, `--font-body: Raleway`), spacing
- **Shared layout classes** — `.container`, `.glass-panel`, `.deco-divider`, `.section-title`, `.section-subtitle`
- **Page layout** — `.page`, `.page-panel`, `.page-panel h2/p`, `.updated` (used by about, privacy, terms)
- **Button system** — `.btn` (base), `.btn-primary`, `.btn-secondary`, `.btn-outline`
- **Responsive breakpoints** — mobile overrides at 768px

Components use scoped `<style>` blocks only for component-specific styles (e.g. team grid, leaderboard table). Do not duplicate base layout, button, or page styles in component files — they belong in BaseLayout.

The Wasteland Leaderboard uses `<style is:global>` because its DOM is built client-side via JavaScript, so Astro's scoped style attributes aren't applied to those elements. All leaderboard global selectors are scoped under the `.leaderboard` class to prevent leaking.

### Dynamic content

The Wasteland Leaderboard fetches from `https://wasteland.gastownhall.ai/api/scoreboard` client-side. It builds DOM nodes programmatically (no innerHTML) and shows table on desktop, cards on mobile.

### Images

Static images in `public/images/`. Web-optimized source images come from the gas-city-inc repo. Use the global `optimize-image-web` skill when batch-optimizing source PNGs from a JSON spec file.

Blog thumbnails are in `public/images/blog/` and referenced by path in `site.config.json`.

### Project skills

This repo has a project-local `add-content` skill in `.claude/skills/add-content/` for adding new Steve Yegge Medium posts. It updates `site.config.json` and downloads matching thumbnails into `public/images/blog/`.
