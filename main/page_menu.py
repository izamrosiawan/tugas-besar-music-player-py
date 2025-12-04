import customtkinter as ctk

# Spotify Color Scheme
SPOTIFY_BLACK = "#121212"
SPOTIFY_DARK_GRAY = "#181818"
SPOTIFY_GRAY = "#282828"
SPOTIFY_GREEN = "#1DB954"
SPOTIFY_WHITE = "#FFFFFF"
SPOTIFY_LIGHT_GRAY = "#B3B3B3"

class PageMenu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=SPOTIFY_BLACK)
        
        # Logo/Title dengan style lebih menarik
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(pady=80)
        
        ctk.CTkLabel(title_frame, text="🎵", font=("Arial", 60)).pack()
        ctk.CTkLabel(title_frame, text="CIC Music Player", 
                    font=("Arial", 32, "bold"), 
                    text_color=SPOTIFY_WHITE).pack(pady=10)
        ctk.CTkLabel(title_frame, text="Experience Music Like Never Before", 
                    font=("Arial", 14), 
                    text_color=SPOTIFY_LIGHT_GRAY).pack()
        
        # Buttons dengan style lebih modern
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=40)
        
        ctk.CTkButton(button_frame, text="🎧 Masuk sebagai Pengguna", 
                    width=350, height=50, 
                    font=("Arial", 16, "bold"), corner_radius=25,
                    command=lambda: controller.show_frame("PageUser"), 
                    fg_color=SPOTIFY_GREEN, hover_color="#1ed760", 
                    text_color=SPOTIFY_WHITE).pack(pady=15)
        
        ctk.CTkButton(button_frame, text="⚙️ Masuk sebagai Admin", 
                    width=350, height=50,
                    font=("Arial", 16, "bold"), corner_radius=25,
                    command=lambda: controller.show_frame("PageAdmin"), 
                    fg_color=SPOTIFY_GRAY, hover_color="#3E3E3E", 
                    text_color=SPOTIFY_WHITE).pack(pady=15)
