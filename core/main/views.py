from django.contrib.auth import mixins
from django.views import generic
from core import models

class IndexView(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'core/main/index.html'
    extra_context = {'title':'Dashboard'}

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
class HelpView(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'core/main/help.html'
    extra_context = {'title': 'Help'}

class FrequentlyAskedQuestionsView(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'core/main/frequently-asked-questions.html'
    extra_context = {'title': 'Frequently Asked Questions'}
