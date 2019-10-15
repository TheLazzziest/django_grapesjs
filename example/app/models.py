from django.utils.translation import ugettext as _
from django.db import models

from django_grapesjs.models.base import (
    BaseGrapesJSModel, BaseMetaGrapesJSModel, ModelToDictMixin
)
from django_grapesjs.models.fields import GrapesJsHtmlField


class GrapesJSModel(models.Model):
    html = GrapesJsHtmlField()


class GrapesJSJSONModel(ModelToDictMixin,
                        BaseMetaGrapesJSModel,
                        BaseGrapesJSModel):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('grapes model')
        verbose_name_plural = _('grapesjs models')