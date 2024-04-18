from modeltranslation.translator import TranslationOptions, register

from . import models


@register(models.FrontendTranslation)
class FrontTranslationOptions(TranslationOptions):
    fields = ("text",)


@register(models.ConnectionType)
class ConnectionTypeTranslationOptions(TranslationOptions):
    fields = ("description",)


@register(models.Instruction)
class InstructionTranslationOptions(TranslationOptions):
    fields = ("text",)
