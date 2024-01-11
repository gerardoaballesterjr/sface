from django import urls
from core.page import views

app_name = 'page'

urlpatterns = [
    urls.path('', views.IndexView.as_view(), name='index'),
    urls.path('about', views.AboutView.as_view(), name='about'),
    urls.path('contact', views.ContactView.as_view(), name='contact'),
    urls.path('privacy-policy', views.PrivacyPolicyView.as_view(), name='privacy-policy'),
]
