from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel, District, UserCar, ConnectorType


class Location(BaseModel):
    district = models.ForeignKey(to=District, on_delete=models.PROTECT, verbose_name=_("District"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    address = models.CharField(max_length=100, verbose_name=_("Address"))
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_("Longitude"))
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_("Latitude"))

    def __str__(self):
        return self.name


class ChargePoint(BaseModel):
    name = models.CharField(max_length=128, verbose_name=_("Name"))
    location = models.ForeignKey(to=Location, on_delete=models.PROTECT, verbose_name=_("Location"))
    charger_id = models.CharField(max_length=50, verbose_name=_("Charger ID"))
    last_boot_notification = models.DateTimeField(verbose_name=_("Last Boot Notification"), null=True, blank=True)
    last_heartbeat = models.DateTimeField(verbose_name="Last Heartbeat", null=True, blank=True)
    is_connected = models.BooleanField(default=False, verbose_name=_("is Connected"))  # auto
    is_visible_in_mobile = models.BooleanField(default=True)  # manual

    def __str__(self):
        return f"{self.name} - {self.charger_id}"


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

    charge_point = models.ForeignKey(ChargePoint, on_delete=models.PROTECT)
    name = models.CharField(max_length=40, null=True, verbose_name=_("Name"))

    connector_id = models.IntegerField(verbose_name=_("Connector Id within Charger"))
    standard = models.CharField(max_length=50, choices=ConnectorType.choices, verbose_name=_("Connector's standard"))
    max_voltage = models.IntegerField(default=0, verbose_name=_("Connector's Max Voltage"))
    max_amperage = models.IntegerField(default=0, verbose_name=_("Connector's Max Amperage"))
    max_electric_power = models.IntegerField(default=0, verbose_name=_("Connector's Max electric power"))
    status = models.CharField(_("Статус"), choices=Status.choices, max_length=50, default=Status.UNAVAILABLE)

    class Meta:
        unique_together = ("charge_point_id", "connector_id")
        verbose_name = _("Connector")
        verbose_name_plural = _("Connector")
        ordering = ["id"]

    def __str__(self):
        return f"{self.charge_point}: № {self.connector_id}"


class ChargingTransaction(BaseModel):
    class Status(models.TextChoices):
        IN_PROGRESS = "IN_PROGRESS", _("In Progress")
        FINISHED = "FINISHED", _("Finished")

    car = models.ForeignKey(to=UserCar, verbose_name=_("Car"), on_delete=models.PROTECT)
    connector = models.ForeignKey(to=Connector, verbose_name=_("Connector"), on_delete=models.PROTECT)
    start_time = models.DateTimeField(verbose_name=_("Start Time"))
    end_time = models.DateTimeField(verbose_name=_("End Time"))
    status = models.CharField(verbose_name=_("Status"), max_length=30, choices=Status.choices,
                              default=Status.IN_PROGRESS)
    battery_percent_on_start = models.IntegerField(verbose_name=_("Battery Percent on Start"), default=0)
    battery_percent = models.IntegerField(verbose_name=_("Battery Percent"), default=0)

    meter_on_start = models.IntegerField(verbose_name=_("Meter On Start"))
    current_meter = models.IntegerField(verbose_name=_("Current Meter"), default=0)
    meter_on_end = models.IntegerField(verbose_name=_("Meter on End"), null=True, blank=True)
