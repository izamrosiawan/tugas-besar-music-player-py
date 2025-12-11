import pygame
import os

pygame.mixer.init()
pygame.init()

class SongNode:
    def __init__(self, id, title, duration, file_path=None, genre="Unknown", album=None):
        self.id = id
        self.title = title
        self.duration = duration
        self.file_path = file_path
        self.genre = genre
        self.album = album
        self.next = None


class AlbumNode:
    def __init__(self, album_name, year=None):
        self.album_name = album_name
        self.year = year
        self.songs = []
        self.next = None
    
    def add_song(self, song):
        self.songs.append(song)


class ArtistNode:
    def __init__(self, artist_name):
        self.artist_name = artist_name
        self.songs_head = None
        self.albums_head = None
        self.next = None

    def add_song(self, id, title, duration, file_path=None, genre="Unknown", album=None):
        new_song = SongNode(id, title, duration, file_path, genre, album)
        if not self.songs_head:
            self.songs_head = new_song
        else:
            curr = self.songs_head
            while curr.next:
                curr = curr.next
            curr.next = new_song
        return new_song
    
    def add_album(self, album_name, year=None):
        new_album = AlbumNode(album_name, year)
        if not self.albums_head:
            self.albums_head = new_album
        else:
            curr = self.albums_head
            while curr.next:
                curr = curr.next
            curr.next = new_album
        return new_album


class MusicLibrary:
    def __init__(self):
        self.artists_head = None

    def add_artist(self, name):
        new_artist = ArtistNode(name)
        if not self.artists_head:
            self.artists_head = new_artist
        else:
            curr = self.artists_head
            while curr.next:
                curr = curr.next
            curr.next = new_artist
        return new_artist


class PlaylistNode:
    def __init__(self, song):
        self.song = song
        self.prev = None
        self.next = None


class Playlist:
    def __init__(self, name="My Playlist"):
        self.name = name
        self.head = None
        self.tail = None

    def add_song(self, song):
        new_node = PlaylistNode(song)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node


class PlaylistManager:
    def __init__(self):
        self.playlists = []
        self.active_playlist = None
    
    def create_playlist(self, name):
        playlist = Playlist(name)
        self.playlists.append(playlist)
        if not self.active_playlist:
            self.active_playlist = playlist
        return playlist
    
    def delete_playlist(self, name):
        self.playlists = [p for p in self.playlists if p.name != name]
        if self.active_playlist and self.active_playlist.name == name:
            self.active_playlist = self.playlists[0] if self.playlists else None
    
    def get_playlist(self, name):
        for p in self.playlists:
            if p.name == name:
                return p
        return None
    
    def add_to_playlist(self, playlist_name, song):
        """Add song to specific playlist"""
        playlist = self.get_playlist(playlist_name)
        if playlist:
            playlist.add_song(song)
            return True
        return False


class PlayHistory:
    def __init__(self):
        self.stack = []

    def push(self, song):
        self.stack.append(song)

    def pop(self):
        return self.stack.pop() if self.stack else None


class PlayQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, song):
        self.queue.append(song)

    def dequeue(self):
        return self.queue.pop(0) if self.queue else None


class MusicPlayer:
    def __init__(self):
        self.library = MusicLibrary()
        self.playlist_manager = PlaylistManager()
        self.playlist_manager.create_playlist("My Playlist")
        self.history = PlayHistory()
        self.queue = PlayQueue()
        self.current_song = None
        self.is_playing = False
        self.is_paused = False
        self.volume = 0.7
        pygame.mixer.music.set_volume(self.volume)
        
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        
        self.start_time = 0
        self.pause_time = 0
    
    @property
    def playlist(self):
        return self.playlist_manager.active_playlist if self.playlist_manager.active_playlist else Playlist()

    def get_all_songs(self):
        songs = []
        curr_artist = self.library.artists_head
        while curr_artist:
            curr_song = curr_artist.songs_head
            while curr_song:
                songs.append(curr_song)
                curr_song = curr_song.next
            curr_artist = curr_artist.next
        return songs

    def play_song(self, song_node, callback=None):
        import time
        if self.current_song:
            self.history.push(self.current_song)
        
        self.current_song = song_node
        
        if song_node.file_path:
            try:
                if os.path.exists(song_node.file_path):
                    pygame.mixer.music.load(song_node.file_path)
                    pygame.mixer.music.play()
                    self.is_playing = True
                    self.is_paused = False
                    self.start_time = time.time()
                    self.pause_time = 0
                    return f"🎵 Memutar: {song_node.title}"
                else:
                    self.is_playing = False
                    return f"▶️ Memutar: {song_node.title} (file tidak ditemukan)"
            except Exception as e:
                self.is_playing = False
                return f"⚠️ Error memutar {song_node.title}: {str(e)}"
        else:
            self.is_playing = False
            return f"▶️ Memutar: {song_node.title} (audio tidak tersedia)"

    def pause_song(self):
        import time
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.pause_time = time.time()
            return "⏸️ Musik dijeda"
        return "Tidak ada musik yang sedang diputar"

    def resume_song(self):
        import time
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            if self.pause_time > 0:
                pause_duration = time.time() - self.pause_time
                self.start_time += pause_duration
                self.pause_time = 0
            return "▶️ Musik dilanjutkan"
        return "Tidak ada musik yang dijeda"

    def stop_song(self):
        if self.is_playing or self.is_paused:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            return "⏹️ Musik dihentikan"
        return "Tidak ada musik yang sedang diputar"

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
        return f"🔊 Volume: {int(self.volume * 100)}%"

    def get_is_playing(self):
        return pygame.mixer.music.get_busy() and not self.is_paused
    
    def get_pos(self):
        import time
        if self.is_playing and not self.is_paused:
            return time.time() - self.start_time
        elif self.is_paused:
            return self.pause_time - self.start_time
        return 0

