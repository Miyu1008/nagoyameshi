from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Store
from accounts.models import CustomUser as User

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

# 新規会員登録のフォームを追加
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

class StoreRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_store = True
        if commit:
            user.save()
        return user
