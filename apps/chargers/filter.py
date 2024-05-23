import os

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
        if not (self.lookup_val_from_date and self.lookup_val_to_date):
            return queryset

        from telegram import Bot, ParseMode
        from datetime import datetime
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('ERROR_LOG_CHANNEL_ID')

        Bot(token=token).send_message(
            chat_id=chat_id, parse_mode=ParseMode.HTML,
            text=f"{self.lookup_val_from_date} {self.lookup_val_to_date}"
        )

        from_date = datetime.strptime(self.lookup_val_from_date, "%Y-%m-%d")
        to_date = datetime.strptime(self.lookup_val_to_date, "%Y-%m-%d")

        from_date = from_date.replace(hour=0, minute=0, second=0, microsecond=0)
        to_date = to_date.replace(hour=23, minute=59, second=59)
        return queryset.filter(
            created_at__gte=from_date,
            created_at__lte=to_date
        )
