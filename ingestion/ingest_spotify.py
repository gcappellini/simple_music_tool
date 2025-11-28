"""
Spotify ingestion skeleton.

Responsibilities:
- Fetch track metadata
- Fetch daily stats (streams, saves, followers)
- Fetch audio features
- Insert into: track, track_stats, audio_features
"""

from db import get_db
import datetime


class SpotifyIngestor:
    def __init__(self, spotify_client):
        """
        spotify_client = wrapper for your Spotify API calls
        """
        self.db = get_db()
        self.spotify = spotify_client

    # -----------------------------
    # TRACK METADATA
    # -----------------------------
    def ingest_artist_tracks(self, artist_id, spotify_artist_id):
        tracks = self.spotify.get_artist_tracks(spotify_artist_id)

        for t in tracks:
            self._upsert_track(artist_id, t)

    def _upsert_track(self, artist_id, track):
        sql = """
            INSERT INTO track (artist_id, title, spotify_id, release_date, duration_ms)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(spotify_id)
            DO UPDATE SET
                title=excluded.title,
                release_date=excluded.release_date,
                duration_ms=excluded.duration_ms;
        """
        self.db.execute(sql, (
            artist_id,
            track["name"],
            track["id"],
            track.get("release_date"),
            track.get("duration_ms")
        ))

    # -----------------------------
    # DAILY STATS
    # -----------------------------
    def ingest_daily_stats(self, track_id, spotify_track_id):
        today = datetime.date.today()
        stats = self.spotify.get_track_stats(spotify_track_id)

        sql = """
        INSERT INTO track_stats
            (track_id, platform, date, value_1, value_2, value_3)
        VALUES (?, 'spotify', ?, ?, ?, ?)
        ON CONFLICT(track_id, platform, date)
        DO UPDATE SET
            value_1=excluded.value_1,
            value_2=excluded.value_2,
            value_3=excluded.value_3;
        """

        self.db.execute(sql, (
            track_id,
            today,
            stats.get("streams"),
            stats.get("saves"),
            stats.get("playlist_adds")
        ))

    # -----------------------------
    # AUDIO FEATURES
    # -----------------------------
    def ingest_audio_features(self, track_id, spotify_track_id):
        features = self.spotify.get_track_audio_features(spotify_track_id)

        sql = """
        INSERT INTO audio_features (
            track_id, danceability, energy, valence, tempo,
            acousticness, instrumentalness, liveness, speechiness
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(track_id)
        DO UPDATE SET
            danceability=excluded.danceability,
            energy=excluded.energy,
            valence=excluded.valence,
            tempo=excluded.tempo,
            acousticness=excluded.acousticness,
            instrumentalness=excluded.instrumentalness,
            liveness=excluded.liveness,
            speechiness=excluded.speechiness;
        """

        self.db.execute(sql, (
            track_id,
            features.get("danceability"),
            features.get("energy"),
            features.get("valence"),
            features.get("tempo"),
            features.get("acousticness"),
            features.get("instrumentalness"),
            features.get("liveness"),
            features.get("speechiness")
        ))