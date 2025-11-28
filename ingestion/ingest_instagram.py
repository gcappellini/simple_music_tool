"""
Instagram ingestion skeleton.

Responsibilities:
- Fetch hourly engagement data
- Insert into fan_activity (artist-level)
"""

from db import get_db
import datetime


class InstagramIngestor:
    def __init__(self, instagram_client):
        self.db = get_db()
        self.ig = instagram_client

    # -----------------------------
    # HOURLY FAN ACTIVITY
    # -----------------------------
    def ingest_fan_activity(self, artist_id, instagram_user_id):
        # Typically: active followers, online viewer distribution, or story viewers
        activity = self.ig.get_hourly_activity(instagram_user_id)

        today = datetime.date.today()

        for hour, score in activity.items():
            sql = """
            INSERT INTO fan_activity (artist_id, platform, date, hour, activity_score)
            VALUES (?, 'instagram', ?, ?, ?)
            ON CONFLICT DO NOTHING;
            """

            self.db.execute(sql, (
                artist_id,
                today,
                hour,
                score
            ))