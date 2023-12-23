from django import http
import uuid, json

def uuid_generator():
    return uuid.uuid4().hex

def slug_generator(instance, slug=None):
    slug = slug if slug is not None else uuid_generator()
    if instance.__class__.objects.filter(slug=slug).exists():
        return slug_generator(instance, uuid_generator())
    return slug

def form_htmx_response(success_url):
    return http.HttpResponse(status=204, headers={'HX-Trigger': json.dumps({'form': {'success_url': str(success_url),}})})