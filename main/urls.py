from django import urls

urlpatterns = [
    urls.path('', urls.include('core.page.urls')),
    urls.path('core/', urls.include('core.urls')),
]
