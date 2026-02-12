from django.http import JsonResponse
from .models import P2POrder

def serialize_order(order):
    return {
        "id": order.id,
        "crypto": order.crypto,
        "fiat": order.fiat,
        "price": str(order.price),
        "available": str(order.available),
        "min_amount": str(order.min_amount),
        "max_amount": str(order.max_amount),
        "nickname": order.nickname,
        "is_merchant": order.is_merchant,
        "parsed_at": order.parsed_at,
    }


def p2p_buy_list(request):
    queryset = P2POrder.objects.filter(trade_type="BUY").order_by("-parsed_at")
    data = [serialize_order(obj) for obj in queryset]
    return JsonResponse(data, safe=False)


def p2p_sell_list(request):
    queryset = P2POrder.objects.filter(trade_type="SELL").order_by("-parsed_at")
    data = [serialize_order(obj) for obj in queryset]
    return JsonResponse(data, safe=False)
