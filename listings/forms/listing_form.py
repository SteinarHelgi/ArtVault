from django import forms
from django.utils import timezone
from artvault.models import Artwork


MEDIUM_CHOICES = [
    ("Oil", "Oil"),
    ("Watercolor", "Watercolor"),
    ("Acrylic", "Acrylic"),
    ("Drawing", "Drawing"),
    ("Ink drawing", "Ink drawing"),
    ("Digital", "Digital"),
    ("Photograph", "Photograph"),
    ("Mixed media", "Mixed media"),
    ("Print", "Print"),
    ("Other", "Other"),
]

EDITION_CHOICES = [
    ("Original", "Original"),
    ("Limited edition", "Limited Edition"),
    ("Open edition", "Open Edition"),
]

ART_MOVEMENT_CHOICES = [
    ("Surrealism", "Surrealism"),
    ("Modernism", "Modernism"),
    ("Realism", "Realism"),
    ("Impressionism", "Impressionism"),
    ("Expressionism", "Expressionism"),
    ("Contemporary", "Contemporary"),
    ("Abstract", "Abstract"),
    ("Minimalism", "Minimalism"),
    ("Pop art", "Pop Art"),
    ("Cubism", "Cubism"),
    ("Other", "Other"),
]


class ArtworkListingForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    medium = forms.ChoiceField(
        choices=MEDIUM_CHOICES, widget=forms.Select(attrs={"class": "form-control"})
    )

    edition = forms.ChoiceField(
        choices=EDITION_CHOICES, widget=forms.Select(attrs={"class": "form-control"})
    )

    art_movement = forms.ChoiceField(
        choices=ART_MOVEMENT_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    def clean(self):
            cleaned_data = super().clean()

            if cleaned_data:
                auction_start_date = cleaned_data.get("auction_start_date")
                auction_end_date = cleaned_data.get("auction_end_date")
                today = timezone.now().date()

                if auction_start_date and auction_start_date < today:
                    self.add_error(
                        "auction_start_date",
                        "Auction start date cannot be before today.",
                    )

                if auction_start_date and auction_end_date:
                    if auction_end_date < auction_start_date:
                        self.add_error(
                            "auction_end_date",
                            "Auction end date cannot be before the auction start date.",
                        )

            return cleaned_data
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
            "starting_price": forms.NumberInput(
                attrs={
                    "min": 0,
                    "max": 2147483647,
                    "step": 1,
                }
            ),
            "auction_end_date": forms.DateInput(attrs={"type": "date"}),
        }
