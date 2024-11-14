from ..config.settings import *
from config.logging_config import logger
import customtkinter as ctk
from typing import Literal


# Reusable notification frame
class Notif(ctk.CTkFrame):
    def __init__(self, parent, sentiment: Literal["positive", "negative"], text: str) -> None:
        background_colour = PAS_GREEN if sentiment == "positive" else PAS_RED

        super().__init__(master=parent, fg_color=background_colour, border_width=0)
        self.place_configure(relx=0.99, rely=0.01,
                             anchor=ctk.NE, width=200, height=70)
        self.label = ctk.CTkLabel(
            self, text=text, text_color=DARK_GREY, font=(FONT_REGULAR, 20))
        self.label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Hide notification after 10s
        self.after(10000, lambda: self.place_forget())
