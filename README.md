# `expeditions-adobe-portfolio-rss`

RSS feed generator for my photo travel blog hosted on Adobe Portfolio.

## How this works

### Generate RSS feed

`generate_rss_feed.py` serves for extracting the data for RSS feed and converting it to `rss.xml` file.

- `extract_site_data()`: Scrapes the website.
- `parse_site_metadata(soup)`: Finds website title, link, and description.
- `parse_posts(soup)`: Scrapes the posts and finds title, link, description, date, image, and tags.
- `generate_rss_feed(site_metadata, posts)`: Combines data together as a RSS feed.

This code is setup to be triggered **manually** using `generate_rss.yml` Github Action.
The Github Action runs the code and creates a PR that can be reviewed and merged, if all looks good.

### Deploy to Cloudflare pages

The Github Action `deploy.yml` deploys the RSS feed to Cloudflare pages.
