from .models import Stock
from datetime import datetime
import websockets
import json

from django.conf import settings

TIME_ZONE_OBJ = settings.TIME_ZONE_OBJ


async def client():
    async for websocket in websockets.connect('ws://b-mocks.dev.app.getbaraka.com:9989'):
        print("Connected to WebSocket server")
        try:
            async for message in websocket:
                ping = (json.loads(message))

                if ping['type'] == 'trade':
                    ping['data'] = ping['data'][0]
                    stamp = ping['data']['t']
                    time = datetime.fromtimestamp(stamp/1000, TIME_ZONE_OBJ)
                    time = time.replace(second=0)
                    stock, _ = Stock.objects.get_or_create(stock_name=str(ping['data']['s']))
                    stock.trade_set.create(time=time, price=float(ping['data']['p']), volume=int(ping['data']['v']))
                    print("TRADE RECORDED")

        except websockets.ConnectionClosed:
            print("Connection lost! Retrying..")
            continue  # retry WebSocket connection by exponential back off
        except Exception:
            print('Oops something went wrong - check your code')
            continue
