from fastapi import APIRouter
from services.gdelt import get_news_by_currency
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/news")
def get_news(currency_pair: str, date: str):
    # 최근 3개월 체크
    today = datetime.today()
    three_months_ago = today - timedelta(days=90)
    request_date = datetime.strptime(date, "%Y-%m-%d")
    
    if request_date < three_months_ago:
        return {"available": False, "articles": []}
    
    articles = get_news_by_currency(currency_pair, date)
    return {"available": True, "articles": articles}