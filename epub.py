from ebooklib import epub
from datetime import datetime
from pathlib import Path
import os


def create_epub(articles):

    book = epub.EpubBook()

    book.set_identifier(
        "morning-paper"
    )

    book.set_title(
        "Morning Paper - Daily Edition"
    )

    book.add_author(
        "The Discontinued Kindle Project"
    )

    book.add_metadata(
        "DC",
        "publisher",
        "Morning Paper"
    )

    book.add_metadata(
        "DC",
        "description",
        "A personal daily news edition generated for Kindle."
    )
        
    book.set_language(
        "en"
    )


    #
    # CSS
    #

    style = epub.EpubItem(
        uid="style",
        file_name="style.css",
        media_type="text/css",
        content="""

        body {
            font-family: serif;
            line-height: 1.4;
        }

        h1 {
            text-align:center;
        }

        h2 {
            margin-top:25px;
        }

        h3 {
            margin-bottom:5px;
            margin-top: 0px;
            line-height: 20px;
        }

        .headline {
            overflow:hidden;
            margin-bottom:20px;
            border-bottom:1px solid #999;
            padding-bottom:15px;
        }
        .headline a {
            text-decoration:none;
        }

        .thumbnail {
            float:left;
            width:120px;
            height:90px;
            object-fit:cover;
            margin-right:15px;
        }

        .meta {
            font-size:0.9em;
        }

        .article-image {
            width:100%;
            max-width:758px;
        }

        """
    )

    book.add_item(style)


    #
    # Add images to EPUB
    #

    image_map = {}


    for article in articles:

        if not article.get("local_images"):
            continue


        image_path = Path(
            article["local_images"][0]
        )


        if not image_path.exists():
            continue


        filename = image_path.name


        with open(
            image_path,
            "rb"
        ) as f:

            image = epub.EpubImage()

            image.file_name = (
                "images/"
                + filename
            )

            image.media_type = (
                "image/jpeg"
            )

            image.content = f.read()


            book.add_item(
                image
            )


            image_map[
                str(image_path)
            ] = (
                "images/"
                + filename
            )



    #
    # Landing page
    #

    cover = epub.EpubHtml(
        title="Morning Paper",
        file_name="index.xhtml",
        lang="en"
    )


    cover.add_item(style)


    html = f"""

    <html>

    <body>


    <h1>
    Morning Paper
    </h1>


    <h3>
    {datetime.now().strftime('%B %d, %Y')}
    </h3>


    <hr>


    <h2>
    Today's Headlines
    </h2>

    """


    for index, article in enumerate(articles[:10]):

        image_html = ""


        if article.get("local_images"):

            path = str(
                Path(
                    article["local_images"][0]
                )
            )


            if path in image_map:

                image_html = f"""

                <img
                class="thumbnail"
                src="{image_map[path]}"
                />

                """


        html += f"""

        <div class="headline">

        <a href="article_{index}.xhtml">

        {image_html}

        <h3>
        {article['title']}
        </h3>

        <div class="meta">

        {article.get('source','')}

        <br>

        {article.get('date','')}

        </div>

        </a>

        </div>

        """


    html += """

    </body>

    </html>

    """


    cover.content = html


    book.add_item(
        cover
    )


    #
    # Article chapters
    #

    chapters = []


    for index, article in enumerate(articles):

        chapter = epub.EpubHtml(

            title=article["title"],

            file_name=f"article_{index}.xhtml",

            lang="en"

        )


        chapter.add_item(style)


        image_html = ""


        if article.get("local_images"):

            path = str(
                Path(
                    article["local_images"][0]
                )
            )


            if path in image_map:

                image_html = f"""

                <img
                class="article-image"
                src="{image_map[path]}"
                />

                """



        chapter.content = f"""

        <html>

        <body>


        {image_html}


        <h1>
        {article['title']}
        </h1>


        <h3>
        {article.get('source','')}
        </h3>


        <p>
        {article.get('date','')}
        </p>


        <hr>


        <p>
        {article['body'].replace(chr(10), '<br><br>')}
        </p>


        </body>

        </html>

        """


        book.add_item(
            chapter
        )


        chapters.append(
            chapter
        )



    #
    # Table of contents
    #

    book.toc = [
        cover
    ] + chapters



    book.spine = [
        "nav",
        cover
    ] + chapters



    book.add_item(
        epub.EpubNcx()
    )

    book.add_item(
        epub.EpubNav()
    )


    os.makedirs(
        "output",
        exist_ok=True
    )


    output = (
        "output/"
        "morning-paper.epub"
    )


    epub.write_epub(
        output,
        book
    )


    return output