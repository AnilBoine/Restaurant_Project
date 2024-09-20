from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomManager(models.Manager):
    def get_price_range(self,r1,r2):
        return self.filter(price__range=(r1,r2))
    
    def get_veg_list(self):
        return self.filter(category__exact="Veg")
    
    def get_nonveg_list(self):
        return self.filter(category__exact="Nonveg")
    
    def get_beverages_list(self):
        return self.filter(category__exact="Beverages")

class Product(models.Model):
    cat =(("Veg","Veg"),("Nonveg","Nonveg"),("Beverages","Beverages"))

    userid = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    product_id= models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField (max_length=50,choices=cat,default="")
    decs = models.TextField(max_length=255)
    price = models.IntegerField()
    image = models.ImageField(upload_to="product_img")
    objects = models.Manager()
    prod = CustomManager()


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=50)
    desc = models.TextField(max_length=255) 
    image = models.ImageField(upload_to="event_img")

    def __str__(self):
        return self.event_name

   
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

class Cart(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty =  models.PositiveIntegerField(default =0)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)


class Order(models.Model):
    order_id =  models.IntegerField(primary_key=True)
    user_id  = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)



class SliderImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='slider_images/')
    caption = models.CharField(max_length=200)

    def __str__(self):
        return self.title
