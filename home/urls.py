from django.urls import re_path
from home.views import home_page, RegisterView, LoginView

urlpatterns = [
    re_path(r'^$',home_page),
    re_path(r'^register/$', RegisterView.as_view()),
    re_path(r'^login/$', LoginView.as_view()),
]
