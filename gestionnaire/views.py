from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirmpwd = request.POST['comfirmpwd']
        if User.objects.filter(username=username):
            messages.error(request, 'username already taken please try another.')
            return redirect('signup')
        if User.objects.filter(email=email):
            messages.error(request, 'This email has an account.')
            return redirect('signup')
        if len(username)>10:
            messages.error(request, 'Please the username must not be more than 10 character.')
            return redirect('signup')
        if len(username)<5:
            messages.error(request, 'Please the username must be at leat 5 characters.')
            return redirect('signup')
        if not username.isalnum():
            messages.error(request, 'username must be alphanumeric')
            return redirect('signup')

        if password != confirmpwd:
            messages.error(request, 'The password did not match! ')  
            return redirect('signup')                  

        my_user = User.objects.create_user(username, email, password)
        my_user.first_name =firstname
        my_user.last_name = lastname
        my_user.is_active = False
        my_user.save()
        messages.success(request, 'Your account has been successfully created.')
    return render(request, 'gestionnaire/register.html')    


