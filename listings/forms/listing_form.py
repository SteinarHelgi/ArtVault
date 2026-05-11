from django import forms
from artvault.models import Artwork


MEDIUM_CHOICES = [
    ("oil", "Oil"),
    ("watercolor", "Watercolor"),
    ("acrylic", "Acrylic"),
    ("drawing", "Drawing"),
    ("ink_drawing", "Ink drawing"),
    ("digital", "Digital"),
    ("photograph", "Photograph"),
]

EDITION_CHOICES = [
    ("original", "Original"),
    ("limited_edition", "Limited Edition"),
    ("open_edition", "Open Edition"),
]


class ArtworkListingForm(forms.ModelForm):
    medium = forms.ChoiceField(
        choices=MEDIUM_CHOICES, widget=forms.Select(attrs={"class": "form-control"})
    )

    edition = forms.ChoiceField(
        choices=EDITION_CHOICES, widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Artwork
        fields = [
            "title",
            "medium",
            "edition",
            "dimensions",
            "history",
            "artist_name",
            "date",
            "starting_price",
            "art_movement",
            "auction_start_date",
            "auction_end_date",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Title of the artwork"}),
            "dimensions": forms.TextInput(attrs={"placeholder": "200x200"}),
            "history": forms.Textarea(attrs={"rows": 5}),
            "date": forms.DateInput(attrs={"type": "date"}),
            "auction_start_date": forms.DateInput(attrs={"type": "date"}),
            "auction_end_date": forms.DateInput(attrs={"type": "date"}),
        }
