from django.contrib import admin

from nonrelated_inlines.admin import NonrelatedStackedInline

from .models import Customer, Invoice


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


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['email', 'name']
    inlines = [
        CustomerInvoiceStackedInline
    ]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'amount']
