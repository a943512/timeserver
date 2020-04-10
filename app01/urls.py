from django.urls import re_path
from app01 import views

urlpatterns = [
    re_path('/time/$', views.TmeView.as_view()),
    re_path('time/(?P<pk>\d+)/$', views.TmeView.as_view()),
    re_path('/time/(?P<nowtime>[0-9-]*)/(?P<token>[a-zA-Z0-9-]*)/$', views.TmeView.as_view()),
    re_path('login/$', views.LoginView.as_view()),
    re_path('register/$', views.RegisterView.as_view()),
]

