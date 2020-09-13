from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200)
    parent = models.ForeignKey('self', blank=True, null=True, default=None, related_name='children', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "Categories"     

    def __str__(self):                      
        full_path = [self.name]                  
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])
    

class Product(models.Model):
    class Meta:
        ordering = ("name",)

    category = models.ManyToManyField(Category, blank=False)
    name = models.CharField(max_length=150)
    brand = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200)
    description = models.TextField(max_length=500, default="Empty description.")
    image = models.ImageField(upload_to="products/images", null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    quantity = models.IntegerField(default=10)  # available quantity of given product
    featured = models.BooleanField(default=False)  # is product featured?

    def __str__(self):
        return self.name

    @property
    def available(self):
        return self.quantity > 0
