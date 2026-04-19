import os
import requests
from dotenv import load_dotenv

load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")

SERIES_IDS = {
    "JPY/USD": "DEXJPUS",
    "KRW/USD": "DEXKOUS",
    "EUR/USD": "DEXUSEU",
    "달러인덱스": "DTWEXBGS",
    "GBP/USD": "DEXUSUK",
    "CAD/USD": "DEXCAUS",
    "CHF/USD": "DEXSZUS"
}

def fetch_rates(currency_pair, start_date, end_date):
    series_id = SERIES_IDS[currency_pair]
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": end_date
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = []
        for obs in data["observations"]:
            if obs["value"] != ".":
                results.append({
                    "date": obs["date"],
                    "rate": float(obs["value"])
                })
        return results
    except Exception as e:
        raise Exception(f"FRED API 요청 실패: {e}")
    
from db.models import save_rates

def fetch_and_save_all(start_date, end_date):
    for currency_pair in SERIES_IDS.keys():
        print(f"{currency_pair} 가져오는 중...")
        try:
            rates = fetch_rates(currency_pair, start_date, end_date)
            save_rates(currency_pair, rates)
            print(f"{currency_pair} 저장 완료 — {len(rates)}개")
        except Exception as e:
            print(f"{currency_pair} 실패: {e}")