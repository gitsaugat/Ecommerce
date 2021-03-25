from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse
from .models import Product , Order  ,OrderItem , ShippingInfo
import json
import random
import time
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
# Create your views here.
def homeview(request):
    
    context = {
        "title" : "Home",
        "products" : Product.objects.all( )
    }
    return render( request , 'products/home.html' , context  )

@login_required
def cart(request):
    
    if request.user.is_authenticated:
        customer = request.user 
        order , created = Order.objects.get_or_create( customer = customer , completed=not True )
        order_items = order.orderitem_set.all()
    else:
        order_items = []

    context = { 'items' : order_items , 'order' : order  }
    

    return render( request , 'products/cart.html' , context )
@login_required
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user 
        order , created = Order.objects.get_or_create( customer = customer , completed=not True )
        order_items = order.orderitem_set.all()
    else:
        order_items = []
    context = { 'items' : order_items , 'order' : order  }
    return render(request , 'products/checkout.html' , context)

@login_required
def updateOrder(request):
    data = json.loads( request.body )
    productid , action = [ data['productId'] , data['action'] ]
    product = Product.objects.get( id = productid )
    order , created = Order.objects.get_or_create( customer = request.user , completed=not True )
    orderItem , created = OrderItem.objects.get_or_create( order = order , product = product )

    if action == 'add':
        orderItem.quantity = orderItem.quantity+1
        messages.success(request, f'Added' )

    elif action == "remove":
        orderItem.quantity = orderItem.quantity-1  
        messages.warning(request, f'removed' )
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    orderItem.save()


    return JsonResponse( 'Created' , safe=not True )
@login_required
def processOrder(request):
    time.sleep(1)
    requested_data = json.loads( request.body )
    order , created = Order.objects.get_or_create( customer= request.user , completed = not True )
    print(requested_data['dataonHold']['total'])
    if int(requested_data['dataonHold']['total']) == order.get_cart_total:
        order.completed = not False
        order.transaction_id = random.random()
        order.save()

    if requested_data:
        ShippingInfo.objects.create(
            customer = request.user,
            order= order ,
            address = requested_data['dataonHold']['address'],
            city = requested_data['dataonHold']['city'],
            state = requested_data['dataonHold']['state'],
            postalcode=requested_data['dataonHold']['zip'],
        )
    else:
        print("cannot do anything")

    return JsonResponse( "lol", safe = False )



     

     

    