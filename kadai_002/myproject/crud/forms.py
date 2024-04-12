from django import forms # Djangoのformsモジュールをインポート
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Store


# SearchFormクラスを定義
class SearchForm(forms.Form):
        keyword = forms.CharField(label='', max_length=50)

class CustomUserCreationForm(UserCreationForm):
    # 必要なフィールドを追加
    first_name = forms.CharField(label= "氏名", max_length=30, required=True)
    email = forms.CharField(label= "メールアドレス", max_length=30, required=True)
    password1 = forms.CharField(
        label= "パスワード",
        max_length=30,
        required=True,
        widget=forms.PasswordInput,
        help_text="")
    password2 = forms.CharField(
        label= "パスワード(確認用)",
        max_length=30,
        required=True,
        widget=forms.PasswordInput,
        help_text="パスワードを再入力してください")
    postal_code = forms.CharField(label= "郵便番号", max_length=30, required=True)
    address = forms.CharField(label= "住所", max_length=30, required=True)
    phone_number = forms.CharField(label= "電話番号", max_length=30, required=True)
    birthday = forms.CharField(label= "誕生日", max_length=30, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password1', 'password2',
                  'postal_code', 'address', 'phone_number', 'birthday')
        
class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'address', 'phone_number', 'image']
