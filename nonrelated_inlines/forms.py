from django.forms import modelformset_factory
from django.forms.models import BaseModelFormSet


class NonrelatedInlineFormSet(BaseModelFormSet):
    """
    A basic implementation of an inline formset that doesn't make assumptions
    about any relationship between the form model and its parent instance.
    """
    def __init__(self, instance=None, save_as_new=None, **kwargs):
        self.instance = instance
        super().__init__(**kwargs)
        self.queryset = self.real_queryset

    @classmethod
    def get_default_prefix(cls):
        opts = cls.model._meta
        return (
            opts.app_label + '-' + opts.model_name
        )

    def save_new(self, form, commit=True):
        obj = super().save_new(form, commit=False)
        self.save_new_instance(self.instance, obj)
        if commit:
            obj.save()
        return obj


def nonrelated_inlineformset_factory(
    model, obj=None,
    queryset=None,
    formset=NonrelatedInlineFormSet,
    save_new_instance=None,
    **kwargs
):
    """
    FormSet factory that sets an explicit queryset on new classes.
    """
    FormSet = modelformset_factory(model, formset=formset, **kwargs)
    FormSet.real_queryset = queryset
    FormSet.save_new_instance = save_new_instance
    return FormSet
