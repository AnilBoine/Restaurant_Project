from django.contrib import admin
from .models import *

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display =["product_id","product_name","category","decs","price","image"]

admin.site.register(Product,ProductAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display = ["event_id", "event_name", "desc", "image"]

admin.site.register(Event, EventAdmin)

class ContactMessageAdmin(admin.ModelAdmin):
    list_display =["name","email","message"]


admin.site.register(ContactMessage,ContactMessageAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=["product_id","qty","user_id"]

admin.site.register(Cart,CartAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display=["order_id","user_id","product_id","qty"]

admin.site.register(Order,OrderAdmin)

class SliderImageAdmin(admin.ModelAdmin):
    list_display=["title","image","caption"]

admin.site.register(SliderImage,SliderImageAdmin)
