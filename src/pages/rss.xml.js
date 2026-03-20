import rss from "@astrojs/rss";
import siteConfig from "../../site.config.json";

export function GET(context) {
  return rss({
    title: `${siteConfig.site.name} Blog`,
    description: siteConfig.site.description,
    site: context.site || siteConfig.site.url,
    items: siteConfig.blogPosts.map((post) => ({
      title: post.title,
      description: post.description,
      link: post.url,
      pubDate: new Date(post.date),
    })),
    customData: `<language>en-us</language>`,
  });
}
