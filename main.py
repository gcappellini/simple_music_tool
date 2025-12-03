from recommendations.timing import best_hour_for_platform, save_recommendation

def generate_timing_recommendations():
    for platform in ["instagram", "youtube"]:
        best = best_hour_for_platform(platform)
        if best is not None:
            save_recommendation(platform, best, "Based on audience activity.")
            print(f"Best hour for {platform}: {best}")

if __name__ == "__main__":
    generate_timing_recommendations()