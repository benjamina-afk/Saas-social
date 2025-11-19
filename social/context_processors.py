# social/context_processors.py

from .models import Client

def clients_list(request):
    return {
        "clients": Client.objects.all().order_by("raison_social")
    }
