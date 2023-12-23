from django import urls
from core.authentication import views

app_name = 'authentication'

urlpatterns = [
    urls.path('login', views.LoginView.as_view(), name='login'),
    urls.path('logout', views.LogoutView.as_view(), name='logout'),
]