from django.contrib import admin
from django.apps import apps
from django import forms
import models
import utils


class TokenAdminForm(forms.ModelForm):
    class Meta:
        model = models.Token
        exclude = ('token_digest', )

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['token_value'] = utils.get_random_string()
        super(TokenAdminForm, self).__init__(*args, **kwargs)


class TokenAdmin(admin.ModelAdmin):
    form = TokenAdminForm


def register(app_fullname, admins, ignore_models=[]):
    app_label = app_fullname.split('.')[-2:][0]
    for n, model in apps.get_app_config(app_label).models.items():
        if model.__name__ in ignore_models:
            continue
        name = "%sAdmin" % model.__name__
        admin_class = admins.get(name, None)
        if admin_class is None:
            admin_class = type(
                "%sAdmin" % model.__name__,
                (admin.ModelAdmin,), {},
            )

        if admin_class.list_display == ('__str__',):
            excludes = getattr(admin_class, 'list_excludes', ())
            additionals = getattr(admin_class, 'list_additionals', ())
            admin_class.list_display = tuple(
                [f.name for f in model._meta.fields
                 if f.name not in excludes]) + additionals

        admin.site.register(model, admin_class)


register(__name__, globals())
