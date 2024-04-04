from .models import Enquiry,Mybook,Support, cartModel
from django import forms

class Enquiryform(forms.ModelForm):
    class Meta():
        model = Enquiry
        fields = "__all__"
        
class Supportform(forms.ModelForm):
    class Meta():
        model = Support
        fields = "__all__"
        
class cartform(forms.ModelForm):
    class Meta():
        model = cartModel
        fields = "__all__"
        
        

        


        
