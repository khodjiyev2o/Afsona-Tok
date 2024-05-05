from django.views.generic import TemplateView


class AppRedirectAPIView(TemplateView):
    template_name = "deeplink.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["play_market_link"] = "https://play.google.com/store/apps/details?id=co.khalikov.stoploss"
        context["apple_store_link"] = "https://apps.apple.com/uz/app/stoploss-az-capital/id6450660735"
        context["app_link"] = "stoploss://stoploss.khalikov.co/{}/{}".format(
            self.kwargs["content"], self.kwargs["content_id"]
        )
        print(context["app_link"])
        return context

__all__ = ['AppRedirectAPIView']
