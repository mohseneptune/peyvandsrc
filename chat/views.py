from django.shortcuts import render, redirect, get_object_or_404
from chat.models import Room, Message
from chat.models import Relation
from django.contrib.auth import get_user_model

User = get_user_model()


def room_create_view(request, relation_id):
    relation = get_object_or_404(Relation, pk=relation_id)
    room = Room.objects.create(relation=relation, name=f'room_{relation_id}')
    room.members.add(relation.sender)
    room.members.add(relation.reciver)
    room.members.add(User.objects.filter(is_superuser=True).first())
    room.save()
    return redirect('chat:room', room_id=room.id)
    

def room_view(request, room_id):
    template_name = 'chat/room.html'
    template_title = 'اتاق گفتگو'

    room = get_object_or_404(Room, pk=room_id)

    messages = Message.objects.filter(room=room)[0:25]

    context = {
        'template_title': template_title,
        'room': room,
        'messages': messages
    }
    return render(request, template_name, context)