from django import urls
from core.dashboard import views

app_name = 'dashboard'

urlpatterns = [
    urls.path('', views.IndexView.as_view(), name='index'),
]