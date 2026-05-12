from django.contrib import admin
from .models import Artmovement, ArtmovementArtwork, ArtmovementArtist

# Register your models here.

admin.site.register(Artmovement)
admin.site.register(ArtmovementArtwork)
admin.site.register(ArtmovementArtist)
