from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel, District, UserCar


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
    class ConnectorType(models.TextChoices):
        CHADEMO = 'CHADEMO'
        CHAOJI = 'CHAOJI'
        DOMESTIC_A = 'DOMESTIC_A'
        DOMESTIC_B = 'DOMESTIC_B'
        DOMESTIC_C = 'DOMESTIC_C'
        DOMESTIC_D = 'DOMESTIC_D'
        DOMESTIC_E = 'DOMESTIC_E'
        DOMESTIC_F = 'DOMESTIC_F'
        DOMESTIC_G = 'DOMESTIC_G'
        DOMESTIC_H = 'DOMESTIC_H'
        DOMESTIC_I = 'DOMESTIC_I'
        DOMESTIC_J = 'DOMESTIC_J'
        DOMESTIC_K = 'DOMESTIC_K'
        DOMESTIC_L = 'DOMESTIC_L'
        DOMESTIC_M = 'DOMESTIC_M'
        DOMESTIC_N = 'DOMESTIC_N'
        DOMESTIC_O = 'DOMESTIC_O'
        GBT_AC = 'GBT_AC'
        GBT_DC = 'GBT_DC'
        IEC_60309_2_SINGLE_16 = 'IEC_60309_2_single_16'
        IEC_60309_2_THREE_16 = 'IEC_60309_2_three_16'
        IEC_60309_2_THREE_32 = 'IEC_60309_2_three_32'
        IEC_60309_2_THREE_64 = 'IEC_60309_2_three_64'
        IEC_62196_T1 = 'IEC_62196_T1'
        IEC_62196_T1_COMBO = 'IEC_62196_T1_COMBO'
        IEC_62196_T2 = 'IEC_62196_T2'
        IEC_62196_T2_COMBO = 'IEC_62196_T2_COMBO'
        IEC_62196_T3A = 'IEC_62196_T3A'
        IEC_62196_T3C = 'IEC_62196_T3C'
        NEMA_5_20 = 'NEMA_5_20'
        NEMA_6_30 = 'NEMA_6_30'
        NEMA_6_50 = 'NEMA_6_50'
        NEMA_10_30 = 'NEMA_10_30'
        NEMA_10_50 = 'NEMA_10_50'
        NEMA_14_30 = 'NEMA_14_30'
        NEMA_14_50 = 'NEMA_14_50'
        PANTOGRAPH_BOTTOM_UP = 'PANTOGRAPH_BOTTOM_UP'
        PANTOGRAPH_TOP_DOWN = 'PANTOGRAPH_TOP_DOWN'
        TESLA_R = 'TESLA_R'
        TESLA_S = 'TESLA_S'

    class ConnectorFormat(models.TextChoices):
        SOCKET = 'SOCKET'
        CABLE = 'CABLE'

    class PowerType(models.TextChoices):
        AC_1_PHASE = 'AC_1_PHASE'  # 'AC single phase.'
        AC_2_PHASE = 'AC_2_PHASE'  # 'AC two phases, only two of the three available phases connected.'
        AC_2_PHASE_SPLIT = 'AC_2_PHASE_SPLIT'  # '3 AC two phases using split phase system.'
        AC_3_PHASE = 'AC_3_PHASE'  # 'AC three phases.'
        DC = 'DC'  # 'Direct Current.'

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

    connector_id = models.IntegerField(verbose_name=_("Connector Id within EVS"))
    standard = models.CharField(max_length=50, choices=ConnectorType.choices, verbose_name=_("Connector's standard"))
    format = models.CharField(max_length=50, choices=ConnectorFormat.choices, verbose_name=_("Connector's format"))
    power_type = models.CharField(max_length=50, choices=PowerType.choices, verbose_name=_("Connector's power type"))
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
