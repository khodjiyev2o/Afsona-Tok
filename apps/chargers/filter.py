from datetime import datetime

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
            'query_string': '',
            'display': _('All'),
        }

    def queryset(self, request, queryset):
        lookup_val_from_date = request.GET.get(self.lookup_kwarg_from_date, None)
        lookup_val_to_date = request.GET.get(self.lookup_kwarg_to_date, None)

        if not (lookup_val_from_date and lookup_val_to_date):
            return queryset

        from_date = datetime.strptime(lookup_val_from_date, "%Y-%m-%d")
        to_date = datetime.strptime(lookup_val_to_date, "%Y-%m-%d")

        from_date = from_date.replace(hour=0, minute=0, second=0)
        to_date = to_date.replace(hour=23, minute=59, second=59)
        return queryset.filter(
            created_at__gte=from_date,
            created_at__lte=to_date
        )
