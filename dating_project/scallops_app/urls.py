from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
<<<<<<< HEAD
    path('register', views.process_registration),
    path('process/login', views.process_login),
=======
    path('about_us/', views.display_about_us),
    path('contact_us/', views.display_contact_us),
    path('registration/', views.display_registration),
    path('login/', views.display_login),
    path('message/', views.display_message),
    path('profile/', views.display_profile),
>>>>>>> ad9388dd7ab3fc548549e80d3e939e1963e1c88f
]