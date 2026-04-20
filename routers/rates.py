from fastapi import APIRouter
from db.models import get_volatility
from datetime import date

router = APIRouter()

@router.get("/volatility")
def volatility(currency_pair: str, period: str, year: int):
    if period == "monthly":
        start = f"{year}-01-01"
        end = f"{year}-12-31"
    elif period == "weekly":
        start = f"{year}-01-01"
        end = f"{year}-12-31"
    else:
        start = f"{year}-01-01"
        end = f"{year}-12-31"
    
    data = get_volatility(currency_pair, period, start, end)
    return {"currency_pair": currency_pair, "period": period, "data": data}