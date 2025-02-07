from django.shortcuts import render
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.shortcuts import redirect


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            messages.success(request, 'Registration successful')
            return redirect('register')
        else:
            messages.error(request, 'Please fill out the form correctly')  # Only when form is invalid
    else:
        form = RegistrationForm()  # No message when page loads

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(request, email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now login')
            return redirect('home')
    return render(request, 'accounts/login.html')

def logout(request):
    return 
