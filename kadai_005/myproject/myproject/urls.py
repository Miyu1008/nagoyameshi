"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from nagoyameshi import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.TopView.as_view(), name="top"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(next_page='top'), name='logout'),
    path('SignUpView/', views.SignUpView.as_view(), name="sign_up"),
    path('membershipterms/', views.membershipterms, name="membershipterms"),
    path('companyoverview/', views.companyoverview, name="companyoverview"),
    path('user_dashboard/', views.user_dashboardview, name="user_dashboard"),
    path('store_dashboard/', views.store_dashboardview, name="store_dashboard"),
    path('store_list/', views.store_list, name='store_list'),
    path('store/<int:store_id>/', views.store_detail, name='store_detail'),
    path('store_new/', views.ProductCreateView.as_view(), name="store_new"),
    path('booking/<int:store_id>/', views.BookingView.as_view(), name='booking'),
    path('booking/<int:store_id>/review/', views.ReviewView.as_view(), name='review'),
    path('favorite/<int:store_id>/', views.FavoriteView.as_view(), name='favorite'),
    path('favorite_list/', views.favorite_list, name="favorite_list"),
    path('toggle_favorite/<int:store_id>/', views.FavoriteView.as_view(), name='toggle_favorite'),
    path('create_store_day_off/', views.create_store_day_off, name='create_store_day_off'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'), 
    path('password_change_done/', views.PasswordChangeDone.as_view(), name='password_change_done'), 

    path('', include('django.contrib.auth.urls')),
    path('subscription/', include('subscription.urls')), 
   
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
