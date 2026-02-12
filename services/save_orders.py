from parse.models import P2POrder

def save_orders(orders: list[dict]):
    objs = [P2POrder(**o) for o in orders]
    P2POrder.objects.bulk_create(objs)
