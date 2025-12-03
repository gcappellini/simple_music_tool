import csv
from storage.db import insert

def ingest_instagram_daily_csv(csv_path):
    """
    CSV format:
    date,followers,total_views,total_engagement
    2025-01-12,3512,9400,820
    """
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            query = """
            INSERT OR REPLACE INTO profile_stats (
                date, platform, followers, total_views, total_engagement
            ) VALUES (?, 'instagram', ?, ?, ?)
            """

            insert(query, (
                row["date"],
                int(row["followers"]),
                int(row["total_views"]),
                int(row["total_engagement"])
            ))

    print(f"✅ IG daily stats ingested from {csv_path}")

def ingest_instagram_posts(csv_path):
    """
    Handles BOTH post + post_stats ingestion.
    """
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:

            # 1. ensure post exists
            post_id = insert("""
                INSERT OR IGNORE INTO post (platform, external_id, created_at_post)
                VALUES ('instagram', ?, ?)
            """, (row["external_id"], row["date"]))

            # 2. fetch real internal ID
            if post_id == 0:
                # record already exists → fetch post_id
                from storage.db import fetch_one
                post_id = fetch_one(
                    "SELECT post_id FROM post WHERE external_id = ?",
                    (row["external_id"],)
                )[0]

            # 3. insert daily stats
            insert("""
                INSERT OR REPLACE INTO post_stats
                (post_id, date, views, likes, comments, shares, retention)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                post_id,
                row["date"],
                int(row["views"]),
                int(row["likes"]),
                int(row["comments"]),
                int(row.get("shares", 0) or 0),
                float(row.get("retention", 0) or 0),
            ))

    print(f"✅ IG post stats ingested from {csv_path}")

def ingest_instagram_hourly_activity(date, csv_path):
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            insert("""
                INSERT OR REPLACE INTO activity_hourly
                (platform, date, hour, activity_score)
                VALUES ('instagram', ?, ?, ?)
            """, (date, int(row["hour"]), float(row["activity_score"])))

    print(f"✅ IG hourly activity for {date} ingested.")