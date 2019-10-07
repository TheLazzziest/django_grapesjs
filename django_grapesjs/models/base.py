from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.forms import model_to_dict


class BaseGrapesJSModel(models.Model):
    gjs_assets = HStoreField(null=True)
    gjs_css = HStoreField(null=True)
    gjs_styles = HStoreField(null=True)
    gjs_html = HStoreField(null=True)
    gjs_components = HStoreField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def to_dict(self):
        return model_to_dict(self)
