from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.models import BaseModel
from apps.users.managers import UserManager


class User(AbstractUser, BaseModel):

    class UserLanguages(models.TextChoices):
        ENGLISH = "en", _("English")
        RUSSIAN = "ru", _("Russian")
        UZBEK = "uz", _("Uzbek")

    first_name = None
    last_name = None
    username = None
    full_name = models.CharField(_("Full Name"), max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(_("Date of Birth"), blank=True, null=True)
    phone = PhoneNumberField(_("Phone number"), max_length=255, unique=True)
    photo = models.ImageField(_("Photo"), upload_to="users/%Y/%m", blank=True, null=True)
    balance = models.DecimalField(_("Balance"), max_digits=10, decimal_places=2, default=0)
    language = models.CharField(_("Language"), max_length=255, choices=UserLanguages.choices,
                                default=UserLanguages.RUSSIAN)
    objects = UserManager()
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []  # type: ignore

    def __str__(self):
        return str(self.phone)

    @property
    def tokens(self):
        token = RefreshToken.for_user(self)
        return {"access": str(token.access_token), "refresh": str(token)}

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
