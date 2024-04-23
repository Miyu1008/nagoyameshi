from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, UserRegistrationForm, StoreRegistrationForm
from .models import Store
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views import View
from accounts.models import CustomUser as User

class TopView(TemplateView):
     template_name = "top.html"

def index(request):
     return render(request,'top.html')

def membershipterms(request):
     return render(request,'membership_terms.html')    

def companyoverview(request):
     return render(request,'company_overview.html')

def password_reset_comfirm(request):
     return render(request,'password_reset_confirm.html')

def store_list(request):
    query = request.GET.get('query')
    if query:
        stores = Store.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        stores = Store.objects.all()
    return render(request, 'store_list.html', {'stores': stores})

def store_detail(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    return render(request, 'store_detail.html', {'store': store})

class LoginView(LoginView):
     form_class = AuthenticationForm
     template_name = 'login.html'

def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_store:
                # 店舗用の処理
                login(request, user)
                return HttpResponse("店舗としてログインしました。")
            else:
                # ユーザー用の処理
                login(request, user)
                return HttpResponse("ユーザーとしてログインしました。")
        else:
            return HttpResponse("ログインに失敗しました。")
 
class CustomLogoutView(LoginRequiredMixin, LogoutView):
     template_name = 'top.html'

#会員登録ページに関する処理
class UserCreateView(CreateView):
    template_name = 'sign_up.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('top')

#新規会員登録に関する処理
def create_account(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # 登録成功後のリダイレクト先を指定
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'sign_up.html', {'form': form})

# 新規会員登録のビューを追加
class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = '/login/'

class StoreRegistrationView(CreateView):
    form_class = StoreRegistrationForm
    template_name = 'registration/register.html'
    success_url = '/login/'

"""
class PasswordResetView(LoginRequiredMixin,PasswordContextMixin, FormView):
    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'
    title = _('Password reset')
    token_generator = default_token_generator
"""
#予約
