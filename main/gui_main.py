import customtkinter as ctk
from sistem import MusicPlayer
from page_menu import PageMenu
from page_user import PageUser
from page_admin import PageAdmin
from data_dummy import load_dummy_data

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

SPOTIFY_BLACK = "#121212"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.player = MusicPlayer()
        
        load_dummy_data(self.player)
        
        self.title("CIC Music Player")
        self.geometry("1200x700")
        self.configure(fg_color=SPOTIFY_BLACK)
        self.container = ctk.CTkFrame(self, fg_color=SPOTIFY_BLACK)
        self.container.pack(fill="both", expand=True)
        
        self.frames = {}
        self.frames["PageMenu"] = PageMenu(self.container, self)
        self.frames["PageUser"] = PageUser(self.container, self)
        self.frames["PageAdmin"] = PageAdmin(self.container, self)
        
        for frame in self.frames.values():
            frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.show_frame("PageMenu")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
