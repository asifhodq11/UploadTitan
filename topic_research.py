import random
import requests
from job_logger import log_event

YOUTUBE_TRENDS_API = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"

def get_trending_topic():
    try:
        # Step 1: Pull trending keywords from Google Trends
        response = requests.get(YOUTUBE_TRENDS_API)
        topics = []
        if response.ok:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'xml')
            items = soup.find_all('title')[1:25]  # Skip the feed title
            topics = [item.text.strip() for item in items]

        # Step 2: Add niche keywords to diversify
        niche_keywords = [
            "AI tools", "Passive income", "Tech facts", "iPhone hacks",
            "Fitness tips", "Money saving", "Side hustle", "Luxury lifestyle",
            "Productivity hacks", "Cool gadgets", "Amazon finds", "Finance news"
        ]

        all_ideas = [f"{niche} - {trend}" for niche in niche_keywords for trend in topics]
        ranked_ideas = rank_by_potential(all_ideas)

        return ranked_ideas[0] if ranked_ideas else random.choice(niche_keywords)
    
    except Exception as e:
        print(f"[Topic Research Error]: {e}")
        return random.choice(["AI trends", "Latest tech", "Money tricks"])

def rank_by_potential(ideas):
    # TODO: Add AI-based ranking in future (GPT scoring or CTR predictor)
    random.shuffle(ideas)
    return ideas[:5]
