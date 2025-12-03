import customtkinter as ctk
from sistem import MusicPlayer

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Spotify Color Scheme
SPOTIFY_BLACK = "#121212"
SPOTIFY_DARK_GRAY = "#181818"
SPOTIFY_GRAY = "#282828"
SPOTIFY_GREEN = "#1DB954"
SPOTIFY_WHITE = "#FFFFFF"
SPOTIFY_LIGHT_GRAY = "#B3B3B3"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.player = MusicPlayer()
        artist = self.player.library.add_artist("Contoh Artist")
        album = artist.add_album("Contoh Album")
        album.add_song(1, "Contoh Lagu", "3:30")
        album.add_song(2, "Lagu Kedua", "4:05")
        self.title("CIC Music Player")
        self.geometry("1100x650")
        self.configure(fg_color=SPOTIFY_BLACK)
        self.container = ctk.CTkFrame(self, fg_color=SPOTIFY_BLACK)
        self.container.pack(fill="both", expand=True)
        self.frames = {}
        for F in (PageMenu, PageUser, PageAdmin):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.show_frame(PageMenu)

    def show_frame(self, page):
        self.frames[page].tkraise()

class PageMenu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=SPOTIFY_BLACK)
        ctk.CTkLabel(self, text="Selamat Datang di CIC Player", font=("Arial", 22, "bold"), text_color=SPOTIFY_WHITE).pack(pady=50)
        ctk.CTkButton(self, text="Masuk sebagai Pengguna", width=300, height=40, command=lambda: controller.show_frame(PageUser), fg_color=SPOTIFY_GREEN, hover_color="#1ed760", text_color=SPOTIFY_WHITE).pack(pady=20)
        ctk.CTkButton(self, text="Masuk sebagai Admin", width=300, height=40, command=lambda: controller.show_frame(PageAdmin), fg_color=SPOTIFY_GRAY, hover_color="#3E3E3E", text_color=SPOTIFY_WHITE).pack(pady=20)

class PageUser(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=SPOTIFY_BLACK)
        ctk.CTkButton(self, text="Kembali", width=100, command=lambda: controller.show_frame(PageMenu), fg_color=SPOTIFY_GRAY, hover_color="#3E3E3E").place(x=10, y=10)

        search_frame = ctk.CTkFrame(self, width=340, height=40, corner_radius=10, fg_color=SPOTIFY_DARK_GRAY)
        search_frame.place(x=360, y=10)
        ctk.CTkLabel(search_frame, text="Cari:", font=("Arial", 12), text_color=SPOTIFY_WHITE).place(x=10, y=8)
        self.search_entry = ctk.CTkEntry(search_frame, width=220, placeholder_text="Cari judul/artis...", fg_color=SPOTIFY_GRAY, border_color=SPOTIFY_GRAY, text_color=SPOTIFY_WHITE)
        self.search_entry.place(x=50, y=8)
        self.search_entry.bind("<Return>", lambda e: self.search_songs(controller))
        ctk.CTkButton(search_frame, text="🔍", width=40, command=lambda: self.search_songs(controller), fg_color=SPOTIFY_GREEN, hover_color="#1ed760").place(x=280, y=8)

        self.frame_playlist = ctk.CTkFrame(self, width=340, height=500, corner_radius=10, fg_color=SPOTIFY_DARK_GRAY)
        self.frame_playlist.place(x=10, y=60)
        ctk.CTkLabel(self.frame_playlist, text="Playlist", font=("Arial", 14, "bold"), text_color=SPOTIFY_WHITE).place(x=10, y=10)
        self.playlist_box = ctk.CTkTextbox(self.frame_playlist, width=320, height=440, fg_color=SPOTIFY_GRAY, text_color=SPOTIFY_WHITE, border_color=SPOTIFY_GRAY)
        self.playlist_box.place(x=10, y=50)
        self.playlist_box.configure(state="disabled")

        self.frame_library = ctk.CTkFrame(self, width=340, height=500, corner_radius=10, fg_color=SPOTIFY_DARK_GRAY)
        self.frame_library.place(x=360, y=60)
        ctk.CTkLabel(self.frame_library, text="Daftar Lagu", font=("Arial", 14, "bold"), text_color=SPOTIFY_WHITE).place(x=10, y=10)
        self.library_box = ctk.CTkTextbox(self.frame_library, width=320, height=440, fg_color=SPOTIFY_GRAY, text_color=SPOTIFY_WHITE, border_color=SPOTIFY_GRAY)
        self.library_box.place(x=10, y=50)
        self.library_items = []
        self.selected_index = None
        self.refresh_library(controller)

        self.frame_playlist_action = ctk.CTkFrame(self, width=340, height=500, corner_radius=10, fg_color=SPOTIFY_DARK_GRAY)
        self.frame_playlist_action.place(x=710, y=60)
        ctk.CTkLabel(self.frame_playlist_action, text="Kelola Playlist", font=("Arial", 14, "bold"), text_color=SPOTIFY_WHITE).place(x=10, y=10)
        ctk.CTkLabel(self.frame_playlist_action, text="Masukkan ID Lagu:", text_color=SPOTIFY_LIGHT_GRAY).place(x=10, y=50)
        self.song_id_entry = ctk.CTkEntry(self.frame_playlist_action, width=200, placeholder_text="Contoh: 1", fg_color=SPOTIFY_GRAY, border_color=SPOTIFY_GRAY, text_color=SPOTIFY_WHITE)
        self.song_id_entry.place(x=10, y=80)
        ctk.CTkButton(self.frame_playlist_action, text="Tambah ke Playlist", command=lambda: self.add_to_playlist(controller), width=200, fg_color=SPOTIFY_GREEN, hover_color="#1ed760").place(x=10, y=120)
        ctk.CTkButton(self.frame_playlist_action, text="Hapus dari Playlist", command=lambda: self.remove_from_playlist(controller), width=200, fg_color=SPOTIFY_GRAY, hover_color="#3E3E3E").place(x=10, y=160)
        ctk.CTkButton(self.frame_playlist_action, text="Kosongkan Playlist", command=lambda: self.clear_playlist(controller), width=200, fg_color=SPOTIFY_GRAY, hover_color="#3E3E3E").place(x=10, y=200)
        self.status_label = ctk.CTkLabel(self.frame_playlist_action, text="", text_color=SPOTIFY_GREEN)
        self.status_label.place(x=10, y=250)

        self.frame_control = ctk.CTkFrame(self, width=1070, height=70, fg_color=SPOTIFY_DARK_GRAY)
        self.frame_control.place(x=10, y=570)
        self.current_label = ctk.CTkLabel(self.frame_control, text="Lagu yang sedang diputar:", text_color=SPOTIFY_WHITE)
        self.current_label.place(relx=0.5, y=5, anchor="n")
        control_btns = ctk.CTkFrame(self.frame_control, fg_color=SPOTIFY_DARK_GRAY)
        control_btns.place(relx=0.5, y=35, anchor="n")
        ctk.CTkButton(control_btns, text="Putar", width=140, command=lambda: self.play_selected(controller), fg_color=SPOTIFY_GREEN, hover_color="#1ed760").grid(row=0, column=0, padx=15)
        ctk.CTkButton(control_btns, text="Berikutnya", width=140, command=lambda: self.next_song(controller), fg_color=SPOTIFY_GRAY, hover_color="#3E3E3E").grid(row=0, column=1, padx=15)
        ctk.CTkButton(control_btns, text="Sebelumnya", width=140, command=lambda: self.previous_song(controller), fg_color=SPOTIFY_GRAY, hover_color="#3E3E3E").grid(row=0, column=2, padx=15)

    def refresh_library(self, controller):
        self.library_box.configure(state="normal")
        self.library_box.delete("1.0", "end")
        self.library_items = []
        art = controller.player.library.artists_head
        while art:
            alb = art.albums_head
            while alb:
                song = alb.songs_head
                while song:
                    self.library_box.insert("end", f"{song.id}. {song.title} — {song.duration} ({art.artist_name} / {alb.album_name})\n")
                    self.library_items.append(song)
                    song = song.next
                alb = alb.next
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
            alb = art.albums_head
            while alb:
                song = alb.songs_head
                while song:
                    if keyword in song.title.lower() or keyword in art.artist_name.lower() or keyword in alb.album_name.lower():
                        self.library_box.insert("end", f"{song.id}. {song.title} — {song.duration} ({art.artist_name} / {alb.album_name})\n")
                        self.library_items.append(song)
                        found_count += 1
                    song = song.next
                alb = alb.next
            art = art.next
        
        if found_count == 0:
            self.library_box.insert("end", "Tidak ada hasil ditemukan.\n")
        self.library_box.configure(state="disabled")
        self.selected_index = None


    def get_first_song(self, controller):
        art = controller.player.library.artists_head
        return art.albums_head.songs_head if art and art.albums_head else None

    def play_selected(self, controller):
        song = self.get_first_song(controller)
        if song:
            self.current_label.configure(text=controller.player.play_song(song))

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
            alb = art.albums_head
            while alb and not found_song:
                song = alb.songs_head
                while song:
                    if str(song.id) == str(song_id):
                        found_song = song
                        break
                    song = song.next
                alb = alb.next
            art = art.next
        
        if found_song:
            controller.player.playlist.add_song(found_song)
            self.refresh_playlist(controller)
            self.status_label.configure(text=f"'{found_song.title}' ditambahkan!", text_color=SPOTIFY_GREEN)
            self.song_id_entry.delete(0, 'end')
        else:
            self.status_label.configure(text=f"Lagu ID {song_id} tidak ditemukan!", text_color="#FF6B6B")

    def remove_from_playlist(self, controller):
        song_id_str = self.song_id_entry.get().strip()
        if not song_id_str:
            return self.status_label.configure(text="Masukkan ID lagu yang ingin dihapus!", text_color="#FF6B6B")
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
            self.status_label.configure(text=f"Lagu ID {song_id} dihapus dari playlist!", text_color=SPOTIFY_GREEN)
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
                self.status_label.configure(text=f"Lagu ID {song_id} dihapus dari playlist!", text_color=SPOTIFY_GREEN)
                self.song_id_entry.delete(0, 'end')
                return
            curr = curr.next
        self.status_label.configure(text=f"Lagu ID {song_id} tidak ada di playlist!", text_color="#FF6B6B")

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
            self.current_label.configure(text=controller.player.play_song(self.library_items[self.selected_index]))

    def previous_song(self, controller):
        if self.selected_index is None: return
        self.selected_index = max(self.selected_index - 1, 0)
        if 0 <= self.selected_index < len(self.library_items):
            self.current_label.configure(text=controller.player.play_song(self.library_items[self.selected_index]))

class PageAdmin(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=SPOTIFY_BLACK)
        ctk.CTkButton(self, text="Kembali", width=100, command=lambda: controller.show_frame(PageMenu), fg_color=SPOTIFY_GRAY, hover_color="#3E3E3E").place(x=10, y=10)

        self.frame_library = ctk.CTkFrame(self, width=520, height=500, corner_radius=10, fg_color=SPOTIFY_DARK_GRAY)
        self.frame_library.place(x=10, y=60)
        ctk.CTkLabel(self.frame_library, text="Library Lagu", font=("Arial", 14, "bold"), text_color=SPOTIFY_WHITE).place(x=10, y=10)
        self.admin_library_box = ctk.CTkTextbox(self.frame_library, width=500, height=440, fg_color=SPOTIFY_GRAY, text_color=SPOTIFY_WHITE, border_color=SPOTIFY_GRAY)
        self.admin_library_box.place(x=10, y=50)
        self.refresh_admin_library(controller)

        self.frame_detail = ctk.CTkFrame(self, width=520, height=500, corner_radius=10, fg_color=SPOTIFY_DARK_GRAY)
        self.frame_detail.place(x=540, y=60)
        ctk.CTkLabel(self.frame_detail, text="Form Tambah Lagu", font=("Arial", 14, "bold"), text_color=SPOTIFY_WHITE).place(x=10, y=10)
        ctk.CTkLabel(self.frame_detail, text="Artis:", text_color=SPOTIFY_LIGHT_GRAY).place(x=10, y=50)
        self.artist_entry = ctk.CTkEntry(self.frame_detail, width=480, fg_color=SPOTIFY_GRAY, border_color=SPOTIFY_GRAY, text_color=SPOTIFY_WHITE)
        self.artist_entry.place(x=10, y=75)
        ctk.CTkLabel(self.frame_detail, text="Album:", text_color=SPOTIFY_LIGHT_GRAY).place(x=10, y=110)
        self.album_entry = ctk.CTkEntry(self.frame_detail, width=480, fg_color=SPOTIFY_GRAY, border_color=SPOTIFY_GRAY, text_color=SPOTIFY_WHITE)
        self.album_entry.place(x=10, y=135)
        ctk.CTkLabel(self.frame_detail, text="ID (opsional):", text_color=SPOTIFY_LIGHT_GRAY).place(x=10, y=170)
        self.id_entry = ctk.CTkEntry(self.frame_detail, width=200, fg_color=SPOTIFY_GRAY, border_color=SPOTIFY_GRAY, text_color=SPOTIFY_WHITE)
        self.id_entry.place(x=10, y=195)
        ctk.CTkLabel(self.frame_detail, text="Judul Lagu:", text_color=SPOTIFY_LIGHT_GRAY).place(x=10, y=230)
        self.title_entry = ctk.CTkEntry(self.frame_detail, width=480, fg_color=SPOTIFY_GRAY, border_color=SPOTIFY_GRAY, text_color=SPOTIFY_WHITE)
        self.title_entry.place(x=10, y=255)
        ctk.CTkLabel(self.frame_detail, text="Durasi (mm:ss):", text_color=SPOTIFY_LIGHT_GRAY).place(x=10, y=290)
        self.duration_entry = ctk.CTkEntry(self.frame_detail, width=200, fg_color=SPOTIFY_GRAY, border_color=SPOTIFY_GRAY, text_color=SPOTIFY_WHITE)
        self.duration_entry.place(x=10, y=315)
        self.error_label = ctk.CTkLabel(self.frame_detail, text="", text_color="#FF6B6B")
        self.error_label.place(x=10, y=350)
        ctk.CTkButton(self.frame_detail, text="Simpan Lagu", command=lambda: self.save_song_from_form(controller), width=280, fg_color=SPOTIFY_GREEN, hover_color="#1ed760").place(x=10, y=390)
        self.form_mode = "add"
        self.current_edit_song = None

        self.frame_control = ctk.CTkFrame(self, width=1070, height=70, fg_color=SPOTIFY_DARK_GRAY)
        self.frame_control.place(x=10, y=570)
        ctk.CTkLabel(self.frame_control, text="Panel Aksi Admin", text_color=SPOTIFY_WHITE).place(relx=0.5, y=5, anchor="n")
        button_frame = ctk.CTkFrame(self.frame_control, fg_color=SPOTIFY_DARK_GRAY)
        button_frame.place(relx=0.5, y=35, anchor="n")
        ctk.CTkButton(button_frame, text="Simpan", width=140, command=lambda: self.save_song_from_form(controller), fg_color=SPOTIFY_GREEN, hover_color="#1ed760").grid(row=0, column=0, padx=15)
        ctk.CTkButton(button_frame, text="Perbarui", width=140, command=lambda: self.update_song(controller), fg_color=SPOTIFY_GRAY, hover_color="#3E3E3E").grid(row=0, column=1, padx=15)
        ctk.CTkButton(button_frame, text="Hapus", width=140, command=lambda: self.delete_song(controller), fg_color="#8B0000", hover_color="#A52A2A").grid(row=0, column=2, padx=15)

    def refresh_admin_library(self, controller):
        self.admin_library_box.configure(state="normal")
        self.admin_library_box.delete("1.0", "end")
        art = controller.player.library.artists_head
        while art:
            alb = art.albums_head
            while alb:
                song = alb.songs_head
                while song:
                    self.admin_library_box.insert("end", f"{song.id}. {song.title} — {song.duration} ({art.artist_name} / {alb.album_name})\n")
                    song = song.next
                alb = alb.next
            art = art.next
        self.admin_library_box.configure(state="disabled")

    def clear_form(self):
        self.artist_entry.delete(0, 'end')
        self.album_entry.delete(0, 'end')
        self.id_entry.delete(0, 'end')
        self.title_entry.delete(0, 'end')
        self.duration_entry.delete(0, 'end')
        self.error_label.configure(text="")
        self.form_mode = "add"
        self.current_edit_song = None

    def save_song_from_form(self, controller):
        artist_name, album_name, title, duration = self.artist_entry.get().strip(), self.album_entry.get().strip(), self.title_entry.get().strip(), self.duration_entry.get().strip()
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

        found_album = None
        alb = found_artist.albums_head
        while alb:
            if alb.album_name == album_name:
                found_album = alb
                break
            alb = alb.next
        if not found_album:
            found_album = found_artist.add_album(album_name or "Album Baru")

        if song_id is None:
            max_id = 0
            a = lib.artists_head
            while a:
                b = a.albums_head
                while b:
                    s = b.songs_head
                    while s:
                        try:
                            if int(s.id) > max_id:
                                max_id = int(s.id)
                        except Exception:
                            pass
                        s = s.next
                    b = b.next
                a = a.next
            song_id = max_id + 1

        found_album.add_song(song_id, title, duration)
        controller.frames[PageUser].refresh_library(controller)
        self.refresh_admin_library(controller)
        self.clear_form()
        self.error_label.configure(text="Lagu berhasil ditambahkan!", text_color=SPOTIFY_GREEN)

    def delete_song(self, controller):
        song_id_str = self.id_entry.get().strip()
        if not song_id_str:
            return self.error_label.configure(text="Masukkan ID lagu yang ingin dihapus!", text_color="#FF6B6B")
        try:
            song_id = int(song_id_str)
        except ValueError:
            return self.error_label.configure(text="ID harus berupa angka!", text_color="#FF6B6B")
        
        lib, found = controller.player.library, False
        art = lib.artists_head
        while art and not found:
            alb = art.albums_head
            while alb and not found:
                if alb.songs_head and str(alb.songs_head.id) == str(song_id):
                    alb.songs_head = alb.songs_head.next
                    found = True
                    break
                prev_song = alb.songs_head
                if prev_song:
                    curr_song = prev_song.next
                    while curr_song:
                        if str(curr_song.id) == str(song_id):
                            prev_song.next = curr_song.next
                            found = True
                            break
                        prev_song, curr_song = curr_song, curr_song.next
                alb = alb.next
            art = art.next
        
        if found:
            controller.frames[PageUser].refresh_library(controller)
            self.refresh_admin_library(controller)
            self.clear_form()
            self.error_label.configure(text=f"Lagu ID {song_id} berhasil dihapus!", text_color=SPOTIFY_GREEN)
        else:
            self.error_label.configure(text=f"Lagu dengan ID {song_id} tidak ditemukan!", text_color="#FF6B6B")

    def update_song(self, controller):
        song_id_str = self.id_entry.get().strip()
        if not song_id_str:
            return self.error_label.configure(text="Masukkan ID lagu yang ingin diperbarui!", text_color="#FF6B6B")
        title, duration = self.title_entry.get().strip(), self.duration_entry.get().strip()
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
            alb = art.albums_head
            while alb and not found:
                song = alb.songs_head
                while song:
                    if str(song.id) == str(song_id):
                        song.title, song.duration, found = title, duration, True
                        break
                    song = song.next
                alb = alb.next
            art = art.next
        
        if found:
            controller.frames[PageUser].refresh_library(controller)
            self.refresh_admin_library(controller)
            self.clear_form()
            self.error_label.configure(text=f"Lagu ID {song_id} berhasil diperbarui!", text_color=SPOTIFY_GREEN)
        else:
            self.error_label.configure(text=f"Lagu dengan ID {song_id} tidak ditemukan!", text_color="#FF6B6B")

app = App()
app.mainloop()
