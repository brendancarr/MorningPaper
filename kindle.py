import os
import shutil


def detect_kindle():

    for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

        root = drive + ":\\"

        if not os.path.exists(root):
            continue


        # Kindle has a documents folder
        if os.path.exists(
            root + "documents"
        ):

            return root


    return None



def copy_to_kindle(file_path, gui=None):

    kindle = detect_kindle()


    if not kindle:

        raise Exception(
            "Kindle not detected"
        )


    destination = os.path.join(
        kindle,
        "documents",
        os.path.basename(file_path)
    )


    if gui:
        gui.log(
            f"Copying to Kindle: {destination}"
        )


    shutil.copy2(
        file_path,
        destination
    )


    return destination