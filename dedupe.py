import hashlib


def remove_duplicates(articles):

    seen = set()
    results = []

    for article in articles:

        key = hashlib.md5(
            (
                article["title"]
                .lower()
                .encode("utf-8")
            )
        ).hexdigest()


        if key in seen:
            continue


        seen.add(key)
        results.append(article)


    return results