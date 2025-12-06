import customtkinter as ctk

SPOTIFY_BLACK = "#121212"
SPOTIFY_DARK_GRAY = "#181818"
SPOTIFY_GRAY = "#282828"
SPOTIFY_GREEN = "#1DB954"
SPOTIFY_WHITE = "#FFFFFF"
SPOTIFY_LIGHT_GRAY = "#B3B3B3"

class PageMenu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=SPOTIFY_BLACK)
        
        self.controller = controller
        
        # Logo/Title dengan style lebih menarik
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(pady=50)
        
        ctk.CTkLabel(title_frame, text="🎵", font=("Arial", 60)).pack()
        ctk.CTkLabel(title_frame, text="CIC Music Player", 
                    font=("Arial", 32, "bold"), 
                    text_color=SPOTIFY_WHITE).pack(pady=10)
        ctk.CTkLabel(title_frame, text="Experience Music Like Never Before", 
                    font=("Arial", 14), 
                    text_color=SPOTIFY_LIGHT_GRAY).pack()
        
        # Recommended Songs Section
        rec_frame = ctk.CTkFrame(self, fg_color=SPOTIFY_DARK_GRAY, corner_radius=15)
        rec_frame.pack(pady=20, padx=100, fill="x")
        
        ctk.CTkLabel(rec_frame, text="🔥 Rekomendasi Untuk Anda", 
                    font=("Arial", 18, "bold"), 
                    text_color=SPOTIFY_WHITE).pack(pady=15)
        
        self.rec_box = ctk.CTkTextbox(rec_frame, height=120, 
                                     fg_color=SPOTIFY_GRAY, 
                                     text_color=SPOTIFY_WHITE,
                                     corner_radius=10, 
                                     font=("Consolas", 11))
        self.rec_box.pack(padx=15, pady=(0, 15), fill="both")
        self.rec_box.configure(state="disabled")
        
        # Buttons dengan style lebih modern
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20)
        
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
    
    def show_recommendations(self):
        self.rec_box.configure(state="normal")
        self.rec_box.delete("1.0", "end")
        
        # Get recommendations from history or random
        all_songs = self.controller.player.get_all_songs()
        if not all_songs:
            self.rec_box.insert("end", "Belum ada lagu di library\n")
        else:
            import random
            recommendations = random.sample(all_songs, min(5, len(all_songs)))
            for song in recommendations:
                self.rec_box.insert("end", 
                    f"♫ {song.title} - {song.genre}\n")
        
        self.rec_box.configure(state="disabled")
    
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.show_recommendations()
