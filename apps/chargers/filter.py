from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class DateTimeRangeFilter(admin.filters.FieldListFilter):
    template = 'admin/date_time_range_filter.html'
    lookup_kwarg_from_date = 'created_at__date__gte'
    lookup_kwarg_to_date = 'created_at__date__lte'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.lookup_val_from_date = request.GET.get(self.lookup_kwarg_from_date, None)
        self.lookup_val_to_date = request.GET.get(self.lookup_kwarg_to_date, None)

    def expected_parameters(self):
        return [self.lookup_kwarg_from_date, self.lookup_kwarg_to_date]

    def choices(self, changelist):
        yield {
            'selected': self.lookup_val_from_date is None and self.lookup_val_to_date is None,
            'query_string': changelist.get_query_string(remove=[self.lookup_kwarg_from_date, self.lookup_val_to_date]),
            'display': _('All'),
        }

    def queryset(self, request, queryset):
        if self.lookup_val_from_date and self.lookup_val_to_date:
            return queryset.filter(
                created_at__date__gte=self.lookup_val_from_date,
                created_at__date__lte=self.lookup_val_to_date
            )
        return queryset
