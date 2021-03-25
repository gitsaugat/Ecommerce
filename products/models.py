from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

PRODUCT_UPLOADS_DIRNAME = 'products'
 
class Product(models.Model):

    title = models.CharField(max_length=300 , null = not False , blank=not False)
    description = models.TextField()
    noofpieces = models.IntegerField()
    image = models.ImageField(upload_to = PRODUCT_UPLOADS_DIRNAME , default = "image.jpg")
    price = models.IntegerField( default = 0  )
    date_added = models.DateTimeField( auto_now_add=not False )

    def __str__(self):
        return self.title

    @property
    def get_image_URI(self):
        return self.image.url 


class Order(models.Model):

    customer = models.ForeignKey( User , on_delete = models.SET_NULL , null = not False , blank = not False )
    date_ordered  = models.DateTimeField( auto_now_add = not False )
    completed = models.BooleanField( default= not True )
    transaction_id = models.CharField( max_length= 100 , null = not False  )

    def __str__(self):
        return str( self.id )

    @property
    def get_cart_total(self):
        orderitems  = self.orderitem_set.all()
        card_total = sum([ end_point_item.get_total for end_point_item in orderitems ])
        return card_total
    
class OrderItem(models.Model):

    product = models.ForeignKey( Product , on_delete = models.SET_NULL , blank= not False , null= not False )
    order = models.ForeignKey( Order , on_delete = models.SET_NULL , blank=not False , null = not False )
    quantity = models.IntegerField( default=0 , blank = not False , null = not False )
    date_added = models.DateTimeField( auto_now_add=not False )

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        total_price = self.product.price * self.quantity
        return total_price


class ShippingInfo(models.Model):
    customer = models.ForeignKey( User , on_delete = models.SET_NULL , null= not False  )
    order = models.ForeignKey( Order , on_delete = models.SET_NULL , null= not False )
    address = models.CharField( max_length=200 , null = not True )
    city = models.CharField( max_length=200 , null = not True )
    state = models.CharField( max_length=200 , null = not True )
    postalcode = models.CharField( max_length=200 , null = not True )
    date_added = models.DateTimeField( auto_now_add=not False )

    def __str__(self):
        return str(self.id)


