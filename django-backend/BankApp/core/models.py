from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)  # store hashed passwords

    def __str__(self):
        return self.username


class Shop(models.Model):
    shop_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Receipt(models.Model):
    blocek_id = models.AutoField(primary_key=True)
    date = models.DateField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='receipts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receipts')

    def __str__(self):
        return f"Receipt {self.blocek_id} ({self.date})"


class Product(models.Model):
    product_id = models.CharField(max_length=20, primary_key=True)
    quantity = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.IntegerField()
    name = models.CharField(max_length=50)
    weight = models.FloatField(null=True, blank=True)
    blocek = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f"{self.name} ({self.product_id})"
