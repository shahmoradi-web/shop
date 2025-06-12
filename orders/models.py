from django.db import models

# Create your models here.

from django.db import models

from shop.models import Product


# Create your models here.

class Orders(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)
    province = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
    def __str__(self):
        return f"order #{self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all() )

    def get_post_cost(self):
        weight = sum(item.get_weight() for item in self.items.all() )
        if weight < 1000:
            return 0
        elif 1000 <= weight <= 2000:
            return 30000
        else:
            return 50000

    def get_final_cost(self):
        return self.get_total_cost() + self.get_post_cost()

class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    weight = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.quantity * self.price

    def get_weight(self):
        return self.weight * self.quantity

