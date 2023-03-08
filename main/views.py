from django.shortcuts import render


def home(request):
    name = "main/home.html"
    title = "صفحه اصلی"

    data = {"title": title}

    return render(request, name, data)
