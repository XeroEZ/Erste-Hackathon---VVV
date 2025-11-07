from django.contrib import admin
from .models import User, Shop, Receipt, Product

admin.site.register(User)
admin.site.register(Shop)
admin.site.register(Receipt)
admin.site.register(Product)
