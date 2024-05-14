
from django.views import generic
import os
import stripe
import json
from django.urls import reverse
from django.shortcuts import redirect
from django.http import JsonResponse

class PaymentIndexView(generic.TemplateView):
   template_name = "subscription/home.html"

class PaymentCheckoutView(generic.TemplateView):
   template_name = "subscription/checkout.html"

class PaymentSuccessView(generic.TemplateView):
   template_name = "subscription/success.html"

class PaymentCancelView(generic.TemplateView):
   template_name = "subscription/cancel.html"


def create_checkout_session(request):
   stripe.api_key = 'sk_test_51PE2jMHP6OevB5tXixpSyyGcHX5g4MOh0GeH0AA8qpw3fScMXHilR0knoZxlp2fnSchyRxLDK9gOh1qL8LJfyBnA00Jnk6QzUu'

   try:
       checkout_session = stripe.checkout.Session.create(
           payment_method_types=['card'],
           line_items=[
               {
                   'price_data': {
                       'currency': 'jpy',
                       'unit_amount': 300,
                       'product_data': {
                           'name': 'Stubborn Attachments',
                           'images': ['https://i.imgur.com/EHyR2nP.png'],
                       },
                   },
                   'quantity': 1,
               },
           ],
           mode='payment',
           success_url=request.build_absolute_uri(reverse('subscription:success')),
           cancel_url=request.build_absolute_uri(reverse('subscription:cancel')),
       )
       print(JsonResponse({'id': checkout_session.id}))
       return JsonResponse({'id': checkout_session.id})
   except Exception as e:
       return JsonResponse({'error':str(e)})