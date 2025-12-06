import pygame
import os
import urllib.request
import tempfile
import threading

pygame.mixer.init()

class SongNode:
    def __init__(self, id, title, duration, file_path=None, genre="Unknown"):
        self.id = id
        self.title = title
        self.duration = duration
        self.file_path = file_path
        self.genre = genre
        self.next = None


class ArtistNode:
    def __init__(self, artist_name):
        self.artist_name = artist_name
        self.songs_head = None
        self.next = None

    def add_song(self, id, title, duration, file_path=None, genre="Unknown"):
        new_song = SongNode(id, title, duration, file_path, genre)
        if not self.songs_head:
            self.songs_head = new_song
        else:
            curr = self.songs_head
            while curr.next:
                curr = curr.next
            curr.next = new_song
        return new_song


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
        
        self.temp_dir = tempfile.gettempdir()
        self.cached_files = {}
    
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

    def get_similar_songs(self, current_song, limit=5):
        if not current_song:
            return []
        
        all_songs = self.get_all_songs()
        similar = [s for s in all_songs if s.genre == current_song.genre and s.id != current_song.id]
        return similar[:limit]
    
    def _download_and_play(self, song_node, url, callback=None):
        try:
            temp_file = os.path.join(self.temp_dir, f"music_{song_node.id}.mp3")
            urllib.request.urlretrieve(url, temp_file)
            self.cached_files[url] = temp_file
            
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            if callback:
                callback(f"🎵 Memutar: {song_node.title}")
        except Exception as e:
            self.is_playing = False
            if callback:
                callback(f"⚠️ Error: {str(e)}")

    def play_song(self, song_node, callback=None):
        if self.current_song:
            self.history.push(self.current_song)
        
        self.current_song = song_node
        
        if song_node.file_path:
            try:
                file_to_play = song_node.file_path
                
                if song_node.file_path.startswith('http://') or song_node.file_path.startswith('https://'):
                    if song_node.file_path in self.cached_files:
                        file_to_play = self.cached_files[song_node.file_path]
                        pygame.mixer.music.load(file_to_play)
                        pygame.mixer.music.play()
                        self.is_playing = True
                        self.is_paused = False
                        return f"🎵 Memutar: {song_node.title}"
                    else:
                        download_thread = threading.Thread(
                            target=self._download_and_play,
                            args=(song_node, song_node.file_path, callback),
                            daemon=True
                        )
                        download_thread.start()
                        return f"⏳ Memuat: {song_node.title}..."
                elif not os.path.exists(song_node.file_path):
                    self.is_playing = False
                    return f"▶️ Memutar: {song_node.title} (file tidak ditemukan)"
                else:
                    pygame.mixer.music.load(file_to_play)
                    pygame.mixer.music.play()
                    self.is_playing = True
                    self.is_paused = False
                    return f"🎵 Memutar: {song_node.title}"
            except Exception as e:
                self.is_playing = False
                return f"⚠️ Error memutar {song_node.title}: {str(e)}"
        else:
            self.is_playing = False
            return f"▶️ Memutar: {song_node.title} (audio tidak tersedia)"

    def pause_song(self):
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            return "⏸️ Musik dijeda"
        return "Tidak ada musik yang sedang diputar"

    def resume_song(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
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
    
    def seek(self, position_seconds):
        if self.is_playing or self.is_paused:
            try:
                pygame.mixer.music.set_pos(position_seconds)
                return True
            except:
                return False
        return False
    
    def get_pos(self):
        if self.is_playing or self.is_paused:
            return pygame.mixer.music.get_pos() / 1000.0
        return 0

