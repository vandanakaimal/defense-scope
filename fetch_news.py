import requests

API_KEY = "ed55a22b0d5d42f1978363b89918b62b"  # ⬅️ Paste your NewsAPI key here

def fetch_news():
    url = (
        "https://newsapi.org/v2/everything?"
        "q=defense OR military OR DRDO OR missile OR war OR border&"
        "language=en&sortBy=publishedAt&"
        f"apiKey={API_KEY}"
    )
    response = requests.get(url)
    articles = response.json().get("articles", [])

    news_list = []
    for article in articles:
        news_list.append({
            "title": article["title"],
            "description": article["description"] or "",
            "source": article["source"]["name"],
            "date": article["publishedAt"][:10]
        })

    return news_list
