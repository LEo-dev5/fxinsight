from sqlalchemy import text
from db.database import get_connection

def save_rates(currency_pair, rates):
    with get_connection() as conn:
        for rate in rates:
            conn.execute(
                text("""
                    INSERT INTO exchange_rates (currency_pair, date, rate)
                    VALUES (:currency_pair, :date, :rate)
                    ON CONFLICT (currency_pair, date) DO UPDATE SET rate = :rate
                """),
                {
                    "currency_pair": currency_pair,
                    "date": rate["date"],
                    "rate": rate["rate"]
                }
            )
        conn.commit()

def get_rates(currency_pair, start_date, end_date):
    with get_connection() as conn:
        result = conn.execute(
            text("""
                SELECT date, rate FROM exchange_rates
                WHERE currency_pair = :currency_pair
                AND date BETWEEN :start_date AND :end_date
                ORDER BY date
            """),
            {
                "currency_pair": currency_pair,
                "start_date": start_date,
                "end_date": end_date
            }
        )
        return [{"date": str(row[0]), "rate": float(row[1])} for row in result]
    
def save_volatility(currency_pair, date, period, value):
    with get_connection() as conn:
        conn.execute(
            text("""
                INSERT INTO volatility (currency_pair, date, period, value)
                VALUES (:currency_pair, :date, :period, :value)
                ON CONFLICT (currency_pair, date, period) DO UPDATE SET value = :value
            """),
            {
                "currency_pair": currency_pair,
                "date": date,
                "period": period,
                "value": value
            }
        )
        conn.commit()

def get_volatility(currency_pair, period, start_date, end_date):
    with get_connection() as conn:
        result = conn.execute(
            text("""
                SELECT date, value FROM volatility
                WHERE currency_pair = :currency_pair
                AND period = :period
                AND date BETWEEN :start_date AND :end_date
                ORDER BY date
            """),
            {
                "currency_pair": currency_pair,
                "period": period,
                "start_date": start_date,
                "end_date": end_date
            }
        )
        return [{"date": str(row[0]), "value": float(row[1])} for row in result]