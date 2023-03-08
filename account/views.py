from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from account.forms import RegisterForm, OTPForm, LoginForm
from random import randint
from core.otp import send_opt
from django.contrib.auth import get_user_model, login, logout


User = get_user_model()


def register(request):
    name = "account/register.html"
    title = "ثبت نام"

    form = RegisterForm

    if request.method == "POST":
        form = form(request.POST)

        if form.is_valid():
            register_form_data = form.cleaned_data
            otp = randint(100000, 999999)
            request.session["register_form_data"] = register_form_data
            request.session["otp"] = otp
            otp_result = send_opt(register_form_data["phone"], otp)
            messages.success(request, "کد یکبار مصرف با موفقیت ارسال شد")

            return redirect("account:register_verify")
        else:
            messages.error(
                request, "خطا در ثبت نام. اطلاعات خود را بررسی و مجددا اقدام کنید."
            )

    data = {"title": title, "form": form}

    return render(request, name, data)


def register_verify(request):
    name = "account/verify.html"
    title = "تایید شماره موبایل"
    form = OTPForm

    if ("register_form_data" not in request.session) or ("otp" not in request.session):
        return redirect("account:register")

    phone = request.session["register_form_data"]["phone"]
    otp = request.session.get("otp")

    if request.method == "POST":
        form = form(request.POST)

        if form.is_valid():
            form_otp = form.cleaned_data["otp"]
            register_form_data = request.session.get("register_form_data")
            otp = request.session.get("otp")

            if form_otp == otp:
                user = User.objects.create(**register_form_data)
                login(request, user, "core.backends.PasswordlessAuthBackend")
                request.session.pop("register_form_data")
                request.session.pop("otp")
                messages.success(
                    request, "حساب کاربری شما با موفقیت ایجاد و وارد شدید."
                )
                return redirect("account:user_dashboard")
            else:
                messages.error(request, "کد وارد شده اشتباه است")
        else:
            messages.error(request, "کد وارد شده اشتباه است")

    data = {
        "title": title,
        "form": form,
        "phone": phone,
        "otp": otp,
    }

    return render(request, name, data)


def user_dashboard(request):
    name = "account/user_dashboard.html"
    title = "پنل کاربری"

    data = {"title": title}

    return render(request, name, data)


def login_(request):
    name = "account/login.html"
    title = "ورود"
    form = LoginForm

    if request.method == "POST":
        form = form(request.POST)

        if form.is_valid():
            phone = form.cleaned_data["phone"]
            otp = randint(100000, 999999)
            request.session["phone"] = phone
            request.session["otp"] = otp
            otp_result = send_opt(phone, otp)
            messages.success(request, "کد یکبار مصرف با موفقیت ارسال شد")
            return redirect("account:login_verify")
        else:
            messages.error(request, "شماره موبایل وارد شده اشتباه است.")

    data = {
        "title": title,
        "form": form,
    }
    return render(request, name, data)


def login_verify(request):
    name = "account/verify.html"
    title = "تایید شماره موبایل"
    form = OTPForm

    if ("phone" not in request.session) or ("otp" not in request.session):
        return redirect("account:login")

    phone = request.session.get("phone")
    otp = request.session.get("otp")

    if request.method == "POST":
        form = form(request.POST)

        if form.is_valid():
            form_otp = form.cleaned_data["otp"]
            phone = request.session.get("phone")
            otp = request.session.get("otp")

            if form_otp == otp:
                user = get_object_or_404(User, phone=phone)
                login(request, user, "core.backends.PasswordlessAuthBackend")
                request.session.pop("phone")
                request.session.pop("otp")
                messages.success(request, "شما با موفقیت وارد شدید.")
                return redirect("account:user_dashboard")
            else:
                messages.error(request, "کد وارد شده اشتباه است")
        else:
            messages.error(request, "کد وارد شده اشتباه است")

    context = {
        "title": title,
        "form": form,
        "phone": phone,
        "otp": otp,
    }
    return render(request, name, context)


def logout_(request):
    logout(request)
    return redirect('main:home')