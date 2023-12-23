from django.contrib import auth
from django.views import generic
from django import http, urls, shortcuts
from core.authentication import forms

class LoginView(generic.FormView):
    template_name = 'authentication/login.html'
    extra_context = {'title':'Login'}
    form_class = forms.LoginForm
    success_url = urls.reverse_lazy('dashboard:index')

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return http.HttpResponseRedirect(self.success_url)
        return super().dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return http.HttpResponse(status=204, headers={'Hx-Redirect': self.success_url})

class LogoutView(generic.View):
    def get(self, request):
        return shortcuts.render(request, 'authentication/logout.html', {'title': 'Logout', 'action': urls.reverse_lazy('authentication:logout')})
    
    def post(self, request):
        auth.logout(request)
        return http.HttpResponse(status=204, headers={'Hx-Redirect': urls.reverse_lazy('dashboard:index')})