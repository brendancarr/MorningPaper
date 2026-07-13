import trafilatura
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from images import download_image
from database import (
    get_article,
    save_article
)

def extract_article(article, gui=None):

    cached = get_article(
        article["url"]
    )
    if cached:

        if gui:
            gui.log(
                f"CACHED: {article['title']}"
            )

        return {

            "url": cached[1],
            "title": cached[2],
            "source": cached[3],
            "date": cached[4],
            "body": cached[5],
            "local_images":
                [cached[6]]
        }

    title = article.get("title", "Unknown")

    try:

        if gui:
            gui.log(f"Extracting START: {title[:80]}")


        response = requests.get(
            article["url"],
            timeout=20,
            headers={
                "User-Agent": "Mozilla/5.0 MorningPaper/1.0"
            }
        )


        if response.status_code != 200:

            if gui:
                gui.log(
                    f"SKIP {title}: HTTP {response.status_code}"
                )

            return None


        downloaded = response.text
        article["images"] = find_images(
            downloaded,
            article["url"]
        )

        article["local_images"] = []

        for image in article["images"]:

            local = download_image(
                image
            )

            if local:
                article["local_images"].append(
                    local
                )
                
        text = trafilatura.extract(
            downloaded,
            include_images=False,
            include_tables=False,
            favor_precision=True
        )


        if not text:

            if gui:
                gui.log(
                    f"NO CONTENT: {title[:80]}"
                )

            return None


        article["body"] = text


        if gui:
            gui.log(
                f"Extracting DONE: {title[:80]} ({len(text)} chars)"
            )

        save_article(article)

        return article


    except requests.exceptions.Timeout:

        if gui:
            gui.log(
                f"TIMEOUT: {title[:80]}"
            )

        return None


    except Exception as e:

        if gui:
            gui.log(
                f"ERROR {title[:80]}: {e}"
            )

        return None

def find_images(html, article_url):

    soup = BeautifulSoup(
        html,
        "lxml"
    )

    images = []


    # normal images
    for img in soup.find_all("img"):

        src = (
            img.get("src")
            or img.get("data-src")
            or img.get("data-original")
        )

        if src:

            images.append(
                urljoin(
                    article_url,
                    src
                )
            )


    # OpenGraph image (usually the hero image)
    og = soup.find(
        "meta",
        property="og:image"
    )

    if og and og.get("content"):

        images.insert(
            0,
            urljoin(
                article_url,
                og["content"]
            )
        )


    return images[:3]

def extract_all(articles, gui):

    results = []

    total = len(articles)

    for index, article in enumerate(articles, 1):

        gui.log(
            f"[{index}/{total}]"
        )

        result = extract_article(
            article,
            gui
        )

        if result:
            results.append(result)


    return results


from bs4 import BeautifulSoup
from urllib.parse import urljoin


def extract_images(html, base_url):

    soup = BeautifulSoup(
        html,
        "lxml"
    )

    images = []

    for img in soup.find_all("img"):

        src = (
            img.get("src")
            or
            img.get("data-src")
        )

        if not src:
            continue

        url = urljoin(
            base_url,
            src
        )

        images.append(url)


    return images[:5]