from django.http import JsonResponse
from django.shortcuts import render,redirect
import json
from app.forms import CustomUserForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .forms import SearchForm
from .models import product
def home(request):
    products = product.objects.filter(trending=1)
    return render(request,"shop/index.html",{"products":products})

def remove_cart(request,cid):
    cartitem = Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")
def remove_fav(request,fid):
    item = Favourite.objects.get(id=fid)
    item.delete()
    return redirect("/favviewpage")

def favviewpage(request):
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        return render(request,"shop/fav.html",{"fav":fav})
    else:
        return redirect("/")
    

def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"shop/cart.html",{"cart":cart})

        
    else:
        return redirect("/")


#def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            #print(request.user.id)
            product_status=product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Allready in Cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to Cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product stock not available '},status=200)

            
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)

            
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            product_qty = data['product_qty']
            product_id = data['pid']
            product_status = product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse({'status': 'Product already in cart'}, status=400)
                else:
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
                        return JsonResponse({'status': 'Product added to cart'}, status=200)
                    else:
                        return JsonResponse({'status': 'Product stock not available'}, status=400)
            else:
                return JsonResponse({'status': 'Product not found'}, status=404)
        else:
            return JsonResponse({'status': 'Login to add cart'}, status=401)
    else:
        return JsonResponse({'status': 'Invalid access'}, status=400)

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"logout successfully...")
    return redirect("/")



def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"logged successfully...")
                return redirect("/")
            else:
                messages.success(request,"invalid details")
                return redirect("/login")
        return render(request,"shop/login.html")

def register(request):
    form=CustomUserForm()
    if request.method== 'POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"registration success you can login now...")
            return redirect('/login')
    return render(request,"shop/register.html",{'form':form})

def collections(request):
    category=Category.objects.filter(status=0)
    return render(request,"shop/collections.html",{"category":category})
def collectionsview(request,name):
    if(Category.objects.filter(name=name,status=0)):
        #products=product.objects.filter(categorys_name=name)
        products = product.objects.filter(Category__name=name)

        return render(request,"shop/products/index.html",{"products":products,"category":name})
    else:
        messages.warning(request,"no such category")
        return redirect('collections')
    
def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
        if(product.objects.filter(name=pname,status=0)):
            products = product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/products/details.html",{"products":products})
        else:
            messages.warning(request,"no such found")
            return redirect('collections')
    
    else:
        messages.warning(request,"no such found")
        return redirect('collections')
def fav_page(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            
            product_id = data['pid']
            
            product_status = product.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user=request.user.id, product_id=product_id):
                    return JsonResponse({'status': 'Product already in favourite'}, status=200)
                else:
                    Favourite.objects.create(user=request.user, product_id=product_id)
                    return JsonResponse({'status': 'PRODUCT added to  favourite'}, status=200)
           
        else:
            return JsonResponse({'status': 'Login to add favourite'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid access'}, status=200)
    




#def search(request):
    query = request.GET.get('query', '')
    products = product.objects.all()

    if query:
        # Filter products based on the search query
        products = products.filter(name__icontains=query)

    form = SearchForm()

    return render(request, 'shop/search.html', {
        'form': form,
        'query': query,
        'products': products
    })
from django.shortcuts import render
from .models import product

def search(request):
    query = request.GET.get('q')
    

    
    data = product.objects.filter(name__icontains=query)

    return render(request, 'shop/search.html',{'data':data })
