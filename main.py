import customtkinter as ctk
from settings import *
import customtkinter as ctk
from PIL import Image
from tkinter import font
import scrapetube
import openai

def valid_username(username):
        for param in ['channel_url', 'channel_username', 'channel_id']:
            try:
                videos = list(scrapetube.get_channel(
                    content_type='videos', **{param: username}, limit=1))
                if videos:
                    return True
            except Exception as e:
                print(f"Failed with {param}: {e}")
        return False

def check_api(openai_key):
    client = openai.OpenAI(api_key=openai_key)
    try:
        client.models.list()
        print("API key is valid!")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


class StartScreen(ctk.CTkFrame):
    successfuly = False
    username = ''

    def __init__(self, parent):

        super().__init__(master=parent, fg_color=DARK_GREY, corner_radius=0)
        self.parent = parent
        self.place_configure(relx=0.5, rely=0.5,
                             anchor=ctk.CENTER, width=730, height=380)

        self.h1 = ctk.CTkLabel(self, text="Choose YouTube channel!", font=(
            FONT_REGULAR, 38), text_color=WHITE)
        self.h1.place(relx=0.36, rely=0.15, anchor=ctk.CENTER)

        self.yt_label = ctk.CTkLabel(self, text="https://www.youtube.com/",
                                     text_color=LIGHT_GREY,
                                     font=(FONT_REGULAR, 24))
        self.yt_label.place(relx=0.26, rely=0.37, anchor=ctk.CENTER)

        self.username_entry = ctk.CTkEntry(self, border_width=0, fg_color=GREY,
                                           corner_radius=6, width=240, height=42,
                                           font=(FONT_REGULAR, 16))
        self.username_entry.place(relx=0.65, rely=0.38, anchor=ctk.CENTER)

        self.openai_label = ctk.CTkLabel(self, text="Enter your OpenAi key:",
                                         text_color=LIGHT_GREY,
                                         font=(FONT_REGULAR, 24))
        self.openai_label.place(relx=0.245, rely=0.59, anchor=ctk.CENTER)

        self.openai_entry = ctk.CTkEntry(self, border_width=0, fg_color=GREY,
                                         corner_radius=6, width=240, height=42,
                                         font=(FONT_REGULAR, 16))
        self.openai_entry.place(relx=0.65, rely=0.6, anchor=ctk.CENTER)

        self.error_usr_msg = ctk.CTkLabel(self, text="", text_color=PAS_RED, fg_color='transparent',
                                      font=(FONT_REGULAR, 12))
        self.error_usr_msg.place(relx=0.65, rely=0.485, anchor=ctk.CENTER)

        self.error_api_msg = ctk.CTkLabel(self, text="", text_color=PAS_RED, fg_color='transparent',
                                      font=(FONT_REGULAR, 12))
        self.error_api_msg.place(relx=0.65, rely=0.705, anchor=ctk.CENTER)

        self.go_btn = ctk.CTkButton(self, text='Let\'s GO!', border_width=0,
                                    command=self.check_, fg_color=PAS_RED, hover_color=CLOSE_RED,
                                    corner_radius=6, text_color=BLACK,
                                    font=(FONT_REGULAR, 16), height=46, width=132)
        self.go_btn.place(relx=0.85, rely=0.84, anchor=ctk.CENTER)


    def check_(self):
        self.show_api_error()
        username = self.username_entry.get()
        api_key = self.openai_entry.get()

        if valid_username(username) != True:
            self.show_username_error()
            print("Invalid username")
            return
        
        if check_api(api_key) != True:
            self.show_api_error()
            return

        self.successfuly = True
        self.username = username
        self.openai_api = api_key

        success_notification = SuccessNotif(self.parent)
        self.after(10000, lambda: success_notification.place_forget())
        self.place_forget()
        return

    def show_username_error(self):
        self.error_usr_msg.configure(text="Invalid username")
        self.username_entry.configure(border_width=1, border_color=PAS_RED)

    def show_api_error(self):
        self.error_api_msg.configure(text="Invalid OpenAi API key")
        self.openai_entry.configure(border_width=1, border_color=PAS_RED)

    


class SuccessNotif(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=DARK_GREY,
                         corner_radius=0, border_color=PAS_GREEN, border_width=1)
        self.place_configure(relx=0.99, rely=0.01,
                             anchor=ctk.NE, width=200, height=75)
        self.label = ctk.CTkLabel(
            self, text='Successfully', text_color=PAS_GREEN, font=(FONT_REGULAR, 16))
        self.label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)


class App(ctk.CTk):
    def __init__(self):
        # setup
        super().__init__()
        ctk.set_appearance_mode('Dark')
        self.geometry('1100x600')
        self.title('AI Banker')
        self.minsize(800, 500)
        self.config(background='#0e0f0f')

        # layout
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=7)
        self.columnconfigure(0, weight=5, uniform='a')
        self.columnconfigure(1, weight=10, uniform='a')
        self.columnconfigure(2, weight=8, uniform='a')

        # initialize login database
        self.start_screen = StartScreen(self)
        # self.minor_frame_lower = MinorFrameLower(self, 'self.ai_response')

        # run
        self.mainloop()


App()
