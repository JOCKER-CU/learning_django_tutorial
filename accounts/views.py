from django.shortcuts import render
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.shortcuts import redirect
from django.conf import settings
from .models import Account
from django.http import HttpResponse
#verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from django.core.mail import EmailMessage

from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from carts.views import _cart_id  
from carts.models import Cart, CartItem


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

            # messages.success(request, 'Thank you for registering with us. We have sent yo a verification email to you email address. Please verify it.')
            return redirect('/accounts/login/?command=verification&email='+email)
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
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart = cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart = cart)


                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass

            auth.login(request, user)
            messages.success(request, 'You are now login')
            return redirect('dashboard')
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
        messages.success(request, "Congratulation!, Your account has been activated. You can now log in.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect('register')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


@csrf_exempt
def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            try:
                user = Account.objects.get(email__exact=email)

                current_site = get_current_site(request)
                protocol = "https" if request.is_secure() else "http"
                mail_subject = "Password Reset"
                message = render_to_string('accounts/reset_password_email.html', {
                    'user': user,
                    'domain': current_site.domain,  # Ensure correct domain usage
                    'protocol': protocol,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),  # Ensure user.pk exists
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                # send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email = EmailMessage(
                subject=mail_subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=[to_email],
                )
                send_email.content_subtype = "html"  # To send HTML emails
                result = send_email.send()
                print("Email send result:", result)
                messages.success(request, "We've sent you a password reset link to your email address.")
                return redirect('login')

            except Exception as e:
                print("Error sending password reset email:", str(e))
                messages.error(request, "An error occurred while sending the password reset email.")
        else:
            messages.error(request, "Email does not exist.")
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def resetPassword_validate(request, uidb64, token):
        try:
             # Decode the user ID from base64
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            request.session['uid'] = uid
            messages.success(request, "Please reset your password")
            return redirect('resetPassword')
        else:
            messages.error(request, "This link is has been expired!")
            return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        # Handle POST request (form submission)
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            uid = request.session.get('uid')
            if uid is not None:
                try:
                    user = Account.objects.get(pk=uid)
                    user.set_password(password)
                    user.save()
                    messages.success(request, "Password has been reset successfully!")
                    return redirect('login')
                except Account.DoesNotExist:
                    messages.error(request, "User does not exist!")
                    return redirect('resetPassword')
            else:
                messages.error(request, "Session expired. Please try again.")
                return redirect('forgotPassword')
        else:
            messages.error(request, "Passwords do not match!")
            return redirect('resetPassword')
    else:
        # Handle GET request (display the password reset form)
        return render(request, 'accounts/resetPassword.html')