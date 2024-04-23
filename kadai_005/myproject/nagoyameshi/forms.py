from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from nagoyameshi.models import CustomUser
from .models import Store

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("email", "user_type")  # username を email に置き換え、user_typeを追加

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'address', 'phone_number']


class BookingForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='姓')
    last_name = forms.CharField(max_length=30, label='名')
    tel = forms.CharField(max_length=30, label='電話番号')
    remarks = forms.CharField(label='備考', widget=forms.Textarea())

class AvailabilityForm(forms.Form):
    # ここにフィールドを定義します
    pass