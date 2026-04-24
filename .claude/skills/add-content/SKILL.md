---
name: add-content
description: "Add new Medium and Sells Brothers posts to the Gas City Hall website. Use when new markdown files appear in docs-fodder/steve-blog-posts/ or docs-fodder/sellsbrothers-posts/, Steve has published new Medium posts, the user says 'add content' or 'add blog post', or asks to update the City Wire section."
---

# Add Content to Gas City Hall

Add new Medium and Sells Brothers posts to the site by updating `site.config.json` and downloading blog images.

## Workflow

### 1. Identify New Content

Compare the latest posts on `https://steve-yegge.medium.com/`, plus local captures in `docs-fodder/sellsbrothers-posts/*.md`, against existing entries in `site.config.json` `blogPosts`.

Posts already present in `site.config.json` do not need to be added again.

### 2. Extract Metadata

For each missing Medium post, collect:

- **Title**: Use the Medium post title exactly.
- **Date**: Use the published date from Medium. If Medium only shows a relative date such as `1 day ago`, resolve it against the current date before writing `site.config.json`.
- **URL**: Use the canonical `https://steve-yegge.medium.com/...` post URL.
- **Description**: Use the Medium listing snippet or the first substantive paragraph. Keep it to one or two sentences.
- **Lead image URL**: Use the post thumbnail or hero image from Medium's listing page.

If a clean Markdown file is available from the user-scope `medium-to-markdown` skill, prefer it over scraping/listing metadata:

```bash
python ~/.claude/skills/medium-to-markdown/scripts/medium_to_markdown.py \
  "https://steve-yegge.medium.com/post-slug-id" \
  --frontmatter \
  -o /tmp/medium-post.md
```

For `medium-to-markdown --frontmatter` files:

- **Title**: YAML `title`
- **Date**: YAML `date` (`YYYY-MM-DD`), converted to `Mon D, YYYY`
- **URL**: YAML `source`
- **Description**: First substantive paragraph after the frontmatter, skipping headings, images, and blank lines
- **Lead image URL**: First `![...](<url>)` image in the post body

For Sells Brothers posts, generate a local RSS-derived capture first:

```bash
python ~/.claude/skills/sellsbrothers-to-markdown/scripts/sellsbrothers_to_markdown.py \
  "https://sellsbrothers.com/post-slug" \
  --frontmatter \
  -o "docs-fodder/sellsbrothers-posts/Post Title.md"
```

For `sellsbrothers-to-markdown --frontmatter` files:

- **Title**: YAML `title`
- **Date**: YAML `date` (`YYYY-MM-DD`), converted to `Mon D, YYYY`
- **URL**: YAML `source`
- **Description**: First substantive paragraph after the frontmatter, skipping headings, images, and blank lines
- **Lead image URL**: First `![...](<url>)` image in the post body

### 3. Update `site.config.json`

Add new entries to the `blogPosts` array and keep them in newest-first order.

Each entry should look like:

```json
{
  "title": "The Title",
  "url": "https://...",
  "description": "One to two sentence description.",
  "date": "Apr 3, 2026",
  "image": "/images/blog/kebab-case-title.jpg"
}
```

Rules:

- **date format**: `Mon D, YYYY`
- **image path**: `/images/blog/` + kebab-case title + `.jpg`

### 4. Download Images

Save each image to `public/images/blog/` using the same kebab-case filename referenced in `site.config.json`. Medium image URLs may be from `miro.medium.com` or `cdn-images-1.medium.com`; Sells Brothers image URLs are usually from `cdn.blot.im`.

Example:

```bash
curl -sL -o public/images/blog/gas-town-from-clown-show-to-v1-0.jpg "<medium_image_url>"
```

### 5. Verify

Run `npm run build` or `npm run dev` and confirm the City Wire section renders the new cards and loads the new images correctly.
