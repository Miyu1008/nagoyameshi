from django.urls import path
from . import views

from subscription import views 

app_name ="subscription"

urlpatterns = [
    path('index/', views.PaymentIndexView.as_view(), name='index'),
    path('checkout/', views.PaymentCheckoutView.as_view(), name='checkout'),
    path('create_checkout_session/', views.create_checkout_session, name='checkout_session'),
    path('success/', views.PaymentSuccessView.as_view(), name='success'),
    path('cancel/', views.PaymentCancelView.as_view(), name='cancel'),
]