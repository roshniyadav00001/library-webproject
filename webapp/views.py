from django.shortcuts import render, HttpResponse, redirect
from .import views
from django.http import JsonResponse
from .forms import Enquiryform, Supportform, cartform
from .models import *

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# import get_object_or_404()
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
import random



def home(request):
    categorydata= Categorymodel.objects.all()
    sliderdata= slider.objects.all()
    pred={}
    for x in categorydata:
        pred[x]= Mybook.objects.filter(category=x)[:4]
        
    context={'slider':sliderdata, 'category': categorydata,  'Mybook':pred}
   
    return render(request, 'webapp/home.html', context)



def search(request):
    q= request.POST.get('search')
    data= Mybook.objects.filter(name_icontains=q)
    context={'data': data}
    return render(request, 'webapp/search.html', context)


def cart(request):
    userid=request.user.id
    cartdata= cartModel.objects.filter(userid=userid)
    
    total=0
    for x in cartdata:
        mrp= str(x.pid.mrp)
        newmrp= float(mrp.replace(",", ""))
        total+= newmrp * x.qty
    
    if total>=1000:
        sc= 0
    else:
        sc= 50
    
    gst= 18
    
    netamount= total+ total*gst/100+ sc
    context={'cart': cartdata, 'total': total, 'net': netamount, 'sc': sc, 'gst':gst}
    return render(request, 'webapp/cart.html', context)



@login_required
def add_to_cart(request, id):
    userid= request.user
    # pid= request.POST.get('pid')
    productData= get_object_or_404(Mybook, id=id)
    
    cart,created = cartModel.objects.get_or_create(userid=userid, pid=productData)
    if not created:
        cart.qty+=1
        cart.save()
    
    return redirect('cart')  



def delete_cart(request, id):
    cart= cartModel.objects.get(id=id)
    cart.delete()
    return redirect('cart') 

def updatecart(request):
    newqty=request.POST.get('qtychange')
    cartid= request.POST.get('cartid')
    cartData= cartModel.objects.get(id=cartid)
    cartData.qty= newqty
    cartData.save()
    return redirect('cart') 

def about(request):
    return render(request, 'webapp/about.html')

def contact(request):
    if request.method=="POST":
        form =Enquiryform(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'webapp/contact.html', {'msg': "Thanks for contacting with Us !!!"})
        
    return render(request, 'webapp/contact.html')

def product(request):
    data= Mybook.objects.all()
    context={'data':data}
    return render(request, 'webapp/product.html', context)

def Support(request):
    if request.method=="POST":
        form =Supportform(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'webapp/support.html', {'msg': "Thanks for contacting with Us !!!"})
        
    return render(request, 'webapp/support.html')


def Category(request, id):
    data= Mybook.objects.filter(category=id)
    context={'data':data}
    return render(request, 'webapp/category-books.html', context)


def details(request,id):
    data= Mybook.objects.get(id=id)
    context={'x':data}
    return render(request, 'webapp/details.html', context)

def signup(request):
    msg={}
    
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        
        if password1==password2:
            user=User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            msg= {'msg': "User Account Created Successfully"}
        else:
            msg={'msg': "Password Must Be Same"} 
            
            
    return render(request, 'webapp/signup.html', msg) 


def userlogin(request):
    msg={}
    
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user= authenticate(username=username,  password=password) 
        
        if user is not None:
            login(request,user) 
            return redirect('my-account')
          
        else:
            msg={'msg': "Invalidusername or password"} 
            
            
    return render(request, 'webapp/login.html', msg)    

def myaccount(request):
    orderData=OrderItems.objects.filter(userid= request.user)
    
    if(request.method=="POST"):
        tid=request.POST.get('trackingid')
        tracking=OrderItems.objects.get(orderid=tid)
        trackingData= orderTracking.objects.filter(trackingid=tracking.id)
        context={'orders': orderData, 'trackingData': trackingData} 
        
    else:
        context={'orders':orderData}                 
    return render(request, 'webapp/my-account.html', context)

def userlogout(request):
    logout(request)
    return redirect('login')

def checkout(request):
    userid= request.user.id
    
    selectedItems= request.POST.get('pids').split(',')
    
    cartdata= cartModel.objects.filter(userid=userid, pid__in= selectedItems)
    
    total=0
    for x in cartdata:
        mrp= str(x.pid.mrp)
        newmrp= float(mrp.replace(",", ""))
        total+= newmrp * x.qty
    
    if total>=1000:
        sc= 0
    else:
        sc= 50
    gst= 18
    
    netamount= total+ total*gst/100+ sc
    countries = country.objects.all()
    context= {'cart': cartdata, 'total': total, 'net': netamount, 'sc': sc, 'gst': gst, 'countries': countries}
    return render(request, 'webapp/checkout.html', context)
          
def getStates(request):
    cid = request.GET.get('cid')
    states= state.objects.filter(cid=cid).values('id', 'name')
    return JsonResponse(list(states), safe=False)     

def getCity(request):
    sid = request.GET.get('sid')
    citydata= city.objects.filter(sid=sid).values('id', 'name')
    return JsonResponse(list(citydata), safe=False) 

def sendOrder(request):
    order= Order()
    
    if request.method== "POST":
        
        order.userid= request.user
        order.first_name= request.POST.get('fname')
        order.last_name= request.POST.get('lname')
        order.email= request.POST.get('email')
        order.contact= request.POST.get('contact')
        order.address= request.POST.get('addline1')+','+request.POST.get('addline2')
        order.country= request.POST.get('country')
        order.state= request.POST.get('state')
        order.city= request.POST.get('city')
        order.pincode= request.POST.get('pincode')
        order.message= request.POST.get('message')
        order.orderamt= request.POST.get('totalamt')
        
        trackingno= "LABORD"+str(random.randint(111111, 999999))
        order.trackingno= trackingno
        order.payment_mode= request.POST.get('paymode')
        order.save()
        
        cartitems= cartModel.objects.filter(userid=request.user)
        
        for x in cartitems:
            neworders= OrderItems()
            neworders.userid= request.user
            neworders.productid= x.pid
            productData= Mybook.objects.filter(title=x.pid).first()
            productData.stock= productData.stock-x.qty
            productData.save()
            
            neworders.order_qty=x.qty
            neworders.orderid=trackingno
            neworders.save()
            
        cartdata= cartModel.objects.filter(userid=request.user)       
        cartdata.delete()
        
        currentOrder= OrderItems.objects.filter(orderid=trackingno) 
        
        if order.payment_mode=="offline":
            return render(request, 'webapp/order-confirm.html', {'trn': trackingno, 'currentorders': currentOrder})
        else:
            return render(request, 'webapp/payment.html', {'amount': float(request.POST.get('totalamt'))*100})
        
        
def OrderHistory(request):
    pass


def complete_payment(request):
    if request.method =="POST":
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )   
        return render(request, "webpp/payment-success.html", {'amount': amount*100 })
    
    

    
 
             



