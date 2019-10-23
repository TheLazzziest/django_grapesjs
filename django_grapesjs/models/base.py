from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.db.models import TextField
from django.forms import model_to_dict


class ModelToDictMixin(object):
    """Model mixin to convert Model object to a dict."""

    def to_dict(self):
        return model_to_dict(self)


class BaseMetaGrapesJSModel(models.Model):
    """Basic model with meta data fields for a template."""

    title = models.CharField(max_length=255, null=True)
    domain = models.CharField(max_length=255, null=True, blank=True)
    path = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class BaseGrapesJSModel(models.Model):
    """Basic model for storing a template data."""

    gjs_assets = HStoreField(null=True, blank=True)

    gjs_css = TextField(null=True, blank=True)
    gjs_html = TextField(null=True, blank=True)

    gjs_styles = HStoreField(null=True, blank=True)
    gjs_components = HStoreField(null=True, blank=True)

    class Meta:
        abstract = True
