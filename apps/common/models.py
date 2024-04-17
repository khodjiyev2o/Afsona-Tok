from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


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


class ConnectionType(BaseModel):
    class AC_DC_TYPE_Choice(models.TextChoices):
        AC = "AC", _("AC")
        DC = "DC", _("DC")

    name = models.CharField(max_length=255, verbose_name=_("Name"))
    _type = models.CharField(max_length=255, verbose_name=_("Type"), choices=AC_DC_TYPE_Choice.choices)
    icon = models.ImageField(_("Icon"), upload_to="icons/%Y/%m")
    max_voltage = models.IntegerField(verbose_name=_("Max Voltage"))
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class UserCar(BaseModel):
    class STATE_NUMBER_TYPES(models.TextChoices):
        INDIVIDUAL = 'INDIVIDUAL', _('INDIVIDUAL')  # физическое лицо
        LEGAL = 'LEGAL', _('LEGAL')  # юридическое лицо
        DIPLOMATIC = 'DIPLOMATIC', _('DIPLOMATIC')  # Дипломатический
        OON = 'OON', _('OON')  # Организация Объединённых Наций
        InternationalResident = 'InternationalResident', _('InternationalResident')  # Международные резиденты
        InternationalOrganization = 'InternationalOrganization', _(
            'InternationalOrganization')  # Международные организации

    vin = models.CharField(_("VIN"), max_length=100, null=True, blank=True)
    state_number = models.CharField(_("Гос.номер"), max_length=100, null=True, blank=True)
    state_number_type = models.CharField(_("Type of State Number"), choices=STATE_NUMBER_TYPES.choices, null=True,
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
    connector_type = models.ManyToManyField(
        to=ConnectionType, blank=True, verbose_name=_("Connector Types"), related_name="car_connector_types"
    )
    user = models.ForeignKey("users.User", verbose_name=_("User"), related_name="cars", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}-{self.manufacturer.name}-{self.model.name}"

    class Meta:
        verbose_name = _("User Car")
        verbose_name_plural = _("User Cars")
        unique_together = ['user', 'vin']


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
    country = models.ForeignKey(Country, verbose_name=_("Country"), on_delete=models.PROTECT, related_name="regions")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")


class District(BaseModel):
    name = models.CharField(_("Name"), max_length=50)
    region = models.ForeignKey(to=Region, verbose_name=_("Region"), on_delete=models.PROTECT, related_name="districts")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = _("District")
        verbose_name_plural = _("Districts")


class Support(BaseModel):
    telegram_link = models.CharField(max_length=255, verbose_name=_("Telegram Link"))
    phone_number = PhoneNumberField(_("Phone number"), max_length=255)
    email = models.EmailField(verbose_name=_("Email"))

    class Meta:
        verbose_name = _("Support")
        verbose_name_plural = _("Support")


class MainSettings(BaseModel):
    price = models.DecimalField(_('Price for 1 kwt of electricity'), max_digits=10, decimal_places=2)
    user_minimum_balance = models.DecimalField(_('Price for 1 kwt of electricity'), max_digits=10, decimal_places=2)
    ios_version = models.CharField(max_length=20)
    android_version = models.CharField(max_length=20)

    class Meta:
        verbose_name = _("MainSettings")
        verbose_name_plural = _("MainSettings")
