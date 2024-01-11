from django.contrib.auth import mixins
from django.views import generic
from django import urls, http
from django.contrib import messages
from core import models, utils
from core.user import forms
import json

class IndexView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.User
    template_name = 'core/user/index.html'
    extra_context = {'title': 'User'}

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return self.handle_no_permission()
        return super().get_queryset().filter(is_superuser=False).order_by('-created_at')
    
class CreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.User
    template_name = 'core/form.html'
    form_class = forms.UserCreationForm
    success_url = urls.reverse_lazy('core:user:index')
    extra_context = {
        'title': 'Create User',
        'action': urls.reverse_lazy('core:user:create'),
    }

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        object = form.save()
        messages.info(self.request, f'User created successfully.')
        return http.HttpResponse(status=204, headers={
            'HX-Trigger': json.dumps({
                'form': {'path': str(self.success_url),}
            }),
        })
    
class UpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.User
    template_name = 'core/form.html'
    form_class = forms.UserChangeForm
    success_url = urls.reverse_lazy('core:user:index')
    extra_context = {'title': 'Update User'}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return self.handle_no_permission()
        self.extra_context['action'] = self.get_object().get_update_url
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        object = form.save()
        messages.info(self.request, f'User updated successfully.')
        return http.HttpResponse(status=204, headers={
            'HX-Trigger': json.dumps({
                'form': {'path': str(self.success_url),}
            }),
        })
    
class DeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.User
    template_name = 'core/delete.html'
    success_url = urls.reverse_lazy('core:user:index')
    extra_context = {'title': 'Delete User'}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return self.handle_no_permission()
        self.extra_context['action'] = self.get_object().get_delete_url
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        object = self.get_object()
        object.delete()
        messages.info(self.request, f'User deleted successfully.')
        return http.HttpResponse(status=204, headers={
            'HX-Trigger': json.dumps({
                'form': {'path': str(self.success_url),}
            }),
        })