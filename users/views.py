from django.shortcuts import render , redirect
from .forms import UserRegistrationForm
from django.contrib import messages

# Create your views here.

def register_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username").upper()
            messages.success(request, f'Account for {username} was successfully created' )
            return redirect('/')
        else:
            messages.warning(request , "Couldnt validate the form")
            return redirect('/register/user')
    
    form = UserRegistrationForm()
    context = {
        "title" : "Register User",
        "form" : form 
    }

    return render(request , 'users/register.html' , context)