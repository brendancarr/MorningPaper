import customtkinter as ctk
import threading

from kindle import detect_kindle
from calibre import detect_calibre
from config import RSS

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class MorningPaper(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Morning Paper")
        self.geometry("700x650")

        self.build_ui()

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Morning Paper",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(pady=15)

        self.sources = ctk.CTkFrame(self)
        self.sources.pack(fill="x", padx=20)

        self.vars = {}

        for source in RSS:

            v = ctk.BooleanVar(value=True)
            self.vars[source] = v

            ctk.CTkCheckBox(
                self.sources,
                text=source,
                variable=v
            ).pack(anchor="w", padx=15, pady=2)

        self.status = ctk.CTkTextbox(self, height=180)
        self.status.pack(fill="both", expand=True, padx=20, pady=20)

        self.progress = ctk.CTkProgressBar(self)
        self.progress.pack(fill="x", padx=20)
        self.progress.set(0)

        self.button = ctk.CTkButton(
            self,
            text="Build Newspaper",
            command=self.build
        )
        self.button.pack(pady=20)

        self.log("Searching for Kindle...")
        self.log(detect_kindle())

        self.log("Searching for Calibre...")
        self.log(detect_calibre())

    def log(self, text):

        self.after(
            0,
            lambda: self._log(text)
        )


    def _log(self, text):

        self.status.insert(
            "end",
            text + "\n"
        )

        self.status.see(
            "end"
        )

    def set_progress(self, value):

        self.after(
            0,
            lambda: self.progress.set(value)
        )

    def build(self):

        self.button.configure(
            state="disabled"
        )

        self.progress.set(0)

        thread = threading.Thread(
            target=self.run_build,
            daemon=True
        )

        thread.start()


    def run_build(self):

        try:

            from newspaper import build_newspaper

            build_newspaper(self)

        except Exception as e:

            self.log(
                f"ERROR: {e}"
            )

        finally:

            self.button.configure(
                state="normal"
            )