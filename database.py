import sqlite3
import os


DB = "morningpaper.db"


def get_connection():

    return sqlite3.connect(DB)



def init_db():

    db = get_connection()

    cursor = db.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (

        id INTEGER PRIMARY KEY,

        url TEXT UNIQUE,

        title TEXT,

        source TEXT,

        date TEXT,

        body TEXT,

        image TEXT,

        created DATETIME DEFAULT CURRENT_TIMESTAMP

    )
    """)


    db.commit()
    db.close()



def get_article(url):

    db = get_connection()

    cur = db.cursor()

    cur.execute(
        """
        SELECT *
        FROM articles
        WHERE url=?
        """,
        (url,)
    )

    row = cur.fetchone()

    db.close()

    return row



def save_article(article):

    db = get_connection()

    cur = db.cursor()


    cur.execute(
        """
        INSERT OR REPLACE INTO articles
        (
            url,
            title,
            source,
            date,
            body,
            image
        )
        VALUES (?,?,?,?,?,?)
        """,
        (
            article["url"],
            article["title"],
            article["source"],
            article.get("date",""),
            article["body"],
            article.get(
                "local_images",
                [None]
            )[0]
        )
    )


    db.commit()
    db.close()