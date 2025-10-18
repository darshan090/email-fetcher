from django.urls import path
from . import views

urlpatterns = [    
    path('',views.home, name='home'),
    path('google/login/',views.google_login_view,name='google_login'),
    path('google/callback/',views.google_callback,name='google_callback'),
    path('google/emails/',views.fetch_emails,name='fetch_emails'),
]