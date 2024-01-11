from django import urls

app_name = 'core'

urlpatterns = [
    urls.path('', urls.include('core.main.urls')),
    urls.path('auth/', urls.include('core.auth.urls')),
    urls.path('seminar/', urls.include('core.seminar.urls')),
    urls.path('user/', urls.include('core.user.urls')),
]
