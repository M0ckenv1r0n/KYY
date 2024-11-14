import customtkinter as ctk

from ..utils.validation import valid_username, check_api
from ..config.settings import *
from config.logging_config import logger
from .notification_frame import Notif

class StartScreen(ctk.CTkFrame):
    def __init__(self, parent, on_login_success) -> None:
        super().__init__(master=parent, fg_color=DARK_GREY, corner_radius=0)
        self.parent = parent
        self.on_login_success = on_login_success
        self._init_ui()  # UI initialization

    def _init_ui(self) -> None:
        self.place_configure(relx=0.5, rely=0.5,
                             anchor=ctk.CENTER, width=730, height=380)

        self.h1 = ctk.CTkLabel(self, text="Choose YouTube channel!", font=(
            FONT_REGULAR, 38), text_color=WHITE)
        self.h1.place(relx=0.36, rely=0.15, anchor=ctk.CENTER)

        self.yt_label = ctk.CTkLabel(
            self, text="https://www.youtube.com/@", text_color=LIGHT_GREY, font=(FONT_REGULAR, 24))
        self.yt_label.place(relx=0.26, rely=0.37, anchor=ctk.CENTER)

        self.username_entry = ctk.CTkEntry(
            self, border_width=0, fg_color=GREY, corner_radius=6, width=240, height=42, font=(FONT_REGULAR, 16))
        self.username_entry.place(relx=0.65, rely=0.38, anchor=ctk.CENTER)

        self.openai_label = ctk.CTkLabel(
            self, text="Enter your OpenAi key:", text_color=LIGHT_GREY, font=(FONT_REGULAR, 24))
        self.openai_label.place(relx=0.245, rely=0.59, anchor=ctk.CENTER)

        self.openai_entry = ctk.CTkEntry(self, border_width=0, fg_color=GREY,
                                         corner_radius=6, width=240, height=42, font=(FONT_REGULAR, 16), show="*")
        self.openai_entry.place(relx=0.65, rely=0.6, anchor=ctk.CENTER)

        self.error_usr_msg = ctk.CTkLabel(
            self, text="", text_color=PAS_RED, fg_color='transparent', font=(FONT_REGULAR, 12))
        self.error_usr_msg.place(relx=0.65, rely=0.48, anchor=ctk.CENTER)

        self.error_api_msg = ctk.CTkLabel(
            self, text="", text_color=PAS_RED, fg_color='transparent', font=(FONT_REGULAR, 12))
        self.error_api_msg.place(relx=0.65, rely=0.70, anchor=ctk.CENTER)

        self.go_btn = ctk.CTkButton(self, text='Let\'s GO!', border_color=CLOSE_RED, border_width=2, command=self.check_inputs,
                                    fg_color=CLOSE_RED, hover_color=DARK_GREY, corner_radius=6, text_color=WHITE,
                                    font=(FONT_REGULAR, 16), height=46, width=132)
        self.go_btn.place(relx=0.85, rely=0.825, anchor=ctk.CENTER)


    # Check credentials and pass them back to the main app via callback
    def check_inputs(self) -> None:
        username = self.username_entry.get().strip()
        api_key = self.openai_entry.get().strip()

        if not username:
            self.show_username_error("Username cannot be empty.")
            return

        if not valid_username(username):
            self.show_username_error("Invalid username.")
            return

        if not api_key:
            self.show_api_error("API key cannot be empty.")
            return

        if not check_api(api_key):
            self.show_api_error("Invalid API key.")
            return
        
        try:
            self.on_login_success(username, api_key)

        except Exception as e:
            logger.error("An Unexpected Error Occurred | " + e)
            unsuccess_notification = Notif(self.parent, "negative", "An Unexpected Error Occurred")


    def show_username_error(self, message="Invalid username") -> None:
        # Display error message
        self.error_usr_msg.configure(text=message)
        self.username_entry.configure(border_width=1, border_color=PAS_RED)

    def show_api_error(self, message="Invalid OpenAi API key") -> None:
        self.error_api_msg.configure(text=message)
        self.openai_entry.configure(border_width=1, border_color=PAS_RED)
