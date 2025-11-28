"""
YouTube ingestion skeleton.

Responsibilities:
- Fetch video stats
- Fetch daily performance
- Insert into: track_stats, fan_activity
"""

from db import get_db
import datetime


class YouTubeIngestor:
    def __init__(self, youtube_client):
        self.db = get_db()
        self.youtube = youtube_client

    # -----------------------------
    # DAILY VIDEO STATS
    # -----------------------------
    def ingest_daily_stats(self, track_id, youtube_video_id):
        today = datetime.date.today()
        stats = self.youtube.get_video_stats(youtube_video_id)

        sql = """
        INSERT INTO track_stats
            (track_id, platform, date, value_1, value_2, value_3)
        VALUES (?, 'youtube', ?, ?, ?, ?)
        ON CONFLICT(track_id, platform, date)
        DO UPDATE SET
            value_1=excluded.value_1,
            value_2=excluded.value_2,
            value_3=excluded.value_3;
        """

        self.db.execute(sql, (
            track_id,
            today,
            stats.get("views"),
            stats.get("likes"),
            stats.get("comments")
        ))

    # -----------------------------
    # FAN ACTIVITY (hourly traffic)
    # -----------------------------
    def ingest_fan_activity(self, artist_id, youtube_channel_id):
        # YouTube API exposes "realtime concurrent viewers" for live or streams
        # If not available, this function can be adapted later.
        activity = self.youtube.get_realtime_activity(youtube_channel_id)

        for hour, score in activity.items():
            sql = """
            INSERT INTO fan_activity (artist_id, platform, date, hour, activity_score)
            VALUES (?, 'youtube', ?, ?, ?)
            ON CONFLICT DO NOTHING;
            """

            self.db.execute(sql, (
                artist_id,
                datetime.date.today(),
                hour,
                score
            ))