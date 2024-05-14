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
from .forms import CustomAuthenticationForm
from django.views.generic.edit import CreateView
from .forms import StoreForm
import datetime
from django.db.models import Q
from django.utils.timezone import localtime, make_aware
from django.views.generic import View
from .forms import BookingForm
from .forms import AvailabilityForm
from django.utils import timezone
from .models import Store, Booking, Date
from .models import Favorite
from django.contrib import messages
from django.http import HttpResponse
from .models import StoreDayOff
from .forms import StoreDayOffForm
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.views.generic import TemplateView




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

    


#店舗情報編集
class ProductCreateView(CreateView):
     model = Store
     fields = '__all__'

def store_edit(request, pk):
    store = get_object_or_404(Store, pk=pk)
    if request.method == "POST":
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            store = form.save(commit=False)
            store.save()
            return redirect('store_detail', pk=store.pk)
    else:
        form = StoreForm(instance=store)
    return render(request, 'nagoyameshi/store_dashboard.html', {'form': form})



#カレンダー
class CalendarView(View):
    def get(self, request, store_id, *args, **kwargs):
        store = Store.objects.get(pk=store_id)
        today = datetime.date.today()
        year = kwargs.get('year')
        month = kwargs.get('month')
        day = kwargs.get('day')
        if year and month and day:
            start_date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            start_date = today
        days = [start_date + datetime.timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]

        #ここを直す
        calendar = {}
        for day in days:
            row = {}
            for hour in range(9, 27):
                row[hour] = True
            calendar[day] = row

        #直す

        unavailable_dates = store.unavailable_dates.all()
        unavailable_dates_list = [unavailable_date.date for unavailable_date in unavailable_dates]
        #直す　1週間分だけ取得できるようにする
        for hour in calendar: 
            for date in calendar[hour]:
                if date not in unavailable_dates_list:
                   calendar[hour][date] = True


        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(hours=1)  # 予約時間が1時間と仮定

        booking_data = Booking.objects.exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data:
            local_time = timezone.localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] = False
        print(calendar)
        return render(request, 'calendar.html', {
            'calendar': calendar,
            'days': days,
            'start_day': start_day,
            'end_day': end_day,
            'before': days[0] - datetime.timedelta(days=7),
            'next': days[-1] + datetime.timedelta(days=1),
            'today': today,
            'store': store,
            #'date': date,  # date変数を追加
        })

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
class BookingView(View):
    def get(self, request, *args, **kwargs):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        form = BookingForm(request.POST or None)

        return render(request, 'booking.html', {
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        start_time = make_aware(datetime.datetime(year=year, month=month, day=day, hour=hour))
        end_time = make_aware(datetime.datetime(year=year, month=month, day=day, hour=hour + 1))
        booking_data = Booking.objects.filter(start=start_time)
        form = BookingForm(request.POST or None)
        if booking_data.exists():
            form.add_error(None, '既に予約があります。\n別の日時で予約をお願いします。')
        else:
            if form.is_valid():
                booking = Booking()
                booking.start = start_time
                booking.end = end_time
                booking.first_name = form.cleaned_data['first_name']
                booking.last_name = form.cleaned_data['last_name']
                booking.tel = form.cleaned_data['tel']
                booking.remarks = form.cleaned_data['remarks']
                booking.save()
                return redirect('store') # あとで変更

        return render(request, 'booking.html', {
            'year': year,
            'month': month,
            'day': day,
            'hour': hour,
            'form': form,
        })
    


def make_reservation(request):
    if request.method == 'POST':
        # 予約の処理を行う
        # 予約の詳細はリクエストから取得し、データベースに保存する

        # 予約日
        reservation_date = request.POST.get('reservation_date')

        # 店舗
        store_id = request.POST.get('store_id')
        store = Store.objects.get(pk=store_id)

        # 予約日が定休日かどうかをチェック
        if StoreDayOff.objects.filter(store=store, day_off__date=reservation_date).exists():
            return HttpResponse("Sorry, the shop is closed on this day.")
        else:
            # 予約を保存するなどの適切な処理を行う
            return HttpResponse("Reservation made successfully!")

    else:
        # GETリクエストの場合、予約フォームを表示する
        stores = Store.objects.all()
        return render(request, 'reservation_form.html', {'stores': stores})
    
    
def create_store_day_off(request):
    if request.method == 'POST':
        form = StoreDayOffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store_list')  # リダイレクト先を適切なビューに修正する
    else:
        form = StoreDayOffForm()
    return render(request, 'create_store_day_off.html', {'form': form})




