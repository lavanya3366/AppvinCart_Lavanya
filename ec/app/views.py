import queue
from django.conf import settings
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
import razorpay
from . models import Cart, Customer, Product
from . forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.db.models import Q
# Create your views here.
def home(request):
    return render(request,"app/home.html")

def about(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,"app/about.html",locals())

def contact(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,"app/contact.html",locals())


class CategoryView(View):
    def get(self,request,val):
        product=Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())
class CategoryTitle(View):
    def get(self,request,val):
        product=Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())
class ProductDetail(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        return render(request,'app/productdetail.html',locals())

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',locals())
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/customerregistration.html',locals()) 

class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'app/profile.html',locals())
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data ['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            
            reg=Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'app/profile.html',locals())

def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',locals())
class updateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        return render(request,'app/updateAddress.html',locals()) 
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add= Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data ['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile Update successfully")
            
        else:
            messages.warning(request,"Invalid Input Data")
            
        return redirect("address")
# def add_to_cart(request):
#     user=request.user
#     product_id=request.GET.get('prod_id')
#     product=Product.objects.get(id=product_id)
#     Cart(user=user,product=product).save()
#     return redirect("/cart")

from django.http import HttpResponseBadRequest, JsonResponse

from django.http import HttpResponseBadRequest

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')

    # Check if product_id is provided
    if not product_id:
        return HttpResponseBadRequest("Product ID is missing")

    # Remove trailing slashes if any
    product_id = product_id.rstrip('/')

    try:
        product_id = int(product_id)  # Convert to integer
        product = Product.objects.get(id=product_id)
        
        # Check if the product already exists in the cart
        cart_item = Cart.objects.filter(user=user, product=product).first()
        if cart_item:
            # If the product exists, update the quantity
            cart_item.quantity += 1
            cart_item.save()
        else:
            # If the product doesn't exist, add it to the cart
            Cart(user=user, product=product).save()
        
        return redirect("/cart")
    except ValueError:
        return HttpResponseBadRequest("Invalid Product ID")
    except Product.DoesNotExist:
        return HttpResponseBadRequest("Product does not exist")


def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity*p.product.discounted_price
        amount=amount+value
    totalamount=amount+40
    return render(request,'app/addtocart.html',locals())

class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value=p.quantity * p.product.discounted_price
            famount =famount+value
        totalamount=famount+40
        razoramount=int(totalamount*100)
        client=razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        data={"amount":razoramount, "currency":"INR","receipt":"order_rcptid_12"}
        payment_response=client.order.create(data=data)
        print(payment_response)
        
        return render(request,'app/checkout.html',locals())
        
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        prod_id = int(prod_id)  # Convert to integer
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        prod_id = int(prod_id)  # Convert to integer
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        prod_id = int(prod_id)  # Convert to integer
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


  
# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404

# def plus_cart(request):
#     if request.method == 'GET':
#         prod_id = request.GET.get('prod_id')
#         cart_item = get_object_or_404(Cart, product_id=prod_id, user=request.user)
#         cart_item.quantity += 1
#         cart_item.save()

#         cart_items = Cart.objects.filter(user=request.user)
#         amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
#         total_amount = amount + 40

#         data = {
#             'quantity': cart_item.quantity,
#             'amount': amount,
#             'totalamount': total_amount
#         }
#         return JsonResponse(data)

from django.shortcuts import render
from .models import Product

def product_list(request):
    # Retrieve all products by default
    products = Product.objects.all()

    # Check if the user has submitted a sorting option
    sort_option = request.GET.get('sort')
    if sort_option:
        if sort_option == 'low_to_high':
            # Sort products by selling price in ascending order
            products = products.order_by('selling_price')
        elif sort_option == 'high_to_low':
            # Sort products by selling price in descending order
            products = products.order_by('-selling_price')

    # Pass the sorted products to the template
    context = {'products': products}
    return render(request, 'app/product_list.html', context)

from django.shortcuts import render, redirect
from .models import Product

from django.shortcuts import render
from .models import Product

def product_list(request):
    products = Product.objects.all()
    for product in products:
        product.avg_rating = product.average_rating()  # Add average rating to each product
    context = {'products': products}
    return render(request, 'ratings.html', context)

