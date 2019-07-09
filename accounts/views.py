from django.shortcuts import render, redirect
from django.contrib import messages, auth
from contacts.models import Contact
from django.contrib.auth.models import User 

# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            #username
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username Already exists')
                return redirect('register')
            else:
                #email
                if User.objects.filter(email=email).exists():
                    messages.error(request,'Email Already registered')
                else:
                    user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)

                    #login
                    # Login after register
                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in')
                    # return redirect('index')

                    user.save()
                    messages.success(request,'you are registered')
                    return redirect('login')
        else:
            messages.error(request,'Password not matches')
    return render(request,'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are logged In!')
            return redirect('dashboard')
        
        else:
            messages.error(request,'Incorrect Username or Password!')
            return redirect('login')
    return render(request,'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'You are succesfully logged out')
        return redirect('index')

def dashboard(request):
    user_accounts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'account': user_accounts
    }
    return render(request,'accounts/dashboard.html',context)