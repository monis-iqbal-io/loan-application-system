from django.urls import path
from .views import home_view ,step1_view , step2_view , step3_view , step4_view , preview_view , submit_view , thank_you_view

urlpatterns = [
    path('step-1/', step1_view, name='step1'),
    path('step-2/', step2_view, name='step2'),
    path('step-3/', step3_view, name='step3'),
    path('step-4/', step4_view, name='step4'),
    path('preview/', preview_view, name='preview'),
    path('submit/', submit_view, name='submit'),
    path('thank-you/', thank_you_view, name='thank_you'),
   
]