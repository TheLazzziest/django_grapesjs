from django import forms
from django.forms import fields
from .fields import GrapesJsField


class GrapesJSAdminFormMixin(forms.ModelForm):
    """GrapesJS base form for admin."""
    html = GrapesJsField()


class BaseGrapesJSMetaDataForm(forms.ModelForm):
    """GrapesJS base form with form metadata."""

    title = fields.CharField(required=False)
    url = fields.URLField(required=False)

    def clean_url(self):
        return self.cleaned_data['url']


class BaseGrapesJSForm(forms.ModelForm):
    """GrapesJS base form for client-side."""

    gjs_assets = fields.CharField(required=False)
    gjs_css = fields.CharField(required=False)
    gjs_styles = fields.CharField(required=False)
    gjs_html = fields.CharField(required=False)
    gjs_components = fields.CharField(required=False)
