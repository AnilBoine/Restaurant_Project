
from django.shortcuts import redirect, render,get_object_or_404
from .models import Event,ContactMessage,Product,Cart,Order,SliderImage
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import random
import razorpay

# Create your views here.

def home(request):
    slider_images = SliderImage.objects.all()
    return render(request, 'index.html', {'slider_images': slider_images})

def contact(request):
    return render(request,"contact.html")

def events(request):
    return render(request,"events.html")

def about(request):
    return render(request,"about.html")


def gallery(request):
    return render(request,"gallery.html")


def registeration(request):
    return render(request,"register.html")

def reservations(request):
    
    return render(request, 'reservations.html')




def register(request):
    if request.method =="POST":
        uname = request.POST.get('uname')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        context ={}
        if uname =="" or pass1 =="" or pass2 =="":
            context['error'] = "Fields can't be empty"
            return render(request,"register.html",context)
        elif pass1 != pass2:
            context['error'] = "Password and Confirm password doesn't match!"
            return render(request,"register.html",context)
        else:
            try:
                user = User.objects.create(username = uname ,password=pass1)
                user.set_password(pass1)
                user.save()
                return redirect("signin")
            except Exception:
                context['error'] = "User already exists"
                return render(request,"register.html",context)
    else:
        return render(request,"register.html")

def signin(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        pass1 = request.POST.get('pass1')
        context ={}
        if uname =="" or pass1 =="":
            context['error'] = "Fields can't be empty"
            return render(request,"signin.html",context)
        else:
            user = authenticate(username =uname ,password =pass1)
            if user is not None:
                login(request,user)
                return redirect("index")
            else:
                context['error'] = "Invaild Username Or Password!"
                return render(request,"signin.html",context)
    else:
        return render(request,"signin.html")

def signout(request):
    logout(request)
    return redirect("index")

def event_list(request):
    events = Event.objects.all()
    for event in events:
        print(event.event_name)
    context = {'events': events}
    return render(request, 'events.html', context)

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
       
        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            return redirect('contact')  
        else:
            error_message = "All fields are required."
            return render(request, 'contact.html', {'error_message': error_message, 'name': name, 'email': email, 'message': message})
        
    return render(request, 'contact.html')


def order(request):
    allproduct = Product.objects.all()
    context={'allproduct':allproduct}
    return render (request,"order.html",context)


def veglistview(request):
    if request.method =="GET":
        allproduct = Product.prod.get_veg_list()
        context={'allproduct':allproduct}
        return render (request,"order.html",context)
    else:
        allproduct = Product.objects.all()
        context={'allproduct':allproduct}
        return render (request,"order.html",context)
    
def nonveglistview(request):
    if request.method =="GET":
        allproduct = Product.prod.get_nonveg_list()
        context={'allproduct':allproduct}
        return render (request,"order.html",context)
    else:
        allproduct = Product.objects.all()
        context={'allproduct':allproduct}
        return render (request,"order.html",context)
    
def beverageslistview(request):
    if request.method =="GET":
        allproduct = Product.prod.get_beverages_list()
        context={'allproduct':allproduct}
        return render (request,"order.html",context)
    else:
        allproduct = Product.objects.all()
        context={'allproduct':allproduct}
        return render (request,"order.html",context)
    
def rangeview(request):
    if request.method == "GET":
        return render (request,"order.html")
    else:
        min = request.POST.get('min')
        max = request.POST.get('max')
        if min=="":
            min = 0
        if max=="":
            max = 0  
        allproduct = Product.prod.get_price_range(min,max)
        context={'allproduct':allproduct}
        return render (request,"order.html",context)
        
def allsortedview(request):
    sort_option = request.GET.get('sort')

    if sort_option == "high_to_low":
        allproduct = Product.objects.order_by("-price")
    elif sort_option == "low_to_high":
        allproduct = Product.objects.order_by("price")
    else:
        allproduct = Product.objects.all()

    context={'allproduct':allproduct}
    return render (request,"order.html",context)


def cart(request):
    if request.user.is_authenticated:
        user = request.user
        allcarts = Cart.objects.filter(user_id = user.id)   
        total_price = 0 
        for x in allcarts:
            total_price += x.product_id.price * x.qty

        length = len(allcarts)

        context={
            "cart_items":allcarts,
            "total" :total_price,
            "items" :length,
            "username" :user.username 
        }
        
        return render(request,"cart.html",context)
    else:
        allcarts = Cart.objects.filter(user_id = request.user.id)   
        total_price = 0 
        for x in allcarts:
            total_price += x.product_id.price * x.qty

        length = len(allcarts)

        context={
            "cart_items":allcarts,
            "total" :total_price,
            "items" :length,
        }
        
        return render(request,"cart.html",context)  
        

def addToCart(request,product_id):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    allproduct = get_object_or_404(Product,product_id=product_id)
    cart_item,created = Cart.objects.get_or_create(product_id=allproduct,user_id=user)
    if not created:
        cart_item.qty += 1
    else:
        cart_item.qty = 1
    cart_item.save()
    return redirect("cart")

def updateqty(request,qv,product_id):
     
    allcarts = Cart.objects.filter(product_id = product_id)    
    if qv == "1": 
        total = allcarts[0].qty + 1
        allcarts.update(qty = total)
    else:
        if allcarts[0].qty > 1:
            total = allcarts[0].qty - 1
            allcarts.update(qty = total)
        else:
            allcarts = Cart.objects.filter(product_id = product_id)
            allcarts.delete()
    return redirect('cart')

def remove_from_cart(request,product_id):
    if request.user.is_authenticated:
        user =request.user
    else:
        user = None
    cart_item = Cart.objects.filter(product_id = product_id , user_id = user)
    cart_item.delete()
    return redirect("cart")
       

def remove_from_order(request,product_id):
    if request.user.is_authenticated:
        user =request.user
    else:
        user = None
    cart_item = Cart.objects.filter(product_id = product_id , user_id = user)
    cart_item.delete()
    return redirect("cart")

def placeorder(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user =None
    allcarts = Cart.objects.filter(user_id = user)
    total_price = 0 
    for x in allcarts:
        total_price += x.product_id.price * x.qty

    length = len(allcarts)
    context = {}
    context['cart_items'] = allcarts
    context['total'] = total_price
    context['items'] = length
    context['username'] = user

    return render(request,'placeorder.html',context)

def makepayment(request):
    if request.user.is_authenticated:
        user = request.user
        order_id = random.randrange(1000,9999)
        allcarts = Cart.objects.filter(user_id=user)

        for x in allcarts:
            Order.objects.create(order_id = order_id, product_id = x.product_id, user_id = x.user_id, qty = x.qty)
            x.delete()
            
        order = Order.objects.filter(user_id = user)
        total_price = 0
        for x in order:
            total_price += x.product_id.price*x.qty 
            oid = x.order_id

        client = razorpay.Client(auth=("rzp_test_6iW1wGnMXlF1jJ", "nHk7e4BnGri3UuSqEgeKS5M0"))
        data = { "amount": total_price*100, "currency": "INR", "receipt": str(oid) }
        payment = client.order.create(data=data)
        context={}
        context['data']=payment
        context['amount']=payment
        return render(request,"payment.html",context)
    else:
        user = None
        return redirect('signin')


def showorders(request):
    if request.user.is_authenticated:
        user = request.user
        allorders = Order.objects.filter(user_id=user)
        totalprice = 0

        for x in allorders:
            totalprice = totalprice + x.product_id.price * x.qty
            length = len(allorders)
        
        context = {
            "username" : user,
            "allorders" : allorders,
            'totalprice' : totalprice,
            'length' : length,
        }
        return render(request, "showorders.html", context)
