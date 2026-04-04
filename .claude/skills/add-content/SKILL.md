---
name: add-content
description: "Add new Steve Yegge Medium posts to the Gas City Hall website. Use when Steve has published new Medium posts, the user says 'add content' or 'add blog post', or asks to update the City Wire section."
---

# Add Content to Gas City Hall

Add new Steve Yegge Medium posts to the site by updating `site.config.json` and downloading blog images.

## Workflow

### 1. Identify New Content

Compare the latest posts on `https://steve-yegge.medium.com/` against existing entries in `site.config.json` `blogPosts`.

Posts already present in `site.config.json` do not need to be added again.

### 2. Extract Metadata

For each missing Medium post, collect:

- **Title**: Use the Medium post title exactly.
- **Date**: Use the published date from Medium. If Medium only shows a relative date such as `1 day ago`, resolve it against the current date before writing `site.config.json`.
- **URL**: Use the canonical `https://steve-yegge.medium.com/...` post URL.
- **Description**: Use the Medium listing snippet or the first substantive paragraph. Keep it to one or two sentences.
- **Lead image URL**: Use the post thumbnail or hero image from Medium's listing page.

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

Save each image to `public/images/blog/` using the same kebab-case filename referenced in `site.config.json`.

Example:

```bash
curl -sL -o public/images/blog/gas-town-from-clown-show-to-v1-0.jpg "<medium_image_url>"
```

### 5. Verify

Run `npm run build` or `npm run dev` and confirm the City Wire section renders the new cards and loads the new images correctly.
