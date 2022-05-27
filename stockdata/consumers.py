from channels.generic.websocket import WebsocketConsumer


# This consumer is/was for testing purposes
class StockDataConsumer(WebsocketConsumer):
    def connect(self):
        print("CONNECTED")
        self.accept()

    def disconnect(self, close_code):
        print("DISCONNECTED")
        pass

    def receive(self, text_data):
        print("RECEIVED")
        pass
