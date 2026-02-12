from typing import Literal

from services.bybit_client import BybitClient


async def parse_orders(side: Literal["buy", "sell"]):
    client = BybitClient()

    if side == "buy":
        orders = await client.get_buy_orders()
    elif side == "sell":
        orders = await client.get_sell_orders()
    else:
        raise ValueError("Invalid side")

    return {
        "side": side,
        "count": len(orders),
        "orders": orders,
    }
