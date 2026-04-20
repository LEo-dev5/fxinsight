from db.models import get_rates, save_volatility
from datetime import datetime, timedelta
from db.models import save_volatility

def calculate_daily_volatility(currency_pair, date):
    from datetime import datetime, timedelta
    prev_date = (datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    
    today_rates = get_rates(currency_pair, date, date)
    prev_rates = get_rates(currency_pair, prev_date, prev_date)
    
    if not today_rates or not prev_rates:
        return None
    
    change = abs(today_rates[0]["rate"] - prev_rates[0]["rate"]) / prev_rates[0]["rate"] * 100
    return round(change, 4)

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

def calculate_and_save_all(year):
    currencies = ["JPY/USD", "KRW/USD", "EUR/USD", "달러인덱스", "GBP/USD", "CAD/USD", "CHF/USD"]
    
    for currency in currencies:
        print(f"{currency} 변동성 계산 중...")
        
        # 월별
        for month in range(1, 13):
            v = calculate_monthly_volatility(currency, year, month)
            if v:
                date = f"{year}-{month:02d}-01"
                save_volatility(currency, date, "monthly", v)
        
        # 주별
        for week in range(1, 53):
            v = calculate_weekly_volatility(currency, year, week)
            if v:
                from datetime import datetime
                date = datetime.strptime(f"{year}-W{week:02d}-1", "%Y-W%W-%w").strftime("%Y-%m-%d")
                save_volatility(currency, date, "weekly", v)
        
        # 일별
        from datetime import datetime, timedelta
        start = datetime(year, 1, 1)
        end = datetime(year, 12, 31)
        current = start
        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            v = calculate_daily_volatility(currency, date_str)
            if v:
                save_volatility(currency, date_str, "daily", v)
            current += timedelta(days=1)
        
        print(f"{currency} 완료!")