import customtkinter as ctk

SPOTIFY_BLACK = "#121212"
SPOTIFY_DARK_GRAY = "#181818"
SPOTIFY_GRAY = "#282828"
SPOTIFY_GREEN = "#1DB954"
SPOTIFY_WHITE = "#FFFFFF"
SPOTIFY_LIGHT_GRAY = "#B3B3B3"

class PageAdmin(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=SPOTIFY_BLACK)
        
        # Header
        header = ctk.CTkFrame(self, height=60, fg_color=SPOTIFY_DARK_GRAY, corner_radius=0)
        header.pack(fill="x", padx=0, pady=0)
        
        ctk.CTkButton(header, text="← Kembali", width=100, height=35, corner_radius=20,
                    command=lambda: controller.show_frame("PageMenu"), 
                    fg_color=SPOTIFY_GRAY, hover_color="#3E3E3E").place(x=15, y=12)
        
        ctk.CTkLabel(header, text="⚙️ Admin Panel - Kelola Musik", font=("Arial", 18, "bold"),
                    text_color=SPOTIFY_WHITE).place(x=450, y=15)
        
        # Content
        content = ctk.CTkFrame(self, fg_color=SPOTIFY_BLACK)
        content.pack(fill="both", expand=True, padx=15, pady=(10, 20))

        # Left: Library Display
        self.frame_library = ctk.CTkFrame(content, width=580, corner_radius=15, fg_color=SPOTIFY_DARK_GRAY)
        self.frame_library.pack(side="left", fill="both", expand=True, padx=(0, 8))
        
        library_header = ctk.CTkFrame(self.frame_library, height=50, fg_color=SPOTIFY_GRAY, corner_radius=10)
        library_header.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(library_header, text="📚 Library Lagu", font=("Arial", 16, "bold"), 
                    text_color=SPOTIFY_WHITE).pack(side="left", padx=15, pady=10)
        
        self.admin_library_box = ctk.CTkTextbox(self.frame_library, fg_color=SPOTIFY_GRAY, 
                                            text_color=SPOTIFY_WHITE, border_color=SPOTIFY_DARK_GRAY,
                                            corner_radius=10, font=("Consolas", 11))
        self.admin_library_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.refresh_admin_library(controller)

        # Right: Form
        self.frame_detail = ctk.CTkFrame(content, width=580, corner_radius=15, fg_color=SPOTIFY_DARK_GRAY)
        self.frame_detail.pack(side="left", fill="both", expand=True, padx=(8, 0))
        
        form_header = ctk.CTkFrame(self.frame_detail, height=50, fg_color=SPOTIFY_GRAY, corner_radius=10)
        form_header.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(form_header, text="✏️ Form Tambah/Edit Lagu", font=("Arial", 16, "bold"), 
                    text_color=SPOTIFY_WHITE).pack(side="left", padx=15, pady=10)
        
        form_content = ctk.CTkFrame(self.frame_detail, fg_color="transparent")
        form_content.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Form fields dengan styling lebih baik
        ctk.CTkLabel(form_content, text="Artis:", font=("Arial", 12, "bold"), 
                    text_color=SPOTIFY_LIGHT_GRAY).pack(anchor="w", pady=(5, 2))
        self.artist_entry = ctk.CTkEntry(form_content, height=35, corner_radius=10,
                                        fg_color=SPOTIFY_GRAY, border_color=SPOTIFY_GRAY, 
                                        text_color=SPOTIFY_WHITE, placeholder_text="Nama artis...")
        self.artist_entry.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(form_content, text="Genre:", font=("Arial", 12, "bold"), 
                    text_color=SPOTIFY_LIGHT_GRAY).pack(anchor="w", pady=(5, 2))
        self.genre_entry = ctk.CTkEntry(form_content, height=35, corner_radius=10,
                                    fg_color=SPOTIFY_GRAY, border_color=SPOTIFY_GRAY, 
                                    text_color=SPOTIFY_WHITE, 
                                    placeholder_text="Pop, Rock, R&B, Alternative, Electronic, Classic...")
        self.genre_entry.pack(fill="x", pady=(0, 10))
        
        row1 = ctk.CTkFrame(form_content, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 10))
        
        id_frame = ctk.CTkFrame(row1, fg_color="transparent")
        id_frame.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkLabel(id_frame, text="ID (opsional):", font=("Arial", 12, "bold"), 
                    text_color=SPOTIFY_LIGHT_GRAY).pack(anchor="w", pady=(5, 2))
        self.id_entry = ctk.CTkEntry(id_frame, height=35, corner_radius=10,
                                    fg_color=SPOTIFY_GRAY, border_color=SPOTIFY_GRAY, 
                                    text_color=SPOTIFY_WHITE, placeholder_text="Auto...")
        self.id_entry.pack(fill="x")
        
        duration_frame = ctk.CTkFrame(row1, fg_color="transparent")
        duration_frame.pack(side="left", fill="x", expand=True, padx=(5, 0))
        ctk.CTkLabel(duration_frame, text="Durasi:", font=("Arial", 12, "bold"), 
                    text_color=SPOTIFY_LIGHT_GRAY).pack(anchor="w", pady=(5, 2))
        self.duration_entry = ctk.CTkEntry(duration_frame, height=35, corner_radius=10,
                                        fg_color=SPOTIFY_GRAY, border_color=SPOTIFY_GRAY, 
                                        text_color=SPOTIFY_WHITE, placeholder_text="mm:ss")
        self.duration_entry.pack(fill="x")
        
        ctk.CTkLabel(form_content, text="Judul Lagu:", font=("Arial", 12, "bold"), 
                    text_color=SPOTIFY_LIGHT_GRAY).pack(anchor="w", pady=(5, 2))
        self.title_entry = ctk.CTkEntry(form_content, height=35, corner_radius=10,
                                    fg_color=SPOTIFY_GRAY, border_color=SPOTIFY_GRAY, 
                                    text_color=SPOTIFY_WHITE, placeholder_text="Judul lagu...")
        self.title_entry.pack(fill="x", pady=(0, 10))
        
        # File upload section
        ctk.CTkLabel(form_content, text="File Audio (opsional):", font=("Arial", 12, "bold"), 
                    text_color=SPOTIFY_LIGHT_GRAY).pack(anchor="w", pady=(5, 2))
        
        file_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        file_frame.pack(fill="x", pady=(0, 10))
        
        self.file_path_entry = ctk.CTkEntry(file_frame, height=35, corner_radius=10,
                                    fg_color=SPOTIFY_GRAY, border_color=SPOTIFY_GRAY, 
                                    text_color=SPOTIFY_WHITE, 
                                    placeholder_text="Pilih file MP3...")
        self.file_path_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ctk.CTkButton(file_frame, text="📁 Pilih File", width=120, height=35, corner_radius=10,
                    command=self.browse_file, 
                    fg_color=SPOTIFY_GRAY, hover_color="#3E3E3E",
                    font=("Arial", 12, "bold")).pack(side="left")
        
        self.error_label = ctk.CTkLabel(form_content, text="", font=("Arial", 11, "bold"),
                                    text_color="#FF6B6B", wraplength=500)
        self.error_label.pack(pady=10)
        
        # Action buttons
        btn_frame = ctk.CTkFrame(form_content, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(btn_frame, text="💾 Simpan", height=45, corner_radius=10,
                    command=lambda: self.save_song_from_form(controller), 
                    fg_color=SPOTIFY_GREEN, hover_color="#1ed760",
                    font=("Arial", 14, "bold")).pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        ctk.CTkButton(btn_frame, text="✏️ Perbarui", height=45, corner_radius=10,
                    command=lambda: self.update_song(controller), 
                    fg_color=SPOTIFY_GRAY, hover_color="#3E3E3E",
                    font=("Arial", 14, "bold")).pack(side="left", fill="x", expand=True, padx=5)
        
        ctk.CTkButton(btn_frame, text="🗑️ Hapus", height=45, corner_radius=10,
                    command=lambda: self.delete_song(controller), 
                    fg_color="#8B0000", hover_color="#A52A2A",
                    font=("Arial", 14, "bold")).pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        self.form_mode = "add"
        self.current_edit_song = None

    def browse_file(self):
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title="Pilih File Audio",
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")]
        )
        if file_path:
            self.file_path_entry.delete(0, 'end')
            self.file_path_entry.insert(0, file_path)

    def refresh_admin_library(self, controller):
        self.admin_library_box.configure(state="normal")
        self.admin_library_box.delete("1.0", "end")
        art = controller.player.library.artists_head
        while art:
            song = art.songs_head
            while song:
                text = (f"{song.id}. {song.title} — {song.duration} "
                    f"({art.artist_name}) [{song.genre}]\n")
                self.admin_library_box.insert("end", text)
                song = song.next
            art = art.next
        self.admin_library_box.configure(state="disabled")

    def clear_form(self):
        self.artist_entry.delete(0, 'end')
        self.genre_entry.delete(0, 'end')
        self.id_entry.delete(0, 'end')
        self.title_entry.delete(0, 'end')
        self.duration_entry.delete(0, 'end')
        self.file_path_entry.delete(0, 'end')
        self.error_label.configure(text="")
        self.form_mode = "add"
        self.current_edit_song = None

    def save_song_from_form(self, controller):
        artist_name = self.artist_entry.get().strip()
        genre_name = self.genre_entry.get().strip() or "Unknown"
        title = self.title_entry.get().strip()
        duration = self.duration_entry.get().strip()
        
        if not artist_name:
            return self.error_label.configure(text="Artis wajib diisi!")
        if not title:
            return self.error_label.configure(text="Judul lagu wajib diisi!")
        if not duration:
            return self.error_label.configure(text="Durasi wajib diisi!")
        try:
            song_id = int(self.id_entry.get().strip()) if self.id_entry.get().strip() else None
        except ValueError:
            return self.error_label.configure(text="ID harus berupa angka!")

        lib = controller.player.library
        found_artist = None
        art = lib.artists_head
        while art:
            if art.artist_name == artist_name:
                found_artist = art
                break
            art = art.next
        if not found_artist:
            found_artist = lib.add_artist(artist_name)

        if song_id is None:
            max_id = 0
            a = lib.artists_head
            while a:
                s = a.songs_head
                while s:
                    try:
                        if int(s.id) > max_id:
                            max_id = int(s.id)
                    except Exception:
                        pass
                    s = s.next
                a = a.next
            song_id = max_id + 1

        file_path = self.file_path_entry.get().strip() or None
        found_artist.add_song(song_id, title, duration, file_path, genre_name)
        controller.frames["PageUser"].refresh_library(controller)
        self.refresh_admin_library(controller)
        self.clear_form()
        self.error_label.configure(text="Lagu berhasil ditambahkan!", text_color=SPOTIFY_GREEN)

    def delete_song(self, controller):
        song_id_str = self.id_entry.get().strip()
        if not song_id_str:
            return self.error_label.configure(
                text="Masukkan ID lagu yang ingin dihapus!", 
                text_color="#FF6B6B")
        try:
            song_id = int(song_id_str)
        except ValueError:
            return self.error_label.configure(text="ID harus berupa angka!", text_color="#FF6B6B")
        
        lib, found = controller.player.library, False
        art = lib.artists_head
        while art and not found:
            if art.songs_head and str(art.songs_head.id) == str(song_id):
                art.songs_head = art.songs_head.next
                found = True
                break
            prev_song = art.songs_head
            if prev_song:
                curr_song = prev_song.next
                while curr_song:
                    if str(curr_song.id) == str(song_id):
                        prev_song.next = curr_song.next
                        found = True
                        break
                    prev_song, curr_song = curr_song, curr_song.next
            art = art.next
        
        if found:
            controller.frames["PageUser"].refresh_library(controller)
            self.refresh_admin_library(controller)
            self.clear_form()
            self.error_label.configure(
                text=f"Lagu ID {song_id} berhasil dihapus!", 
                text_color=SPOTIFY_GREEN)
        else:
            self.error_label.configure(
                text=f"Lagu dengan ID {song_id} tidak ditemukan!", 
                text_color="#FF6B6B")

    def update_song(self, controller):
        song_id_str = self.id_entry.get().strip()
        if not song_id_str:
            return self.error_label.configure(
                text="Masukkan ID lagu yang ingin diperbarui!", 
                text_color="#FF6B6B")
        title = self.title_entry.get().strip()
        duration = self.duration_entry.get().strip()
        genre = self.genre_entry.get().strip()
        if not title:
            return self.error_label.configure(text="Judul lagu wajib diisi!", text_color="#FF6B6B")
        if not duration:
            return self.error_label.configure(text="Durasi wajib diisi!", text_color="#FF6B6B")
        try:
            song_id = int(song_id_str)
        except ValueError:
            return self.error_label.configure(text="ID harus berupa angka!", text_color="#FF6B6B")
        
        lib, found = controller.player.library, False
        art = lib.artists_head
        while art and not found:
            song = art.songs_head
            while song:
                if str(song.id) == str(song_id):
                    song.title = title
                    song.duration = duration
                    if genre:
                        song.genre = genre
                    found = True
                    break
                song = song.next
            art = art.next
        
        if found:
            controller.frames["PageUser"].refresh_library(controller)
            self.refresh_admin_library(controller)
            self.clear_form()
            self.error_label.configure(
                text=f"Lagu ID {song_id} berhasil diperbarui!", 
                text_color=SPOTIFY_GREEN)
        else:
            self.error_label.configure(
                text=f"Lagu dengan ID {song_id} tidak ditemukan!", 
                text_color="#FF6B6B")
