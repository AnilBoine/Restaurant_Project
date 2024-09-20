"""
URL configuration for restaurant_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from restaurant_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='index'),
    path('contact/', views.contact, name='contact'),


    path('order/', views.order, name='order'),
   
    path('gallery/', views.gallery, name='gallery'),
    path('about/', views.about, name='about'),
    path('register/',views.register,name="register"),
    path('signin/',views.signin,name="signin"),
    path('signout/',views.signout,name="signout"),
    path('contact_view/', views.contact_view, name='contact_view'),

    path('event_list/', views.event_list, name='event_list'),
    path('veglistview/',views.veglistview,name="veglistview"),
    path('nonveglistview/',views.nonveglistview,name="nonveglistview"),
    path('beverageslistview/',views.beverageslistview,name="beverageslistview"),
    path('rangeview/',views.rangeview,name="rangeview"),
    path('allsortedview/',views.allsortedview,name="allsortedview"),
    
    path('cart/',views.cart,name="cart"),
    path('addtocart/<int:product_id>',views.addToCart,name="addToCart"),
    path("updateqty/<qv>/<product_id>",views.updateqty,name="updateqty"),
    path("remove_from_cart/<int:product_id>",views.remove_from_cart,name="remove_from_cart"),
    path("remove_from_order/<int:product_id>",views.remove_from_order,name="remove_from_order"),

    path('placeorder/',views.placeorder,name="placeorder"),
    path('makepayment/',views.makepayment,name="makepayment"),
    path('showorders/',views.showorders,name="showorders"),
     

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
