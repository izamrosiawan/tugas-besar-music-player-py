import customtkinter as ctk
from tkinter import messagebox
import time

SPOTIFY_BLACK = "#121212"
SPOTIFY_DARK_GRAY = "#181818"
SPOTIFY_GRAY = "#282828"
SPOTIFY_GREEN = "#1DB954"
SPOTIFY_WHITE = "#FFFFFF"
SPOTIFY_LIGHT_GRAY = "#B3B3B3"

class PageUser(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=SPOTIFY_BLACK)
        
        header = ctk.CTkFrame(self, height=60, fg_color=SPOTIFY_DARK_GRAY, corner_radius=0)
        header.pack(fill="x", padx=0, pady=0)
        
        ctk.CTkButton(header, text="← Kembali", width=100, height=35, corner_radius=20,
                    command=lambda: controller.show_frame("PageMenu"), 
                    fg_color=SPOTIFY_GRAY, hover_color="#3E3E3E").place(x=15, y=12)

        self.search_entry = ctk.CTkEntry(header, width=400, height=35, corner_radius=20,
                                        placeholder_text="🔍 Cari lagu, artis, atau album...",
                                        fg_color=SPOTIFY_GRAY, border_color=SPOTIFY_GRAY, 
                                        text_color=SPOTIFY_WHITE)
        self.search_entry.place(x=400, y=12)
        self.search_entry.bind("<Return>", lambda e: self.search_songs(controller))
        
        content = ctk.CTkFrame(self, fg_color=SPOTIFY_BLACK)
        content.pack(fill="both", expand=True, padx=15, pady=(10, 10))
        
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_columnconfigure(2, weight=1)
        
        self.frame_playlist = ctk.CTkFrame(content, corner_radius=15, fg_color=SPOTIFY_DARK_GRAY)
        self.frame_playlist.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        playlist_header = ctk.CTkFrame(self.frame_playlist, height=50, fg_color=SPOTIFY_GRAY, corner_radius=10)
        playlist_header.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(playlist_header, text="📋 Daftar Playlist", font=("Arial", 16, "bold"), 
                    text_color=SPOTIFY_WHITE).pack(side="left", padx=15, pady=10)
        
        self.playlist_list_box = ctk.CTkTextbox(self.frame_playlist, fg_color=SPOTIFY_GRAY, 
                                        text_color=SPOTIFY_WHITE, border_color=SPOTIFY_DARK_GRAY,
                                        corner_radius=10, font=("Consolas", 11))
        self.playlist_list_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.playlist_list_box.bind("<Button-1>", lambda e: self.on_playlist_click(controller, e))
        self.playlist_items = []
        self.refresh_playlist_list(controller)

        self.frame_library = ctk.CTkFrame(content, corner_radius=15, fg_color=SPOTIFY_DARK_GRAY)
        self.frame_library.grid(row=0, column=1, sticky="nsew", padx=5)
        
        library_header = ctk.CTkFrame(self.frame_library, height=50, fg_color=SPOTIFY_GRAY, corner_radius=10)
        library_header.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(library_header, text="🎵 Daftar Lagu", font=("Arial", 16, "bold"), 
                    text_color=SPOTIFY_WHITE).pack(side="left", padx=15, pady=10)
        
        ctk.CTkButton(library_header, text="🔄", width=35, height=28, corner_radius=8,
                    command=lambda: self.refresh_library(controller), 
                    fg_color=SPOTIFY_GREEN, hover_color="#1ed760",
                    font=("Arial", 14),
                    cursor="hand2").pack(side="right", padx=10)
        
        self.library_box = ctk.CTkTextbox(self.frame_library, fg_color=SPOTIFY_GRAY, 
                                        text_color=SPOTIFY_WHITE, border_color=SPOTIFY_DARK_GRAY,
                                        corner_radius=10, font=("Consolas", 11))
        self.library_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.library_box.bind("<Button-1>", lambda e: self.on_library_click(controller, e))
        self.library_items = []
        self.selected_index = None
        self.current_playlist_mode = None  # Track jika sedang di mode playlist
        self.refresh_library(controller)

        self.frame_playlist_action = ctk.CTkFrame(content, corner_radius=15, fg_color=SPOTIFY_DARK_GRAY)
        self.frame_playlist_action.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        
        action_header = ctk.CTkFrame(self.frame_playlist_action, height=50, fg_color=SPOTIFY_GRAY, corner_radius=10)
        action_header.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(action_header, text="⚡ Kelola Playlist", font=("Arial", 16, "bold"), 
                    text_color=SPOTIFY_WHITE).pack(side="left", padx=15, pady=10)
        
        action_scrollable = ctk.CTkScrollableFrame(self.frame_playlist_action, fg_color="transparent", 
                                                    height=450)
        action_scrollable.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        action_content = action_scrollable
        
        ctk.CTkLabel(action_content, text="📝 BUAT PLAYLIST BARU", font=("Arial", 11, "bold"), 
                    text_color=SPOTIFY_GREEN).pack(anchor="w", pady=(5, 5))
        
        self.new_playlist_entry = ctk.CTkEntry(action_content, height=32, corner_radius=10,
                                        placeholder_text="Nama playlist baru...",
                                        fg_color=SPOTIFY_GRAY, border_color=SPOTIFY_GRAY, 
                                        text_color=SPOTIFY_WHITE)
        self.new_playlist_entry.pack(fill="x", pady=(0, 5))
        
        ctk.CTkButton(action_content, text="➕ Buat Playlist", height=35, corner_radius=10,
                    command=lambda: self.create_user_playlist(controller), 
                    fg_color=SPOTIFY_GREEN, hover_color="#1ed760", 
                    font=("Arial", 11, "bold")).pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(action_content, text="━" * 25, 
                    text_color=SPOTIFY_GRAY).pack(pady=5)
        
        ctk.CTkLabel(action_content, text="🎵 KELOLA PLAYLIST", font=("Arial", 11, "bold"), 
                    text_color=SPOTIFY_GREEN).pack(anchor="w", pady=(5, 5))
        
        ctk.CTkLabel(action_content, text="Pilih Playlist:", font=("Arial", 10), 
                    text_color=SPOTIFY_LIGHT_GRAY).pack(anchor="w", pady=(0, 2))
        
        self.user_playlist_dropdown = ctk.CTkOptionMenu(
            action_content, 
            values=["My Playlist"],
            fg_color=SPOTIFY_GRAY, 
            button_color=SPOTIFY_GREEN,
            button_hover_color="#1ed760",
            dropdown_fg_color=SPOTIFY_GRAY,
            font=("Arial", 10))
        self.user_playlist_dropdown.pack(fill="x", pady=(0, 8))
        
        ctk.CTkLabel(action_content, text="Nama Lagu:", font=("Arial", 10), 
                    text_color=SPOTIFY_LIGHT_GRAY).pack(anchor="w", pady=(0, 2))
        self.song_name_entry = ctk.CTkEntry(action_content, height=32, corner_radius=10,
                                        placeholder_text="Cari nama lagu untuk ditambah...",
                                        fg_color=SPOTIFY_GRAY, border_color=SPOTIFY_GRAY, 
                                        text_color=SPOTIFY_WHITE)
        self.song_name_entry.pack(fill="x", pady=(0, 5))
        
        ctk.CTkButton(action_content, text="➕ Tambah Lagu", height=35, corner_radius=10,
                    command=lambda: self.add_to_user_playlist(controller), 
                    fg_color=SPOTIFY_GREEN, hover_color="#1ed760", 
                    font=("Arial", 10, "bold")).pack(fill="x", pady=2)
        
        ctk.CTkButton(action_content, text="➖ Hapus Lagu", height=35, corner_radius=10,
                    command=lambda: self.remove_from_user_playlist(controller), 
                    fg_color="#FF6B6B", hover_color="#FF4444",
                    font=("Arial", 10, "bold")).pack(fill="x", pady=2)
        
        ctk.CTkButton(action_content, text="🗑️ Hapus Playlist", height=35, corner_radius=10,
                    command=lambda: self.delete_user_playlist(controller), 
                    fg_color="#8B0000", hover_color="#A52A2A",
                    font=("Arial", 10, "bold")).pack(fill="x", pady=(2, 5))
        
        self.status_label = ctk.CTkLabel(action_content, text="", font=("Arial", 9),
                                        text_color=SPOTIFY_GREEN, wraplength=280)
        self.status_label.pack(pady=5)

        self.frame_control = ctk.CTkFrame(self, height=90, fg_color=SPOTIFY_DARK_GRAY, corner_radius=0)
        self.frame_control.pack(side="bottom", fill="x", padx=0, pady=0)
        
        self.seekbar = ctk.CTkProgressBar(self.frame_control, height=4,
                                         progress_color=SPOTIFY_WHITE, fg_color="#4d4d4d")
        self.seekbar.set(0)
        self.seekbar.pack(fill="x", padx=20, pady=0)
        
        main_row = ctk.CTkFrame(self.frame_control, fg_color="transparent")
        main_row.pack(fill="x", padx=15, pady=(8, 8))
        
        left_section = ctk.CTkFrame(main_row, fg_color="transparent", width=350)
        left_section.pack(side="left", fill="both", anchor="w")
        left_section.pack_propagate(False)
        
        self.current_label = ctk.CTkLabel(left_section, text="", 
                                        font=("Arial", 13, "bold"), text_color=SPOTIFY_WHITE, 
                                        anchor="w")
        self.current_label.pack(anchor="w", side="top")
        
        self.artist_label = ctk.CTkLabel(left_section, text="", 
                                        font=("Arial", 11), text_color=SPOTIFY_LIGHT_GRAY, 
                                        anchor="w")
        self.artist_label.pack(anchor="w", side="top")
        
        center_section = ctk.CTkFrame(main_row, fg_color="transparent")
        center_section.pack(side="left", expand=True)
        
        btn_row = ctk.CTkFrame(center_section, fg_color="transparent")
        btn_row.pack(pady=(0, 5), anchor="center")
        
        ctk.CTkButton(btn_row, text="⏮", width=32, height=32, corner_radius=16,
                    command=lambda: self.previous_song(controller), 
                    fg_color="transparent", hover_color=SPOTIFY_GRAY,
                    text_color=SPOTIFY_LIGHT_GRAY, font=("Arial", 16)).pack(side="left", padx=8)
        
        self.play_pause_btn = ctk.CTkButton(btn_row, text="▶", width=38, height=38, 
                    corner_radius=19, command=lambda: self.toggle_play_pause(controller), 
                    fg_color=SPOTIFY_WHITE, hover_color="#e0e0e0",
                    text_color=SPOTIFY_BLACK, font=("Arial", 15, "bold"))
        self.play_pause_btn.pack(side="left", padx=8)
        
        ctk.CTkButton(btn_row, text="⏭", width=32, height=32, corner_radius=16,
                    command=lambda: self.next_song(controller), 
                    fg_color="transparent", hover_color=SPOTIFY_GRAY,
                    text_color=SPOTIFY_LIGHT_GRAY, font=("Arial", 16)).pack(side="left", padx=8)
        
        self.is_playing_state = False
        
        timer_row = ctk.CTkFrame(center_section, fg_color="transparent")
        timer_row.pack(anchor="center")
        
        self.time_current = ctk.CTkLabel(timer_row, text="0:00", 
                                        font=("Arial", 10), text_color=SPOTIFY_LIGHT_GRAY)
        self.time_current.pack(side="left", padx=5)
        
        ctk.CTkLabel(timer_row, text="/", 
                    font=("Arial", 10), text_color=SPOTIFY_LIGHT_GRAY).pack(side="left")
        
        self.time_total = ctk.CTkLabel(timer_row, text="0:00", 
                                    font=("Arial", 10), text_color=SPOTIFY_LIGHT_GRAY)
        self.time_total.pack(side="left", padx=5)
        
        right_section = ctk.CTkFrame(main_row, fg_color="transparent", width=350)
        right_section.pack(side="right", fill="both", anchor="e")
        right_section.pack_propagate(False)
        
        volume_container = ctk.CTkFrame(right_section, fg_color="transparent")
        volume_container.pack(side="right")
        
        ctk.CTkLabel(volume_container, text="🔊", font=("Arial", 14)).pack(side="left", padx=5)
        self.volume_slider = ctk.CTkSlider(
            volume_container, from_=0, to=100, width=100,
            command=lambda v: self.change_volume(controller, v),
            button_color=SPOTIFY_WHITE, 
            button_hover_color="#e0e0e0",
            progress_color=SPOTIFY_WHITE,
            fg_color="#4d4d4d",
            height=4, button_length=12)
        self.volume_slider.set(70)
        self.volume_slider.pack(side="left")
        
        self.controller = controller
        self.check_song_ended()
    
    def create_user_playlist(self, controller):
        playlist_name = self.new_playlist_entry.get().strip()
        if not playlist_name:
            messagebox.showwarning("Input Kosong", "Masukkan nama playlist!")
            return
        
        controller.player.playlist_manager.create_playlist(playlist_name)
        self.refresh_playlist_list(controller)
        self.update_playlist_dropdown(controller)
        self.user_playlist_dropdown.set(playlist_name)
        self.new_playlist_entry.delete(0, 'end')
        messagebox.showinfo("Sukses", f"Playlist '{playlist_name}' berhasil dibuat!\n\nSekarang Anda bisa tambah lagu ke playlist ini.")
    
    def add_to_user_playlist(self, controller):
        song_name = self.song_name_entry.get().strip().lower()
        if not song_name:
            messagebox.showerror("Error", "Masukkan nama lagu!")
            return
        
        playlist_name = self.user_playlist_dropdown.get()
        if playlist_name == "Pilih Playlist":
            messagebox.showwarning("Pilih Playlist", "Pilih playlist tujuan terlebih dahulu!")
            return
        
        art = controller.player.library.artists_head
        song_found = None
        
        while art:
            song = art.songs_head
            while song:
                if song_name in song.title.lower():
                    song_found = song
                    break
                song = song.next
            if song_found:
                break
            art = art.next
        
        if not song_found:
            messagebox.showerror("Error", f"Lagu '{song_name}' tidak ditemukan!")
            return
        
        controller.player.playlist_manager.add_to_playlist(playlist_name, song_found)
        self.refresh_playlist_list(controller)
        self.song_name_entry.delete(0, 'end')
        messagebox.showinfo("Sukses", f"Lagu '{song_found.title}' ditambahkan ke '{playlist_name}'!")
    
    def delete_user_playlist(self, controller):
        playlist_name = self.user_playlist_dropdown.get()
        if playlist_name == "Pilih Playlist" or playlist_name == "My Playlist":
            messagebox.showwarning("Tidak Bisa Hapus", "Pilih playlist yang ingin dihapus (My Playlist tidak bisa dihapus)!")
            return
        
        confirm = messagebox.askyesno("Konfirmasi", f"Hapus playlist '{playlist_name}'?")
        if not confirm:
            return
        
        controller.player.playlist_manager.delete_playlist(playlist_name)
        
        self.refresh_playlist_list(controller)
        self.update_playlist_dropdown(controller)
        messagebox.showinfo("Sukses", f"Playlist '{playlist_name}' berhasil dihapus!")
    
    def remove_from_user_playlist(self, controller):
        song_name = self.song_name_entry.get().strip().lower()
        if not song_name:
            messagebox.showerror("Error", "Masukkan nama lagu yang ingin dihapus!")
            return
        
        playlist_name = self.user_playlist_dropdown.get()
        if playlist_name == "Pilih Playlist":
            messagebox.showwarning("Pilih Playlist", "Pilih playlist terlebih dahulu!")
            return
        
        playlist = controller.player.playlist_manager.get_playlist(playlist_name)
        if not playlist or not playlist.head:
            messagebox.showerror("Error", "Playlist kosong!")
            return
        
        if song_name in playlist.head.song.title.lower():
            song_title = playlist.head.song.title
            if playlist.head == playlist.tail:
                playlist.head = playlist.tail = None
            else:
                playlist.head = playlist.head.next
                if playlist.head:
                    playlist.head.prev = None
            self.refresh_playlist_list(controller)
            self.song_name_entry.delete(0, 'end')
            messagebox.showinfo("Sukses", f"Lagu '{song_title}' dihapus dari '{playlist_name}'!")
            return
        
        curr = playlist.head
        while curr:
            if song_name in curr.song.title.lower():
                song_title = curr.song.title
                if curr.prev:
                    curr.prev.next = curr.next
                if curr.next:
                    curr.next.prev = curr.prev
                if curr == playlist.tail:
                    playlist.tail = curr.prev
                self.refresh_playlist_list(controller)
                self.song_name_entry.delete(0, 'end')
                messagebox.showinfo("Sukses", f"Lagu '{song_title}' dihapus dari '{playlist_name}'!")
                return
            curr = curr.next
        
        messagebox.showerror("Error", f"Lagu '{song_name}' tidak ditemukan di playlist '{playlist_name}'!")
    
    def update_playlist_dropdown(self, controller):
        playlist_names = []
        for playlist in controller.player.playlist_manager.playlists:
            playlist_names.append(playlist.name)
        
        if playlist_names:
            self.user_playlist_dropdown.configure(values=playlist_names)
            self.user_playlist_dropdown.set(playlist_names[0])
        else:
            self.user_playlist_dropdown.configure(values=["Pilih Playlist"])
            self.user_playlist_dropdown.set("Pilih Playlist")
    

    def check_song_ended(self):
        import pygame
        try:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    print("[AUTO-PLAY] USEREVENT detected")
                    self.next_song(self.controller)
                    return
            
            if self.controller.player.current_song:
                current_pos = self.controller.player.get_pos()
                is_playing = self.controller.player.is_playing
                is_busy = pygame.mixer.music.get_busy()
                
                duration_str = self.controller.player.current_song.duration
                try:
                    parts = duration_str.split(":")
                    if len(parts) == 2:
                        total_seconds = int(parts[0]) * 60 + int(parts[1])
                    else:
                        total_seconds = 180
                    
                    if total_seconds > 0 and current_pos >= 0:
                        progress = (current_pos / total_seconds)
                        self.seekbar.set(min(progress, 1.0))
                        
                        mins_curr = int(current_pos // 60)
                        secs_curr = int(current_pos % 60)
                        self.time_current.configure(text=f"{mins_curr}:{secs_curr:02d}")
                        
                        mins_total = int(total_seconds // 60)
                        secs_total = int(total_seconds % 60)
                        self.time_total.configure(text=f"{mins_total}:{secs_total:02d}")
                    
                    if is_playing and is_busy:
                        if current_pos >= total_seconds - 0.2:
                            print(f"[AUTO-PLAY] Next song at {current_pos:.1f}/{total_seconds}s")
                            pygame.mixer.music.stop()
                            self.next_song(self.controller)
                            return
                    
                    elif is_playing and not is_busy and current_pos > 1.0:
                        print(f"[AUTO-PLAY] Song ended (busy=False at {current_pos:.1f}s)")
                        self.next_song(self.controller)
                        return
                        
                except Exception as e:
                    print(f"Error in check: {e}")
        except Exception as e:
            print(f"Error in check_song_ended: {e}")
        
        self.after(100, self.check_song_ended)

    def on_library_click(self, controller, event):
        try:
            index = self.library_box.index("@%s,%s" % (event.x, event.y))
            line_number = int(index.split('.')[0]) - 1
            if 0 <= line_number < len(self.library_items):
                self.selected_index = line_number
                song = self.library_items[line_number]
                artist_name = self.get_artist_name(controller, song)
                
                def update_status(msg):
                    self.current_label.configure(text=song.title)
                    self.artist_label.configure(text=artist_name)
                    self.is_playing_state = True
                    self.play_pause_btn.configure(text="⏸")
                
                msg = controller.player.play_song(song, callback=update_status)
                self.current_label.configure(text=song.title)
                self.artist_label.configure(text=artist_name)
                self.seekbar.set(0)
                self.time_current.configure(text="0:00")
                self.time_total.configure(text=song.duration)
                self.is_playing_state = True
                self.play_pause_btn.configure(text="⏸")
        except:
            pass

    def get_artist_name(self, controller, song):
        art = controller.player.library.artists_head
        while art:
            curr_song = art.songs_head
            while curr_song:
                if curr_song.id == song.id:
                    return art.artist_name
                curr_song = curr_song.next
            art = art.next
        return "Unknown Artist"
    
    def refresh_playlist_list(self, controller):
        self.playlist_list_box.configure(state="normal")
        self.playlist_list_box.delete("1.0", "end")
        self.playlist_items = []
        
        idx = 1
        
        for playlist in controller.player.playlist_manager.playlists:
            song_count = 0
            curr = playlist.head
            while curr:
                song_count += 1
                curr = curr.next
            
            text = f"{idx}. 📋 {playlist.name} ({song_count} lagu)\n"
            self.playlist_list_box.insert("end", text)
            self.playlist_items.append({"type": "user", "playlist": playlist})
            idx += 1
        
        if idx > 1:
            self.playlist_list_box.insert("end", "\n")
        
        genres = {}
        art = controller.player.library.artists_head
        while art:
            song = art.songs_head
            while song:
                genre = song.genre
                if genre not in genres:
                    genres[genre] = []
                genres[genre].append(song)
                song = song.next
            art = art.next
        
        for genre, songs in genres.items():
            text = f"{idx}. 🎧 {genre} Playlist ({len(songs)} lagu)\n"
            self.playlist_list_box.insert("end", text)
            self.playlist_items.append({"type": "genre", "genre": genre, "songs": songs})
            idx += 1
        
        self.playlist_list_box.configure(state="disabled")
    
    def on_playlist_click(self, controller, event):
        try:
            index = self.playlist_list_box.index("@%s,%s" % (event.x, event.y))
            line_number = int(index.split('.')[0]) - 1
            if 0 <= line_number < len(self.playlist_items):
                playlist_data = self.playlist_items[line_number]
                if playlist_data["type"] == "user":
                    self.show_user_playlist_songs(controller, playlist_data["playlist"])
                else:
                    self.show_playlist_songs(controller, playlist_data)
                print(f"[CLICK] Selected playlist: {playlist_data}")
        except Exception as e:
            print(f"[ERROR] on_playlist_click: {e}")
    
    def show_user_playlist_songs(self, controller, playlist):
        self.current_playlist_mode = f"user_{playlist.name}"
        self.selected_index = None
        
        self.library_box.configure(state="normal")
        self.library_box.delete("1.0", "end")
        self.library_items = []
        
        self.library_box.insert("end", f"📋 {playlist.name}\n\n", "header")
        
        current_song_id = controller.player.current_song.id if controller.player.current_song else None
        
        curr = playlist.head
        while curr:
            song = curr.song
            artist_name = self.get_artist_name(controller, song)
            
            playing_indicator = "🔊 " if song.id == current_song_id else "   "
            
            album_info = f" • {song.album}" if song.album else ""
            text = f"{playing_indicator}{song.id}. {song.title} — {song.duration} ({artist_name}){album_info}\n"
            self.library_box.insert("end", text)
            self.library_items.append(song)
            curr = curr.next
        
        self.library_box.configure(state="disabled")
        
        if self.library_items:
            self.selected_index = 0
            first_song = self.library_items[0]
            artist_name = self.get_artist_name(controller, first_song)
            
            controller.player.play_song(first_song)
            
            self.current_label.configure(text=first_song.title)
            self.artist_label.configure(text=artist_name)
            self.seekbar.set(0)
            self.time_current.configure(text="0:00")
            self.time_total.configure(text=first_song.duration)
            self.is_playing_state = True
            self.play_pause_btn.configure(text="⏸")
            
            self.update_library_highlight(controller)
    
    def show_playlist_songs(self, controller, playlist_data):
        genre = playlist_data["genre"]
        songs = playlist_data["songs"]
        
        self.current_playlist_mode = genre
        self.selected_index = None  # Reset index saat ganti playlist
        
        self.library_box.configure(state="normal")
        self.library_box.delete("1.0", "end")
        self.library_items = []
        
        self.library_box.insert("end", f"🎵 {genre} Playlist\n\n", "header")
        
        current_song_id = controller.player.current_song.id if controller.player.current_song else None
        
        for song in songs:
            artist_name = self.get_artist_name(controller, song)
            
            playing_indicator = "🔊 " if song.id == current_song_id else "   "
            
            album_info = f" • {song.album}" if song.album else ""
            text = f"{playing_indicator}{song.id}. {song.title} — {song.duration} ({artist_name}){album_info}\n"
            self.library_box.insert("end", text)
            self.library_items.append(song)
        
        self.library_box.configure(state="disabled")
        print(f"[PLAYLIST] Mode: {genre} ({len(songs)} lagu, {len(self.library_items)} items loaded)")
        
        if self.library_items:
            self.selected_index = 0
            first_song = self.library_items[0]
            artist_name = self.get_artist_name(controller, first_song)
            
            controller.player.play_song(first_song)
            
            self.current_label.configure(text=first_song.title)
            self.artist_label.configure(text=artist_name)
            self.seekbar.set(0)
            self.time_current.configure(text="0:00")
            self.time_total.configure(text=first_song.duration)
            self.is_playing_state = True
            self.play_pause_btn.configure(text="⏸")
            
            print(f"[AUTO-START] Playing: {first_song.title} ({artist_name})")
            
            self.update_library_highlight(controller)
    
    def update_library_highlight(self, controller):
        if not controller.player.current_song:
            return
        
        self.library_box.configure(state="normal")
        content = self.library_box.get("1.0", "end")
        lines = content.split("\n")
        
        current_song_id = controller.player.current_song.id
        
        new_content = []
        for line in lines:
            if line.strip():
                clean_line = line.replace("🔊 ", "   ")
                
                if f"{current_song_id}." in clean_line:
                    clean_line = "🔊 " + clean_line[3:]
                
                new_content.append(clean_line)
            else:
                new_content.append(line)
        
        self.library_box.delete("1.0", "end")
        self.library_box.insert("1.0", "\n".join(new_content))
        self.library_box.configure(state="disabled")
    
    def refresh_library(self, controller):
        import random
        self.current_playlist_mode = None
        self.selected_index = None
        
        self.library_box.configure(state="normal")
        self.library_box.delete("1.0", "end")
        self.library_items = []
        
        current_song_id = controller.player.current_song.id if controller.player.current_song else None
        
        all_songs = []
        art = controller.player.library.artists_head
        while art:
            song = art.songs_head
            while song:
                all_songs.append((song, art.artist_name))
                song = song.next
            art = art.next
        
        random.seed(42)
        random.shuffle(all_songs)
        
        for song, artist_name in all_songs:
            album_info = f" • {song.album}" if song.album else ""
            
            playing_indicator = "🔊 " if song.id == current_song_id else "   "
            
            text = (f"{playing_indicator}{song.title} — {song.duration} "
                f"({artist_name}){album_info}\n")
            self.library_box.insert("end", text)
            self.library_items.append(song)
        
        self.library_box.configure(state="disabled")
        print(f"[LIBRARY] Showing all songs ({len(all_songs)} total, shuffled)")

    def search_songs(self, controller):
        keyword = self.search_entry.get().strip().lower()
        if not keyword:
            self.refresh_library(controller)
            return
        
        self.library_box.configure(state="normal")
        self.library_box.delete("1.0", "end")
        self.library_items = []
        art = controller.player.library.artists_head
        found_count = 0
        while art:
            song = art.songs_head
            while song:
                if (keyword in song.title.lower() or 
                    keyword in art.artist_name.lower()):
                    text = (f"{song.title} — {song.duration} "
                        f"({art.artist_name})\n")
                    self.library_box.insert("end", text)
                    self.library_items.append(song)
                    found_count += 1
                song = song.next
            art = art.next
        
        if found_count == 0:
            self.library_box.insert("end", "Tidak ada hasil ditemukan.\n")
        self.library_box.configure(state="disabled")
        self.selected_index = None

    def get_first_song(self, controller):
        art = controller.player.library.artists_head
        return art.songs_head if art else None

    def play_selected(self, controller):
        if self.selected_index is not None and 0 <= self.selected_index < len(self.library_items):
            song = self.library_items[self.selected_index]
        else:
            song = self.get_first_song(controller)
            self.selected_index = 0
        
        if song:
            def update_status(msg):
                self.current_label.configure(text=f"{song.title}")
                self.is_playing_state = True
                self.play_pause_btn.configure(text="⏸")
            
            msg = controller.player.play_song(song, callback=update_status)
            self.current_label.configure(text=f"{song.title}")
            self.seekbar.set(0)
            self.time_current.configure(text="0:00")
            self.time_total.configure(text=song.duration)
            self.is_playing_state = True
            self.play_pause_btn.configure(text="⏸")
    
    def toggle_play_pause(self, controller):
        if controller.player.current_song is None:
            self.play_selected(controller)
        elif controller.player.is_paused:
            controller.player.resume_song()
            self.is_playing_state = True
            self.play_pause_btn.configure(text="⏸")
        elif controller.player.is_playing:
            controller.player.pause_song()
            self.is_playing_state = False
            self.play_pause_btn.configure(text="▶")
        else:
            self.play_selected(controller)

    def pause_resume(self, controller):
        if controller.player.is_paused:
            msg = controller.player.resume_song()
        else:
            msg = controller.player.pause_song()
        self.status_label.configure(text=msg, text_color=SPOTIFY_GREEN)

    def stop_music(self, controller):
        msg = controller.player.stop_song()
        self.current_label.configure(text="⏹️ Musik dihentikan")
        self.status_label.configure(text=msg, text_color=SPOTIFY_GREEN)

    def change_volume(self, controller, value):
        volume = float(value) / 100
        controller.player.set_volume(volume)
    
    
    def add_to_playlist(self, controller):
        song_name = self.song_name_old_entry.get().strip().lower()
        if not song_name:
            return self.status_label.configure(text="Masukkan nama lagu!", text_color="#FF6B6B")
        
        found_song = None
        art = controller.player.library.artists_head
        while art and not found_song:
            song = art.songs_head
            while song:
                if song_name in song.title.lower():
                    found_song = song
                    break
                song = song.next
            art = art.next
        
        if found_song:
            controller.player.playlist.add_song(found_song)
            self.refresh_playlist(controller)
            self.status_label.configure(
                text=f"'{found_song.title}' ditambahkan!", 
                text_color=SPOTIFY_GREEN)
            self.song_name_old_entry.delete(0, 'end')
        else:
            self.status_label.configure(
                text=f"Lagu '{song_name}' tidak ditemukan!", 
                text_color="#FF6B6B")

    def remove_from_playlist(self, controller):
        song_name = self.song_name_old_entry.get().strip().lower()
        if not song_name:
            return self.status_label.configure(
                text="Masukkan nama lagu yang ingin dihapus!", 
                text_color="#FF6B6B")
        
        playlist = controller.player.playlist
        if not playlist.head:
            return self.status_label.configure(text="Playlist kosong!", text_color="#FF6B6B")
        
        if song_name in playlist.head.song.title.lower():
            song_title = playlist.head.song.title
            if playlist.head == playlist.tail:
                playlist.head = playlist.tail = None
            else:
                playlist.head = playlist.head.next
                if playlist.head:
                    playlist.head.prev = None
            self.refresh_playlist(controller)
            self.status_label.configure(
                text=f"'{song_title}' dihapus dari playlist!", 
                text_color=SPOTIFY_GREEN)
            self.song_name_old_entry.delete(0, 'end')
            return
        
        curr = playlist.head
        while curr:
            if song_name in curr.song.title.lower():
                song_title = curr.song.title
                if curr.prev:
                    curr.prev.next = curr.next
                if curr.next:
                    curr.next.prev = curr.prev
                if curr == playlist.tail:
                    playlist.tail = curr.prev
                self.refresh_playlist(controller)
                self.status_label.configure(
                    text=f"'{song_title}' dihapus dari playlist!", 
                    text_color=SPOTIFY_GREEN)
                self.song_name_old_entry.delete(0, 'end')
                return
            curr = curr.next
        self.status_label.configure(
            text=f"Lagu '{song_name}' tidak ada di playlist!", 
            text_color="#FF6B6B")

    def clear_playlist(self, controller):
        controller.player.playlist.head = None
        controller.player.playlist.tail = None
        self.refresh_playlist(controller)
        self.status_label.configure(text="Playlist dikosongkan!", text_color=SPOTIFY_GREEN)

    def refresh_playlist(self, controller):
        self.playlist_box.configure(state="normal")
        self.playlist_box.delete("1.0", "end")
        curr = controller.player.playlist.head
        if not curr:
            self.playlist_box.insert("end", "Playlist kosong\n")
        else:
            while curr:
                self.playlist_box.insert("end", f"{curr.song.id}. {curr.song.title} — {curr.song.duration}\n")
                curr = curr.next
        self.playlist_box.configure(state="disabled")

    def next_song(self, controller):
        if not self.library_items:
            print("[NEXT] No songs in library")
            return
        
        mode = f"Playlist: {self.current_playlist_mode}" if self.current_playlist_mode else "All Songs"
        print(f"[NEXT] Mode: {mode}, Total songs: {len(self.library_items)}")
            
        if self.selected_index is None:
            self.selected_index = 0
        else:
            current_song = self.library_items[self.selected_index]
            current_artist = self.get_artist_name(controller, current_song)
            
            next_index = None
            for i in range(self.selected_index + 1, len(self.library_items)):
                song = self.library_items[i]
                if self.get_artist_name(controller, song) == current_artist:
                    next_index = i
                    break
            
            if next_index is None:
                for i in range(0, self.selected_index):
                    song = self.library_items[i]
                    if self.get_artist_name(controller, song) == current_artist:
                        next_index = i
                        break
            
            if next_index is None:
                next_index = self.selected_index
            
            self.selected_index = next_index
        
        if 0 <= self.selected_index < len(self.library_items):
            song = self.library_items[self.selected_index]
            artist_name = self.get_artist_name(controller, song)
            
            def update_status(msg):
                self.current_label.configure(text=song.title)
                self.artist_label.configure(text=artist_name)
                self.is_playing_state = True
                self.play_pause_btn.configure(text="⏸")
            
            msg = controller.player.play_song(song, callback=update_status)
            self.current_label.configure(text=song.title)
            self.artist_label.configure(text=artist_name)
            self.seekbar.set(0)
            self.time_current.configure(text="0:00")
            self.time_total.configure(text=song.duration)
            self.is_playing_state = True
            self.play_pause_btn.configure(text="⏸")
            
            controller.player.start_time = time.time()
            controller.player.paused_position = 0
            
            print(f"[NEXT] Playing: {song.title} ({artist_name}) [index: {self.selected_index}/{len(self.library_items)-1}]")
            
            self.update_library_highlight(controller)

    def previous_song(self, controller):
        if self.selected_index is None: 
            self.selected_index = 0
        else:
            self.selected_index = max(self.selected_index - 1, 0)
        if 0 <= self.selected_index < len(self.library_items):
            song = self.library_items[self.selected_index]
            artist_name = self.get_artist_name(controller, song)
            
            def update_status(msg):
                self.current_label.configure(text=song.title)
                self.artist_label.configure(text=artist_name)
                self.is_playing_state = True
                self.play_pause_btn.configure(text="⏸")
            
            msg = controller.player.play_song(song, callback=update_status)
            self.current_label.configure(text=song.title)
            self.artist_label.configure(text=artist_name)
            self.seekbar.set(0)
            self.time_current.configure(text="0:00")
            self.time_total.configure(text=song.duration)
            self.is_playing_state = True
            self.play_pause_btn.configure(text="⏸")
            print(f"[PREV] Playing: {song.title}")
    
    def on_seekbar_click(self, controller, event):
        self.seeking = True
        value = self.seekbar.get()
        self.seek_song(controller, value)
        self.after(200, lambda: setattr(self, 'seeking', False))
    
    def seek_song(self, controller, value):
        if controller.player.current_song:
            duration_str = controller.player.current_song.duration
            try:
                parts = duration_str.split(":")
                if len(parts) == 2:
                    total_seconds = int(parts[0]) * 60 + int(parts[1])
                else:
                    total_seconds = 180
                
                seek_position = (float(value) / 100) * total_seconds
                controller.player.seek(seek_position)
            except:
                pass
