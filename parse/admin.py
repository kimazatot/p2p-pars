from django.contrib import admin
from .models import P2POrder, P2POrderBuy, P2POrderSell


@admin.register(P2POrder)
class P2POrderAdmin(admin.ModelAdmin):
    list_display = (
        "crypto",
        "fiat",
        "trade_type",
        "price",
        "available",      # ← было available_amount
        "min_amount",     # ← было min_limit
        "max_amount",     # ← было max_limit
        "nickname",
        "is_merchant",
        "parsed_at",
    )

    list_filter = ("crypto", "fiat", "trade_type", "is_merchant")
    search_fields = ("nickname", "user_id")
    ordering = ("-parsed_at",)


@admin.register(P2POrderBuy)
class P2POrderBuyAdmin(P2POrderAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(trade_type="BUY")


@admin.register(P2POrderSell)
class P2POrderSellAdmin(P2POrderAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(trade_type="SELL")
