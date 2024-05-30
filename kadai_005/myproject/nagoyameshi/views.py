from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Store, Booking
from .forms import CustomUserCreationForm  # CustomUserCreationFormのインポート
from .forms import CustomAuthenticationForm,  ReviewForm
from django.views.generic.edit import CreateView
from .forms import StoreForm
import datetime
from django.db.models import Q
from django.utils.timezone import localtime, make_aware
from django.views.generic import View
from .forms import BookingForm
from .forms import AvailabilityForm
from django.utils import timezone
from .models import Store, Booking, Date, reverse
from .models import Favorite
from django.contrib import messages
from django.http import HttpResponse
from .models import StoreDayOff, Review
from .forms import StoreDayOffForm
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.views.generic import TemplateView
from django.http import HttpResponseBadRequest
from django.db.models import Avg
from .models import Product



import stripe
from django.conf import settings
from django.urls import reverse_lazy


class TopView(TemplateView):
    template_name = "top.html"

#ログイン、ログアウト
class LoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        if user.user_type == 1:  # 例えばユーザータイプが '1' の場合
            return reverse_lazy('user_dashboard')  # 一般ユーザーのダッシュボードへ
        elif user.user_type == 2:  # ユーザータイプが '2' の場合
            return reverse_lazy('store_dashboard')  # 店舗ユーザーのダッシュボードへ
        else:
            return super().get_success_url()  # デフォルトのリダイレクト先

class CustomLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'top.html'

class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "password_change"
        return context

class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    """パスワード変更完了"""
    template_name = 'password_change_done.html'

def membershipterms(request):
     return render(request,'membership_terms.html')    

def companyoverview(request):
     return render(request,'company_overview.html')

def user_dashboardview(request):
     return render(request,'user_dashboard.html')

def store_dashboardview(request):
     return render(request,'store_dashboard.html')

#新規登録
class SignUpView(CreateView):
    form_class = CustomUserCreationForm  # CustomUserCreationForm を使用するように更新
    success_url = reverse_lazy('login')
    template_name = 'sign_up.html'


#店舗一覧、詳細
def store_list(request):
    query = request.GET.get('query')
    if query:
        stores = Store.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        stores = Store.objects.all()
    return render(request, 'store_list.html', {'stores': stores})

def store_detail(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    is_favorite = False
    if request.method == "POST":
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            store = form.save(commit=False)
            store.save()
            return redirect('store_detail', pk=store.pk)
          
        if request.user.is_authenticated:
           is_favorite = Favorite.objects.filter(user=request.user, store=store).exists()
           return render(request, 'store_detail.html', {'store': store, 'is_favorite': is_favorite})

    else:
        form = StoreForm(instance=store)
    return render(request, 'store_detail.html', {'form': form, 'store': store})



def StoreInfo(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    id = store_id
    query = get_gnavi_data(id, "", "", "", 1)
    res_list = rest_search(query)
    stores_info = extract_restaurant_info(res_list)
    review_count = Review.objects.filter(shop_id=store_id).count()
    score_ave = Review.objects.filter(shop_id = store_id).aggregate(Avg('score'))
    average = score_ave['score__avg']
    if average:
        average_rate = average / 5 * 100
    else:
        average_rate = 0

    if request.method == 'GET':        
        review_form = ReviewForm()
        review_list = Review.objects.filter(shop_id = store_id)

    else:
        form = ReviewForm(data=request.POST)
        score = request.POST['score']
        comment = request.POST['comment']

        if form.is_valid():
            review = Review()
            review.store_id = store_id
            review.store_name = stores_info[0][1]
            review.store_address = stores_info[0][7]
            review.image_url = stores_info[0][5]
            review.user = request.user
            review.score = score
            review.comment = comment
            review.save()
            return redirect('techapp:store_info', store_id)

    params = {
        'title': '店舗詳細',
        'review_count': review_count,
        'stores_info': stores_info,
        'review_form': review_form,
        'review_list': review_list,
        'average': average,
        'average_rate': average_rate,
    }
    return render(request, 'store_detail', params)

#レビュー　booking、favorite参考に
#データが登録できるように修正する
class ReviewView(View):
    def post(self, request, store_id):
        store = Store.objects.get(id=store_id)
        form_data = {
            'comment': request.POST.get('comment'),
            'score': request.POST.get('score'),
            'store': store,
            'user': request.user
        }
        form = ReviewForm(form_data)

        if form.is_valid():
            print("あいうえお")
            store_id = form.cleaned_data['store_id']
            store = Store.objects.get(id=store_id)
            
            # レビューが既に存在するか確認
            existing_review = Review.objects.filter(store=store, user=request.user).first()
            if existing_review:
                # レビューが既に存在する場合は、更新処理を行う
                existing_review.score = form.cleaned_data['score']
                existing_review.comment = form.cleaned_data['comment']
                existing_review.save()
                messages.success(request, "レビューを更新しました。")
            else:
                # 新しいレビューを作成
                review = Review()
                review.store = store
                review.score = form.cleaned_data['score']
                review.comment = form.cleaned_data['comment']
                review.user = request.user
                review.save()
                messages.success(request, "レビューを追加しました。")
            
            # レビューが保存または更新された後、店舗詳細ページにリダイレクト
            return render(request, 'store_detail.html', {'store': store})
        else:
            print(form.errors)
        # フォームが有効でない場合、store_idがNoneであればエラーメッセージを表示
        if store_id is None:
            messages.error(request, "店舗IDが不明です。")
            return redirect('store_detail')  # 適切なエラーページにリダイレクト
        # フォームが有効でない場合、エラーメッセージを含むフォームと共にテンプレートを再表示
        messages.error(request, "レビューの追加に失敗しました。")
        return render(request, 'store_detail.html', {'form': form, 'store': store})


#店舗情報編集
class ProductCreateView(CreateView):
     model = Product
     fields = '__all__'
     template_name = 'store_new.html' 
     


#お気に入り
class FavoriteView(View):
    def post(self, request, store_id):
        if request.user.is_authenticated:
            store = Store.objects.get(id=store_id)
            favorite, created = Favorite.objects.get_or_create(user=request.user, store=store)
            if created:
                messages.success(request, "お気に入りに追加しました。")
            else:
                favorite.delete()
                messages.success(request, "お気に入りから削除しました。")
        else:
            return redirect('login')
        
        return redirect('store_detail', store_id=store_id)

    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        return render(request, 'favorite_list.html', {'favorites': favorites})
    

def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    if favorites:  # リストが空でないことを確認
        print(favorites[0].user)
    return render(request, 'favorite_list.html', {'favorites': favorites})


#予約
class BookingView(View,LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        time = self.kwargs.get('time')
        store_id = self.kwargs.get('store_id')
        
        form = BookingForm(initial={'store_id': store_id})
        
        return render(request, 'booking.html', {
            'year': year,
            'month': month,
            'day': day,
            'time': time,
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        year = int(request.POST['date_year'])
        month = int(request.POST['date_month'])
        day = int(request.POST['date_day'])
        time = request.POST['time']
        
        hour, minute = map(int, time.split(':'))
        start_time = make_aware(datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute))
        end_time = start_time + datetime.timedelta(hours=1)
        booking_data = Booking.objects.filter(start=start_time)
        
        form = BookingForm(request.POST)
        
        if form.is_valid():
            store_id = form.cleaned_data['store_id']
            store = Store.objects.get(id=store_id)
            
            if booking_data.exists():
                form.add_error(None, '既に予約があります。\n別の日時で予約をお願いします。')
            else:
                booking = Booking()
                booking.start = start_time
                booking.end = end_time
                
                booking.tel = form.cleaned_data['tel']
                booking.remarks = form.cleaned_data['remarks']
                booking.store = store
                booking.user = request.user
                booking.save()
                
                return redirect(reverse('booking', kwargs={'store_id': store_id}))
        
        return render(request, 'booking.html', {
            'year': year,
            'month': month,
            'day': day,
            'time': time,
            'form': form,
        })


    
def create_store_day_off(request):
    if request.method == 'POST':
        form = StoreDayOffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store_list')  # リダイレクト先を適切なビューに修正する
    else:
        form = StoreDayOffForm()
    return render(request, 'create_store_day_off.html', {'form': form})




