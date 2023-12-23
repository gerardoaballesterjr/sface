from django import urls

urlpatterns = [
    urls.path('', urls.include('core.dashboard.urls')),
    urls.path('authentication/', urls.include('core.authentication.urls')),
    urls.path('seminar/', urls.include('core.seminar.urls')),
    urls.path('user/', urls.include('core.user.urls')),
]
