from gui import MorningPaper
from database import init_db

if __name__ == "__main__":

    init_db()

    app = MorningPaper()
    app.mainloop()