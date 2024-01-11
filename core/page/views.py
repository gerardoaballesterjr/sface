from django.views import generic

class IndexView(generic.TemplateView):
    template_name = 'page/index.html'
    extra_context = {'title': 'Sface'}

class AboutView(generic.TemplateView):
    template_name = 'page/about.html'
    extra_context = {'title': 'About'}

class ContactView(generic.TemplateView):
    template_name = 'page/contact.html'
    extra_context = {'title': 'Contact'}

class PrivacyPolicyView(generic.TemplateView):
    template_name = 'page/privacy-policy.html'
    extra_context = {'title': 'Privacy Policy'}
