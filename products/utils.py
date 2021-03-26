from .models import Activity
from django.contrib import messages

def createActivity( user , message ):
    Activity.objects.create( user = user , message = message )





