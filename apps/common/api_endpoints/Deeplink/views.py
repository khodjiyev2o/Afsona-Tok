from django.views.generic import TemplateView
from django_user_agents.utils import get_user_agent
from user_agents.parsers import UserAgent

from django.shortcuts import redirect


class AppRedirectAPIView(TemplateView):
    template_name = "deeplink.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        django_user_agent: UserAgent = get_user_agent(request)

        if django_user_agent.os.family == 'iOS':
            return redirect(to=context['apple_store_link'])
        elif django_user_agent.os.family == 'Android':
            return redirect(to=context['apple_store_link'])

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["play_market_link"] = "https://play.google.com/store/apps/details?id=com.afsona_tok"
        context["apple_store_link"] = "https://apps.apple.com/uz/app/afsona-tok/id6502282213"
        context["app_link"] = "app://app.transitgroup.uz/{}/{}".format(
            self.kwargs["content"], self.kwargs["content_id"]
        )
        return context


__all__ = ['AppRedirectAPIView']
