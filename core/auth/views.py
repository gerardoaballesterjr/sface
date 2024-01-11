from django.contrib import auth
from django.views import generic
from django import http, urls, shortcuts
from core.auth import forms

class LogInView(generic.FormView):
    template_name = 'auth/log-in.html'
    extra_context = {'title':'Log In'}
    form_class = forms.LoginForm
    success_url = urls.reverse_lazy('core:main:index')

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return http.HttpResponseRedirect(self.success_url)
        return super().dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return http.HttpResponse(status=204, headers={
            'Hx-Redirect': self.success_url,
        })

class LogOutView(generic.View):
    def get(self, request):
        return shortcuts.render(request, 'auth/log-out.html', {
            'title': 'Log Out',
            'action': urls.reverse_lazy('core:auth:log-out'),
        })
    
    def post(self, request):
        auth.logout(request)
        return http.HttpResponse(status=204, headers={
            'Hx-Redirect': urls.reverse_lazy('core:main:index'),
        })