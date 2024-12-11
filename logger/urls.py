from django.urls import path, re_path
from . import views

urlpatterns = [
    path('__gen_500/', views.__gen_500_errors)
]