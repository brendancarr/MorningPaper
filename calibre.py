import os
import subprocess


def detect_calibre():

    paths = [
        r"C:\Program Files\Calibre2\ebook-convert.exe",
        r"C:\Program Files\Calibre\ebook-convert.exe",
        r"C:\Program Files (x86)\Calibre2\ebook-convert.exe"
    ]

    for path in paths:

        if os.path.exists(path):
            return path

    return None



def convert_to_azw3(epub_file, gui=None):

    calibre = detect_calibre()

    if not calibre:

        raise Exception(
            "Calibre ebook-convert.exe not found"
        )


    output = epub_file.replace(
        ".epub",
        ".azw3"
    )


    if gui:
        gui.log(
            "Converting EPUB to AZW3..."
        )


    result = subprocess.run(
        [
            calibre,
            epub_file,
            output,
            "--authors",
            "The Discontinued Kindle Project",
            "--publisher",
            "Morning Paper",
            "--title",
            "Morning Paper Daily Edition"
        ],
        capture_output=True,
        text=True
    )


    if result.returncode != 0:

        raise Exception(
            result.stderr
        )


    return output