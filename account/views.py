from random import randint

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from account.forms import (EntezaaraatFrom, KhosousiaatFrom, LoginForm,
                           OTPForm, PhoneChangeForm, ProfileChangeForm,
                           RegisterForm)
from account.models import Entezaaraat, Khosousiaat
from chat.models import Relation
from core.otp import send_opt

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
            messages.success(request, "کد تایید به شماره موبایل شما ارسال شد")

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
            messages.success(request, "کد تایید به شماره موبایل شما ارسال شد")
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
    messages.info(request, "شما از حساب کاربری خود خارج شدید.")
    return redirect("main:home")


def profile(request):
    name = "account/profile.html"
    title = "حساب کاربری"

    context = {
        "title": title,
        "khosousiaat": request.user.khosousiaat,
        "entezaaraat": request.user.entezaaraat,
    }
    return render(request, name, context)


def profile_change(request):
    name = "account/profile_change.html"
    title = "ویرایش حساب کاربری"

    if request.method == "POST":
        form = ProfileChangeForm(instance=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "حساب کاربری شما با موفقیت ویرایش شد")
            return redirect("account:user_dashboard")

        else:
            messages.error(request, "لطفا اطلاعات خود را بررسی و دوباره تلاش کنید.")
    else:
        form = ProfileChangeForm(instance=request.user)

    context = {"title": title, "form": form}
    return render(request, name, context)


def phone_change(request):
    name = "account/phone_change.html"
    title = "ویرایش شماره موبایل"

    if request.method == "POST":
        form = PhoneChangeForm(data=request.POST, instance=request.user)

        if form.is_valid():
            phone = form.cleaned_data["phone"]
            otp = randint(100000, 999999)
            request.session["phone"] = phone
            request.session["otp"] = otp
            otp_result = send_opt(phone, otp)
            messages.success(request, "کد تایید به شماره موبایل شما ارسال شد")
            return redirect("account:phone_change_verify")
        else:
            messages.error(request, "شماره موبایل وارد شده اشتباه است")

    else:
        form = PhoneChangeForm(instance=request.user)

    context = {"title": title, "form": form}
    return render(request, name, context)


def phone_change_verify(request):
    name = "account/verify.html"
    title = "تایید شماره موبایل"

    if ("phone" not in request.session) or ("otp" not in request.session):
        return redirect("account:login")

    phone = request.session.get("phone")
    otp = request.session.get("otp")

    if request.method == "POST":
        form = OTPForm(request.POST)

        if form.is_valid():
            form_otp = form.cleaned_data["otp"]

            if form_otp == otp:
                user = request.user
                user.phone = phone
                user.save()
                request.session.pop("phone")
                request.session.pop("otp")
                messages.success(request, "شماره موبایل شما با موفقیت ویراش شد")
                return redirect("account:user_dashboard")
            else:
                messages.error(request, "کد وارد شده اشتباه است. دوباره تلاش کنید.")

        else:
            messages.error(request, "کد وارد شده اشتباه است. دوباره تلاش کنید.")
    else:
        form = OTPForm()

    context = {
        "title": title,
        "form": form,
        "phone": phone,
        "otp": otp,
    }
    return render(request, name, context)


def khosousiaat_change(request):
    name = "account/khosousiaat_change.html"
    title = "ویرایش خصوصیات"

    khosousiaat = request.user.khosousiaat

    if request.method == "POST":
        form = KhosousiaatFrom(instance=khosousiaat, data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "خصوصیات شما با موفقیت ویرایش شد")
            return redirect("account:user_dashboard")

        else:
            messages.error(request, "لطفا اطلاعات خود را بررسی و دوباره تلاش کنید.")
    else:
        form = KhosousiaatFrom(instance=khosousiaat)

    context = {"title": title, "form": form}
    return render(request, name, context)


def entezaaraat_change(request):
    name = "account/entezaaraat_change.html"
    title = "ویرایش انتظارات"

    entezaaraat = request.user.entezaaraat

    if request.method == "POST":
        form = EntezaaraatFrom(instance=entezaaraat, data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "انتظارات شما با موفقیت ویرایش شد")
            return redirect("account:user_dashboard")

        else:
            messages.error(request, "لطفا اطلاعات خود را بررسی و دوباره تلاش کنید.")
    else:
        form = EntezaaraatFrom(instance=entezaaraat)

    context = {"title": title, "form": form}
    return render(request, name, context)


def partner_search(request):
    name = "account/partner_search.html"
    title = "جستجوی همسان"
    user = request.user
    entezaaraat = Entezaaraat.objects.get(user=user)

    if user.gender == "1":
        users = User.objects.exclude(pk=request.user.pk).filter(gender="2")
    else:
        users = User.objects.exclude(pk=request.user.pk).filter(gender="1")

    partners = Khosousiaat.objects.filter(user__in=users)

    # partners = partners.filter(tavallod__in=entezaaraat.tavallod_range())
    # partners = partners.filter(qad__in=entezaaraat.qad_range())
    # partners = partners.filter(vazn__in=entezaaraat.vazn_range())

    # if entezaaraat.zibaayi != '0' and entezaaraat.zibaayi != None:
    #     partners = partners.filter(zibaayi=entezaaraat.zibaayi)

    # if entezaaraat.ostaane_tavallod != '0' and entezaaraat.ostaane_tavallod != None:
    #     partners = partners.filter(ostaane_tavallod=entezaaraat.ostaane_tavallod)

    # if entezaaraat.ostaane_sokounat != '0' and entezaaraat.ostaane_sokounat != None:
    #     partners = partners.filter(ostaane_sokounat=entezaaraat.ostaane_sokounat)

    # if entezaaraat.shahre_sokounat != '0' and entezaaraat.shahre_sokounat != None:
    #     partners = partners.filter(shahre_sokounat=entezaaraat.shahre_sokounat)

    # if entezaaraat.ehsaasaat != '0' and entezaaraat.ehsaasaat != None:
    #     partners = partners.filter(ehsaasaat=entezaaraat.ehsaasaat)

    # if entezaaraat.ertebaataat != '0' and entezaaraat.ertebaataat != None:
    #     partners = partners.filter(ertebaataat=entezaaraat.ertebaataat)

    # if entezaaraat.jensi != '0' and entezaaraat.jensi != None:
    #     partners = partners.filter(jensi=entezaaraat.jensi)

    # if entezaaraat.salaamat != '0' and entezaaraat.salaamat != None:
    #     partners = partners.filter(salaamat=entezaaraat.salaamat)

    if entezaaraat.tahsil != "0" and entezaaraat.tahsil != None:
        partners = partners.filter(tahsil=entezaaraat.tahsil)

    if entezaaraat.qowmiat != "0" and entezaaraat.qowmiat != None:
        partners = partners.filter(qowmiat=entezaaraat.qowmiat)

    if entezaaraat.shoql != "0" and entezaaraat.shoql != None:
        partners = partners.filter(shoql=entezaaraat.shoql)

    if entezaaraat.din != "0" and entezaaraat.din != None:
        partners = partners.filter(din=entezaaraat.din)

    context = {"title": title, "partners": partners}

    return render(request, name, context)



def get_relation_state(user1, user2):
    """
    0 -> no relation
    
    11 -> user1 has sent request to user2 and status = SENT
    12 -> user1 has sent reqeust to user2 and status = ACCEPTED
    13 -> user1 has sent request to user2 and status = REJECTED
    
    21 -> user2 has sent request to user1 and status = SENT
    22 -> user2 has sent request to user1 and status = ACCEPTED
    23 -> user2 has sent request to user1 and status = REJECTED
    """
    relation = Relation.objects.filter(
        Q(sender=user1, reciver=user2) | Q(sender=user2, reciver=user1)
    ).first()

    if not relation:
        return 0

    if relation.sender == user1:
        if relation.status == '1':
            return 11
        if relation.status == '2':
            return 12
        if relation.status == '3':
            return 13

    elif relation.sender == user2:
        if relation.status == '1':
            return 21
        if relation.status == '2':
            return 22
        if relation.status == '3':
            return 23


def user_detail(request, pk):
    name = "account/user_detail.html"
    title = "مشخصات کاربر"

    user1 = request.user
    user2 = get_object_or_404(User, pk=pk)

    relation_state = get_relation_state(user1, user2)

    # if user1 == user2: return redirect('account:profile')

    khosousiaat = user2.khosousiaat
    entezaaraat = user2.entezaaraat

    context = {
        "title": title,
        "user2": user2,
        "khosousiaat": khosousiaat,
        "entezaaraat": entezaaraat,
        "state": relation_state
    }

    return render(request, name, context)


def relation_request(request, sender, reciver, action):
    
    sender = get_object_or_404(User, pk=sender)
    reciver = get_object_or_404(User, pk=reciver)
    user2_id = request.GET.get('user2_id')
    
    if action == 'create':
        new_relation = Relation(sender=sender, reciver=reciver, status=1)
        new_relation.save()

    elif action == 'delete':
        relation = Relation.objects.filter(sender=sender, reciver=reciver).first()
        relation.delete()

    elif action == 'accept':
        relation = Relation.objects.filter(sender=sender, reciver=reciver).first()
        relation.status = 2
        relation.save()

    elif action == 'reject':
        relation = Relation.objects.filter(sender=sender, reciver=reciver).first()
        relation.status = 3
        relation.save()

    elif action == 'sent':
        relation = Relation.objects.filter(sender=sender, reciver=reciver).first()
        relation.status = 1
        relation.save()
    
    return redirect('account:user_detail', pk=user2_id)


def sending_requests(request):
    name = "account/sending_requests.html"
    title = "مشاهده درخواست های ارسالی"

    relations = Relation.objects.filter(sender=request.user)

    context = {
        'title': title,
        'relations': relations
    }

    return render(request, name, context)


def reciving_requests(request):
    name = "account/reciving_requests.html"
    title = "مشاهده درخواست های دریافتی"

    relations = Relation.objects.filter(reciver=request.user)

    context = {
        'title': title,
        'relations': relations
    }

    return render(request, name, context)