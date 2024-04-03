from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        abstract = True


class FrontendTranslation(BaseModel):
    key = models.CharField(_("Key"), max_length=255, unique=True)
    text = models.CharField(_("Text"), max_length=1024)

    class Meta:
        verbose_name = _("Frontend translation")
        verbose_name_plural = _("Frontend translations")

    def __str__(self):
        return str(self.key)


class Manufacturer(BaseModel):
    name = models.CharField(_("Name"), max_length=30)
    icon = models.ImageField(_("Icon"), upload_to='manufacturer/', null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Manufacturer")
        verbose_name_plural = _("Manufacturers")


class CarModel(BaseModel):
    name = models.CharField(_("Name"), max_length=100)
    manufacturer = models.ForeignKey(
        Manufacturer,
        verbose_name=_("Manufacturer"),
        related_name="car_models",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Car model")
        verbose_name_plural = _("Car models")

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


class UserCar(BaseModel):
    class STATE_NUMBER_TYPES(models.TextChoices):
        INDIVIDUAL = 'INDIVIDUAL', _('INDIVIDUAL')  # физическое лицо
        LEGAL = 'LEGAL', _('LEGAL')  # юридическое лицо

    vin = models.CharField(_("VIN"), max_length=100, null=True, blank=True)
    state_number = models.CharField(_("Гос.номер"), max_length=100, null=True, blank=True)
    state_number_type = models.IntegerField(_("Type of State Number"), choices=STATE_NUMBER_TYPES.choices, null=True,
                                            blank=True)
    manufacturer = models.ForeignKey(
        Manufacturer,
        verbose_name=_("Manufacturer"),
        related_name="cars",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    model = models.ForeignKey(CarModel, related_name="cars", on_delete=models.CASCADE, null=True, blank=True)
    ## charging_type = models.ManyToManyField(TypeConnection, verbose_name=_("Type Connection"), related_name="cars")
    user = models.ForeignKey("users.User", verbose_name=_("User"), related_name="cars", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}-{self.manufacturer.name}-{self.model.name}"

    class Meta:
        verbose_name = _("User Car")
        verbose_name_plural = _("User Cars")

class Country(BaseModel):
    ico_code = models.CharField(max_length=10, verbose_name=_("ISO code"))
    name = models.CharField(max_length=30, verbose_name=_(_("Name")))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")


class Region(BaseModel):
    name = models.CharField(_("Name"), max_length=255)
    country = models.ForeignKey(Country, verbose_name=_("Country"), on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")


class District(BaseModel):
    name = models.CharField(_("Name"), max_length=50)
    region = models.ForeignKey(to=Region, verbose_name=_("Region"), on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = _("District")
        verbose_name_plural = _("Districts")
