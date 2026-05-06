
from django import forms

from artvault.models import Artwork



class ArtworkListingForm(forms.ModelForm):
    imagepath = forms.CharField(max_length=255)
    
    class Meta:
        model = Artwork
        fields = [
             "title",
            "medium",
            "edition",
            "dimensions",
            "sold",
            "history",
            "artist_name",
            "date",
            "starting_price",
            "art_movement",
        ]
