from django.shortcuts import render

from artvault.models import Artwork


# Create your views here
def index(request):
    return render(request, "artvault/index.html", {"art": Artwork.objects.all()})


def blabla(request): ...


def browse_artwork(request):
    return render(
        request, "artvault/browse_artwork.html", {"art": Artwork.objects.all()}
    )


def artwork_details(request, id):
    return render(
        request,
        "artvault/artwork_details.html",
        {"art": Artwork.objects.all(), "id": id},
    )
