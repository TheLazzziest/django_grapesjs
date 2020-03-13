from mock import mock
from django import test
from django.core.exceptions import ValidationError
from django_grapesjs.forms.fields import GrapesJsField
from django_grapesjs.forms.widgets import GrapesJsWidget

__all__ = ('GrapesJsWidgetTestCase', )



class GrapesJsWidgetTestCase(test.TestCase):
    def test_get_formatted_id_value(self):
        value = 'value-id'
        correct_value = 'value_id'

        widget = GrapesJsWidget()
        result = widget.get_formatted_id_value(value)

        self.assertEqual(correct_value, result)

    @mock.patch('django.forms.widgets.Widget.get_context')
    def test_get_context(self, context_mock):
        value = 0
        attrs = [
            'apply_django_tag',
            'apply_django_tag',
            'template_choices',
            'html_name_init_conf',
        ]
        check_data = {'widget': {'attrs': {'id': 'test'}}}

        widget = GrapesJsWidget()
        context_mock.return_value = check_data

        data = check_data.copy()

        for attr in attrs:
            data['widget'][attr] = value

        attrs.append('default_html')

        for attr in attrs:
            setattr(widget, attr, value)

        self.assertDictEqual(data, widget.get_context('name', 'value', 'attrs'))

