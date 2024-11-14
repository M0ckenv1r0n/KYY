from ..config.settings import *
from config.logging_config import logger
import customtkinter as ctk



class InfoScreen(ctk.CTkFrame):
    def __init__(self, parent, username: str, available_video_count: int, cum_video_count: int, proceed_to_chat) -> None:
        super().__init__(master=parent, fg_color=DARK_GREY, corner_radius=0)
        self.proceed_to_chat = proceed_to_chat
        self.parent = parent
        self.username = username
        self.place_configure(relx=0.5, rely=0.5,
                             anchor=ctk.CENTER, width=730, height=320)
        
        self._init_ui(username, available_video_count, cum_video_count)  # UI initialization

    def _init_ui(self, username: str, available_video_count: int, cum_video_count: int) -> None:

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