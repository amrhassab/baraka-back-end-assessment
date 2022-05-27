import asyncio
from django.core.management.base import BaseCommand
from stockdata.wsclient import client


class Command(BaseCommand):

    def handle(self, *args, **options):
        print(f"Connecting to WebSocket server")
        asyncio.run(client())
