from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from nagoyameshi.models import CustomUser
from .models import Store, StoreDayOff
import datetime
from .models import User, Review,  Product

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

class ProductCreationFrom(forms.Form):
    class Meta:
        model =  Product
        fields = ['name', 'description', 'address', 'phone_number']



class BookingForm(forms.Form):
    TIME_CHOICES = [(datetime.time(hour=i).strftime('%H:%M'), f'{i}:00') for i in range(24)]
    date = forms.DateField(widget=forms.SelectDateWidget())
    time = forms.ChoiceField(choices=TIME_CHOICES)
    first_name = forms.CharField(max_length=30, label='姓')
    last_name = forms.CharField(max_length=30, label='名')
    tel = forms.CharField(max_length=30, label='電話番号')
    remarks = forms.CharField(label='備考', widget=forms.Textarea())
    store_id = forms.IntegerField(widget=forms.HiddenInput()) 

    
    somedate = datetime.datetime(2024,1,1)



class AvailabilityForm(forms.Form):
    # ここにフィールドを定義します
    pass

class StoreDayOffForm(forms.ModelForm):
    class Meta:
        model = StoreDayOff
        fields = ['store', 'day_off']


def activate_user(uidb64, token):    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        return False

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return True
    
    return False

class ReviewForm(forms.ModelForm):   
    class Meta:
        model = Review
        fields = ['score', 'comment','store','user']
