from django import urls
from core.main import views

app_name = 'main'

urlpatterns = [
    urls.path('', views.IndexView.as_view(), name='index'),
    urls.path('help', views.HelpView.as_view(), name='help'),
    urls.path('FAQ', views.FAQView.as_view(), name='FAQ'),
]
