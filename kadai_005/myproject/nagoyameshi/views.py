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
from datetime import datetime, date, timedelta, time
from django.db.models import Q
from django.utils.timezone import localtime, make_aware
from django.views.generic import View
from .forms import BookingForm
from .forms import AvailabilityForm
from django.views import View
from django.utils import timezone
from datetime import date, datetime, timedelta
from .models import Store, Booking, Date
from .models import Favorite
from django.contrib import messages

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
    if request.method == "POST":
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            store = form.save(commit=False)
            store.save()
            return redirect('store_detail', pk=store.pk)
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
        today = date.today()
        year = kwargs.get('year')
        month = kwargs.get('month')
        day = kwargs.get('day')
        if year and month and day:
            start_date = date(year=int(year), month=int(month), day=int(day))
        else:
            start_date = today
        days = [start_date + timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]

        calendar = {}
        for hour in range(10, 21):
            row = {}
            for day in days:
                row[day] = True
            calendar[hour] = row

        available_dates = store.available_dates.all()
        for available_date in available_dates:
            if available_date.date in calendar[start_date.hour]:
                calendar[start_date.hour][available_date.date] = True

        start_time = datetime.now()
        end_time = start_time + timedelta(hours=1)  # 予約時間が1時間と仮定

        booking_data = Booking.objects.exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data:
            local_time = timezone.localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] = False

        return render(request, 'calendar.html', {
            'calendar': calendar,
            'days': days,
            'start_day': start_day,
            'end_day': end_day,
            'before': days[0] - timedelta(days=7),
            'next': days[-1] + timedelta(days=1),
            'today': today,
            'store': store,
        })

#お気に入り
class FavoriteView(View):
    def post(self, request, store_id):
        if request.user.is_authenticated:
            # ログインしている場合の処理
            store = Store.objects.get(id=store_id) 
            favorite, created = Favorite.objects.get_or_create(user=request.user, store=store)
            if created:
                messages.success(request, "お気に入りに追加しました。")

            else:
                messages.error(request, "すでにお気に入りに登録されています。")

        else:
            return redirect('login')
        
        return redirect('store_detail', store_id=store_id)  # リダイレクト先を適切なビューに修正する

    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        return render(request, 'favorite_list.html', {'favorites': favorites})
    
def favorite_list(request):
     return render(request,'favorite_list.html')

"""
class CalendarView(View):
    def get(self, request,  store_id, *args, **kwargs):
        store = get_object_or_404(Store, pk=store_id)
        #staff_data = Staff.objects.filter(id=self.kwargs['pk']).select_related('user').select_related('store')[0]
        today = date.today()
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            # 週始め
            start_date = date(year=year, month=month, day=day)
        else:
            start_date = today
        # 1週間
        days = [start_date + timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]

        calendar = {}
        # 10時～20時
        for hour in range(10, 21):
            row = {}
            for day in days:
                row[day] = True
            calendar[hour] = row
        start_time = make_aware(datetime.combine(start_day, time(hour=10, minute=0, second=0)))
        end_time = make_aware(datetime.combine(end_day, time(hour=20, minute=0, second=0)))
        
        booking_data = Booking.objects.exclude(Q(start__gt=end_time) | Q(end__lt=start_time))
        for booking in booking_data:
            local_time = localtime(booking.start)
            booking_date = local_time.date()
            booking_hour = local_time.hour
            if (booking_hour in calendar) and (booking_date in calendar[booking_hour]):
                calendar[booking_hour][booking_date] = False

        return render(request, 'calendar.html', {
            #'staff_data': staff_data,
            'calendar': calendar,
            'days': days,
            'start_day': start_day,
            'end_day': end_day,
            'before': days[0] - timedelta(days=7),
            'next': days[-1] + timedelta(days=1),
            'today': today,
            'store': store,
        })

"""
    
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
        start_time = make_aware(datetime(year=year, month=month, day=day, hour=hour))
        end_time = make_aware(datetime(year=year, month=month, day=day, hour=hour + 1))
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
    


