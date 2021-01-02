from django import forms
from . import Auction

class NewAuctionForm(forms.Form):
    name = forms.TextInput()
    description = forms.TextInput()
    opening_bid = forms.DecimalField()
    
    