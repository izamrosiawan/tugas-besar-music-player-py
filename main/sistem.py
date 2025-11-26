# Backend — Struktur Data

class SongNode:
    def __init__(self, id, title, duration):
        self.id = id
        self.title = title
        self.duration = duration
        self.next = None


class AlbumNode:
    def __init__(self, album_name):
        self.album_name = album_name
        self.songs_head = None
        self.next = None

    def add_song(self, id, title, duration):
        new_song = SongNode(id, title, duration)
        if not self.songs_head:
            self.songs_head = new_song
        else:
            curr = self.songs_head
            while curr.next:
                curr = curr.next
            curr.next = new_song
        return new_song


class ArtistNode:
    def __init__(self, artist_name):
        self.artist_name = artist_name
        self.albums_head = None
        self.next = None

    def add_album(self, album_name):
        new_album = AlbumNode(album_name)
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


# Playlist

class PlaylistNode:
    def __init__(self, song):
        self.song = song
        self.prev = None
        self.next = None


class Playlist:
    def __init__(self):
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


# Stack & Queue

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


# Music Player (wrapper)

class MusicPlayer:
    def __init__(self):
        self.library = MusicLibrary()
        self.playlist = Playlist()
        self.history = PlayHistory()
        self.queue = PlayQueue()
        self.current_song = None

    def play_song(self, song_node):
        if self.current_song:
            self.history.push(self.current_song)
        self.current_song = song_node
        return f"Memutar lagu: {song_node.title}"
