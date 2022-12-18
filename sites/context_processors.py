from .models import Sites

def get_sites(request):
    sites=Sites.objects.all()
    return {'site':sites,}