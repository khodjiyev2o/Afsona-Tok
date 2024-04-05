from django.db import models
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

    # FK
    location = models.ForeignKey(to=Location, on_delete=models.PROTECT, verbose_name=_("Location"))

    def __str__(self):
        return f"{self.name} - {self.charger_id}"

    class Meta:
        verbose_name = _("ChargePoint")
        verbose_name_plural = _("ChargePoints")
        ordering = ["-id"]


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

    name = models.CharField(max_length=40, null=True, verbose_name=_("Name"))
    connector_id = models.IntegerField(verbose_name=_("Connector Id within Charger"))
    standard = models.ForeignKey(ConnectionType, verbose_name=_("Connector's standard"), on_delete=models.PROTECT)
    status = models.CharField(_("Статус"), choices=Status.choices, max_length=50, default=Status.UNAVAILABLE)

    # FK
    charge_point = models.ForeignKey(ChargePoint, on_delete=models.PROTECT)

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
        LOCAL = "LOCAL", _("Local")
        REMOTE = "REMOTE", _("Remote")
        OTHER = "OTHER", _("Other")

    class StartReason(models.TextChoices):
        LOCAL = "LOCAL", _("Local")
        REMOTE = "REMOTE", _("Remote")

    user = models.ForeignKey("users.User", verbose_name=_("User"), on_delete=models.PROTECT)
    user_car = models.ForeignKey("common.UserCar", verbose_name=_("User Car"), null=True, blank=True,
                                 on_delete=models.SET_NULL)
    connector = models.ForeignKey(to=Connector, verbose_name=_("Connector"), on_delete=models.PROTECT)
    end_time = models.DateTimeField(verbose_name=_("End Time"), null=True, blank=True)
    battery_percent_on_start = models.IntegerField(verbose_name=_("Battery Percent on Start"), default=0)
    battery_percent_on_end = models.IntegerField(verbose_name=_("Battery Percent on End"), null=True, blank=True)
    meter_on_start = models.IntegerField(verbose_name=_("Meter On Start"))
    meter_on_end = models.IntegerField(verbose_name=_("Meter on End"), null=True, blank=True)
    meter_used = models.IntegerField(verbose_name=_("Meter Used"), default=0)
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

    class Meta:
        verbose_name = _("ChargingTransaction")
        verbose_name_plural = _("ChargingTransactions")
        ordering = ["-id"]

    def __str__(self):
        return f"{self.id}: {self.user} - {self.total_price}"


class ChargeCommand(BaseModel):
    class Commands(models.TextChoices):
        REMOTE_START_TRANSACTION = "REMOTE_START_TRANSACTION", _("Remote start transaction")
        REMOTE_STOP_TRANSACTION = "REMOTE_STOP_TRANSACTION", _("Remote start transaction")

    user_car = models.ForeignKey("common.UserCar", verbose_name=_("User Car"), null=True, blank=True,
                                 on_delete=models.SET_NULL)
    user = models.ForeignKey("users.User", verbose_name=_("User"), on_delete=models.PROTECT)
    command = models.CharField(max_length=50, verbose_name=_("Command"), choices=Commands.choices)
    id_tag = models.CharField(max_length=20, verbose_name=_("Unique Id tag of command"))  # should be unique

    is_delivered = models.BooleanField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    status = models.BooleanField(null=True, blank=True)
    done_at = models.DateTimeField(null=True, blank=True)
