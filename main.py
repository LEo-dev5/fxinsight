from fastapi import FastAPI
from fastapi.responses import FileResponse
from routers import rates, news

from apscheduler.schedulers.background import BackgroundScheduler
from services.fred import fetch_and_save_all
from services.volatility import calculate_and_save_all
from datetime import datetime



app = FastAPI()

app.include_router(rates.router, prefix="/api")
app.include_router(news.router, prefix="/api")

@app.get("/")
def read_index():
    return FileResponse("static/index.html")


def daily_update():
    today = datetime.today()
    year = today.year
    date_str = today.strftime("%Y-%m-%d")
    print(f"자동 갱신 시작: {date_str}")
    fetch_and_save_all(date_str, date_str)
    calculate_and_save_all(year)
    print("자동 갱신 완료!")

scheduler = BackgroundScheduler()
scheduler.add_job(daily_update, 'cron', hour=7, minute=0)
scheduler.start()