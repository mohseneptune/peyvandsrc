from django.shortcuts import render, get_object_or_404, redirect
from account.models import Khosousiaat, Entezaaraat
from chat.models import Relation
from django.contrib.auth import get_user_model


User = get_user_model()


def admin_dashboard(request):
    name = 'adminpanel/admin_dashboard.html'
    title = 'پنل مدیریت'

    data = {
        'title': title
    }

    return render(request, name, data)



def requests_list(request):
    name = 'adminpanel/requests_list.html'
    title = 'پنل مدیریت'

    relations = Relation.objects.filter(status='2')
    
    data = {
        'title': title,
        'relations': relations
    }


    return render(request, name, data)
