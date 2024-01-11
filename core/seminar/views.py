from django.contrib.auth import mixins
from django.views import generic
from django import urls, http
from django.contrib import messages
from core import models
from core.seminar import forms
import json

class IndexView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Seminar
    template_name = 'core/seminar/index.html'
    extra_context = {'title': 'Seminar'}

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).order_by('-created_at')
    
class CreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Seminar
    template_name = 'core/form.html'
    form_class = forms.SeminarForm
    success_url = urls.reverse_lazy('core:seminar:index')
    extra_context = {
        'title': 'Create Seminar',
        'action':urls.reverse_lazy('core:seminar:create'),
    }

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        messages.info(self.request, f'Seminar created successfully.')
        return http.HttpResponse(status=204, headers={
            'HX-Trigger': json.dumps({
                'form': {'path': str(self.success_url),}
            }),
        })
    
class UpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Seminar
    template_name = 'core/form.html'
    form_class = forms.SeminarForm
    success_url = urls.reverse_lazy('core:seminar:index')
    extra_context = {'title': 'Update Seminar'}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        if self.get_object().user != self.request.user:
            return self.handle_no_permission()
        self.extra_context['action'] = self.get_object().get_update_url
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        object = form.save()
        messages.info(self.request, f'Seminar updated successfully.')
        return http.HttpResponse(status=204, headers={
            'HX-Trigger': json.dumps({
                'form': {'path': str(self.success_url),}
            }),
        })
    
class DeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Seminar
    template_name = 'core/delete.html'
    success_url = urls.reverse_lazy('core:seminar:index')
    extra_context = {'title': 'Delete Seminar'}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        if self.get_object().user != self.request.user:
            return self.handle_no_permission()
        self.extra_context['action'] = self.get_object().get_delete_url
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        object = self.get_object()
        object.delete()
        messages.info(self.request, f'Seminar deleted successfully.')
        return http.HttpResponse(status=204, headers={
            'HX-Trigger': json.dumps({
                'form': {'path': str(self.success_url),}
            }),
        })
    
class DetailView(mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Seminar
    template_name = 'core/seminar/detail.html'
    extra_context = {}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        if self.get_object().user != self.request.user:
            return self.handle_no_permission()
        self.extra_context['title'] = str(self.get_object().name)
        self.extra_context['data'] = [{'data': eval(object.data), 'created_at': object.created_at.isoformat()} for object in models.Statistic.objects.filter(seminar=self.get_object())]
        return super().dispatch(*args, **kwargs)

class StreamView(mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Seminar
    template_name = 'core/seminar/stream.html'
    extra_context = {}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        if self.get_object().user != self.request.user:
            return self.handle_no_permission()
        self.extra_context['title'] = str(self.get_object().name).capitalize()
        self.extra_context['websocket'] = self.request.build_absolute_uri().replace('http', 'ws')
        return super().dispatch(*args, **kwargs)