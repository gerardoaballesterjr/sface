from django import urls
from core.auth import views

app_name = 'auth'

urlpatterns = [
    urls.path('log-in', views.LogInView.as_view(), name='log-in'),
    urls.path('log-out', views.LogOutView.as_view(), name='log-out'),
]
