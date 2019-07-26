"""
Customizations for the Django administration interface.
"""

from django.contrib import admin
from app.models import Choice, Poll, Invoice
from django.contrib.auth.models import Permission

class ChoiceInline(admin.TabularInline):
    """Choice objects can be edited inline in the Poll editor."""
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    """Definition of the Poll editor."""
    fieldsets = [
        (None, {'fields': ['text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('text', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['text']
    date_hierarchy = 'pub_date'

class InvoiceAdmin(admin.ModelAdmin):
    """Definition of Invoice editor."""
    fieldsets = [
        (None, {'fields': ['text']}),
        ('Invoice Date', {'fields' : ['date']}),
        ('Creation Date', {'fields' : ['date_creation']}),
        ('Invoice Image', {'fields' : ['invoice_capture']}),
    ]
    list_display = ('text','date')
    list_filter = ['date']
    search_fields = ['text']
    date_hierarchy = 'date'

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('content_type')

admin.site.register(Poll, PollAdmin) #makes this model appear in admin site for edition I guessç
admin.site.register(Invoice, InvoiceAdmin)
