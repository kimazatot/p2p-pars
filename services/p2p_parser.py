import time
import logging
from datetime import datetime
from typing import List, Dict, Optional
import requests

logger = logging.getLogger(__name__)

class BybitP2PParser:
    def __init__(self):
        self.base_url = "https://api2.bybit.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json",
        }
        self.trade_types = {"BUY": "0", "SELL": "1"}

    def get_p2p_listings(self, crypto, fiat, trade_type, limit, page):
        payload = {
            "tokenId": crypto,
            "currencyId": fiat,
            "side": self.trade_types[trade_type],
            "size": str(limit),
            "page": str(page),
            "payment": []
        }

        r = requests.post(
            f"{self.base_url}/fiat/otc/item/online",
            json=payload,
            headers=self.headers,
            timeout=15
        )

        if r.status_code != 200:
            return []

        return r.json().get("result", {}).get("items", [])

    def parse_item(self, item, crypto, fiat, trade_type) -> dict:
        return {
            "user_id": item.get("userId", ""),
            "nickname": item.get("nickName", ""),
            "price": item.get("price", 0),
            "available": item.get("quantity", 0),
            "min_amount": item.get("minAmount", 0),
            "max_amount": item.get("maxAmount", 0),
            "crypto": crypto,
            "fiat": fiat,
            "trade_type": trade_type,
            "payment_methods": ", ".join(
                p.get("paymentType", "") for p in item.get("payments", [])
            ),
            "completed_orders": item.get("recentOrderNum", 0),
            "completion_rate": item.get("recentExecuteRate", "0%"),
            "is_merchant": item.get("isMerchant", False),
            "is_online": item.get("online", False),
            "last_online": "",
            "order_amount_crypto": item.get("quantity", 0),
            "order_amount_fiat": float(item.get("quantity", 0)) * float(item.get("price", 0)),
        }

    def fetch_orders(self, crypto, fiat, trade_type, pages=5, limit=20):
        results = []

        for page in range(1, pages + 1):
            items = self.get_p2p_listings(crypto, fiat, trade_type, limit, page)
            if not items:
                break

            for item in items:
                results.append(self.parse_item(item, crypto, fiat, trade_type))

            time.sleep(0.3)

        return results
