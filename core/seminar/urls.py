from django import urls
from core.seminar import views

app_name = 'seminar'

urlpatterns = [
    urls.path('', views.IndexView.as_view(), name='index'),
    urls.path('create', views.CreateView.as_view(), name='create'),
    urls.path('update/<slug:slug>', views.UpdateView.as_view(), name='update'),
    urls.path('delete/<slug:slug>', views.DeleteView.as_view(), name='delete'),
    urls.path('detail/<slug:slug>', views.DetailView.as_view(), name='detail'),
    urls.path('stream/<slug:slug>', views.StreamView.as_view(), name='stream'),
]
