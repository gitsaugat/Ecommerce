from django.urls import path
from .views import (
    homeview,
    cart,
    checkout,
    updateOrder,
    processOrder
)
urlpatterns = [
    path('' , homeview , name = "homeview" ),
    path('cart/' , cart  , name = "cartview" ),
    path('checkout/' ,checkout , name = "checkoutview" ),
    path('updateitem/' , updateOrder , name = "updateorder"),
    path('processorder/' , processOrder , name = "processorder" )
]
