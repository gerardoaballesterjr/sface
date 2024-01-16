from django import urls
from core.page import views

app_name = 'page'

urlpatterns = [
    urls.path('', views.IndexView.as_view(), name='index'),
]
