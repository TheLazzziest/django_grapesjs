import json
from http import HTTPStatus

from django.http import JsonResponse, Http404
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin

from django_grapesjs import (
    settings, get_grapesjs_model,
    get_grapesjs_create_form,
    get_grapesjs_update_form
)
from django_grapesjs.utils import build_url


class GrapesJSContextDataMixin(object):
    """A mixin for providing grapes.js context data during template rendering."""

    def get_context_data(self, **additional_context):
        """Get default context."""
        context = super().get_context_data()
        lookup_field = settings.GRAPESJS_MODEL_LOOKUP_FIELD
        context = {
            **context, **{
                'GRAPESJS_STORAGE_ID_PREFIX': settings.GRAPESJS_STORAGE_ID_PREFIX,
                'GRAPESJS_CONTAINER_ID': settings.GRAPESJS_CONTAINER_ID,
                'GRAPESJS_STORAGE_TYPE': settings.GRAPESJS_STORAGE_TYPE,
                'GRAPESJS_CHECK_LOCAL': settings.GRAPESJS_CHECK_LOCAL,
                'GRAPESJS_STEPS_BEFORE_SAVE': settings.GRAPESJS_STEPS_BEFORE_SAVE,
                'GRAPESJS_URL_STORE': build_url(
                    settings.GRAPESJS_URL_STORE,
                    additional_context.get(lookup_field)
                ),
                'GRAPESJS_URL_LOAD': build_url(
                    settings.GRAPESJS_URL_LOAD,
                    additional_context.get(lookup_field)
                ),
                'GRAPESJS_ALLOWED_ORIGIN_LIST': settings.GRAPESJS_ALLOWED_ORIGIN_LIST
            }
        }

        return context


class GrapesJSProcessingDataMixin(object):
    """Common context data which is applied to a html page."""

    @staticmethod
    def parse_json_body(body):
        """Helper method to parse data in JSON format."""
        return json.loads(body)  # noqa

    def setup(self, request, *args, **kwargs):
        self.model = get_grapesjs_model()
        self.model_lookup_field = settings.GRAPESJS_MODEL_LOOKUP_FIELD

        super().setup(request, *args, **kwargs)


class GrapesJSAjaxViewMixin(object):
    """A view mixin for processing AJAX request."""

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return JsonResponse(status=HTTPStatus.FORBIDDEN, data={})
        return super().dispatch(request, *args, **kwargs)


class GrapesJSTemplateViewMixin(GrapesJSContextDataMixin):
    """A bare template view mixin for a template view."""

    template_name = 'django_grapesjs/views/base.html'


class GrapesJSListViewMixin(GrapesJSContextDataMixin,
                            GrapesJSProcessingDataMixin,
                            MultipleObjectMixin):
    """A list view mixing for a grapes.js model."""

    def setup(self, request, *args, **kwargs):
        self.model = get_grapesjs_model()
        super().setup(request, *args, **kwargs)


class GrapesJSDetailViewMixin(GrapesJSContextDataMixin,
                              GrapesJSProcessingDataMixin,
                              SingleObjectMixin):
    """A detail view mixin for rendering a grapes.js template."""

    http_methods = ("GET",)

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.pk_url_kwarg = self.model_lookup_field

    def get_context_data(self, object):
        """Overridden method for getting a context data for grapes.js builder rendering."""
        lookup_field = settings.GRAPESJS_MODEL_LOOKUP_FIELD
        model_data = {
            lookup_field: str(object.id)
        }
        return super().get_context_data(**model_data)


class GrapesJSAjaxDetailViewMixin(GrapesJSAjaxViewMixin,
                                  GrapesJSDetailViewMixin):
    """A form class view mixin for a loading grapes.js template data."""

    def get_context_data(self, object):
        return object.to_dict()

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return JsonResponse(data=context, status=HTTPStatus.OK)
        except Http404 as http_error:
            return JsonResponse(data={'error': list(http_error.args)}, status=HTTPStatus.BAD_REQUEST)


class GrapesJSCreateViewMixin(GrapesJSContextDataMixin,
                              GrapesJSProcessingDataMixin,
                              FormMixin):
    """A create view mixin for making a grapes.js template."""

    http_methods = ('POST',)

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.form_class = get_grapesjs_create_form()


class GrapesJSAjaxCreateViewMixin(GrapesJSAjaxViewMixin,
                                  GrapesJSCreateViewMixin):
    """A create view mixin for making a grapes.js template model via ajax request."""

    def get_form_kwargs(self):
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        if self.request.method in ('POST',):
            kwargs.update({
                'data': self.parse_json_body(
                    self.request.body.decode('utf-8')
                ),
                'files': self.request.FILES,
            })
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form_data = self.form_valid(form)
            http_status = HTTPStatus.OK
        else:
            form_data = self.form_invalid(form)
            http_status = HTTPStatus.BAD_REQUEST
        return JsonResponse(data=form_data, status=http_status)


class GrapesJSUpdateViewMixin(GrapesJSProcessingDataMixin,
                              SingleObjectMixin):
    """An update view mixin for updating a template model."""

    http_methods = ("POST",)

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.form_class = get_grapesjs_update_form()


class GrapesJSAjaxUpdateViewMixin(GrapesJSAjaxViewMixin,
                                  GrapesJSUpdateViewMixin):
    """An update view mixin for updating a grapes.js template model."""

    def get_form_kwargs(self):
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        if self.request.method in ('POST',):
            kwargs.update({
                'data': self.parse_json_body(
                    self.request.body.decode('utf-8')
                ),
                'files': self.request.FILES,
                'instance': self.object
            })
        return kwargs

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            form = self.get_form()
            if form.is_valid():
                self.object = form.save()
                form_data = self.object.to_dict()
                http_status = HTTPStatus.OK
            else:
                form_data = form.errors
                http_status = HTTPStatus.BAD_REQUEST
            return JsonResponse(data=form_data, status=http_status)
        except Http404 as http_error:
            return JsonResponse(data={'error': list(http_error.args)}, status=HTTPStatus.BAD_REQUEST)


class GrapesJSDeleteViewMixin(GrapesJSContextDataMixin,
                              GrapesJSProcessingDataMixin):
    """A delete view mixin for processing deleting of a template model."""

    http_methods = ('POST',)

    def setup(self, request, *args, **kwargs):
        self.model = get_grapesjs_model()
        super().setup(request, *args, **kwargs)

# def saveTemplate(cls, request, *args, **kwargs):
#     template_data = json.loads(
#         request.body.decode('utf-8')
#     )
#     form_data = {
#         'data': template_data,
#         'files': request.FILES,
#     }
#     form_class = cls.get_form_class()
#     model_class = cls.get_model_class()
#     lookup_field = settings.GRAPESJS_MODEL_LOOKUP_FIELD
#     try:
#         template_instance = model_class.objects.get(
#             **{lookup_field: kwargs[lookup_field]}
#         )
#         form_data['instance'] = template_instance
#     finally:
#         grapesjs_form = form_class(**form_data)
#
#     if grapesjs_form.is_valid():
#         status = HTTPStatus.OK
#         data = grapesjs_form.save().to_dict()
#     else:
#         status = HTTPStatus.BAD_REQUEST
#         data = grapesjs_form.errors
#     return JsonResponse(status=status, data=data)
