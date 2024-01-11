from django.urls import re_path 
from core.seminar import consumers

urlpatterns = [
    re_path(r'core/seminar/stream/(?P<slug>\w+)', consumers.SeminarConsumer.as_asgi())
]