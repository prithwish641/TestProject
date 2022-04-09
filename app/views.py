from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced, Buy
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator





class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        return render(request, 'app/home.html', {'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'laptops':laptops})

def home(request):
 return render(request, 'app/home.html')

def search_options(request):
    if request.method=='GET':
        search_query = ''
        if request.GET.get('developer'):
            search_query = request.GET.get('developer')
        searched_products = Product.objects.filter(Q(title__icontains=search_query) | Q(brand__icontains=search_query))
    return render(request, 'app/search_products.html', {'searched_products':searched_products})

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart})

class CardDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/carddetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required   
def add_to_buy(request):
    user = request.user
    product_id = request.GET.get('prodc_id')
    product = Product.objects.get(id=product_id)
    Buy(user=user, product=product).save()
    return redirect('/buy-now')


    
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount= 90.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discount_price)
                amount += tempamount 
                totalamount = shipping_amount+amount
            return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount})
        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount=0.0
        shipping_amount=90.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount 
            totalamount = shipping_amount+amount
            
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
            }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount=0.0
        shipping_amount=90.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount 
            
            
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':shipping_amount+amount
            }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=90.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount 
            
            
        data = {
            'amount':amount,
            'totalamount':shipping_amount+amount
            }
        return JsonResponse(data)

@login_required
def buy_now(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    buy_items = Buy.objects.filter(user=user)
    item_length = len(buy_items)
    item_lst = item_length-1
    item_last = buy_items[item_lst]
    #print(buy_items)
    amount = 0.0
    shipping_amount=90.0
    buy_product = [p for p in Buy.objects.all() if p.user==request.user]
    #print(buy_product)
    if buy_product:
        for p in buy_product:
            tempamount = p.product.discount_price
            amount += tempamount
        totalamount=amount+shipping_amount
    price_amnt = item_last.product.discount_price+shipping_amount
    return render(request, 'app/buynow.html', {'add':add, 'price_amnt':price_amnt, 'item_last':item_last})

@login_required
def profile(request):
 return render(request, 'app/profile.html')

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed':op})

#def change_password(request):
 #return render(request, 'app/changepassword.html')

def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung' or data == 'Realmi' or data == 'Moto':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    return render(request, 'app/mobile.html', {'mobiles':mobiles} )
    
def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'Lenevo' or data == 'HP' or data == 'Dell' or data == 'Apple':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    return render(request, 'app/laptop.html', {'laptops':laptops})

def topwear(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'Male' or data == 'Female':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    return render(request, 'app/topwear.html', {'topwears':topwears})

def topwear(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'Male' or data == 'Female':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    return render(request, 'app/topwear.html', {'topwears':topwears})

def wedding(request, data=None):
    if data == None:
        wedding_products = Product.objects.filter(category='WC')
    #elif data == 'Male' or data == 'Female':
        #topwears = Product.objects.filter(category='WC').filter(brand=data)
    return render(request, 'app/wedding.html', {'wedding_products':wedding_products})

def birthday(request, data=None):
    if data == None:
        birthday_products = Product.objects.filter(category='BC')
    #elif data == 'Male' or data == 'Female':
        #topwears = Product.objects.filter(category='WC').filter(brand=data)
    return render(request, 'app/birthday.html', {'birthday_products':birthday_products})
    

def congratulation(request, data=None):
    if data == None:
        congratulation_products = Product.objects.filter(category='CC')
    #elif data == 'Male' or data == 'Female':
        #topwears = Product.objects.filter(category='WC').filter(brand=data)
    return render(request, 'app/congratulation.html', {'congratulation_products':congratulation_products})


def anniversary(request, data=None):
    if data == None:
        anniversary_products = Product.objects.filter(category='AN')
    #elif data == 'Male' or data == 'Female':
        #topwears = Product.objects.filter(category='WC').filter(brand=data)
    return render(request, 'app/anniversary.html', {'anniversary_products':anniversary_products})

def customer_care(request):
    if request.method == 'GET':
        problem = request.GET['inputProblem']
        print(problem)
    return render(request, 'app/chatbot.html')
    
    
    
class CustomerRegistrationView(View):
    def get(get, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
        
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congatulations!! Successfully registered')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})
 
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount=90.0
    cart_product = [p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discount_price)
            amount += tempamount
        totalamount=amount+shipping_amount
    return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items})

    
@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(get, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']
            reg = Customer(user=usr, name=name, locality=locality, city=city, zipcode=zipcode, state=state)
            reg.save()
            messages.success(request, 'Congatulations!! Successfully updated')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
