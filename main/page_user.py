import customtkinter as ctk

SPOTIFY_BLACK = "#121212"
SPOTIFY_DARK_GRAY = "#181818"
SPOTIFY_GRAY = "#282828"
SPOTIFY_GREEN = "#1DB954"
SPOTIFY_WHITE = "#FFFFFF"
SPOTIFY_LIGHT_GRAY = "#B3B3B3"

class PageUser(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=SPOTIFY_BLACK)
        
        # Header dengan tombol kembali dan search
        header = ctk.CTkFrame(self, height=60, fg_color=SPOTIFY_DARK_GRAY, corner_radius=0)
        header.pack(fill="x", padx=0, pady=0)
        
        ctk.CTkButton(header, text="← Kembali", width=100, height=35, corner_radius=20,
                    command=lambda: controller.show_frame("PageMenu"), 
                    fg_color=SPOTIFY_GRAY, hover_color="#3E3E3E").place(x=15, y=12)

        # Search bar di header
        self.search_entry = ctk.CTkEntry(header, width=400, height=35, corner_radius=20,
                                        placeholder_text="🔍 Cari lagu, artis, atau album...",
                                        fg_color=SPOTIFY_GRAY, border_color=SPOTIFY_GRAY, 
                                        text_color=SPOTIFY_WHITE)
        self.search_entry.place(x=400, y=12)
        self.search_entry.bind("<Return>", lambda e: self.search_songs(controller))
        
        content = ctk.CTkFrame(self, fg_color=SPOTIFY_BLACK)
        content.pack(fill="both", expand=True, padx=15, pady=(10, 10))
        
        # Left: Playlist
        self.frame_playlist = ctk.CTkFrame(content, width=380, corner_radius=15, fg_color=SPOTIFY_DARK_GRAY)
        self.frame_playlist.pack(side="left", fill="both", expand=True, padx=(0, 8))
        
        playlist_header = ctk.CTkFrame(self.frame_playlist, height=50, fg_color=SPOTIFY_GRAY, corner_radius=10)
        playlist_header.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(playlist_header, text="📋 Playlist", font=("Arial", 16, "bold"), 
                    text_color=SPOTIFY_WHITE).pack(side="left", padx=15, pady=10)
        
        # Playlist selector
        playlist_select_frame = ctk.CTkFrame(self.frame_playlist, fg_color="transparent")
        playlist_select_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        self.playlist_dropdown = ctk.CTkOptionMenu(
            playlist_select_frame, 
            values=["My Playlist"],
            command=lambda x: self.switch_playlist(controller, x),
            fg_color=SPOTIFY_GRAY, 
            button_color=SPOTIFY_GREEN,
            button_hover_color="#1ed760",
            dropdown_fg_color=SPOTIFY_GRAY,
            font=("Arial", 11))
        self.playlist_dropdown.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ctk.CTkButton(playlist_select_frame, text="➕", width=35, height=28, corner_radius=8,
                    command=lambda: self.create_new_playlist(controller), 
                    fg_color=SPOTIFY_GREEN, hover_color="#1ed760",
                    font=("Arial", 16)).pack(side="left", padx=2)
        
        ctk.CTkButton(playlist_select_frame, text="🗑️", width=35, height=28, corner_radius=8,
                    command=lambda: self.delete_current_playlist(controller), 
                    fg_color="#8B0000", hover_color="#A52A2A",
                    font=("Arial", 14)).pack(side="left", padx=2)
        
        self.playlist_box = ctk.CTkTextbox(self.frame_playlist, fg_color=SPOTIFY_GRAY, 
                                        text_color=SPOTIFY_WHITE, border_color=SPOTIFY_DARK_GRAY,
                                        corner_radius=10, font=("Consolas", 11))
        self.playlist_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.playlist_box.configure(state="disabled")

        # Middle: Library
        self.frame_library = ctk.CTkFrame(content, width=380, corner_radius=15, fg_color=SPOTIFY_DARK_GRAY)
        self.frame_library.pack(side="left", fill="both", expand=True, padx=8)
        
        library_header = ctk.CTkFrame(self.frame_library, height=50, fg_color=SPOTIFY_GRAY, corner_radius=10)
        library_header.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(library_header, text="🎵 Daftar Lagu", font=("Arial", 16, "bold"), 
                    text_color=SPOTIFY_WHITE).pack(side="left", padx=15, pady=10)
        
        self.library_box = ctk.CTkTextbox(self.frame_library, fg_color=SPOTIFY_GRAY, 
                                        text_color=SPOTIFY_WHITE, border_color=SPOTIFY_DARK_GRAY,
                                        corner_radius=10, font=("Consolas", 11))
        self.library_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.library_box.bind("<Button-1>", lambda e: self.on_library_click(controller, e))
        self.library_items = []
        self.selected_index = None
        self.refresh_library(controller)

        # Right: Playlist Actions
        self.frame_playlist_action = ctk.CTkFrame(content, width=380, corner_radius=15, fg_color=SPOTIFY_DARK_GRAY)
        self.frame_playlist_action.pack(side="left", fill="both", expand=True, padx=(8, 0))
        
        action_header = ctk.CTkFrame(self.frame_playlist_action, height=50, fg_color=SPOTIFY_GRAY, corner_radius=10)
        action_header.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(action_header, text="⚡ Kelola Playlist", font=("Arial", 16, "bold"), 
                    text_color=SPOTIFY_WHITE).pack(side="left", padx=15, pady=10)
        
        action_content = ctk.CTkFrame(self.frame_playlist_action, fg_color="transparent")
        action_content.pack(fill="both", expand=True, padx=15, pady=10)
        
        ctk.CTkLabel(action_content, text="ID Lagu:", font=("Arial", 12), 
                    text_color=SPOTIFY_LIGHT_GRAY).pack(anchor="w", pady=(10, 5))
        self.song_id_entry = ctk.CTkEntry(action_content, height=35, corner_radius=10,
                                        placeholder_text="Masukkan ID...",
                                        fg_color=SPOTIFY_GRAY, border_color=SPOTIFY_GRAY, 
                                        text_color=SPOTIFY_WHITE)
        self.song_id_entry.pack(fill="x", pady=(0, 15))
        
        ctk.CTkButton(action_content, text="➕ Tambah ke Playlist", height=40, corner_radius=10,
                    command=lambda: self.add_to_playlist(controller), 
                    fg_color=SPOTIFY_GREEN, hover_color="#1ed760", 
                    font=("Arial", 13, "bold")).pack(fill="x", pady=5)
        
        ctk.CTkButton(action_content, text="➖ Hapus dari Playlist", height=40, corner_radius=10,
                    command=lambda: self.remove_from_playlist(controller), 
                    fg_color=SPOTIFY_GRAY, hover_color="#3E3E3E",
                    font=("Arial", 13, "bold")).pack(fill="x", pady=5)
        
        ctk.CTkButton(action_content, text="🗑️ Kosongkan Playlist", height=40, corner_radius=10,
                    command=lambda: self.clear_playlist(controller), 
                    fg_color="#8B0000", hover_color="#A52A2A",
                    font=("Arial", 13, "bold")).pack(fill="x", pady=5)
        
        self.status_label = ctk.CTkLabel(action_content, text="", font=("Arial", 11),
                                        text_color=SPOTIFY_GREEN, wraplength=300)
        self.status_label.pack(pady=15)

        # Bottom: Player Controls (Fixed at bottom)
        self.frame_control = ctk.CTkFrame(self, height=140, fg_color=SPOTIFY_DARK_GRAY, corner_radius=0)
        self.frame_control.pack(side="bottom", fill="x", padx=0, pady=0)
        
        # Now Playing Label
        self.current_label = ctk.CTkLabel(self.frame_control, text="▶️ Tidak ada lagu yang diputar", 
                                        font=("Arial", 13, "bold"), text_color=SPOTIFY_WHITE)
        self.current_label.pack(pady=(10, 5))
        
        # Seekbar with time labels
        seekbar_frame = ctk.CTkFrame(self.frame_control, fg_color="transparent")
        seekbar_frame.pack(fill="x", padx=20, pady=(0, 5))
        
        self.time_current = ctk.CTkLabel(seekbar_frame, text="0:00", font=("Arial", 10),
                                        text_color=SPOTIFY_LIGHT_GRAY)
        self.time_current.pack(side="left", padx=5)
        
        self.seekbar = ctk.CTkSlider(seekbar_frame, from_=0, to=100, 
                                    command=lambda v: self.seek_song(controller, v),
                                    fg_color=SPOTIFY_GRAY, progress_color=SPOTIFY_GREEN,
                                    button_color=SPOTIFY_GREEN, button_hover_color="#1ed760")
        self.seekbar.pack(side="left", fill="x", expand=True, padx=5)
        self.seekbar.set(0)
        
        self.time_total = ctk.CTkLabel(seekbar_frame, text="0:00", font=("Arial", 10),
                                      text_color=SPOTIFY_LIGHT_GRAY)
        self.time_total.pack(side="left", padx=5)
        
        # Control Buttons
        control_btns = ctk.CTkFrame(self.frame_control, fg_color="transparent")
        control_btns.pack()
        
        ctk.CTkButton(control_btns, text="⏮️", width=60, height=40, corner_radius=20,
                    command=lambda: self.previous_song(controller), 
                    fg_color=SPOTIFY_GRAY, hover_color="#3E3E3E",
                    font=("Arial", 16)).grid(row=0, column=0, padx=5)
        
        ctk.CTkButton(control_btns, text="▶️ Putar", width=120, height=40, corner_radius=20,
                    command=lambda: self.play_selected(controller), 
                    fg_color=SPOTIFY_GREEN, hover_color="#1ed760",
                    font=("Arial", 14, "bold")).grid(row=0, column=1, padx=5)
        
        ctk.CTkButton(control_btns, text="⏸️", width=60, height=40, corner_radius=20,
                    command=lambda: self.pause_resume(controller), 
                    fg_color=SPOTIFY_GRAY, hover_color="#3E3E3E",
                    font=("Arial", 16)).grid(row=0, column=2, padx=5)
        
        ctk.CTkButton(control_btns, text="⏹️", width=60, height=40, corner_radius=20,
                    command=lambda: self.stop_music(controller), 
                    fg_color=SPOTIFY_GRAY, hover_color="#3E3E3E",
                    font=("Arial", 16)).grid(row=0, column=3, padx=5)
        
        ctk.CTkButton(control_btns, text="⏭️", width=60, height=40, corner_radius=20,
                    command=lambda: self.next_song(controller), 
                    fg_color=SPOTIFY_GRAY, hover_color="#3E3E3E",
                    font=("Arial", 16)).grid(row=0, column=4, padx=5)
        
        # Volume Control
        volume_frame = ctk.CTkFrame(self.frame_control, fg_color="transparent")
        volume_frame.pack(side="right", padx=20)
        
        ctk.CTkLabel(volume_frame, text="🔊", font=("Arial", 14)).pack(
            side="left", padx=5)
        self.volume_slider = ctk.CTkSlider(
            volume_frame, from_=0, to=100, width=120,
            command=lambda v: self.change_volume(controller, v),
            button_color=SPOTIFY_GREEN, 
            button_hover_color="#1ed760",
            progress_color=SPOTIFY_GREEN)
        self.volume_slider.set(70)
        self.volume_slider.pack(side="left", padx=5)
        
        self.controller = controller

    def check_song_ended(self):
        import pygame
        try:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    if self.controller.player.current_song:
                        similar_songs = self.controller.player.get_similar_songs(
                            self.controller.player.current_song)
                        if similar_songs:
                            import random
                            next_song = random.choice(similar_songs)
                            
                            def update_status(msg):
                                self.current_label.configure(text=f"♪ {next_song.title}")
                            
                            msg = self.controller.player.play_song(next_song, callback=update_status)
                            self.current_label.configure(text=f"⏳ {next_song.title}")
                            self.seekbar.set(0)
            
            if self.controller.player.is_playing and self.controller.player.current_song:
                current_pos = pygame.mixer.music.get_pos() / 1000.0
                duration_str = self.controller.player.current_song.duration
                try:
                    parts = duration_str.split(":")
                    if len(parts) == 2:
                        total_seconds = int(parts[0]) * 60 + int(parts[1])
                    else:
                        total_seconds = 180
                    
                    if total_seconds > 0 and current_pos >= 0:
                        progress = (current_pos / total_seconds) * 100
                        self.seekbar.set(min(progress, 100))
                    
                    mins_curr = int(current_pos // 60)
                    secs_curr = int(current_pos % 60)
                    self.time_current.configure(text=f"{mins_curr}:{secs_curr:02d}")
                    
                    mins_total = int(total_seconds // 60)
                    secs_total = int(total_seconds % 60)
                    self.time_total.configure(text=f"{mins_total}:{secs_total:02d}")
                except:
                    pass
        except:
            pass
        self.after(100, self.check_song_ended)

    def on_library_click(self, controller, event):
        try:
            index = self.library_box.index("@%s,%s" % (event.x, event.y))
            line_number = int(index.split('.')[0]) - 1
            if 0 <= line_number < len(self.library_items):
                self.selected_index = line_number
                song = self.library_items[line_number]
                
                def update_status(msg):
                    self.current_label.configure(text=f"♪ {song.title}")
                
                msg = controller.player.play_song(song, callback=update_status)
                self.current_label.configure(text=f"⏳ {song.title}")
                self.seekbar.set(0)
        except:
            pass

    def refresh_library(self, controller):
        self.library_box.configure(state="normal")
        self.library_box.delete("1.0", "end")
        self.library_items = []
        art = controller.player.library.artists_head
        while art:
            song = art.songs_head
            while song:
                text = (f"{song.id}. {song.title} — {song.duration} "
                    f"({art.artist_name}) [{song.genre}]\n")
                self.library_box.insert("end", text)
                self.library_items.append(song)
                song = song.next
            art = art.next
        self.library_box.configure(state="disabled")
        self.selected_index = None

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
                    keyword in art.artist_name.lower() or 
                    keyword in song.genre.lower()):
                    text = (f"{song.id}. {song.title} — {song.duration} "
                        f"({art.artist_name}) [{song.genre}]\n")
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
                self.current_label.configure(text=f"♪ {song.title}")
            
            msg = controller.player.play_song(song, callback=update_status)
            self.current_label.configure(text=f"⏳ {song.title}")
            self.seekbar.set(0)

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
        song_id_str = self.song_id_entry.get().strip()
        if not song_id_str:
            return self.status_label.configure(text="Masukkan ID lagu!", text_color="#FF6B6B")
        try:
            song_id = int(song_id_str)
        except ValueError:
            return self.status_label.configure(text="ID harus angka!", text_color="#FF6B6B")
        
        found_song = None
        art = controller.player.library.artists_head
        while art and not found_song:
            song = art.songs_head
            while song:
                if str(song.id) == str(song_id):
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
            self.song_id_entry.delete(0, 'end')
        else:
            self.status_label.configure(
                text=f"Lagu ID {song_id} tidak ditemukan!", 
                text_color="#FF6B6B")

    def remove_from_playlist(self, controller):
        song_id_str = self.song_id_entry.get().strip()
        if not song_id_str:
            return self.status_label.configure(
                text="Masukkan ID lagu yang ingin dihapus!", 
                text_color="#FF6B6B")
        try:
            song_id = int(song_id_str)
        except ValueError:
            return self.status_label.configure(text="ID harus angka!", text_color="#FF6B6B")
        
        playlist = controller.player.playlist
        if not playlist.head:
            return self.status_label.configure(text="Playlist kosong!", text_color="#FF6B6B")
        
        if str(playlist.head.song.id) == str(song_id):
            if playlist.head == playlist.tail:
                playlist.head = playlist.tail = None
            else:
                playlist.head = playlist.head.next
                if playlist.head:
                    playlist.head.prev = None
            self.refresh_playlist(controller)
            self.status_label.configure(
                text=f"Lagu ID {song_id} dihapus dari playlist!", 
                text_color=SPOTIFY_GREEN)
            self.song_id_entry.delete(0, 'end')
            return
        
        curr = playlist.head
        while curr:
            if str(curr.song.id) == str(song_id):
                if curr.prev:
                    curr.prev.next = curr.next
                if curr.next:
                    curr.next.prev = curr.prev
                if curr == playlist.tail:
                    playlist.tail = curr.prev
                self.refresh_playlist(controller)
                self.status_label.configure(
                    text=f"Lagu ID {song_id} dihapus dari playlist!", 
                    text_color=SPOTIFY_GREEN)
                self.song_id_entry.delete(0, 'end')
                return
            curr = curr.next
        self.status_label.configure(
            text=f"Lagu ID {song_id} tidak ada di playlist!", 
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
        if self.selected_index is None:
            self.selected_index = 0 if self.library_items else None
            if self.selected_index is None: return
        else:
            self.selected_index = min(self.selected_index + 1, len(self.library_items) - 1)
        if 0 <= self.selected_index < len(self.library_items):
            song = self.library_items[self.selected_index]
            
            def update_status(msg):
                self.current_label.configure(text=f"♪ {song.title}")
            
            msg = controller.player.play_song(song, callback=update_status)
            self.current_label.configure(text=f"⏳ {song.title}")
            self.seekbar.set(0)

    def previous_song(self, controller):
        if self.selected_index is None: 
            self.selected_index = 0
        else:
            self.selected_index = max(self.selected_index - 1, 0)
        if 0 <= self.selected_index < len(self.library_items):
            song = self.library_items[self.selected_index]
            
            def update_status(msg):
                self.current_label.configure(text=f"♪ {song.title}")
            
            msg = controller.player.play_song(song, callback=update_status)
            self.current_label.configure(text=f"⏳ {song.title}")
            self.seekbar.set(0)

    def create_new_playlist(self, controller):
        from tkinter import simpledialog
        name = simpledialog.askstring("Playlist Baru", "Nama playlist:")
        if name:
            controller.player.playlist_manager.create_playlist(name)
            self.update_playlist_dropdown(controller)
            self.playlist_dropdown.set(name)
            controller.player.playlist_manager.active_playlist = (
                controller.player.playlist_manager.get_playlist(name))
            self.status_label.configure(
                text=f"Playlist '{name}' dibuat!", 
                text_color=SPOTIFY_GREEN)

    def delete_current_playlist(self, controller):
        current = self.playlist_dropdown.get()
        if current == "My Playlist":
            return self.status_label.configure(
                text="Tidak bisa hapus playlist default!", 
                text_color="#FF6B6B")
        controller.player.playlist_manager.delete_playlist(current)
        self.update_playlist_dropdown(controller)
        self.playlist_dropdown.set("My Playlist")
        controller.player.playlist_manager.active_playlist = (
            controller.player.playlist_manager.get_playlist("My Playlist"))
        self.refresh_playlist(controller)
        self.status_label.configure(
            text=f"Playlist '{current}' dihapus!", 
            text_color=SPOTIFY_GREEN)

    def switch_playlist(self, controller, name):
        playlist = controller.player.playlist_manager.get_playlist(name)
        if playlist:
            controller.player.playlist_manager.active_playlist = playlist
            self.refresh_playlist(controller)

    def update_playlist_dropdown(self, controller):
        names = [p.name for p in controller.player.playlist_manager.playlists]
        self.playlist_dropdown.configure(values=names if names else ["My Playlist"])
    
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
