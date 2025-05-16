# from . import views
from django.urls import path
from secondproject.views import Home

urlpatterns=[
    # path('',views.home,name='home'),
    path('',Home.as_view(),name='home'),
]