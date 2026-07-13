from feeds import get_articles
from articles import extract_all
from epub import create_epub
from dedupe import remove_duplicates
from calibre import convert_to_azw3
from kindle import copy_to_kindle

def build_newspaper(gui):

    gui.log(
        "Fetching RSS..."
    )


    feeds=get_articles(gui)


    gui.set_progress(.25)


    gui.log(
        f"{len(feeds)} articles found"
    )


    gui.log(
        "Extracting articles..."
    )


    articles=extract_all(
        feeds,
        gui
    )

    articles = remove_duplicates(
        articles
    )

    gui.set_progress(.65)


    gui.log(
        f"{len(articles)} articles extracted"
    )


    gui.log(
        "Creating EPUB..."
    )


    epub=create_epub(
        articles
    )

    gui.log(
        "Creating Kindle version..."
    )


    azw3 = convert_to_azw3(
        epub,
        gui
    )


    gui.log(
        f"Created {azw3}"
    )


    copy_to_kindle(
        azw3,
        gui
    )


    gui.log(
        "Copied to Kindle!"
    )

    gui.set_progress(1)


    gui.log(
        f"Created {epub}"
    )