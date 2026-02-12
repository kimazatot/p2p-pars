import os
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional

import django
from pybit.unified_trading import HTTP
import requests
import schedule

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from parse.models import P2POrder

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BybitP2PParserPyBit:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

        try:
            self.session = HTTP(
                testnet=False,
                api_key=api_key,
                api_secret=api_secret,
            )
            logger.info("PyBit сессия успешно инициализирована")
        except Exception as e:
            logger.error(f"Ошибка инициализации pybit: {e}")
            self.session = None

        self.base_url = "https://api2.bybit.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
        }
        self.trade_types = {'BUY': '0', 'SELL': '1'}

    def get_p2p_listings(self,
                         crypto: str = "USDT",
                         fiat: str = "KGS",
                         trade_type: str = "BUY",
                         limit: int = 20,
                         page: int = 1,
                         amount: float = None,
                         payment_methods: List[str] = None) -> Dict:
        url = f"{self.base_url}/fiat/otc/item/online"
        payload = {
            "tokenId": crypto,
            "currencyId": fiat,
            "side": self.trade_types.get(trade_type.upper(), "0"),
            "size": str(limit),
            "page": str(page),
            "amount": str(amount) if amount else "",
            "authMaker": False,
            "canTrade": False,
            "payment": []
        }
        if payment_methods:
            payload["payment"] = self._get_payment_ids(payment_methods)

        try:
            logger.info(f"Запрос P2P: {crypto}/{fiat}, тип: {trade_type}, страница: {page}")
            response = requests.post(url, json=payload, headers=self.headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if data.get('result') and 'items' in data['result']:
                    return data
                else:
                    logger.warning(f"Неожиданная структура ответа: {data.keys()}")
            else:
                logger.error(f"Ошибка API: {response.status_code}")
        except Exception as e:
            logger.error(f"Ошибка при запросе P2P: {e}")

        return {"result": {"items": [], "total": 0}}

    def _get_payment_ids(self, payment_names: List[str]) -> List[str]:
        payment_map = {
            "Tinkoff": "75", "Sberbank": "64", "QIWI": "62", "YooMoney": "74",
            "Raiffeisen": "65", "RosBank": "185", "MBank": "310", "PayPal": "1",
            "Cash": "17", "BankTransfer": "13"
        }
        ids = []
        for name in payment_names:
            if name in payment_map:
                ids.append(payment_map[name])
            else:
                for key, pid in payment_map.items():
                    if name.lower() in key.lower():
                        ids.append(pid)
                        break
        return ids

    def _parse_order_item(self, item: Dict, crypto: str, fiat: str, trade_type: str) -> Optional[Dict]:
        try:
            parsed = {
                'user_id': item.get('userId', ''),
                'nickname': item.get('nickName', 'Неизвестно'),
                'price': float(item.get('price', 0)),
                'available': float(item.get('quantity', 0)),
                'min_amount': float(item.get('minAmount', 0)),
                'max_amount': float(item.get('maxAmount', 0)),
                'crypto': crypto,
                'fiat': fiat,
                'trade_type': trade_type,
                'payment_methods': self._extract_payment_methods(item.get('payments', [])),
                'completed_orders': item.get('recentOrderNum', 0),
                'completion_rate': item.get('recentExecuteRate', '0%'),
                'is_merchant': item.get('isMerchant', False),
                'is_online': item.get('online', False),
                'last_online': self._format_timestamp(item.get('lastOnlineTime')),
                'order_amount_crypto': float(item.get('quantity', 0)),
                'order_amount_fiat': float(item.get('quantity', 0)) * float(item.get('price', 0))
            }
            if 'makerDetail' in item:
                parsed['maker_level'] = item['makerDetail'].get('level', '')
                parsed['maker_total_orders'] = item['makerDetail'].get('orderNum', 0)
            return parsed
        except Exception as e:
            logger.warning(f"Ошибка парсинга ордера: {e}")
            return None

    def _extract_payment_methods(self, payments: list) -> str:
        methods = []
        for payment in payments:
            if isinstance(payment, dict):
                method = payment.get('paymentType', '')
            elif isinstance(payment, str):
                method = payment
            else:
                method = ''
            if method:
                methods.append(method)
        return ', '.join(methods) if methods else 'Не указано'

    def _format_timestamp(self, timestamp_ms: Optional[int]) -> str:
        if not timestamp_ms:
            return 'Неизвестно'
        try:
            dt = datetime.fromtimestamp(timestamp_ms / 1000)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return 'Ошибка формата'


def run_parsing():
    parser = BybitP2PParserPyBit(
        api_key=os.getenv("BYBIT_API_KEY"),
        api_secret=os.getenv("BYBIT_API_SECRET")
    )
    pairs = [("USDT", "KGS"), ("USDT", "RUB"), ("USDT", "KZT")]
    trade_types = ["BUY", "SELL"]

    for crypto, fiat in pairs:
        for trade in trade_types:
            logger.info(f"Парсинг {trade} для {crypto}/{fiat}")
            for page in range(1, 6):
                data = parser.get_p2p_listings(crypto, fiat, trade, limit=20, page=page)
                items = data.get('result', {}).get('items', [])
                if not items:
                    logger.info(f"Страница {page} пуста")
                    break

                for item in items:
                    parsed = parser._parse_order_item(item, crypto, fiat, trade)
                    if parsed:
                        P2POrder.objects.update_or_create(
                            order_id=parsed['user_id'],
                            defaults={
                                'user_id': parsed['user_id'],
                                'crypto': parsed['crypto'],
                                'fiat': parsed['fiat'],
                                'trade_type': parsed['trade_type'],
                                'min_amount': float(item.get('minAmount', 0)),
                                'max_amount': float(item.get('maxAmount', 0)),
                                'available': float(item.get('quantity', 0)),
                                'price': float(item.get('price', 0)),
                                'order_amount_crypto': parsed['order_amount_crypto'],
                                'order_amount_fiat': parsed['order_amount_fiat'],
                                'payment_methods': parsed['payment_methods'],
                                'nickname': parsed['nickname'],
                                'completed_orders': parsed['completed_orders'],
                                'completion_rate': parsed['completion_rate'],
                                'is_merchant': parsed['is_merchant'],
                                'is_online': parsed['is_online'],
                                'last_online': parsed['last_online'],
                            }
                        )

                time.sleep(0.3)

    logger.info("Парсинг завершён, данные сохранены в базе!")

    def parse_between(start_hour, end_hour):
        """Парсит каждые N секунд между start_hour и end_hour"""
        while True:
            now = datetime.now()
            if start_hour <= now.hour < end_hour:
                run_parsing()
                time.sleep(60)
            else:
                time.sleep(300)

    if __name__ == "__main__":
        import threading

        t1 = threading.Thread(target=parse_between, args=(5, 6))
        t2 = threading.Thread(target=parse_between, args=(11, 12))

        t1.start()
        t2.start()

        t1.join()
        t2.join()



def schedule_jobs():
    schedule.every().day.at("11:00").do(run_parsing)
    schedule.every().day.at("17:00").do(run_parsing)
    logger.info("Автопарсинг запланирован на 11:00 и 17:00")

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    run_parsing()
    schedule_jobs()
