# The Discontinued Kindle Project
A Morning Newspaper for your Kindle. Is your old Kindle not able to access the Amazon Store anymore? Turn it into your morning newspaper!

# Requirements

python 3x
customtkinter
feedparser
trafilatura
beautifulsoup4
ebooklib
requests
lxml

# How to Use

1. Plug in your kindle, make sure it has a drive letter, and there should be a documents folder inside it that contains whatever leftover books are still on it.
2. Run the app! It will create a database file to cache articles (feel free to delete it anytime). 
3. Pick your sources using the checkboxes. Currently there is CBC, BBC, Nasa, and Ars Technica - you can edit those in your config.py file, and in future releases I'll add the ability to do this in the GUI.
4. Click the build newspaper button, and it will download and transfer everything. 

# Running the app

Either run it from the command line, or download the latest release. Sorry, I only compiled for Windows.
```
py morningpaper.py
```

