from django.urls import path
from .views import (
    homeview,
    cart,
    checkout,
    updateOrder,
    processOrder,
    typewise,
    activityPage
)
urlpatterns = [
    path('' , homeview , name = "homeview" ),
    path('cart/' , cart  , name = "cartview" ),
    path('checkout/' ,checkout , name = "checkoutview" ),
    path('updateitem/' , updateOrder , name = "updateorder"),
    path('processorder/' , processOrder , name = "processorder" ),
    path('products/<str:typeof>/', typewise , name = "typewise"),
    path('activity/' , activityPage , name = "activity")
]
