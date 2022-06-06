# django-nonrelated-inlines

Django admin inlines for unrelated models

![CircleCI](https://img.shields.io/circleci/build/github/bhomnick/django-nonrelated-inlines)
![PyPI](https://img.shields.io/pypi/v/django-nonrelated-inlines)

## Getting started

This app allows you to create admin inlines for models that don't have an
explicit foreign key relationship.

To use, subclass your inline from either `NonrelatedStackedInline` or 
`NonrelatedTabularInline` and add `get_form_queryset` and `save_new_instance`
methods.

* `get_form_queryset(self, obj)` returns all objects that should be shown in
  the inline formset.
* `save_new_instance(self, parent, instance)` given a parent object and a new
  child object instance should associate the child object with the parent.

For example, let's assume we have `Customer` and `Invoice` models. `Invoice`
objects are associated with a `Customer` if they share the same email address.

```python
from nonrelated_inlines.admin import NonrelatedStackedInline


class CustomerInvoiceStackedInline(NonrelatedStackedInline):
    model = Invoice
    fields = [
        'id',
        'amount'
    ]

    def get_form_queryset(self, obj):
        return self.model.objects.filter(email=obj.email)

    def save_new_instance(self, parent, instance):
        instance.email = parent.email
```

When viewing an `Customer` instance, we fetch a queryset of all `Invoice`
instances sharing the same email address. Similarly, when saving a new `Invoice`
instance we make sure to set its email attribute to the same value as its parent
`Customer`.
