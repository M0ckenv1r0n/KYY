import customtkinter as ctk

from src.gui.start_screen import StartScreen
from src.gui.notification_frame import Notif
from src.gui.info_screen import InfoScreen

from src.config.settings import *
from src.gui.chat_screen import ChatScreen
from src.utils.youtube_utils import get_transcript
from config.logging_config import logger
from src.handlers.chat_gpt_handler import ChatGPTHandler


class App(ctk.CTk):
    def __init__(self) -> None:
        # setup
        super().__init__()
        ctk.set_appearance_mode('Dark')
        self.geometry('800x500')#1100x600
        self.title('KYY')
        self.minsize(800, 500)
        self.config(background='#0e0f0f')

        # Core layout configuration
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        # Initial screen layout
        self.start_screen = StartScreen(self, self.on_login_success)

    def on_login_success(self, username: str, api_key: str) -> None:
        self.api_key = api_key

        # Call YouTube scrap in order to get transcript, available_video_count and cum_video_count using the username
        logger.info(f"Scrap attempt for {username}")
        scrap_response = get_transcript(username)

        self.transcript = scrap_response[0]
        available_video_count = scrap_response[1]
        cum_video_count = scrap_response[2]

        logger.info(f"Transripts for {username} successfully scraped")

        success_notification = Notif(self, "positive", "Successfully")

        # Show the InfoScreen and hide the StartScreen
        self.settings_screen = InfoScreen(
            self, username, available_video_count, cum_video_count, self.proceed_to_chat)
        self.start_screen.place_forget()

    def proceed_to_chat(self, username: str) -> None:
        logger.info(
            f"Transitioning to ChatScreen with username: {username}")

        # Generate the system prompt
        # get_system_prompt from settings.py
        system_prompt = get_system_prompt(username)

        # Initialize ChatGPTHandler
        chat_handler = ChatGPTHandler(
            system_prompt=system_prompt,
            api_key=self.api_key
        )

        chat_handler.add_to_context("user", self.transcript)

        # Transition to the main chat screen
        self.llm_chat_screen = ChatScreen(self, chat_handler)
        self.settings_screen.place_forget()

    def run(self) -> None:
        logger.info("App mainloop running.")
        self.mainloop()
        logger.info("Application is now closed.")


if __name__ == "__main__":
    app = App()
    app.run()
