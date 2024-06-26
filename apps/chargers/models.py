import time

import requests
import sentry_sdk
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel, District, ConnectionType


class Location(BaseModel):
    district = models.ForeignKey(to=District, on_delete=models.PROTECT, verbose_name=_("District"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    address = models.CharField(max_length=100, verbose_name=_("Address"))
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_("Longitude"))
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_("Latitude"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        ordering = ["-id"]


class UserFavouriteLocation(BaseModel):
    user = models.ForeignKey("users.User", verbose_name=_("User"), on_delete=models.CASCADE)
    location = models.ForeignKey(Location, verbose_name=_("Location"), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"


class ChargePoint(BaseModel):
    name = models.CharField(max_length=128, verbose_name=_("Name"))
    charger_id = models.CharField(max_length=50, verbose_name=_("Charger ID"))
    last_boot_notification = models.DateTimeField(verbose_name=_("Last Boot Notification"), null=True, blank=True)
    last_heartbeat = models.DateTimeField(verbose_name="Last Heartbeat", null=True, blank=True)
    is_connected = models.BooleanField(default=False, verbose_name=_("is Connected"))
    is_visible_in_mobile = models.BooleanField(default=True)
    max_electric_power = models.IntegerField(default=0, verbose_name=_("ChargePoint's Max electric power"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))
    price_per_kwh = models.DecimalField(
        verbose_name=_('Price for 1 kwt of electricity'), max_digits=10, decimal_places=2, default=2500
    )

    # FK
    location = models.ForeignKey(to=Location, on_delete=models.PROTECT, verbose_name=_("Location"),
                                 related_name="chargers")

    def __str__(self):
        return f"{self.name} - {self.charger_id}"

    class Meta:
        verbose_name = _("Charge Point")
        verbose_name_plural = _("Charge Points")
        ordering = ["order"]


class Connector(BaseModel):
    class Status(models.TextChoices):
        AVAILABLE = "Available"
        PREPARING = "Preparing"
        CHARGING = "Charging"
        SUSPENDED_EVSE = "SuspendedEVSE"
        SUSPENDED_EV = "SuspendedEV"
        FINISHING = "Finishing"
        RESERVED = "Reserved"
        UNAVAILABLE = "Unavailable"
        FAULTED = "Faulted"

    class LastStatusReason(models.TextChoices):
        NORMAL = "normal", _("Normal")
        CHARGER_DISCONNECTED = "charger_disconnected", _("Charge Disconnected")
        MANUAL = "manual", _("Manual")

    name = models.CharField(max_length=40, null=True, verbose_name=_("Name"))
    connector_id = models.IntegerField(verbose_name=_("Connector Id within Charger"))
    standard = models.ForeignKey(ConnectionType, verbose_name=_("Connector's standard"), on_delete=models.PROTECT)
    status = models.CharField(_("Status"), choices=Status.choices, max_length=50, default=Status.UNAVAILABLE)
    last_status_reason = models.CharField(
        max_length=30, choices=LastStatusReason.choices, default=LastStatusReason.NORMAL,
        db_default=LastStatusReason.NORMAL, verbose_name=_("Last status reason")
    )

    # FK
    charge_point = models.ForeignKey(ChargePoint, on_delete=models.PROTECT, related_name='connectors',
                                     verbose_name=_("Charge Point"))

    class Meta:
        unique_together = ("charge_point", "connector_id")
        verbose_name = _("Connector")
        verbose_name_plural = _("Connectors")
        ordering = ["-id"]

    def __str__(self):
        return f"{self.charge_point}: № {self.name} - {self.connector_id}"


class ChargingTransaction(BaseModel):
    class Status(models.TextChoices):
        IN_PROGRESS = "IN_PROGRESS", _("In Progress")
        FINISHED = "FINISHED", _("Finished")

    class StopReason(models.TextChoices):
        LOCAL = "Local", _("Local")
        REMOTE = "Remote", _("Remote")
        CONNECTOR_ERROR = "ConnectorError", _("Connector Error")
        OTHER = "Other", _("Other")

    class StartReason(models.TextChoices):
        LOCAL = "Local", _("Local")
        REMOTE = "Remote", _("Remote")

    user = models.ForeignKey("users.User", verbose_name=_("User"), on_delete=models.SET_NULL, null=True, blank=True)
    user_car = models.ForeignKey("common.UserCar", verbose_name=_("User Car"), null=True, blank=True,
                                 on_delete=models.SET_NULL)
    connector = models.ForeignKey(to=Connector, verbose_name=_("Connector"), on_delete=models.PROTECT)
    end_time = models.DateTimeField(verbose_name=_("End Time"), null=True, blank=True)
    battery_percent_on_start = models.IntegerField(verbose_name=_("Battery Percent on Start"), default=0, db_default=0)
    battery_percent_on_end = models.IntegerField(verbose_name=_("Battery Percent on End"), default=0, db_default=0)
    meter_on_start = models.IntegerField(verbose_name=_("Meter On Start"))
    meter_on_end = models.IntegerField(verbose_name=_("Meter on End"), null=True, blank=True)
    meter_used = models.FloatField(verbose_name=_("Meter Used"), default=0)
    total_price = models.DecimalField(verbose_name=_("Total Price"), null=True, blank=True, decimal_places=2,
                                      max_digits=10)
    status = models.CharField(verbose_name=_("Status"), max_length=30, choices=Status.choices,
                              default=Status.IN_PROGRESS)
    start_reason = models.CharField(
        max_length=40, verbose_name=_("Start Reason"), choices=StartReason.choices, null=True, blank=True
    )
    stop_reason = models.CharField(
        max_length=40, verbose_name=_("Stop Reason"), choices=StopReason.choices, null=True, blank=True
    )
    is_limited = models.BooleanField(default=False, verbose_name=_("Is Limited"))
    limited_money = models.DecimalField(verbose_name=_("Limited money"), null=True, blank=True, decimal_places=2,
                                        max_digits=10)

    start_command = models.ForeignKey(
        "ChargeCommand", on_delete=models.PROTECT, related_name='start_command_transaction',
        verbose_name=_("Start Command"), null=True, blank=True
    )
    price_per_kwh = models.DecimalField(
        verbose_name=_('Price for 1 kwt of electricity'), max_digits=10, decimal_places=2, default=2500
    )

    class Meta:
        verbose_name = _("ChargingTransaction")
        verbose_name_plural = _("ChargingTransactions")
        ordering = ["-id"]

    @property
    def consumed_kwh(self) -> float:
        end = self.meter_on_end if self.meter_on_end else 0
        return round((end - self.meter_on_start) / 1000, 2)

    @property
    def duration_in_minute(self) -> int:
        end_time = self.end_time or timezone.now()
        minute: int = int((end_time - self.created_at).total_seconds() // 60)
        return minute

    def __str__(self):
        return f"{self.id}: {self.user} - {self.total_price}"


class ChargeCommand(BaseModel):
    class Commands(models.TextChoices):
        REMOTE_START_TRANSACTION = "REMOTE_START_TRANSACTION", _("Remote start transaction")
        REMOTE_STOP_TRANSACTION = "REMOTE_STOP_TRANSACTION", _("Remote stop transaction")

    class Initiator(models.TextChoices):
        USER = "USER", _("User")
        SYSTEM = "SYSTEM", _("System")

    initiator = models.CharField(
        max_length=50, choices=Initiator, db_default=Initiator.USER,
        verbose_name=_("Initiator"), editable=False
    )

    user_car = models.ForeignKey("common.UserCar", verbose_name=_("User Car"), null=True, blank=True,
                                 on_delete=models.SET_NULL)
    connector = models.ForeignKey(to=Connector, on_delete=models.PROTECT, verbose_name=_("Connector"))
    user = models.ForeignKey("users.User", verbose_name=_("User"), on_delete=models.PROTECT)
    command = models.CharField(max_length=50, verbose_name=_("Command"), choices=Commands.choices)
    id_tag = models.CharField(max_length=20, verbose_name=_("Unique Id tag of command"))  # should be unique

    is_delivered = models.BooleanField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    status = models.BooleanField(null=True, blank=True)
    done_at = models.DateTimeField(null=True, blank=True)

    is_limited = models.BooleanField(db_default=False)
    limited_money = models.DecimalField(verbose_name=_("Limited money"), null=True, blank=True, decimal_places=2,
                                        max_digits=10)

    def send_command_start_to_ocpp_service(self) -> bool:
        payload = {
            "id_tag": self.id_tag,
            "charger_identify": self.connector.charge_point.charger_id,
            "connector_id": self.connector.connector_id
        }

        try:
            response = requests.post(url=settings.OCPP_SERVER_START_URL, json=payload, timeout=3)
            is_delivered: bool = response.json().get('status')

            OCPPServiceRequestResponseLogs.objects.create(
                charger_id=payload.get("charger_identify"),
                request_action="RemoteStartTransaction",
                request_body=str(payload),
                response_body=str(response.json())
            )
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return False

        return is_delivered

    def send_command_stop_to_ocpp_service(self, transaction_id: int, retry=3, timeout=3) -> bool:
        retry_delay = 1

        for _ in range(retry):
            try:
                payload = {
                    "transaction_id": transaction_id,
                    "charger_identify": self.connector.charge_point.charger_id,
                    "id_tag": self.id_tag
                }
                response = requests.post(url=settings.OCPP_SERVER_STOP_URL, json=payload, timeout=timeout)
                is_delivered: bool = response.json().get('status')

                OCPPServiceRequestResponseLogs.objects.create(
                    charger_id=payload.get("charger_identify"),
                    request_action="RemoteStopTransaction",
                    request_body=str(payload),
                    response_body=str(response.json())
                )
            except Exception as e:
                sentry_sdk.capture_exception(e)
                time.sleep(retry_delay)
                continue

            if is_delivered: return True  # noqa
            time.sleep(retry_delay)
        return False


class OCPPServiceRequestResponseLogs(BaseModel):
    charger_id = models.CharField(max_length=50, verbose_name=_("Charger ID"))
    request_action = models.CharField(max_length=50, verbose_name=_("Request Action"))
    request_body = models.TextField(verbose_name=_("Request"), null=True, blank=True)
    response_body = models.TextField(verbose_name=_("Response"), null=True, blank=True)

    class Meta:
        verbose_name = _("OCPP Service Request Response Log")
        verbose_name_plural = _("OCPP Service Request Response Logs")
        ordering = ["-id"]

    def __str__(self):
        return f"{self.id}"
