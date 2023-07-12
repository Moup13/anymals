from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.http import require_POST

from .decorators import user_not_authenticated
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateMainForm, UserUpdateEmailForm, UserUpdateRequestForm, \
    UserUpdateMainProfileForm
from .tokens import account_activation_token


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('accounts:login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('/')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


@user_not_authenticated
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))

            messages.success(request,
                             'Пожалуйста подтвердите ваш аккаунт,ссылка на подтверждение отправлена на вашу почту.')
            return redirect("/")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request, "signup.html", {"form": form})


@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("home")


def test(request):
    return render(request, 'base.html')


@user_not_authenticated
def custom_login(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect("/")


        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue

                messages.error(request, error)

    form = UserLoginForm()

    return render(
        request=request,
        template_name="login.html",
        context={"form": form}
    )


def profile(request):
    try:

        customer = request.user
        form = UserUpdateMainForm(instance=customer)
        form1 = UserUpdateEmailForm(instance=customer)
        pass_form = PasswordChangeForm(user=request.user)
        request_form = UserUpdateRequestForm(instance=customer)

        if request.method == 'POST':
            form = UserUpdateMainForm(request.POST, request.FILES, instance=customer)
            form1 = UserUpdateEmailForm(request.POST, request.FILES, instance=customer)
            pass_form = PasswordChangeForm(user=request.user, data=request.POST)

            if form.is_valid():
                form.save()
            elif form1.is_valid():
                form1.save()
            elif pass_form.is_valid():
                pass_form.save()

                return redirect('accounts:login')
            else:
                return render(request, 'settings.html', customer)


    except Exception:

        return redirect('accounts:login')
    context = {'form': form, 'form1': form1, 'pass_form': pass_form, 'request_form': request_form}

    return render(request, 'settings.html', context)


def main_profile(request):
    customer = request.user
    request_form = UserUpdateRequestForm(instance=customer)
    main_form = UserUpdateMainProfileForm(instance=customer)
    if request.method == 'POST':
        main_form = UserUpdateMainProfileForm(request.POST, request.FILES, instance=customer)
        request_form = UserUpdateRequestForm(request.POST, request.FILES, instance=customer)
        if main_form.is_valid():
            main_form.save()
        elif request_form.is_valid():
            request_form.save()
    context = {'main_form': main_form, 'request_form': request_form}
    return render(request, 'profile.html', context)


def delete_user(request):
    user = request.user
    if request.user.is_authenticated:
        user.is_active = False
        user.save()
        messages.success(request, 'Profile successfully disabled.')
        return redirect('/')


@login_required(login_url='accounts:login')
#
# def profile(request):
#     customer = request.user
#     form = UserUpdateForm(instance=customer)
#
#     if request.method == 'POST':
#         form = UserUpdateForm(request.POST, request.FILES, instance=customer)
#         if form.is_valid():
#             form.save()
#
#         return render(request, 'settings.html', {'form': form})
#     elif request.method == 'GET':
#         filter = ChessSettingsFilter(request.POST, queryset=CustomUser.objects.all())
#         return render(request, 'settings.html', {'filter': filter})
#

def change_password(request):
    lis_form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        lis_form = PasswordChangeForm(user=request.user, data=request.POST)
        if lis_form.is_valid():
            lis_form.save()
            update_session_auth_hash(request, lis_form.user)
            return render(request, 'change_done.html',
                          {'pass_form': lis_form,
                           'pass_msg': 'Password Updated'})
    return render(request, 'change-password.html',
                  {'form': lis_form})


def AdvLogoutView(request):
    logout(request)
    return HttpResponseRedirect('http://127.0.0.1:8000/')


import json

from django.http import HttpRequest, JsonResponse

from .models import User


@require_POST
def pick_username(request: HttpRequest) -> JsonResponse:
    request_data = json.loads(request.body)

    username = request_data.get("username")

    existing_user = User.objects.filter(username=username).exists()
    if existing_user:
        return JsonResponse({"status": False, "message": "Username already taken!"}, status=400)

    new_user = User.objects.create(username=username)
    request.session["username"] = new_user.username

    return JsonResponse(
        {"status": True, "message": "Successful! You can now join/create conversations."},
        status=201,
    )


@user_not_authenticated
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))

            messages.success(request,
                             'Пожалуйста подтвердите ваш аккаунт,ссылка на подтверждение отправлена на вашу почту.')
            return redirect("/")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request, "signup.html", {"form": form})
