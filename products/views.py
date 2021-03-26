from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse
from .models import Product , Order  ,OrderItem , ShippingInfo , Activity
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .utils import createActivity
import json
import random
import time

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
        createActivity( request.user , f' Howdy , you made an order successfully which is worth of ${ str(order.get_cart_total) } ' )
    else:
        print("cannot do anything")

    return JsonResponse( "lol", safe = False )


def typewise(request , typeof):
    anothertype = ""
    if typeof == "shirt":
        anothertype = "SH"
    elif typeof == "shoes":
        anothertype = "SO"
    elif typeof == "jackets":
        anothertype = "JK"
    elif typeof == "bags":
        anothertype = "BG"
    elif typeof == "piants":
        anothertype = "PT"
    else:
        anothertype = None


    context = {
        'products' : Product.objects.filter( category = anothertype )
    }
    if context['products']:
        print(context)
    else:
        print("not found")
    return render( request , 'products/products.html' , context   )


def activityPage(request):
    context = {
        'activities' : Activity.objects.filter( user = request.user )
    }

    return render( request , 'products/activity.html' , context )