from django.db import models
from django.utils import timezone
from decimal import Decimal

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)

class Warehouse(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=12, decimal_places=0,default=Decimal('0'))
    description = models.TextField()
    image = models.CharField(max_length=200)
    
    warehouses = models.ManyToManyField(Warehouse, related_name='products', through='Stock')

class Stock(models.Model):
    quantity = models.IntegerField(default=0)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class FlashSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    flash_price = models.DecimalField(max_digits=12, decimal_places=0)
    campaign_stock = models.IntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time

class StockReservation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('EXPIRED', 'Expired'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Cho phép null để phục vụ bán hàng bình thường
    flash_sale = models.ForeignKey(FlashSale, on_delete=models.SET_NULL, null=True, blank=True)
    
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    reserved_price = models.DecimalField(max_digits=12, decimal_places=0) # Chốt giá lúc giữ chỗ
    
    expire_time = models.DateTimeField()
    created_time = models.DateTimeField(auto_now_add=True)

class Order(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation = models.ForeignKey(StockReservation, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=12, decimal_places=0)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)