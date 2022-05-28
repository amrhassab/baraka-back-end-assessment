# baraka-back-end-assessment
application that returns the candles/bars for particular stocks

Results are cached for 5 minutes

# API 
@PK: symbol (stock symbol ex: APPL, TSLA)
@query-param: interval (candle interval": "minutes" or "hours" defaults to "minutes"
GET http://127.0.0.1:8000/baraka/data/stocks/:symbol/?interval=:interval
