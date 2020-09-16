from django import forms
from django.forms import CharField, ModelForm

from .models import Listing, Comment


class CreateForm(forms.ModelForm):
    user_id         = forms.IntegerField(required=False)
    title           = forms.CharField(
                        max_length=64,
                        label='',
                        widget=forms.TextInput(
                            attrs={
                                "placeholder": "Listing title...",
                                "class": "form-control"
                            }
                        )
                    )

    description     = forms.CharField(
                        max_length=500,
                        label='',
                        widget=forms.Textarea(
                            attrs={
                                "placeholder": "Add a description (max 255 characters)...",
                                "class": "form-control",
                                "rows": 5
                            }
                        )
                    )

    img_url         = forms.CharField(
                        label='',
                        help_text="Make sure that you enter a valid URL.",
                        widget=forms.TextInput(
                            attrs={
                                "placeholder": "Enter URL of product image...",
                                "class": "form-control"
                            }
                        )
                    )
    category        = forms.ChoiceField(
                        choices=Listing.CATEGORIES,
                        label='',
                        widget=forms.Select(
                            attrs={
                                "class": "custom-select"
                            }
                        )
                    )

    starting_bid    = forms.DecimalField(
                        label='',
                        help_text="Lowest amount that you're willing to accept for this item.",
                        widget=forms.NumberInput(
                            attrs={
                                "type": "number",
                                "min": "0.01", 
                                "step": "0.01",
                                "placeholder": "Enter a starting bid...",
                                "class": "form-control"
                            }
                        )
                    )
    class Meta:
        model = Listing
        fields = ['title', 'description', 'img_url', 'category', 'starting_bid']


class CommentForm(forms.Form):
    message           = forms.CharField(
                        max_length=500,
                        label='',
                        widget=forms.Textarea(
                            attrs={
                                "placeholder": "Enter your comment...",
                                "class": "form-control",
                                "rows": 3
                            }
                        )
                    )


