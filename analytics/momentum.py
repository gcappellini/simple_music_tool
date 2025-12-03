from storage.db import fetch_all

def compute_post_momentum(post_id):
    """
    Very basic placeholder:
    momentum = (today_views - yesterday_views) / yesterday_views
    """
    stats = fetch_all(
        "SELECT date, views FROM post_stats WHERE post_id = ? ORDER BY date ASC",
        (post_id,)
    )
    if len(stats) < 2:
        return None
    
    (_, v1), (_, v2) = stats[-2], stats[-1]
    if v1 == 0:
        return None
    return (v2 - v1) / v1