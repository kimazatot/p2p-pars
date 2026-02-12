from django.db import models

class P2POrder(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    user_id = models.CharField(max_length=64)
    nickname = models.CharField(max_length=255)

    crypto = models.CharField(max_length=10)
    fiat = models.CharField(max_length=10)
    trade_type = models.CharField(max_length=4)

    price = models.DecimalField(max_digits=18, decimal_places=8)
    available = models.DecimalField(max_digits=18, decimal_places=8, null=True, blank=True)

    min_amount = models.DecimalField(max_digits=18, decimal_places=8, null=True, blank=True)
    max_amount = models.DecimalField(max_digits=18, decimal_places=8, null=True, blank=True)

    payment_methods = models.TextField()

    completed_orders = models.IntegerField(null=True, blank=True)
    completion_rate = models.CharField(max_length=10, null=True, blank=True)

    is_merchant = models.BooleanField()
    is_online = models.BooleanField(null=True, blank=True)
    last_online = models.CharField(max_length=32, null=True, blank=True)

    order_amount_crypto = models.DecimalField(max_digits=18, decimal_places=8, null=True, blank=True)
    order_amount_fiat = models.DecimalField(max_digits=18, decimal_places=8, null=True, blank=True)

    parsed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["crypto", "fiat", "trade_type"]),
        ]

class P2POrderBuy(P2POrder):
    class Meta:
        proxy = True
        verbose_name = "P2POrder BUY"
        verbose_name_plural = "P2POrder BUY"

class P2POrderSell(P2POrder):
    class Meta:
        proxy = True
        verbose_name = "P2POrder SELL"
        verbose_name_plural = "P2POrder SELL"