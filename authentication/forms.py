from django import forms
import phonenumbers
from .models import *
import re, uuid
CHOICES=[('Male','Male'),
         ('Female','Female'),
         ('Others','Others')
         ]
class RegisterUserForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    mobile = forms.IntegerField()
    # description_es = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'dob', 'gender', 'email', 'password', 'confirm_password','mobile',
                  'user_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Enter a first name.",
            'type': "text"
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Enter a last name.",
            'type': "text"
        })
        self.fields['dob'].widget.attrs.update({
            'class': 'form-control',
            'type': "date"
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Email",
            'type': "email"
        })
        self.fields['mobile'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "number",
            'type': "number"
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Password",
            'type': "password"
        })
        self.fields['confirm_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Confirm Password",
            'type': 'password'
        })
        self.fields['user_type'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "Enter frame length in cm",
            'min':'1'
        })

    def clean(self):    
        super(RegisterUserForm, self).clean()
        if  not User.objects.filter(id=self.instance.pk).exists():
            password = self.cleaned_data.get("password")
            confirm_password = self.cleaned_data.get("confirm_password")
            if len(self.cleaned_data.get("password"))<8:
                self._errors['password'] = self.error_class(['Password should contains minimum 8 characters.'])
                return self.cleaned_data
            if password != confirm_password:
                self._errors['confirm_password'] = self.error_class(['password and confirm_password does not match.'])
                return self.cleaned_data
        else:
            del self._errors['password']
            del self._errors['confirm_password']
            del self._errors['user_type']
        strmobileNumber = '+91' + str(self.cleaned_data.get('mobile'))
        try:
            my_number = phonenumbers.parse(strmobileNumber)
            if not phonenumbers.is_valid_number(my_number):
                self._errors['mobile'] = self.error_class(['Please enter a valid mobile number.'])
                return self.cleaned_data
        except:
            self._errors['mobile'] = self.error_class(['Please enter a valid mobile number.'])
            return self.cleaned_data
        return self.cleaned_data