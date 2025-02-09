from django.shortcuts import render
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.shortcuts import redirect
from django.conf import settings
from .models import Account
#verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from django.core.mail import EmailMessage

from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
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

            #user activation
            # send_activation_email(user)
            current_site = get_current_site(request)
            protocol = "https" if request.is_secure() else "http"
            mail_subject = "Please activate your account"
            message = render_to_string('accounts/acccount_verification_email.html', {
                    'user': user,
                    'domain': current_site.domain,  # Ensure correct domain usage
                    'protocol': protocol,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),  # Ensure user.pk exists
                    'token': default_token_generator.make_token(user),
            })
            to_email = email
            # send_email = EmailMessage(mail_subject, message, to=[to_email])  # Fix email argument
            send_email = EmailMessage(
                subject=mail_subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[to_email],
                )
            send_email.content_subtype = "html"  # To send HTML emails
            result = send_email.send()
            print("Email send result:", result)

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

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now login')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now logout')
    return redirect('login')
     

def activate(request, uidb64, token):
    try:
        # Decode the user ID from base64
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    # Verify the token
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated. You can now log in.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect('register')