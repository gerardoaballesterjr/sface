from django.contrib.auth import mixins
from django.views import generic
from django import urls
from django.contrib import messages
from core import models, utils
from core.user import forms

class SuperuserMixin(mixins.LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class IndexView(SuperuserMixin, generic.ListView):
    model = models.User
    template_name = 'user/index.html'
    extra_context = {'title':'User'}

    def get_queryset(self):
        return super().get_queryset().filter(is_superuser=False).order_by('-created_at')
    
class CreateView(SuperuserMixin, generic.CreateView):
    model = models.User
    template_name = 'user/form.html'
    form_class = forms.UserCreationForm
    success_url = urls.reverse_lazy('user:index')
    extra_context = {'title':'Create User', 'action': urls.reverse_lazy('user:create')}

    def form_valid(self, form):
        object = form.save()
        messages.info(self.request, f'User <strong>{object.first_name} {object.last_name}</strong> created successfully.')
        return utils.form_htmx_response(self.success_url)
    
class UpdateView(SuperuserMixin, generic.UpdateView):
    model = models.User
    template_name = 'user/form.html'
    form_class = forms.UserChangeForm
    success_url = urls.reverse_lazy('user:index')
    extra_context = {'title':'Update User'}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        self.extra_context['action'] = self.get_object().get_update_url
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        object = form.save()
        messages.info(self.request, f'User <strong>{object.first_name} {object.last_name}</strong> updated successfully.')
        return utils.form_htmx_response(self.success_url)
    
class DeleteView(SuperuserMixin, generic.DeleteView):
    model = models.User
    template_name = 'user/delete.html'
    success_url = urls.reverse_lazy('user:index')
    extra_context = {'title':'Delete User'}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        self.extra_context['action'] = self.get_object().get_delete_url
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        object = self.get_object()
        object.delete()
        messages.info(self.request, f'User <strong>{object.first_name} {object.last_name}</strong> deleted successfully.')
        return utils.form_htmx_response(self.success_url)