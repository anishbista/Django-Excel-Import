from django.db import models
from utils.common import CommonModel


class Product(CommonModel):
    sku = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()
    image_link = models.URLField()
    availability = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=50)
    brand = models.CharField(max_length=100)
    gtin = models.CharField(max_length=50)
    sale_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    item_group_id = models.CharField(max_length=100, blank=True, null=True)
    google_product_category = models.CharField(max_length=255, blank=True, null=True)
    product_type = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    material = models.CharField(max_length=100, blank=True, null=True)
    pattern = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.sku} - {self.title}"
