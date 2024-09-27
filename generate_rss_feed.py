import re
from urllib.parse import urljoin
import httpx
from bs4 import BeautifulSoup
from datetime import datetime

TITLE = "Rene Hlavova: Expeditions"
AUTHOR = "Rene Hlavova"
SITE_URL = "https://expeditions.renehlavova.com/"


def extract_site_data() -> BeautifulSoup:
    result = httpx.get("https://expeditions.renehlavova.com/")
    return BeautifulSoup(result.text, "html.parser")


def parse_site_metadata(soup: BeautifulSoup) -> dict:
    description_raw = soup.select_one("div[data-context='page.masthead'] p.main-text")

    if description_raw:
        description = description_raw.text

    return {
        "title": TITLE,
        "link": SITE_URL,
        "description": description,
    }


def parse_posts(soup: BeautifulSoup) -> list[dict]:
    """
    Extracts data from the Expeditions website for RSS feed.
    """
    data = []

    posts = soup.select("a.project-cover")

    for post in posts:
        path = post["href"]
        post_url = urljoin(SITE_URL, path)

        post_title_raw = post.select_one("div.title")
        post_title = post_title_raw.text if post_title_raw else "No title"

        post_date_raw = post.select_one("div.date")
        post_date = post_date_raw.text if post_date_raw else "January, 1970"
        post_iso_date = datetime.strptime(post_date, "%B, %Y").isoformat()

        post_tags_raw = post.select_one("div.description")
        post_tags = post_tags_raw.text if post_tags_raw else "No tags"

        post_image_raw = post.select_one("img")
        post_image = (
            post_image_raw["data-src"] if post_image_raw else "//unsplash.it/200"
        )

        post_text = httpx.get(post_url)
        post_text_soup = BeautifulSoup(post_text.text, "html.parser")
        post_description_raw = post_text_soup.select_one(
            "div.page-content div.rich-text"
        )
        post_description = (
            post_description_raw.text if post_description_raw else "No description"
        )
        post_description_re = re.sub(
            " {2,}", " ", re.sub(r"(?<=[.])(?=[^\s])", r" ", post_description)
        )

        data.append(
            {
                "title": post_title,
                "link": post_url,
                "description": post_description_re,
                "date": post_iso_date,
                "image": post_image,
                "tags": post_tags,
            }
        )

    return data


def generate_rss_feed(site_metadata: dict, posts: list[dict]) -> str:
    rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
        <channel>
            <title>{site_metadata["title"]}</title>
            <link>{site_metadata["link"]}</link>
            <description>{site_metadata["description"]}</description>
    """

    for post in posts:
        rss_feed += f"""
            <item>
                <title>{post["title"]}</title>
                <link>{post["link"]}</link>
                <description>{post["description"]}</description>
                <author>{AUTHOR}</author>
                <pubDate>{post["date"]}</pubDate>
                <enclosure url="{post["image"]}" type="image/jpeg" />
                <guid isPermaLink="false">{post["link"]}</guid>
            </item>
        """

    rss_feed += """</channel></rss>"""

    return rss_feed


if __name__ == "__main__":
    data = extract_site_data()
    site_metadata = parse_site_metadata(data)
    posts = parse_posts(data)
    rss_feed = generate_rss_feed(site_metadata, posts)

    with open("rss.xml", "w") as f:
        f.write(rss_feed)
