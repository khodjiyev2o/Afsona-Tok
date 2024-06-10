from django.views.generic import TemplateView


class AppRedirectAPIView(TemplateView):
    template_name = "deeplink.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["play_market_link"] = "https://play.google.com/store/apps/details?id=com.afsona_tok"
        context["apple_store_link"] = "https://apps.apple.com/uz/app/afsona-tok/id6502282213"
        context["app_link"] = "https://app.transitgroup.uz/{}/{}".format(
            self.kwargs["content"], self.kwargs["content_id"]
        )
        return context


__all__ = ['AppRedirectAPIView']
