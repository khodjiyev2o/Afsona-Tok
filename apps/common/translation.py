from modeltranslation.translator import TranslationOptions, register

from . import models


@register(models.FrontendTranslation)
class FrontTranslationOptions(TranslationOptions):
    fields = ("text",)


@register(models.ConnectionType)
class ConnectionTypeTranslationOptions(TranslationOptions):
    fields = ("description",)


@register(models.AppealTypeList)
class AppealTypeListTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(models.StaticPage)
class StaticPageTranslationOptions(TranslationOptions):
    fields = ("title", "content")
