import asyncio
from .models import P2POrder

async def parse_p2p():
    data = [
        {
            "order_id": "123",
            "price": 100,
            "amount": 2,
            "side": "buy",
        }
    ]

    for item in data:
        P2POrder.objects.update_or_create(
            order_id=item["order_id"],
            defaults=item
        )
