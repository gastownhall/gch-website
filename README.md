# Gas City Hall

Community hub website for [Gas City](https://github.com/gastownhall/gascity), a fully customizable orchestration layer for AI coding agents.

Live at [gascityhall.com](https://gascityhall.com).

## Setup

```bash
npm install
npm run dev
```

## Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server |
| `npm run build` | Typecheck + build to `./deploy/` |
| `npm run preview` | Preview production build locally |
| `npm run deploy` | Build + deploy to Cloudflare Pages |

## Stack

- [Astro 5](https://astro.build) — static site generator
- [Cloudflare Pages](https://pages.cloudflare.com) — hosting
- [Plausible](https://plausible.io) — privacy-focused analytics

## Configuration

All site metadata, social links, analytics config, and blog post entries live in [`site.config.json`](site.config.json). To add a blog post, add an entry there.

## License

Community project. See repository for details.
