from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from .models import Product , Order  ,OrderItem
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
# Create your views here.
@login_required()
def homeview(request):
    
    context = {
        "title" : "Home",
        "products" : Product.objects.all( )
    }
    return render( request , 'products/home.html' , context  )


def cart(request):
    
    if request.user.is_authenticated:
        customer = request.user 
        order , created = Order.objects.get_or_create( customer = customer )
        order_items = order.orderitem_set.all()
    else:
        order_items = []

    context = { 'items' : order_items , 'order' : order  }
    

    return render( request , 'products/cart.html' , context )

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user 
        order , created = Order.objects.get_or_create( customer = customer )
        order_items = order.orderitem_set.all()
    else:
        order_items = []
    context = { 'items' : order_items , 'order' : order  }
    return render(request , 'products/checkout.html' , context)

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


    return JsonResponse( 'Created' , safe=False )