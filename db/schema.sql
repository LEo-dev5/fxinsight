CREATE TABLE exchange_rates (
    id SERIAL PRIMARY KEY,
    currency_pair VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    rate DECIMAL(12, 6) NOT NULL,
    UNIQUE (currency_pair, date)
);

CREATE TABLE volatility (
    id SERIAL PRIMARY KEY,
    currency_pair VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    period VARCHAR(10) NOT NULL,
    value DECIMAL(10, 6) NOT NULL,
    UNIQUE (currency_pair, date, period)
);