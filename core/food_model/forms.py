from django import forms
from .models import *
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core import validators

class LoginForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': 'Your username',
    'class': 'w-full py-4 px-6 rounded-xl',
  }))

  password = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Your password',
    'class': 'w-full py-4 px-6 rounded-xl',
  }))

class RegisterForm(forms.Form):
  # token = forms.CharField(max_length=255,required=False, widget=(forms.HiddenInput()))

  email_regex = RegexValidator(
        regex=r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$',
        message="Enter the correct email input.",
    )

  username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
    'placeholder': 'your username',
    'class': 'w-full py-4 px-6 rounded-xl',
  }))
  email = forms.EmailField(validators=[email_regex]
                           ,widget=forms.EmailInput(attrs={
    'placeholder': 'your username',
    'class': 'w-full py-4 px-6 rounded-xl',
  }))
  password = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder': 'Your Password',
    'class': 'w-full py-4 px-6 rounded-xl',
  }))
  

INPUT_CLASS = 'w-full py-4 px-6 rounded-xl border'


#SHOPOWNER


class NewRestaurantForm(forms.ModelForm):
  class Meta:
    model = Pending
    fields = ('restaurant_name', 'owner_name', 'address', 'pincode', 'phone_number', 'image', 'category', )
    widgets = {
      'restaurant_name': forms.TextInput(attrs={
        'class': INPUT_CLASS
      }),
      'owner_name': forms.TextInput(attrs={
        'class': INPUT_CLASS
      }),
      'address': forms.Textarea(attrs={
        'class': INPUT_CLASS
      }),
      'pincode': forms.NumberInput(attrs={
        'class': INPUT_CLASS
      }),
      'phone_number': forms.NumberInput(attrs={
        'class': INPUT_CLASS
      }),

    }

class NewItemForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Get the request from the kwargs
        super(NewItemForm, self).__init__(*args, **kwargs)
        if request:
            user = request.user
            self.fields['restaurant'].queryset = Pending.objects.filter(created_by=user)

  restaurant = forms.ModelChoiceField(
    queryset = MenuItem.objects.none(),
    label='restaurant',
    empty_label='select a restaurant',
  )

  class Meta:
    model = MenuItem
    fields = ('category','food_name', 'description', 'price', 'image', 'rating', 'restaurant', )
    widgets = {
      'food_name': forms.TextInput(attrs={
        'class': INPUT_CLASS
      }),
      'description': forms.Textarea(attrs={
        'class': INPUT_CLASS
      }),
      'price': forms.NumberInput(attrs={
        'class': INPUT_CLASS
      }),
      'image': forms.FileInput(attrs={
        'class': INPUT_CLASS
      }),
      'rating': forms.NumberInput(attrs={
        'class': INPUT_CLASS
      }),
    }


class EditFoodItemForm(forms.ModelForm):
   class Meta:
      model = MenuItem
      fields = ['food_name', 'description', 'price', 'image', 'rating','is_sold', ]
      widgets = {
         'food_name' : forms.TextInput(attrs={
            'class': INPUT_CLASS,
         }),
         'description' : forms.Textarea(attrs={
            'class': INPUT_CLASS,
         }),
         'image': forms.FileInput(attrs={
            'class': INPUT_CLASS,
         }),
         'rating': forms.NumberInput(attrs={
            'class': INPUT_CLASS,
         }),
      
      }


#USER

class NewProfileForm(forms.ModelForm):
  terms_and_services = forms.BooleanField(required=True)

  class Meta:
    model = Profile
    fields = ('firstname', 'lastname', 'address', 'city', 'pincode', 'phonenumber', 'temp_phonenumber', 'image', 'terms_and_services', )

    widgets = {
       
       'firstname' : forms.TextInput(attrs={
          'class': INPUT_CLASS,
       }),
       'lastname': forms.TextInput(attrs={
          'class': INPUT_CLASS,
       }),
       'address': forms.Textarea(attrs={
          'class': INPUT_CLASS,
       }),
       'city': forms.TextInput(attrs={
          'class': INPUT_CLASS,
       }),
       'pincode': forms.NumberInput(attrs={
          'class': INPUT_CLASS,
       }),
       'phonenumber': forms.TextInput(attrs={
          'class': INPUT_CLASS,
          'placeholder': 'xxx-xxx-xxxx'
       }),
       'temp_phonenumber': forms.TextInput(attrs={
          'class': INPUT_CLASS,
          'placeholder': 'xxx-xxx-xxxx'
       }),
       'image': forms.FileInput(attrs={
          'class': INPUT_CLASS,
       }),
    }

class EditProfileForm(forms.ModelForm):
  terms_and_services = forms.BooleanField(required=True)
  class Meta:
    model = Profile
    fields = ('firstname',  'lastname', 'address', 'city', 'pincode', 'phonenumber', 'temp_phonenumber', 'image', 'terms_and_services', )

    widgets = {
       'firstname' : forms.TextInput(attrs={
          'class': INPUT_CLASS,
       }),
       'lastname': forms.TextInput(attrs={
          'class': INPUT_CLASS,
       }),
       'address': forms.Textarea(attrs={
          'class': INPUT_CLASS,
       }),
       'city': forms.TextInput(attrs={
          'class': INPUT_CLASS,
       }),
       'pincode': forms.NumberInput(attrs={
          'class': INPUT_CLASS,
       }),
       'phonenumber': forms.TextInput(attrs={
          'class': INPUT_CLASS,
       }),
       'temp_phonenumber': forms.TextInput(attrs={
          'class': INPUT_CLASS,
       }),
       'image': forms.FileInput(attrs={
          'class': INPUT_CLASS,
       }),
    }