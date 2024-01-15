from django import forms
from .models import Listing, Bid, Comment

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description'}),
            'starting_bid': forms.NumberInput(attrs={'placeholder': 'Starting Bid'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'Image URL (optional)'}),
            'category': forms.TextInput(attrs={'placeholder': 'Category (optional)'})
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']