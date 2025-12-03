from ingestion.instagram import ingest_instagram_daily_csv, ingest_instagram_posts
from ingestion.youtube import (
    fetch_youtube_channel_stats,
    save_youtube_channel_stats,
    fetch_youtube_videos,
    fetch_youtube_video_stats,
    save_youtube_video_stats,
)

def run_all_ingestion(date, config):
    # IG daily stats
    if config.get("ig_daily_csv"):
        ingest_instagram_daily_csv(config["ig_daily_csv"])

    # IG posts
    if config.get("ig_post_csv"):
        ingest_instagram_posts(config["ig_post_csv"])

    # YouTube channel stats
    if config.get("youtube"):
        key = config["youtube"]["api_key"]
        channel = config["youtube"]["channel_id"]

        stats = fetch_youtube_channel_stats(key, channel)
        save_youtube_channel_stats(date, stats["subscribers"], stats["views"])

        # Each video
        for vid in fetch_youtube_videos(key, channel):
            vstats = fetch_youtube_video_stats(key, vid)
            save_youtube_video_stats(vid, date, vstats)

    print("🎉 All ingestion completed.")