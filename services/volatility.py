from db.models import get_rates, save_volatility
from datetime import datetime, timedelta

def calculate_daily_volatility(currency_pair, date):
    rates = get_rates(currency_pair, date, date)
    if not rates:
        return None
    return 0.0

def calculate_monthly_volatility(currency_pair, year, month):
    start = f"{year}-{month:02d}-01"
    if month == 12:
        end = f"{year+1}-01-01"
    else:
        end = f"{year}-{month+1:02d}-01"
    
    rates = get_rates(currency_pair, start, end)
    if len(rates) < 2:
        return None
    
    values = [r["rate"] for r in rates]
    high = max(values)
    low = min(values)
    avg = sum(values) / len(values)
    volatility = (high - low) / avg * 100
    return round(volatility, 4)

def calculate_weekly_volatility(currency_pair, year, week):
    start_date = datetime.strptime(f"{year}-W{week:02d}-1", "%Y-W%W-%w")
    end_date = start_date + timedelta(days=6)
    
    rates = get_rates(currency_pair, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    if len(rates) < 2:
        return None
    
    values = [r["rate"] for r in rates]
    high = max(values)
    low = min(values)
    avg = sum(values) / len(values)
    volatility = (high - low) / avg * 100
    return round(volatility, 4)