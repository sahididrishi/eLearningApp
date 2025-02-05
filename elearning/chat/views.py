
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def global_chat_room(request):
    return render(request, 'chat/room.html')