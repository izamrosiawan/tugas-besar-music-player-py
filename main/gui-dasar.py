import customtkinter as ctk
import tkinter as tk
from sistem import MusicPlayer


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# App utama
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.player = MusicPlayer()
        # Contoh data awal supaya UI punya lagu untuk diputar
        artist = self.player.library.add_artist("Contoh Artist")
        album = artist.add_album("Contoh Album")
        album.add_song(1, "Contoh Lagu", "3:30")
        album.add_song(2, "Lagu Kedua", "4:05")

        self.title("CIC Music Player")
        self.geometry("1100x650")

        # Container untuk halaman
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (PageMenu, PageUser, PageAdmin):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_frame(PageMenu)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


# Halaman 1 — Menu (Pengguna / Admin)
class PageMenu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Selamat Datang di CIC Player",
                    font=("Arial", 22, "bold")).pack(pady=50)

        ctk.CTkButton(self, text="Masuk sebagai Pengguna",
                    width=300, command=lambda: controller.show_frame(PageUser)).pack(pady=20)

        ctk.CTkButton(self, text="Masuk sebagai Admin",
                    width=300, command=lambda: controller.show_frame(PageAdmin)).pack(pady=20)


# Halaman 2 — Halaman Pengguna (versi perbaikan)
class PageUser(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

    # Tombol 'Kembali' untuk kembali ke menu utama
        ctk.CTkButton(self, text="Kembali",
                    width=100, command=lambda: controller.show_frame(PageMenu)).place(x=10, y=10)

    # Kiri — Playlist (daftar putar pengguna)
        self.frame_playlist = ctk.CTkFrame(self, width=340, height=500, corner_radius=10)
        self.frame_playlist.place(x=10, y=60)

        ctk.CTkLabel(self.frame_playlist, text="Playlist", font=("Arial", 14, "bold")).place(x=10, y=10)
        # playlist (tetap sebagai textbox read-only)
        self.playlist_box = ctk.CTkTextbox(self.frame_playlist, width=320, height=440)
        self.playlist_box.place(x=10, y=50)
        try:
            self.playlist_box.configure(state="disabled")
        except Exception:
            pass

    # Tengah — Daftar lagu (koleksi)
        self.frame_library = ctk.CTkFrame(self, width=340, height=500, corner_radius=10)
        self.frame_library.place(x=360, y=60)

        ctk.CTkLabel(self.frame_library, text="Daftar Lagu", font=("Arial", 14, "bold")).place(x=10, y=10)
        # Ganti dengan CTkTextbox seperti playlist supaya tidak kepotong
        self.library_box = ctk.CTkTextbox(self.frame_library, width=320, height=440)
        self.library_box.place(x=10, y=50)
        # list of SongNode in same order
        self.library_items = []
        self.selected_index = None
        # Isi daftar lagu dari backend
        self.refresh_library(controller)

        # Kanan — Info lagu / album (detail)
        self.frame_info = ctk.CTkFrame(self, width=340, height=500, corner_radius=10)
        self.frame_info.place(x=710, y=60)

        ctk.CTkLabel(self.frame_info, text="Info Lagu / Album", font=("Arial", 14, "bold")).place(x=10, y=10)
        self.info_label = ctk.CTkLabel(self.frame_info, text="Tidak ada lagu diputar", anchor="w")
        self.info_label.place(x=10, y=50)

    # Bawah — Kontrol pemutar
        self.frame_control = ctk.CTkFrame(self, width=1070, height=70)
        self.frame_control.place(x=10, y=570)

        self.current_label = ctk.CTkLabel(self.frame_control, text="Lagu yang sedang diputar:")
        self.current_label.place(relx=0.5, y=5, anchor="n")

        control_btns = ctk.CTkFrame(self.frame_control, fg_color="transparent")
        control_btns.place(relx=0.5, y=35, anchor="n")

        ctk.CTkButton(control_btns, text="Putar", width=140, command=lambda: self.play_selected(controller)).grid(row=0, column=0, padx=15)
        ctk.CTkButton(control_btns, text="Berikutnya", width=140, command=lambda: self.next_song(controller)).grid(row=0, column=1, padx=15)
        ctk.CTkButton(control_btns, text="Sebelumnya", width=140, command=lambda: self.previous_song(controller)).grid(row=0, column=2, padx=15)

    def refresh_library(self, controller):
        try:
            self.library_box.configure(state="normal")
            self.library_box.delete("1.0", "end")
        except Exception:
            pass
        self.library_items = []
        art = controller.player.library.artists_head
        idx = 0
        while art:
            alb = art.albums_head
            while alb:
                song = alb.songs_head
                while song:
                    display = f"{song.id}. {song.title} — {song.duration} ({art.artist_name} / {alb.album_name})\n"
                    try:
                        self.library_box.insert("end", display)
                    except Exception:
                        pass
                    self.library_items.append(song)
                    idx += 1
                    song = song.next
                alb = alb.next
            art = art.next
        # set read-only
        try:
            self.library_box.configure(state="disabled")
        except Exception:
            pass
        # reset selection
        self.selected_index = None


    def get_first_song(self, controller):
        art = controller.player.library.artists_head
        if not art:
            return None
        alb = art.albums_head
        if not alb:
            return None
        return alb.songs_head

    def play_selected(self, controller):
        # play first song (karena sekarang tidak ada selection)
        song = self.get_first_song(controller)
        if song:
            msg = controller.player.play_song(song)
            try:
                self.info_label.configure(text=f"{song.title} — {song.duration}")
                self.current_label.configure(text=msg)
            except Exception:
                pass

    def next_song(self, controller):
        if self.selected_index is None:
            if self.library_items:
                self.selected_index = 0
            else:
                return
        else:
            self.selected_index = min(self.selected_index + 1, len(self.library_items) - 1)
        # play the song
        if 0 <= self.selected_index < len(self.library_items):
            song = self.library_items[self.selected_index]
            msg = controller.player.play_song(song)
            try:
                self.info_label.configure(text=f"{song.title} — {song.duration}")
                self.current_label.configure(text=msg)
            except Exception:
                pass

    def previous_song(self, controller):
        if self.selected_index is None:
            return
        self.selected_index = max(self.selected_index - 1, 0)
        # play the song
        if 0 <= self.selected_index < len(self.library_items):
            song = self.library_items[self.selected_index]
            msg = controller.player.play_song(song)
            try:
                self.info_label.configure(text=f"{song.title} — {song.duration}")
                self.current_label.configure(text=msg)
            except Exception:
                pass

    def play_first(self, controller):
        song = self.get_first_song(controller)
        if song:
            msg = controller.player.play_song(song)
            # update UI
            try:
                self.info_label.configure(text=f"{song.title} — {song.duration}")
                self.current_label.configure(text=msg)
            except Exception:
                pass
        else:
            try:
                self.info_label.configure(text="Tidak ada lagu tersedia")
                self.current_label.configure(text="")
            except Exception:
                pass


# Halaman 3 — Halaman Admin (versi perbaikan)
class PageAdmin(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ctk.CTkButton(self, text="Kembali",
                    width=100, command=lambda: controller.show_frame(PageMenu)).place(x=10, y=10)

    # Kiri — Daftar lagu (Library)
        self.frame_library = ctk.CTkFrame(self, width=520, height=500, corner_radius=10)
        self.frame_library.place(x=10, y=60)

        ctk.CTkLabel(self.frame_library, text="Library Lagu", font=("Arial", 14, "bold")).place(x=10, y=10)
        # gunakan CTkTextbox seperti playlist
        self.admin_library_box = ctk.CTkTextbox(self.frame_library, width=500, height=440)
        self.admin_library_box.place(x=10, y=50)
        # isi awal
        self.refresh_admin_library(controller)
    # Kanan — Form tambah/edit lagu
        self.frame_detail = ctk.CTkFrame(self, width=520, height=500, corner_radius=10)
        self.frame_detail.place(x=540, y=60)

        ctk.CTkLabel(self.frame_detail, text="Form Tambah Lagu",
                    font=("Arial", 14, "bold")).place(x=10, y=10)

        # Form input
        ctk.CTkLabel(self.frame_detail, text="Artis:").place(x=10, y=50)
        self.artist_entry = ctk.CTkEntry(self.frame_detail, width=480)
        self.artist_entry.place(x=10, y=75)

        ctk.CTkLabel(self.frame_detail, text="Album:").place(x=10, y=110)
        self.album_entry = ctk.CTkEntry(self.frame_detail, width=480)
        self.album_entry.place(x=10, y=135)

        ctk.CTkLabel(self.frame_detail, text="ID (opsional):").place(x=10, y=170)
        self.id_entry = ctk.CTkEntry(self.frame_detail, width=200)
        self.id_entry.place(x=10, y=195)

        ctk.CTkLabel(self.frame_detail, text="Judul Lagu:").place(x=10, y=230)
        self.title_entry = ctk.CTkEntry(self.frame_detail, width=480)
        self.title_entry.place(x=10, y=255)

        ctk.CTkLabel(self.frame_detail, text="Durasi (mm:ss):").place(x=10, y=290)
        self.duration_entry = ctk.CTkEntry(self.frame_detail, width=200)
        self.duration_entry.place(x=10, y=315)

        # Error label
        self.error_label = ctk.CTkLabel(self.frame_detail, text="", text_color="red")
        self.error_label.place(x=10, y=350)

        # Simpan button di form
        ctk.CTkButton(self.frame_detail, text="Simpan Lagu", 
                    command=lambda: self.save_song_from_form(controller),
                    width=280).place(x=10, y=390)
        
        # Tambah mode tracking untuk form (add/update)
        self.form_mode = "add"  # "add" atau "update"
        self.current_edit_song = None  # menyimpan song yang sedang diedit
    # Bawah — Panel kontrol admin
        self.frame_control = ctk.CTkFrame(self, width=1070, height=70)
        self.frame_control.place(x=10, y=570)

        ctk.CTkLabel(self.frame_control, text="Panel Aksi Admin").place(relx=0.5, y=5, anchor="n")

        button_frame = ctk.CTkFrame(self.frame_control, fg_color="transparent")
        button_frame.place(relx=0.5, y=35, anchor="n")

        ctk.CTkButton(button_frame, text="Simpan", width=140, command=lambda: self.save_song_from_form(controller)).grid(row=0, column=0, padx=15)
        ctk.CTkButton(button_frame, text="Perbarui", width=140, command=lambda: self.update_song(controller)).grid(row=0, column=1, padx=15)
        ctk.CTkButton(button_frame, text="Hapus", width=140, command=lambda: self.delete_song(controller)).grid(row=0, column=2, padx=15)

    def refresh_admin_library(self, controller):
        try:
            self.admin_library_box.configure(state="normal")
            self.admin_library_box.delete("1.0", "end")
        except Exception:
            pass
        art = controller.player.library.artists_head
        while art:
            alb = art.albums_head
            while alb:
                song = alb.songs_head
                while song:
                    display = f"{song.id}. {song.title} — {song.duration} ({art.artist_name} / {alb.album_name})\n"
                    try:
                        self.admin_library_box.insert("end", display)
                    except Exception:
                        pass
                    song = song.next
                alb = alb.next
            art = art.next
        # set read-only
        try:
            self.admin_library_box.configure(state="disabled")
        except Exception:
            pass

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
        artist_name = self.artist_entry.get().strip()
        album_name = self.album_entry.get().strip()
        title = self.title_entry.get().strip()
        duration = self.duration_entry.get().strip()
        
        # Validasi input
        if not artist_name:
            self.error_label.configure(text="Artis wajib diisi!")
            return
        if not title:
            self.error_label.configure(text="Judul lagu wajib diisi!")
            return
        if not duration:
            self.error_label.configure(text="Durasi wajib diisi!")
            return
        
        try:
            song_id = int(self.id_entry.get().strip()) if self.id_entry.get().strip() else None
        except ValueError:
            self.error_label.configure(text="ID harus berupa angka!")
            return

        # cari artist jika ada
        lib = controller.player.library
        art = lib.artists_head
        found_artist = None
        while art:
            if art.artist_name == artist_name:
                found_artist = art
                break
            art = art.next
        if not found_artist:
            found_artist = lib.add_artist(artist_name)

        # cari album
        alb = found_artist.albums_head
        found_album = None
        while alb:
            if alb.album_name == album_name:
                found_album = alb
                break
            alb = alb.next
        if not found_album:
            found_album = found_artist.add_album(album_name or "Album Baru")

        # tambahkan lagu
        if song_id is None:
            # auto id: cari max id +1
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

        # refresh tampilan
        try:
            controller.frames[PageUser].refresh_library(controller)
        except Exception:
            pass
        try:
            self.refresh_admin_library(controller)
        except Exception:
            pass

        # clear form dan tampilkan pesan sukses
        self.clear_form()
        self.error_label.configure(text="Lagu berhasil ditambahkan!", text_color="green")

    def open_add_song(self, controller):
        pass

    def delete_song(self, controller):
        song_id_str = self.id_entry.get().strip()
        
        if not song_id_str:
            self.error_label.configure(text="Masukkan ID lagu yang ingin dihapus!", text_color="red")
            return
        
        try:
            song_id = int(song_id_str)
        except ValueError:
            self.error_label.configure(text="ID harus berupa angka!", text_color="red")
            return
        
        # Cari dan hapus lagu
        lib = controller.player.library
        art = lib.artists_head
        found = False
        
        while art and not found:
            alb = art.albums_head
            while alb and not found:
                # Cek apakah lagu pertama yang akan dihapus
                if alb.songs_head and str(alb.songs_head.id) == str(song_id):
                    alb.songs_head = alb.songs_head.next
                    found = True
                    break
                
                # Cari di linked list
                prev_song = alb.songs_head
                if prev_song:
                    curr_song = prev_song.next
                    while curr_song:
                        if str(curr_song.id) == str(song_id):
                            prev_song.next = curr_song.next
                            found = True
                            break
                        prev_song = curr_song
                        curr_song = curr_song.next
                
                alb = alb.next
            art = art.next
        
        if found:
            # Refresh tampilan
            try:
                controller.frames[PageUser].refresh_library(controller)
            except Exception:
                pass
            try:
                self.refresh_admin_library(controller)
            except Exception:
                pass
            
            self.clear_form()
            self.error_label.configure(text=f"Lagu ID {song_id} berhasil dihapus!", text_color="green")
        else:
            self.error_label.configure(text=f"Lagu dengan ID {song_id} tidak ditemukan!", text_color="red")

    def update_song(self, controller):
        song_id_str = self.id_entry.get().strip()
        
        if not song_id_str:
            self.error_label.configure(text="Masukkan ID lagu yang ingin diperbarui!", text_color="red")
            return
        
        artist_name = self.artist_entry.get().strip()
        album_name = self.album_entry.get().strip()
        title = self.title_entry.get().strip()
        duration = self.duration_entry.get().strip()
        
        if not title:
            self.error_label.configure(text="Judul lagu wajib diisi!", text_color="red")
            return
        if not duration:
            self.error_label.configure(text="Durasi wajib diisi!", text_color="red")
            return
        
        try:
            song_id = int(song_id_str)
        except ValueError:
            self.error_label.configure(text="ID harus berupa angka!", text_color="red")
            return
        
        # Cari lagu yang akan diupdate
        lib = controller.player.library
        art = lib.artists_head
        found = False
        
        while art and not found:
            alb = art.albums_head
            while alb and not found:
                song = alb.songs_head
                while song:
                    if str(song.id) == str(song_id):
                        # Update data lagu
                        song.title = title
                        song.duration = duration
                        found = True
                        break
                    song = song.next
                alb = alb.next
            art = art.next
        
        if found:
            # Refresh tampilan
            try:
                controller.frames[PageUser].refresh_library(controller)
            except Exception:
                pass
            try:
                self.refresh_admin_library(controller)
            except Exception:
                pass
            
            self.clear_form()
            self.error_label.configure(text=f"Lagu ID {song_id} berhasil diperbarui!", text_color="green")
        else:
            self.error_label.configure(text=f"Lagu dengan ID {song_id} tidak ditemukan!", text_color="red")



# Jalankan aplikasi
app = App()
app.mainloop()
