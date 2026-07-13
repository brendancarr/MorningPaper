import feedparser
import requests
from config import (ARTICLE_LIMIT, RSS)

def get_articles(gui):

    articles = []

    for source, url in RSS.items():

        if not gui.vars[source].get():
            continue

        gui.log("")
        gui.log(f"Loading feed: {source}")
        gui.log(url)

        try:

            response = requests.get(
                url,
                timeout=15,
                headers={
                    "User-Agent": "MorningPaper/1.0"
                }
            )

            feed = feedparser.parse(
                response.content
            )

            gui.log(
                f"{source}: received {len(feed.entries)} entries"
            )

            for item in feed.entries[:ARTICLE_LIMIT]:

                title = item.get(
                    "title",
                    "NO TITLE"
                )

                link = item.get(
                    "link",
                    ""
                )

                gui.log(
                    f"  + {title}"
                )

                articles.append({

                    "source": source,
                    "title": title,
                    "url": link,
                    "date": item.get(
                        "published",
                        ""
                    )

                })


            gui.log(
                f"{source}: complete"
            )


        except Exception as e:

            gui.log(
                f"{source} ERROR: {e}"
            )


    gui.log(
        f"Total feed articles: {len(articles)}"
    )

    return articles