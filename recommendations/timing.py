from storage.db import fetch_all, insert

def best_hour_for_platform(platform):
    rows = fetch_all("""
        SELECT hour, AVG(activity_score)
        FROM activity_hourly
        WHERE platform = ?
        GROUP BY hour
        ORDER BY AVG(activity_score) DESC
        LIMIT 1
    """, (platform,))
    
    if not rows:
        return None
    return rows[0][0]  # best hour

def save_recommendation(platform, best_hour, reason=""):
    query = """
    INSERT INTO posting_recommendation (platform, recommended_hour, reason)
    VALUES (?, ?, ?)
    """
    return insert(query, (platform, best_hour, reason))