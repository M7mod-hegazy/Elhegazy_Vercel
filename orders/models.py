from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from products.models import Child
from datetime import datetime
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=datetime.now)
    details = models.ManyToManyField(Child, through='OrderDetails')
    is_finished = models.BooleanField()
    total = 0
    items_count = 0

    def __str__(self):
        return 'User: ' + self.user.username + ', Order id: ' + str(self.id)


class OrderDetails(models.Model):
    product = models.ForeignKey(Child, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, default=1)
    code = models.CharField(max_length=200)
    quantity = models.IntegerField()

    def __str__(self):
        return 'User: ' + self.order.user.username + ', Product: ' + self.product.name + ', Order_id: ' + str(self.order.id)

    class Meta:
        ordering = ['-id']


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipment_address = models.CharField(max_length=250)
    shipment_phone = models.CharField(max_length=20)
 
