django_grapesjs
================

.. image:: https://api.codeclimate.com/v1/badges/6b6ca2f03af2d84119c6/maintainability
   :target: https://codeclimate.com/github/gulliverbms/django_grapesjs/maintainability
   :alt: Maintainability

.. image:: https://travis-ci.org/gulliverbms/django_grapesjs.svg?branch=master
   :target: https://travis-ci.org/gulliverbms/django_grapesjs

.. image:: https://coveralls.io/repos/github/gulliverbms/django_grapesjs/badge.svg?branch=master
   :target: https://coveralls.io/github/gulliverbms/django_grapesjs?branch=master

.. image:: https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat
   :target: https://github.com/gulliverbms/django_grapesjs/issues
   :alt: contributions welcome

.. image:: http://hits.dwyl.io/gulliverbms/https://github.com/gulliverbms/django_grapesjs.svg
   :target: http://hits.dwyl.io/gulliverbms/https://github.com/gulliverbms/django_grapesjs
   :alt: HitCount


A small library allows you to integrate the page builder "grapesjs" into django admin


Install
=======

.. code-block:: bash

    pip install django_grapesjs


Then add it to your INSTALLED_APPS:

.. code-block:: python

    INSTALLED_APPS = (
        'django_grapesjs',
        ...
        'django.contrib.admin',
    )

For client-side:
================

Set a path to the GrapesJS model

.. code-block:: python

    GRAPESJS_MODEL = 'app.GrapesJSModel'

You can make a model which inherits a base model for GrapesJS template

.. code-block:: python

    class GrapesJSModel(ModelToDictMixin,
                        BaseMetaGrapesJSModel,
                        BaseGrapesJSModel):

        user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

Set a path to the model form which passes GrapesJS template to the model:

.. code-block:: python

    GRAPESJS_CREATE_FORM = 'app.forms.GrapesJSCreateForm'
    GRAPESJS_UPDATE_FORM = 'app.forms.GrapesJSUpdateForm'

Attach view mixin for processing GrapesJS template data

.. code-block:: python


    class GrapesJSTemplateView(GrapesJSTemplateViewMixin, TemplateView):
        pass


    class GrapesJSDetailView(GrapesJSDetailViewMixin, DetailView):
        pass


    class GrapesJSLoadView(GrapesJSAjaxDetailViewMixin, View):
        pass


    class GrapesJSUpdateView(GrapesJSAjaxUpdateViewMixin, UpdateView):
        pass


    class GrapesJSListView(GrapesJSListViewMixin, GrapesJSCreateViewMixin, ListView):
        pass


    class GrapesJSCreateView(GrapesJSCreateViewMixin, CreateView):
        pass



    class GrapesJSDeleteView(GrapesJSDeleteViewMixin, DeleteView):
        pass




Add routes to the main view and several processing ones

.. code-block:: python

    urlpatterns = [
        re_path('^template/list/$', GrapesJSListView.as_view(), name='template-list'),
        re_path('^template/create/', GrapesJSCreateView.as_view(), name='template-create'),
        re_path('^template/(?P<pk>\d+)/?$', GrapesJSDetailView.as_view(), name='template'),
        re_path('^template/load/(?P<pk>\d+)/?$', GrapesJSLoadView.as_view(), name='template-load'),
        re_path('^template/save/(?P<pk>\d+)/?$', GrapesJSUpdateView.as_view(), name='template-save'),
        re_path('^template/delete/(?P<pk>\d+)/?$', GrapesJSDeleteView.as_view(), name='template-delete'),
    ]

For admin usage:
================

To work with the "template_choices", need to add a url-template in the urls.py file

.. code-block:: python

    urlpatterns = [
       path('get_template/', GetTemplate.as_view(), name='dgjs_get_template'),
    ]


Just import the field and add to your model

.. code-block:: python

    from django.db import models
    from django_grapesjs.models import GrapesJsHtmlField


    class ExampleModel(models.Model):
        html = GrapesJsHtmlField()
        ...

        # default_html - path to the html file to display the default value
        # for the field when the form page is received
        html = GrapesJsHtmlField(default_html='default.html')

        # or default - if the page is simply static
        html = GrapesJsHtmlField(default=render_to_string('default.html'))
        ...

        # use the redactor_config argument to select the configuration of the editor
        # Available:
        #     - redactor_config='base' - basic setting, most widgets are used
        #     - redactor_config='min' - minimum setting, only the most necessary
        html = GrapesJsHtmlField(redactor_config='base')
        ...

        # use apply_django_tag = True, if you want to apply render django or jinja tags
        html = GrapesJsHtmlField(default_html='default.html', apply_django_tag=True)
        ...

        # use template_choices to select multiple templates
        html = GrapesJsHtmlField(template_choices=(('django_grapesjs/default.html', 'default'),))

And then inherit "GrapesJsAdminMixin", in the admin class of the current model

.. code-block:: python

    from django.contrib import admin
    from django_grapesjs.admin import GrapesJsAdminMixin
    from app.models import GrapesJSModel

    @admin.register(GrapesJSModel)
    class ExampleAdmin(GrapesJsAdminMixin, admin.ModelAdmin):
        pass

You can use special tags in your templates, for flexible customization

.. code-block:: HTML

   <ignore></ignore>

If you need to comment out some of the html code during the save,
but execute or display at the time editing in page builder - use this tag.
For example, if your template that uses django or jinja tags does not have any styles or javascript
(because they are in another place, for example, in "footer.html"), you can put css and js in this
tag, styles and javascript code in the editor will work, but when saved and used on the site there
will not be repeating fragments

.. code-block:: HTML

   <hidden></hidden>

If you are editing in the editor with apply_django_tag, you might be distracted by the additional:
{% exclude %}, {% include %}, {% for <expression> %}, etc; - use this tag. He temporarily hides
information, embedded in it during editing, and during the save returns to the original form

Custom Settings
===============

.. code-block:: python

    # it must be of dict type which contains the keys: css, js
    # and the appropriate paths to each part of the library
    # An each path can be of different type:
    # can be an absolute one, which starts with: https://... or /...
    # or a relative one which looks like: 'grapesjs/...' (be sure that it's placed there)
    GRAPESJS_CORE_ASSETS = settings.GRAPESJS_CORE_ASSETS

    # A path to form with grapesjs fields
    GRAPESJS_CREATE_FORM = getattr(settings, 'GRAPESJS_CREATE_FORM', None)

    # A path to form with grapesjs fields
    GRAPESJS_UPDATE_FORM = getattr(settings, 'GRAPESJS_UPDATE_FORM', None)

    # path to the html file of the form field. Enter your value for the override
    GRAPESJS_TEMPLATE = getattr(settings, 'GRAPESJS_TEMPLATE', 'django_grapesjs/forms/fields/textarea.html')

    # A path to model with grapejs model field
    GRAPESJS_MODEL = getattr(settings, 'GRAPESJS_MODEL', None)

    # use the value of the field from the db - True, or use the global save editor
    GRAPESJS_DEFAULT_MODELS_DATA = int(getattr(settings, 'GRAPESJS_DEFAULT_MODELS_DATA', True))

    # redefine the path to the demo html file, the markup from this file will be used by default
    GRAPESJS_DEFAULT_HTML = getattr(settings, 'GRAPESJS_DEFAULT_HTML', 'django_grapesjs/demo.html')

    # Grapes JS Settings

    # An ID for html tag container which is used during grapesjs initialisation
    GRAPESJS_CONTAINER_ID = getattr(settings, "GRAPESJS_CONTAINER_ID", "grapesjs")

    # Store Manager

    # A prefix which will be applied to all data properties in request body
    GRAPESJS_STORAGE_ID_PREFIX = getattr(settings, 'GRAPESJS_STORAGE_ID_PREFIX', 'gjs_')

    # A default set of storage type. By default 'remote' is set
    # @see: https://grapesjs.com/docs/modules/Storage.html#setup-remote-storage
    GRAPESJS_STORAGE_TYPE = getattr(settings, 'GRAPESJS_STORAGE_TYPE', 'remote')

    # A number of user action to be made before saving the template state
    GRAPESJS_STEPS_BEFORE_SAVE = int(getattr(settings, 'GRAPESJS_STEPS_BEFORE_SAVE', 5))

    # A url which grapes.js library will send a template data to
    GRAPESJS_URL_STORE = getattr(settings, 'GRAPESJS_URL_STORE', '')

    # An ID for quering an database object
    GRAPESJS_MODEL_LOOKUP_FIELD = getattr(settings, 'GRAPESJS_REQUEST_ID_FIELD', 'pk')

    # A url which grapes.js library will get a template data from
    GRAPESJS_URL_LOAD = getattr(settings, 'GRAPESJS_URL_LOAD', '')

    # Enable checking of a storage of remote or local types
    GRAPESJS_CHECK_LOCAL = int(bool(GRAPESJS_URL_LOAD) or bool(GRAPESJS_URL_STORE))

    # A list of allowed host by CORS policy
    GRAPESJS_ALLOWED_ORIGIN_LIST = getattr(settings, 'GRAPESJS_ALLOWED_ORIGIN_LIST', [])

    # @DEPRECATED
    # True if you want to save html and css
    GRAPESJS_SAVE_CSS = int(getattr(settings, 'GRAPESJS_SAVE_CSS', False))


Warning
===============
the library does not work in "inlines"

Reference
===============
* `grapesjs`_


.. _`grapesjs`: https://github.com/artf/grapesjs

