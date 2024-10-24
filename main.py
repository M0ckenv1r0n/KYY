from settings import *
from chat_window import MainChatFrame
from yt_scrap import get_transcript
import customtkinter as ctk
from tkinter import font
import scrapetube
from openai import OpenAI
import logging
from typing import Literal


# Initialize logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# Check if the provided username corresponds to a valid YouTube channel.
def valid_username(username: str) -> bool:
    try:
        videos = list(scrapetube.get_channel(
        content_type='videos', channel_username=username,limit=1))
        if videos:
            logging.info("YouYube credentials are valid!")
            return True
    except Exception as e:
        logging.error(f"Error retrieving videos: {e}")
        return False

    '''Solution that accepts also channel_url and channel_id, but ineffective coz username is used later'''
    # for param in ['channel_url', 'channel_username', 'channel_id']:
    #     try:
    #         videos = list(scrapetube.get_channel(
    #             content_type='videos', **{param: username}, limit=1))
    #         if videos:
    #             logging.info("YouYube credentials are valid!")
    #             return True
    #     except Exception as e:
    #         logging.error(f"Error retrieving videos with {param}: {e}")
    # return False


# Validate the OpenAI API key by checking the available models.
def check_api(openai_key: str) -> bool:
    try:
        client = OpenAI(api_key=openai_key)
        client.models.list()
        logging.info("API key is valid!")
        return True
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return False


class StartScreen(ctk.CTkFrame):
    def __init__(self, parent, on_login_success) -> None:
        super().__init__(master=parent, fg_color=DARK_GREY, corner_radius=0)
        self.parent = parent
        self.on_login_success = on_login_success
        self._init_ui()  # UI initialization

    def _init_ui(self) -> None:
        # Configure screen
        self.place_configure(relx=0.5, rely=0.5,
                             anchor=ctk.CENTER, width=730, height=380)

        self.h1 = ctk.CTkLabel(self, text="Choose YouTube channel!", font=(
            FONT_REGULAR, 38), text_color=WHITE)
        self.h1.place(relx=0.36, rely=0.15, anchor=ctk.CENTER)

        self.yt_label = ctk.CTkLabel(
            self, text="https://www.youtube.com/", text_color=LIGHT_GREY, font=(FONT_REGULAR, 24))
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
        
        
        self.on_login_success(username, api_key)
        # If credentials are valid, proceed
        try:
            pass

        except Exception as e:
            logging.error(e)
            unsuccess_notification = Notif(self.parent, "negative", "An Unexpected Error Occurred")


    def show_username_error(self, message="Invalid username") -> None:
        # Display error message
        self.error_usr_msg.configure(text=message)
        self.username_entry.configure(border_width=1, border_color=PAS_RED)

    def show_api_error(self, message="Invalid OpenAi API key") -> None:
        self.error_api_msg.configure(text=message)
        self.openai_entry.configure(border_width=1, border_color=PAS_RED)


# Reusable notification frame
class Notif(ctk.CTkFrame):
    def __init__(self, parent, sentiment: Literal["positive", "negative"], text: str) -> None:
        background_colour = PAS_GREEN if sentiment == "positive" else PAS_RED

        super().__init__(master=parent, fg_color=background_colour,
                         corner_radius=15, border_width=0)
        self.place_configure(relx=0.99, rely=0.01,
                             anchor=ctk.NE, width=200, height=75)
        self.label = ctk.CTkLabel(
            self, text=text, text_color=DARK_GREY, font=(FONT_REGULAR, 16))
        self.label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.after(10000, lambda: self.place_forget()) #Hide notification after 10s

# Secondary frame for SettingsScreen


class TerminalLikeBox(ctk.CTkFrame):
    def __init__(self, parent, available_video_count: int, cum_video_count: int) -> None:
        super().__init__(master=parent, fg_color=DARK_DARK_GREY, corner_radius=0)
        self.place_configure(relx=0.5, rely=0.48,
                             anchor=ctk.CENTER, width=600, height=150)

        self.terminal_element = ctk.CTkFrame(self, width=630, height=50, fg_color=GREY, corner_radius=0).place_configure(
            relx=0.5, rely=0, anchor=ctk.CENTER)
        self.title = ctk.CTkLabel(self, text="TERMINAL@KYY/root",
                                  text_color=LIGHT_GREY,
                                  font=(FONT_REGULAR, 12), fg_color=GREY).place(relx=0.02, rely=0.075, anchor=ctk.W)

        self.label1 = ctk.CTkLabel(self, text=f"root@kyy: {cum_video_count} videos successfuly scraped",
                                   text_color=LIGHT_GREY,
                                   font=(FONT_REGULAR, 18)).place(relx=0.02, rely=0.3, anchor=ctk.W)

        self.label2 = ctk.CTkLabel(self, text=f"root@kyy: {available_video_count} videos available for inclusion\n",
                                   text_color=LIGHT_GREY,
                                   font=(FONT_REGULAR, 18)).place(relx=0.02, rely=0.55, anchor=ctk.W)

        self.label3 = ctk.CTkLabel(self, text="in the context window.",
                                   text_color=LIGHT_GREY,
                                   font=(FONT_REGULAR, 18)).place(relx=0.02, rely=0.65, anchor=ctk.W)


class SettingsScreen(ctk.CTkFrame):
    def __init__(self, parent, username: str, available_video_count: int, cum_video_count: int, proceed_to_chat) -> None:
        super().__init__(master=parent, fg_color=DARK_GREY, corner_radius=0)
        self.proceed_to_chat = proceed_to_chat
        self.parent = parent
        self.username = username

        self.place_configure(relx=0.5, rely=0.5,
                             anchor=ctk.CENTER, width=730, height=320)

        self.h1 = ctk.CTkLabel(self, text=f"You Chose {username}!", font=(
            FONT_REGULAR, 38), text_color=WHITE,
            corner_radius=50).place(relx=0.07, rely=0.13, anchor=ctk.W)

        terminal_box = TerminalLikeBox(
            self, available_video_count, cum_video_count)

        # self.label4 = ctk.CTkLabel(self, text="Choose the amount of videos you want to include:",
        #                            text_color=WHITE,
        #                            font=(FONT_REGULAR, 18)).place(relx=0.1, rely=0.7, anchor=ctk.W)
        # self.validate_command = self.register(self.validate_input)

        # self.videos_num_entry = ctk.CTkEntry(self, validate="key", validatecommand=(
        #     self.validate_command, '%P'), border_width=0, fg_color=GREY, corner_radius=6, width=150, height=38, font=(FONT_REGULAR, 18))
        # self.videos_num_entry.place(relx=0.7, rely=0.7, anchor=ctk.W)

        # self.slider = ctk.CTkSlider(self, from_=0, to=10, button_color=PAS_GREEN, number_of_steps =10,
        #                             button_hover_color=PAS_GREEN_LIGHT).place(relx=0.65, rely=0.6, anchor=ctk.CENTER)

        # Button to trigger the transition to another screen

        self.go_btn = ctk.CTkButton(self, text='Let\'s GO!', border_color=CLOSE_RED, border_width=2,
                                    fg_color=CLOSE_RED, hover_color=DARK_GREY, command=self.go_next_screen,
                                    corner_radius=6, text_color=WHITE,
                                    font=(FONT_REGULAR, 16), height=46, width=132).place(relx=0.85, rely=0.86, anchor=ctk.CENTER)

    def go_next_screen(self) -> None:
        logging.info(f"{self.username} pressed 'Go' on SettingsScreen.")

        # Notify the parent app to transition
        self.proceed_to_chat(self.username)

    # def check_num(self):
    #     num = self.videos_num_entry

    # def validate_input(self, value):

    #     if value.isdigit() or value == "":
    #         return True
    #     elif value.count('.') == 1 and value.replace('.', '').isdigit():
    #         return True
    #     return False


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
        logging.info("Scrap attempt for {username}")
        scrap_response = get_transcript(username)

        self.transcript = scrap_response[0]
        available_video_count = scrap_response[1]
        cum_video_count = scrap_response[2]

        logging.info(f"Transripts for {username} successfully scraped")

        success_notification = Notif(self, "positive", "Successfully")

        # Show the SettingsScreen and hide the StartScreen
        self.settings_screen = SettingsScreen(
            self, username, available_video_count, cum_video_count, self.proceed_to_chat)
        self.start_screen.place_forget()

    def proceed_to_chat(self, username: str) -> None:
        logging.info(
            f"Transitioning to MainChatFrame with username: {username}")

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
        self.llm_chat_screen = MainChatFrame(self, chat_handler)
        self.settings_screen.place_forget()

    def run(self) -> None:
        logging.info("App mainloop running.")
        self.mainloop()
        logging.info("Application is now closed.")


class ChatGPTHandler:
    def __init__(self, api_key: str, system_prompt: str) -> None:
        self.client = OpenAI(api_key=api_key)
        self.conversation_context = [
            {"role": "system", "content": system_prompt}]

    def add_to_context(self, role: str, content: str) -> None:
        self.conversation_context.append({"role": role, "content": content})

    def send_request(self, user_message: str, model: str = "gpt-4o-mini", temperature: float = 1.0) -> str:
        # Add the user message to the conversation context
        self.add_to_context("user", user_message)

        response = self.client.chat.completions.create(
            model=model,
            messages=self.conversation_context,
            temperature=temperature

        )

        assistant_message = response.choices[0].message.content

        self.add_to_context("assistant", assistant_message)

        return assistant_message.replace("\n", "")


if __name__ == "__main__":
    app = App()
    app.run()
