import customtkinter as ctk
from tkinter import messagebox

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
        
        # Configure equal column weights
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_columnconfigure(2, weight=1)
        
        # Left: Playlist
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

        # Middle: Library
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

        # Right: Playlist Actions
        self.frame_playlist_action = ctk.CTkFrame(content, corner_radius=15, fg_color=SPOTIFY_DARK_GRAY)
        self.frame_playlist_action.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        
        action_header = ctk.CTkFrame(self.frame_playlist_action, height=50, fg_color=SPOTIFY_GRAY, corner_radius=10)
        action_header.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(action_header, text="⚡ Kelola Playlist", font=("Arial", 16, "bold"), 
                    text_color=SPOTIFY_WHITE).pack(side="left", padx=15, pady=10)
        
        action_content = ctk.CTkFrame(self.frame_playlist_action, fg_color="transparent")
        action_content.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Create new playlist
        ctk.CTkLabel(action_content, text="Nama Playlist Baru:", font=("Arial", 12), 
                    text_color=SPOTIFY_LIGHT_GRAY).pack(anchor="w", pady=(10, 5))
        self.new_playlist_entry = ctk.CTkEntry(action_content, height=35, corner_radius=10,
                                        placeholder_text="Masukkan nama...",
                                        fg_color=SPOTIFY_GRAY, border_color=SPOTIFY_GRAY, 
                                        text_color=SPOTIFY_WHITE)
        self.new_playlist_entry.pack(fill="x", pady=(0, 10))
        
        ctk.CTkButton(action_content, text="➕ Buat Playlist Baru", height=40, corner_radius=10,
                    command=lambda: self.create_user_playlist(controller), 
                    fg_color=SPOTIFY_GREEN, hover_color="#1ed760", 
                    font=("Arial", 13, "bold")).pack(fill="x", pady=5)
        
        # Add song to playlist
        ctk.CTkLabel(action_content, text="ID Lagu:", font=("Arial", 12), 
                    text_color=SPOTIFY_LIGHT_GRAY).pack(anchor="w", pady=(20, 5))
        self.song_id_entry = ctk.CTkEntry(action_content, height=35, corner_radius=10,
                                        placeholder_text="Masukkan ID...",
                                        fg_color=SPOTIFY_GRAY, border_color=SPOTIFY_GRAY, 
                                        text_color=SPOTIFY_WHITE)
        self.song_id_entry.pack(fill="x", pady=(0, 10))
        
        # Playlist selector
        ctk.CTkLabel(action_content, text="Pilih Playlist:", font=("Arial", 12), 
                    text_color=SPOTIFY_LIGHT_GRAY).pack(anchor="w", pady=(5, 5))
        
        self.user_playlist_dropdown = ctk.CTkOptionMenu(
            action_content, 
            values=["My Playlist"],
            fg_color=SPOTIFY_GRAY, 
            button_color=SPOTIFY_GREEN,
            button_hover_color="#1ed760",
            dropdown_fg_color=SPOTIFY_GRAY,
            font=("Arial", 11))
        self.user_playlist_dropdown.pack(fill="x", pady=(0, 10))
        
        ctk.CTkButton(action_content, text="➕ Tambah ke Playlist", height=40, corner_radius=10,
                    command=lambda: self.add_to_user_playlist(controller), 
                    fg_color=SPOTIFY_GREEN, hover_color="#1ed760", 
                    font=("Arial", 13, "bold")).pack(fill="x", pady=5)
        
        ctk.CTkButton(action_content, text="🗑️ Hapus Playlist", height=40, corner_radius=10,
                    command=lambda: self.delete_user_playlist(controller), 
                    fg_color="#8B0000", hover_color="#A52A2A",
                    font=("Arial", 13, "bold")).pack(fill="x", pady=5)
        
        self.status_label = ctk.CTkLabel(action_content, text="", font=("Arial", 11),
                                        text_color=SPOTIFY_GREEN, wraplength=300)
        self.status_label.pack(pady=15)

        # Bottom: Player Controls (Fixed at bottom)
        self.frame_control = ctk.CTkFrame(self, height=90, fg_color=SPOTIFY_DARK_GRAY, corner_radius=0)
        self.frame_control.pack(side="bottom", fill="x", padx=0, pady=0)
        
        # Seekbar di paling atas (read-only, tidak bisa di-drag)
        self.seekbar = ctk.CTkProgressBar(self.frame_control, height=4,
                                         progress_color=SPOTIFY_WHITE, fg_color="#4d4d4d")
        self.seekbar.set(0)
        self.seekbar.pack(fill="x", padx=20, pady=0)
        
        # Main control row dengan 3 section
        main_row = ctk.CTkFrame(self.frame_control, fg_color="transparent")
        main_row.pack(fill="x", padx=15, pady=(8, 8))
        
        # LEFT: Song Info 
        left_section = ctk.CTkFrame(main_row, fg_color="transparent", width=350)
        left_section.pack(side="left", fill="both", anchor="w")
        left_section.pack_propagate(False)
        
        # Song title
        self.current_label = ctk.CTkLabel(left_section, text="", 
                                        font=("Arial", 13, "bold"), text_color=SPOTIFY_WHITE, 
                                        anchor="w")
        self.current_label.pack(anchor="w", side="top")
        
        # Artist name
        self.artist_label = ctk.CTkLabel(left_section, text="", 
                                        font=("Arial", 11), text_color=SPOTIFY_LIGHT_GRAY, 
                                        anchor="w")
        self.artist_label.pack(anchor="w", side="top")
        
        # CENTER: Control Buttons (fixed center)
        center_section = ctk.CTkFrame(main_row, fg_color="transparent")
        center_section.pack(side="left", expand=True)
        
        # Buttons row
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
        
        # Timer row (centered)
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
        
        # RIGHT: Volume Control (same width as left for balance)
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
    
    # ===== FUNGSI PLAYLIST MANAGEMENT =====
    def create_user_playlist(self, controller):
        """Membuat playlist baru dari user"""
        playlist_name = self.new_playlist_entry.get().strip()
        if not playlist_name:
            messagebox.showwarning("Input Kosong", "Masukkan nama playlist!")
            return
        
        # Tambahkan ke sistem
        controller.player.playlist_manager.create_playlist(playlist_name)
        
        # Update dropdown
        self.update_playlist_dropdown(controller)
        
        # Clear input
        self.new_playlist_entry.delete(0, 'end')
        messagebox.showinfo("Sukses", f"Playlist '{playlist_name}' berhasil dibuat!")
    
    def add_to_user_playlist(self, controller):
        """Menambahkan lagu ke playlist user"""
        try:
            song_id = int(self.song_id_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "ID lagu harus berupa angka!")
            return
        
        playlist_name = self.user_playlist_dropdown.get()
        if playlist_name == "Pilih Playlist":
            messagebox.showwarning("Pilih Playlist", "Pilih playlist tujuan terlebih dahulu!")
            return
        
        # Cari lagu by ID
        current_artist = controller.player.artist_manager.head
        song_found = None
        
        while current_artist:
            if current_artist.albums_head:
                album = current_artist.albums_head
                while album:
                    for song in album.songs:
                        if song.id == song_id:
                            song_found = song
                            break
                    if song_found:
                        break
                    album = album.next
            if song_found:
                break
            current_artist = current_artist.next
        
        if not song_found:
            messagebox.showerror("Error", f"Lagu dengan ID {song_id} tidak ditemukan!")
            return
        
        # Add to playlist
        controller.player.playlist_manager.add_to_playlist(playlist_name, song_found)
        self.song_id_entry.delete(0, 'end')
        messagebox.showinfo("Sukses", f"Lagu '{song_found.title}' ditambahkan ke '{playlist_name}'!")
    
    def delete_user_playlist(self, controller):
        """Menghapus playlist user"""
        playlist_name = self.user_playlist_dropdown.get()
        if playlist_name == "Pilih Playlist":
            messagebox.showwarning("Pilih Playlist", "Pilih playlist yang akan dihapus!")
            return
        
        # Konfirmasi
        confirm = messagebox.askyesno("Konfirmasi", f"Hapus playlist '{playlist_name}'?")
        if not confirm:
            return
        
        # Hapus dari sistem
        controller.player.playlist_manager.delete_playlist(playlist_name)
        
        # Update dropdown
        self.update_playlist_dropdown(controller)
        messagebox.showinfo("Sukses", f"Playlist '{playlist_name}' berhasil dihapus!")
    
    def update_playlist_dropdown(self, controller):
        """Update dropdown dengan daftar playlist terbaru"""
        playlist_names = []
        current = controller.player.playlist_manager.head
        while current:
            playlist_names.append(current.name)
            current = current.next
        
        if playlist_names:
            self.user_playlist_dropdown.configure(values=playlist_names)
            self.user_playlist_dropdown.set(playlist_names[0])
        else:
            self.user_playlist_dropdown.configure(values=["Pilih Playlist"])
            self.user_playlist_dropdown.set("Pilih Playlist")
    
    # ===== FUNGSI GENRE PLAYLIST =====

    def check_song_ended(self):
        import pygame
        try:
            # Check pygame events
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
                    
                    # SELALU update seekbar dan timer
                    if total_seconds > 0 and current_pos >= 0:
                        progress = (current_pos / total_seconds)
                        self.seekbar.set(min(progress, 1.0))
                        
                        mins_curr = int(current_pos // 60)
                        secs_curr = int(current_pos % 60)
                        self.time_current.configure(text=f"{mins_curr}:{secs_curr:02d}")
                        
                        mins_total = int(total_seconds // 60)
                        secs_total = int(total_seconds % 60)
                        self.time_total.configure(text=f"{mins_total}:{secs_total:02d}")
                    
                    # Auto-play: cek jika music playing
                    if is_playing and is_busy:
                        # Trigger jika mendekati akhir (0.2s sebelum habis)
                        if current_pos >= total_seconds - 0.2:
                            print(f"[AUTO-PLAY] Next song at {current_pos:.1f}/{total_seconds}s")
                            pygame.mixer.music.stop()
                            self.next_song(self.controller)
                            return
                    
                    # Backup: jika music stopped tapi masih ada current_song
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
        
        # Kumpulkan semua genre unik
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
        
        # Tampilkan playlist per genre
        idx = 1
        for genre, songs in genres.items():
            text = f"{idx}. 🎧 {genre} Playlist ({len(songs)} lagu)\n"
            self.playlist_list_box.insert("end", text)
            self.playlist_items.append({"genre": genre, "songs": songs})
            idx += 1
        
        self.playlist_list_box.configure(state="disabled")
    
    def on_playlist_click(self, controller, event):
        try:
            index = self.playlist_list_box.index("@%s,%s" % (event.x, event.y))
            line_number = int(index.split('.')[0]) - 1
            if 0 <= line_number < len(self.playlist_items):
                playlist_data = self.playlist_items[line_number]
                self.show_playlist_songs(controller, playlist_data)
                print(f"[CLICK] Selected playlist: {playlist_data['genre']}")
        except Exception as e:
            print(f"[ERROR] on_playlist_click: {e}")
    
    def show_playlist_songs(self, controller, playlist_data):
        genre = playlist_data["genre"]
        songs = playlist_data["songs"]
        
        # Set mode playlist
        self.current_playlist_mode = genre
        self.selected_index = None  # Reset index saat ganti playlist
        
        # Update library box untuk menampilkan lagu dari playlist
        self.library_box.configure(state="normal")
        self.library_box.delete("1.0", "end")
        self.library_items = []
        
        self.library_box.insert("end", f"🎵 {genre} Playlist\n\n", "header")
        
        for song in songs:
            # Cari artist name
            artist_name = self.get_artist_name(controller, song)
            
            album_info = f" • {song.album}" if song.album else ""
            text = f"{song.id}. {song.title} — {song.duration} ({artist_name}){album_info}\n"
            self.library_box.insert("end", text)
            self.library_items.append(song)
        
        self.library_box.configure(state="disabled")
        print(f"[PLAYLIST] Mode: {genre} ({len(songs)} lagu, {len(self.library_items)} items loaded)")
        
        # Auto-play lagu pertama dari playlist
        if self.library_items:
            self.selected_index = 0
            first_song = self.library_items[0]
            artist_name = self.get_artist_name(controller, first_song)
            
            # Play lagu pertama
            controller.player.play_song(first_song)
            
            # Update UI
            self.current_label.configure(text=first_song.title)
            self.artist_label.configure(text=artist_name)
            self.seekbar.set(0)
            self.time_current.configure(text="0:00")
            self.time_total.configure(text=first_song.duration)
            self.is_playing_state = True
            self.play_pause_btn.configure(text="⏸")
            
            print(f"[AUTO-START] Playing: {first_song.title} ({artist_name})")
    
    def refresh_library(self, controller):
        # Reset mode playlist
        self.current_playlist_mode = None
        self.selected_index = None
        
        self.library_box.configure(state="normal")
        self.library_box.delete("1.0", "end")
        self.library_items = []
        art = controller.player.library.artists_head
        while art:
            song = art.songs_head
            while song:
                album_info = f" • {song.album}" if song.album else ""
                text = (f"{song.id}. {song.title} — {song.duration} "
                    f"({art.artist_name}){album_info} [{song.genre}]\n")
                self.library_box.insert("end", text)
                self.library_items.append(song)
                song = song.next
            art = art.next
        self.library_box.configure(state="disabled")
        print("[LIBRARY] Showing all songs")

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
        if not self.library_items:
            print("[NEXT] No songs in library")
            return
        
        mode = f"Playlist: {self.current_playlist_mode}" if self.current_playlist_mode else "All Songs"
        print(f"[NEXT] Mode: {mode}, Total songs: {len(self.library_items)}")
            
        if self.selected_index is None:
            self.selected_index = 0
        else:
            # Loop kembali ke awal jika sudah di akhir
            self.selected_index = (self.selected_index + 1) % len(self.library_items)
        
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
            print(f"[NEXT] Playing: {song.title} ({artist_name}) [index: {self.selected_index}/{len(self.library_items)-1}]")

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
