from django.contrib.auth import mixins
from django.views import generic
from core import models

class IndexView(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'dashboard/index.html'
    extra_context = {'title':'Dashboard'}

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)