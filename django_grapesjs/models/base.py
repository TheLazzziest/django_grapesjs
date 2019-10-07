from django.contrib.postgres.fields import JSONField
from django.db import models
from django.forms import model_to_dict


class BaseGrapesJSModel(models.Model):
    gjs_assets = JSONField(null=True)
    gjs_css = JSONField(null=True)
    gjs_styles = JSONField(null=True)
    gjs_html = JSONField(null=True)
    gjs_components = JSONField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def to_dict(self):
        return model_to_dict(self)
