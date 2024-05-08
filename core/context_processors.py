from django.db.models import Sum, Q
from django.db.models.fields import DecimalField
from django.db.models.functions import Coalesce

from apps.payment.models import Transaction as PaymentTransaction
from apps.chargers.models import ChargingTransaction
from django.utils import timezone


def dashboard(request):
    charge_today = ChargingTransaction.objects.aggregate(
        today_total_price=Coalesce(
            Sum('total_price', filter=Q(created_at__date=timezone.now().date())),
            0, output_field=DecimalField()
        ),
        week_total_price=Coalesce(
            Sum('total_price', filter=Q(created_at__week=timezone.now().isocalendar()[1])),
            0, output_field=DecimalField()
        ),
        month_total_price=Coalesce(
            Sum('total_price', filter=Q(created_at__month=timezone.now().month)),
            0, output_field=DecimalField()
        ),

        today_meter_used=Coalesce(
            Sum('meter_used', filter=Q(created_at__date=timezone.now().date())),
            0, output_field=DecimalField()
        ),
        week_meter_used=Coalesce(
            Sum('meter_used', filter=Q(created_at__week=timezone.now().isocalendar()[1])),
            0, output_field=DecimalField()
        ),
        month_meter_used=Coalesce(
            Sum('meter_used', filter=Q(created_at__month=timezone.now().month)),
            0, output_field=DecimalField()
        ),

        today_cash=Coalesce(
            Sum('total_price', filter=Q(created_at__date=timezone.now().date(), user__isnull=True)),
            0, output_field=DecimalField()
        ),
        today_mobile=Coalesce(
            Sum('total_price', filter=Q(created_at__date=timezone.now().date(), user__isnull=False)),
            0, output_field=DecimalField()
        ),
        week_cash=Coalesce(
            Sum('total_price', filter=Q(created_at__week=timezone.now().isocalendar()[1], user__isnull=True)),
            0, output_field=DecimalField()
        ),
        week_mobile=Coalesce(
            Sum('total_price', filter=Q(created_at__week=timezone.now().isocalendar()[1], user__isnull=False)),
            0, output_field=DecimalField()
        ),
        month_cash=Coalesce(
            Sum('total_price', filter=Q(created_at__month=timezone.now().month, user__isnull=True)),
            0, output_field=DecimalField()
        ),
        month_mobile=Coalesce(
            Sum('total_price', filter=Q(created_at__month=timezone.now().month, user__isnull=False)),
            0, output_field=DecimalField()
        ),
    )

    payment = PaymentTransaction.objects.aggregate(
        today_total_price=Coalesce(
            Sum('amount', filter=Q(created_at__date=timezone.now().date())),
            0, output_field=DecimalField()
        ),
        week_total_price=Coalesce(
            Sum('amount', filter=Q(created_at__week=timezone.now().isocalendar()[1])),
            0, output_field=DecimalField()
        ),
        month_total_price=Coalesce(
            Sum('amount', filter=Q(created_at__month=timezone.now().month)),
            0, output_field=DecimalField()
        ),
    )

    return {
        "total_sale": {
            'today': {
                "sum": charge_today['today_total_price'],
                'kwh': charge_today['today_meter_used']
            },
            'week': {
                "sum": charge_today['week_total_price'],
                'kwh': charge_today['week_meter_used']
            },
            'month': {
                "sum": charge_today['month_total_price'],
                'kwh': charge_today['month_meter_used']
            }
        },
        "deposit_topup": {
            'today': payment['today_total_price'],
            'week': payment['week_total_price'],
            'month': payment['month_total_price']
        },

        "total_sale_percent": {
            'today': {
                'cash': charge_today['today_cash'],
                'mobile': charge_today['today_mobile'],
            },
            'week': {
                'cash': charge_today['week_cash'],
                'mobile': charge_today['week_mobile'],
            },
            'month': {
                'cash': charge_today['month_cash'],
                'mobile': charge_today['month_mobile'],
            }
        }
    }
