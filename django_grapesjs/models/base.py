from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.forms import model_to_dict


class ModelToDictMixin(object):
    """Model mixin to convert Model object to a dict."""

    def to_dict(self):
        return model_to_dict(self)


class BaseMetaGrapesJSModel(models.Model):
    """Basic model with meta data fields for a template."""
    title = models.CharField(max_length=255, null=True)
    url = models.URLField(null=True)

    class Meta:
        abstract = True


class BaseGrapesJSModel(models.Model):
    """Basic model for storing a template data."""

    gjs_assets = HStoreField(null=True)
    gjs_css = HStoreField(null=True)
    gjs_styles = HStoreField(null=True)
    gjs_html = HStoreField(null=True)
    gjs_components = HStoreField(null=True)

    class Meta:
        abstract = True
