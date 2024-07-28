from http.client import HTTPResponse
from django.shortcuts import redirect, render

from shop.form import CustomUserForm
from . models import*
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,"shop/index.html",{"products":products})

def logout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logged out Successfully")
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
        messages.success(request,"Logged in Successfully")
        return redirect("/")
      else:
        messages.error(request,"Invalid User Name or Password")
        return redirect("/login_page")
    return render(request,"shop/login_page.html")


def register(request):
    form=CustomUserForm
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account created successfully")
            return redirect('/login')
    return render(request,"shop/register.html",{'form':form})

def collections(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,"shop/collections.html",{"catagory":catagory})

def collectionsview (request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products=Product.objects.filter(Catagory__name=name)
        return render(request,"shop/products/index.html",{"products":products,"catagory_name":name})
    else:
        messages.warning(request,"No such Catagory Found")
        return redirect('collections')
    
def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/products/product_details.html",{"products":products})
        else:
            messages.error(request,"No such Product Found")
            return redirect('collections')
    else:
        messages.error(request,"No such Catagory Found")
        return redirect('collections')

