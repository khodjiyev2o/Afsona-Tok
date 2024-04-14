import os

from sentry_sdk.types import Event, Hint
from telegram import Bot, ParseMode


def before_send_trigger(event: Event, hint: Hint):
    result_text = ""

    for exception_values in event.get("exception", {}).get("values", []):
        result_text += f"{exception_values.get('type')} - {exception_values.get('value')}\n\n"

        for frame in exception_values.get("stacktrace", {}).get("frames", []):
            if frame.get('in_app') is True:
                result_text += f"<code> {frame.get('filename')}:{frame.get('lineno')} </code>\n"
                result_text += "<pre lang='python'>\n"
                for line in frame.get("pre_context", []): result_text += line + "\n" # noqa
                result_text += f"🔥{frame.get('context_line')}🔥\n"
                for line in frame.get("post_context", []): result_text += line + "\n" # noqa
                result_text += "</pre>\n"
    if result_text:
        Bot(token=os.getenv("TELEGRAM_BOT_TOKEN")).send_message(
            chat_id=os.getenv("ERROR_LOG_CHANNEL_ID"), text=result_text, parse_mode=ParseMode.HTML
        )

    return event

