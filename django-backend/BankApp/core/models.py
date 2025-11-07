from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class UserProfile(models.Model):
    """Rozšírenie pre existujúceho Django Usera"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )
    registration_date = models.DateTimeField(auto_now_add=True)
    last_login_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'user_profiles'
    
    def __str__(self):
        return f"Profile: {self.user.username}"

class Organization(models.Model):
    """Organizácia/predajca"""
    organization_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    ico = models.CharField(max_length=20, null=True, blank=True)
    dic = models.CharField(max_length=20, null=True, blank=True)
    ic_dph = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=50, default='Slovensko')
    municipality = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    street_name = models.CharField(max_length=255, null=True, blank=True)
    building_number = models.CharField(max_length=20, null=True, blank=True)
    
    class Meta:
        db_table = 'organizations'
    
    def __str__(self):
        return self.name

class StoreUnit(models.Model):
    """Konkrétna predajňa/pobočka"""
    unit_id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='stores')
    name = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=50, default='Slovensko')
    municipality = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    street_name = models.CharField(max_length=255, null=True, blank=True)
    building_number = models.CharField(max_length=20, null=True, blank=True)
    property_registration_number = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    class Meta:
        db_table = 'store_units'
    
    def __str__(self):
        return f"{self.name} - {self.street_name} {self.building_number}"

class Receipt(models.Model):
    """Pokladničný bločok"""
    receipt_id = models.AutoField(primary_key=True, null=False)
    fs_receipt_id = models.CharField(max_length=100, unique=True, default='TEMP_ID' )  # Pôvodné ID z CSV
    issue_date = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receipts')  # ZMENENÉ
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    store_unit = models.ForeignKey(StoreUnit, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Celkové sumy z účtenky
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_base_basic = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_base_reduced = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vat_amount_basic = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    vat_amount_reduced = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        db_table = 'receipts'
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"Receipt {self.fs_receipt_id} ({self.issue_date.date()})"

class Product(models.Model):
    """Produkt"""
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    original_name = models.CharField(max_length=255, null=True, blank=True)  # Pôvodný názov z CSV
    brand = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    ai_category = models.CharField(max_length=100, null=True, blank=True)  # Kategória od AI
    ai_name = models.CharField(max_length=255, null=True, blank=True)  # Názov od AI
    ai_name_english = models.CharField(max_length=255, null=True, blank=True)  # Anglický názov od AI
    
    class Meta:
        db_table = 'products'
    
    def __str__(self):
        return self.name

class ReceiptItem(models.Model):
    """Položka na účtenke"""
    receipt_item_id = models.AutoField(primary_key=True)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='receipt_items')
    quantity = models.DecimalField(max_digits=10, decimal_places=3)  # Podpora pre desatinné množstvo
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # AI analýza položky
    ai_name_without_brand = models.CharField(max_length=255, null=True, blank=True)
    ai_name_english = models.CharField(max_length=255, null=True, blank=True)
    ai_brand = models.CharField(max_length=100, null=True, blank=True)
    ai_category = models.CharField(max_length=100, null=True, blank=True)
    ai_quantity_value = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    ai_quantity_unit = models.CharField(max_length=20, null=True, blank=True)
    
    class Meta:
        db_table = 'receipt_items'
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

class ChatSession(models.Model):
    """Chat session"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chat_sessions")  # ZMENENÉ
    created_at = models.DateTimeField(auto_now_add=True)  # PRIDAŤ TOTO

    class Meta:
        db_table = 'chat_sessions'
    
    def __str__(self):
        return f"ChatSession {self.id} ({self.user})"

class ChatMessage(models.Model):
    """Chat message"""
    SENDER_CHOICES = [
        ('user', 'User'),
        ('bot', 'Bot'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chat_messages'
        ordering = ['created_at']
    
    def __str__(self):
        return f"[{self.sender}] {self.message[:50]}"