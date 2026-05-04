from django.http import HttpResponse
from django.shortcuts import render

art = [
    {"id": 1, "name": "Name1"},
    {"id": 2, "name": "Name2"},
    {"id": 3, "name": "Name2"},
]


# Create your views here
def index(request):
    return render(request, "artvault/artvault.html", {"art": art})


def get_art_by_id(request, id):
    return HttpResponse(f"Hi there! {request.path},with ID {id}")
