from functools import partial

from django.contrib import admin
from django.contrib.admin.checks import InlineModelAdminChecks
from django.contrib.admin.options import flatten_fieldsets
from django.forms import ALL_FIELDS
from django.forms.models import modelform_defines_fields

from .forms import NonrelatedInlineFormSet, nonrelated_inlineformset_factory


class NonrelatedInlineModelAdminChecks(InlineModelAdminChecks):
    """
    Check used by the admin system to determine whether or not an inline model
    has a relationship to the parent object.

    In this case we always want this check to pass.
    """
    def _check_exclude_of_parent_model(self, obj, parent_model):
        return []

    def _check_relation(self, obj, parent_model):
        return []


class NonrelatedStackedInline(admin.StackedInline):
    """
    Stacked inline base class for models not explicitly related to the inline
    model.
    """
    checks_class = NonrelatedInlineModelAdminChecks
    formset = NonrelatedInlineFormSet

    def get_form_queryset(self, obj):
        raise NotImplementedError()

    def save_new_instance(self, parent, instance):
        raise NotImplementedError()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            self.update_instance(formset.instance, instance)
            instance.save()
        formset.save_m2m()

    def get_formset(self, request, obj=None, **kwargs):
        if 'fields' in kwargs:
            fields = kwargs.pop('fields')
        else:
            fields = flatten_fieldsets(self.get_fieldsets(request, obj))

        exclude = [*(self.exclude or []), *self.get_readonly_fields(request, obj)]
        if self.exclude is None and hasattr(self.form, '_meta') and self.form._meta.exclude:
            exclude.extend(self.form._meta.exclude)
        exclude = exclude or None

        can_delete = self.can_delete and self.has_delete_permission(request, obj)

        queryset = self.model.objects.none()
        if obj:
            queryset = self.get_form_queryset(obj)

        defaults = {
            'form': self.form,
            'formfield_callback': partial(self.formfield_for_dbfield, request=request),
            'formset': self.formset,
            'extra': self.get_extra(request, obj),
            'can_delete': can_delete,
            'can_order': False,
            'fields': fields,
            'min_num': self.get_min_num(request, obj),
            'max_num': self.get_max_num(request, obj),
            'exclude': exclude,
            'queryset': queryset,
            **kwargs,
        }

        if defaults['fields'] is None and not modelform_defines_fields(defaults['form']):
            defaults['fields'] = ALL_FIELDS

        return nonrelated_inlineformset_factory(
            self.model,
            save_new_instance=self.save_new_instance,
            **defaults
        )
