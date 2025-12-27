from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    parent = models.ForeignKey(
        'self', 
        blank=True, 
        null=True, 
        related_name='children', 
        on_delete=models.CASCADE,
        verbose_name="Üst Kategori"
    )
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60, unique=True,editable=True)
    icon_class = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name="İkon Sınıfı (FontAwesome)",
        help_text="İkon kodlarını <a href='https://fontawesome.com/search?o=r&m=free' target='_blank'>buradan</a> bulup kopyalayın. Örn: <b>fa-solid fa-laptop</b>"
    )
    
    class Meta:
        # Benzersizlik kuralı: Aynı üst kategoride aynı isimde iki kategori olamaz
        unique_together = ('slug', 'parent',) 
        verbose_name_plural = 'Kategoriler'

    def __str__(self):
        # Admin panelinde "Elektronik > Bilgisayar" şeklinde görünmesi için
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])
    
    def save(self, *args, **kwargs):
    # Eğer slug alanı boşsa, name'den üret
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Eğer slug doluysa dokunma (Admin panelinden gelen veriyi koru)
        super().save(*args, **kwargs)
    
class Vendor(models.Model):
    user=models.OneToOneField(User, related_name='vendor', on_delete=models.CASCADE)
    name= models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return self.name
    


class Product(models.Model):
    # ... (Kategori ve Vendor kısımları aynı kalacak) ...
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    # --- FİYATLANDIRMA DEĞİŞİKLİĞİ ---
    
    # Bu artık ürünün "İndirimsiz / Ham" fiyatı
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ham Fiyat (Etiket)")
    
    # İndirim oranı (Varsayılan 0, yani indirim yok)
    discount_rate = models.IntegerField(default=0, verbose_name="İndirim Oranı (%)")
    
    # Stok ve Durum
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = 'Ürünler'
    
    def __str__(self):
        return self.name

    # --- SİHİRLİ FONKSİYON (Satış Fiyatını Hesaplar) ---
    @property
    def sell_price(self):
        """
        Eğer indirim oranı varsa indirimli fiyatı döner,
        yoksa normal fiyatı döner.
        """
        if self.discount_rate > 0:
            # Matematik: Fiyat - (Fiyat * Yüzde / 100)
            discount_amount = (self.price * self.discount_rate) / 100
            return self.price - discount_amount
        return self.price
    
    def save(self, *args, **kwargs):
    # Eğer slug alanı boşsa, name'den üret
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Eğer slug doluysa dokunma (Admin panelinden gelen veriyi koru)
        super().save(*args, **kwargs)
