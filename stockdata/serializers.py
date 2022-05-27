from rest_framework import serializers
from .models import Trade, Stock
from django.conf import settings
from datetime import datetime
from django.db.models import Max, Min
import enum


class Interval(enum.Enum):
    MINUTES = "minutes"
    HOURS = "hours"


START_TIME = settings.SERVICE_START_TIME
TIME_ZONE_OBJ = settings.TIME_ZONE_OBJ


class StockSerializer(serializers.ModelSerializer):
    candles = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Stock
        fields = '__all__'

    def get_candles(self, obj):
        interval = self.context['request'].query_params.get('interval', None)

        # Default interval is minutes
        if not interval or interval not in [e.value for e in Interval]:
            interval = Interval.MINUTES.value

        now = datetime.now(tz=TIME_ZONE_OBJ)

        trades = \
            obj.trade_set.filter(
                time__year=now.year,
                time__month=now.month,
                time__day=now.day,
            ).order_by('time')

        candles = {}

        if interval == Interval.HOURS.value:
            range_cap = 24
        else:
            range_cap = 60

        for i in range(0, range_cap):
            if interval == Interval.HOURS.value:
                interval_trades = trades.filter(time__hour=i).order_by('time')
            else:
                interval_trades = trades.filter(time__minute=i).order_by('time')

            start_recording = False

            if len(interval_trades) > 0:
                start_recording = True

                max_price = interval_trades.aggregate(Max('price'))['price__max']
                min_price = interval_trades.aggregate(Min('price'))['price__min']
                close_price = interval_trades.last().price
                open_price = interval_trades.first().price
                candle_start_date_time = interval_trades.aggregate(Min('time'))['time__min']
                candle_end_date_time = interval_trades.aggregate(Max('time'))['time__max']
                last_minute = candle_end_date_time.minute
                last_hour = candle_end_date_time.hour
                last_second = candle_end_date_time.second
                in_progress = False

                # Candle still in progress if hour or minute is not complete
                if (interval == Interval.HOURS.value and i >= last_hour and (last_minute != 59 or last_second != 59)) \
                        or i >= last_minute and last_second != 59:
                    in_progress = True

                color = 'Black (Doji Candle: opening price == closing price)'

                if close_price > open_price:
                    color = 'Green (closing price > opening price)'
                elif open_price > close_price:
                    color = 'Red (closing price < opening price)'

                candles[i] = {
                    "intervalHasTradesRecorded": True,
                    "isInProgress": in_progress,
                    "interval": interval,
                    "symbol": str(obj.stock_name),
                    "time": str(candle_start_date_time.strftime("%H:%M:%S")),
                    "open": open_price,
                    "close": close_price,
                    "high": max_price,
                    'low': min_price,
                    'color': color,
                }

            elif start_recording:
                candles[i] = {
                    "intervalHasTradesRecorded": False,
                    "isInProgress": "N/A",
                    "interval": interval,
                    "symbol": obj.stock_name,
                    "time": "N/A",
                    "open": "N/A",
                    "close": "N/A",
                    "high": "N/A",
                    'low': "N/A",
                    'color': "N/A",
                }

        return candles
