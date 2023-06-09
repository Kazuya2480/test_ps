from django import forms
from django.contrib.auth.models import User 
from . import models

class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']



class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']

class StudentExtraForm(forms.ModelForm):
    class Meta:
        model=models.StudentExtra
        fields=['enrollment',]
        labels={
            'enrollment':'User ID'
        }


class BookForm(forms.ModelForm):
    class Meta:
        model=models.Book
        fields=['category', ]
        
   
       


 