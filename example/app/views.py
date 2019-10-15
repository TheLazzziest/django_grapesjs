from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView, UpdateView
from django_grapesjs.views.mixins import (
    GrapesJSTemplateViewMixin, GrapesJSCreateViewMixin,
    GrapesJSListViewMixin, GrapesJSDeleteViewMixin,
    GrapesJSDetailViewMixin,
    GrapesJSAjaxDetailViewMixin,
    GrapesJSAjaxUpdateViewMixin,
)
from app.models import GrapesJSJSONModel


class GrapesJSTemplateView(GrapesJSTemplateViewMixin, TemplateView):
    title = 'Grapes JS'

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = self.title
        return context


class GrapesJSDetailView(GrapesJSDetailViewMixin, DetailView):
    title = 'Grapes JS: {0}'
    template_name = 'app/detail_view.html'

    def get_context_data(self, object: GrapesJSJSONModel):
        context = super().get_context_data(object)
        context['title'] = self.title.format(object.title)
        return context


class GrapesJSLoadView(GrapesJSAjaxDetailViewMixin, View):
    pass


class GrapesJSUpdateView(GrapesJSAjaxUpdateViewMixin, UpdateView):
    pass


class GrapesJSListView(GrapesJSListViewMixin, GrapesJSCreateViewMixin, ListView):
    """List view to display a grapes.js models."""
    title = 'GrapesJS Model list'
    template_name = 'app/list_view.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = self.title
        return context


class GrapesJSCreateView(GrapesJSCreateViewMixin, CreateView):
    """Create view for making a grapes.js model."""

    def get_success_url(self):
        return reverse("template", args=(self.object.id,))


class GrapesJSDeleteView(GrapesJSDeleteViewMixin, DeleteView):

    def get_success_url(self):
        return reverse("template-list")
