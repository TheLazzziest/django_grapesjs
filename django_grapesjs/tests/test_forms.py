from django import test
from django.core.exceptions import ValidationError
from django_grapesjs.forms import GrapesJsField, GrapesJsWidget

__all__ = ('GrapesJsFieldTestCase', )


class GrapesJsFieldTestCase(test.TestCase):
    list_args = {
        'default_html': lambda inst: inst.widget.default_html,
        'html_name_init_conf': lambda inst: inst.widget.html_name_init_conf,
        'apply_django_tag': lambda inst: inst.widget.apply_django_tag,
        'template_choices': lambda inst: inst.widget.template_choices,
        'validate_tags': lambda inst: inst.validate_tags
    }

    def get_check_dict_attr(self, values_default, dict_values, inst):
        data = {}

        for k, v in self.list_args.items():
            data[k] = values_default or dict_values.get(k) or v(inst)

        return data

    def test_init(self):
        incorrect_value = 'string'

        formfield = GrapesJsField()

        self.assertSetEqual(
            set(GrapesJsField.__init__.__defaults__),
            set(self.get_check_dict_attr(None, {}, formfield).values())
        )

        data = self.get_check_dict_attr(incorrect_value, {}, None)
        formfield = GrapesJsField(**data)

        self.assertSetEqual(
            set(data.values()),
            set(self.get_check_dict_attr(None, {}, formfield).values())
        )

    def test_validate(self):
        formfield = GrapesJsField()

        self.assertIsNone(formfield.validate('string'))

    def test_clean_correct_value(self):
        value = 'string'

        formfield = GrapesJsField()
        result = formfield.clean(value)

        self.assertEqual(value, result)

    def test_clean_incorrect_value(self):
        with self.assertRaises(ValidationError):
            formfield = GrapesJsField()
            formfield.clean('')

        with self.assertRaises(TypeError):
            formfield = GrapesJsField()
            formfield.clean(0)


