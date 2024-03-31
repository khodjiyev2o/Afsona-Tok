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

