import requests
from storage.db import insert

def fetch_youtube_channel_stats(api_key, channel_id):
    url = (
        "https://www.googleapis.com/youtube/v3/channels?"
        "part=statistics&id=" + channel_id + "&key=" + api_key
    )
    r = requests.get(url).json()
    stats = r["items"][0]["statistics"]

    return {
        "subscribers": int(stats["subscriberCount"]),
        "views": int(stats["viewCount"])
    }

def save_youtube_channel_stats(date, subscribers, total_views):
    insert("""
        INSERT OR REPLACE INTO profile_stats
        (date, platform, followers, total_views)
        VALUES (?, 'youtube', ?, ?)
    """, (date, subscribers, total_views))

def fetch_youtube_videos(api_key, channel_id):
    url = (
        "https://www.googleapis.com/youtube/v3/search?"
        "part=id&order=date&maxResults=50&channelId="
        + channel_id + "&key=" + api_key
    )
    r = requests.get(url).json()
    return [item["id"]["videoId"] for item in r["items"] if item["id"]["kind"] == "youtube#video"]

def fetch_youtube_video_stats(api_key, video_id):
    url = (
        "https://www.googleapis.com/youtube/v3/videos?"
        "part=statistics,snippet&id=" + video_id + "&key=" + api_key
    )
    r = requests.get(url).json()
    item = r["items"][0]

    stats = item["statistics"]
    snippet = item["snippet"]

    return {
        "title": snippet["title"],
        "published": snippet["publishedAt"],
        "views": int(stats.get("viewCount", 0)),
        "likes": int(stats.get("likeCount", 0)),
        "comments": int(stats.get("commentCount", 0)),
    }

def save_youtube_video_stats(video_id, date, data):
    # ensure post
    post_id = insert("""
        INSERT OR IGNORE INTO post (platform, external_id, created_at_post, caption)
        VALUES ('youtube', ?, ?, ?)
    """, (video_id, data["published"], data["title"]))

    if post_id == 0:
        from storage.db import fetch_one
        post_id = fetch_one(
            "SELECT post_id FROM post WHERE external_id = ?",
            (video_id,)
        )[0]

    # insert stats
    insert("""
        INSERT OR REPLACE INTO post_stats
        (post_id, date, views, likes, comments)
        VALUES (?, ?, ?, ?, ?)
    """, (
        post_id,
        date,
        data["views"],
        data["likes"],
        data["comments"]
    ))