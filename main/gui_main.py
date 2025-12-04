import customtkinter as ctk
from sistem import MusicPlayer
from page_menu import PageMenu
from page_user import PageUser
from page_admin import PageAdmin
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Spotify Color Scheme
SPOTIFY_BLACK = "#121212"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.player = MusicPlayer()
        
        # Setup library dengan 21 lagu contoh
        self.setup_library()
        
        self.title("CIC Music Player - Spotify Theme")
        self.geometry("1200x700")
        self.configure(fg_color=SPOTIFY_BLACK)
        self.container = ctk.CTkFrame(self, fg_color=SPOTIFY_BLACK)
        self.container.pack(fill="both", expand=True)
        
        # Buat frames dan simpan sebagai dict dengan string key
        self.frames = {}
        self.frames["PageMenu"] = PageMenu(self.container, self)
        self.frames["PageUser"] = PageUser(self.container, self)
        self.frames["PageAdmin"] = PageAdmin(self.container, self)
        
        # Place semua frames
        for frame in self.frames.values():
            frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.show_frame("PageMenu")

    def setup_library(self):
        """Setup library dengan banyak lagu contoh"""
        music_dir = os.path.join(os.path.dirname(__file__), "music")
        
        # Pop Artists
        taylor = self.player.library.add_artist("Taylor Swift")
        album1 = taylor.add_album("1989")
        album1.add_song(1, "Shake It Off", "3:39", os.path.join(music_dir, "song1.mp3"))
        album1.add_song(2, "Blank Space", "3:51", os.path.join(music_dir, "song2.mp3"))
        album1.add_song(3, "Style", "3:51", os.path.join(music_dir, "song3.mp3"))
        
        ed = self.player.library.add_artist("Ed Sheeran")
        album2 = ed.add_album("÷ (Divide)")
        album2.add_song(4, "Shape of You", "3:53", os.path.join(music_dir, "song4.mp3"))
        album2.add_song(5, "Perfect", "4:23", os.path.join(music_dir, "song5.mp3"))
        album2.add_song(6, "Castle on the Hill", "4:21", os.path.join(music_dir, "song6.mp3"))
        
        # Rock Artists
        coldplay = self.player.library.add_artist("Coldplay")
        album3 = coldplay.add_album("A Head Full of Dreams")
        album3.add_song(7, "Adventure of a Lifetime", "4:23", os.path.join(music_dir, "song7.mp3"))
        album3.add_song(8, "Hymn for the Weekend", "4:18", os.path.join(music_dir, "song8.mp3"))
        
        imagine = self.player.library.add_artist("Imagine Dragons")
        album4 = imagine.add_album("Evolve")
        album4.add_song(9, "Believer", "3:24", os.path.join(music_dir, "song9.mp3"))
        album4.add_song(10, "Thunder", "3:07", os.path.join(music_dir, "song10.mp3"))
        album4.add_song(11, "Whatever It Takes", "3:21", os.path.join(music_dir, "song11.mp3"))
        
        # Hip Hop/R&B
        weeknd = self.player.library.add_artist("The Weeknd")
        album5 = weeknd.add_album("Starboy")
        album5.add_song(12, "Starboy", "3:50", os.path.join(music_dir, "song12.mp3"))
        album5.add_song(13, "I Feel It Coming", "4:29", os.path.join(music_dir, "song13.mp3"))
        
        bruno = self.player.library.add_artist("Bruno Mars")
        album6 = bruno.add_album("24K Magic")
        album6.add_song(14, "24K Magic", "3:46", os.path.join(music_dir, "song14.mp3"))
        album6.add_song(15, "That's What I Like", "3:26", os.path.join(music_dir, "song15.mp3"))
        
        # Alternative/Indie
        billie = self.player.library.add_artist("Billie Eilish")
        album7 = billie.add_album("When We All Fall Asleep")
        album7.add_song(16, "bad guy", "3:14", os.path.join(music_dir, "song16.mp3"))
        album7.add_song(17, "when the party's over", "3:16", os.path.join(music_dir, "song17.mp3"))
        
        # Electronic
        marshmello = self.player.library.add_artist("Marshmello")
        album8 = marshmello.add_album("Joytime III")
        album8.add_song(18, "Happier", "3:34", os.path.join(music_dir, "song18.mp3"))
        album8.add_song(19, "Alone", "4:33", os.path.join(music_dir, "song19.mp3"))
        
        # Classic
        beatles = self.player.library.add_artist("The Beatles")
        album9 = beatles.add_album("Abbey Road")
        album9.add_song(20, "Come Together", "4:19", os.path.join(music_dir, "song20.mp3"))
        album9.add_song(21, "Here Comes the Sun", "3:05", os.path.join(music_dir, "song21.mp3"))

    def show_frame(self, page_name):
        """Show frame by name (string)"""
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
