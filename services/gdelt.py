import requests
import time
from datetime import datetime, timedelta

CURRENCY_KEYWORDS = {
    "JPY/USD": "JPY yen BOJ Japan interest rate",
    "KRW/USD": "KRW won Korea BOK interest rate",
    "EUR/USD": "EUR euro ECB Europe interest rate",
    "달러인덱스": "dollar index DXY Fed Federal Reserve",
    "GBP/USD": "GBP pound sterling Bank of England",
    "CAD/USD": "CAD Canadian dollar Bank of Canada",
    "CHF/USD": "CHF Swiss franc SNB Switzerland"
}

def get_news_by_currency(currency_pair, date_str):
    keyword = CURRENCY_KEYWORDS.get(currency_pair, currency_pair)
    return fetch_news(keyword, date_str)

def fetch_news(keyword, date_str):
    try:
        time.sleep(5)  # 5초 대기
        date = datetime.strptime(date_str, "%Y-%m-%d")
        start = date.strftime("%Y%m%d%H%M%S")
        end = (date + timedelta(days=1)).strftime("%Y%m%d%H%M%S")

        url = "https://api.gdeltproject.org/api/v2/doc/doc"
        params = {
            "query": keyword,
            "mode": "artlist",
            "maxrecords": 5,
            "startdatetime": start,
            "enddatetime": end,
            "format": "json"
        }

        response = requests.get(url, params=params, timeout=30)  # 10 → 30으로
        response.raise_for_status()
        data = response.json()

        articles = []
        for article in data.get("articles", []):
            articles.append({
                "title": article.get("title", ""),
                "url": article.get("url", ""),
                "source": article.get("domain", ""),
                "date": date_str
            })
        return articles

    except Exception as e:
        print(f"에러: {e}")
        return []