from django_grapesjs.forms.base import BaseGrapesJSForm, BaseGrapesJSMetaDataForm

from app.models import GrapesJSJSONModel


class GrapesJSCreateForm(BaseGrapesJSMetaDataForm):
    class Meta:
        model = GrapesJSJSONModel
        fields = ('title', 'url',)


class GrapesJSUpdateForm(BaseGrapesJSForm):
    class Meta:
        model = GrapesJSJSONModel
        exclude = ('title', 'url', 'created_at', )

