from channels.auth import BaseMiddleware

from typing import Union
import os
import sentry_sdk
import jwt


class WebsocketJWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, *args, **kwargs):

        user = await self.authenticate(scope=args[0])
        if user is not None:
            args[0]['user'] = user
        return await super().__call__(*args, **kwargs)

    async def authenticate(self, scope):
        from django.contrib.auth.models import AnonymousUser

        raw_token = await self.__get_raw_token(scope)

        if raw_token is None:
            return AnonymousUser()

        validated_token = await self.__claim_raw_token(raw_token)

        if validated_token is None:
            return AnonymousUser()

        return await self.__get_user(validated_token)

    async def __get_user(self, validated_token):
        from django.contrib.auth import get_user_model
        user = await get_user_model().objects.aget(pk=validated_token['user_id'])
        return user

    async def __claim_raw_token(self, token) -> Union[dict | None]:
        from django.conf import settings
        try:
            return jwt.decode(
                token,
                os.getenv('SECRET_KEY'),
                algorithms=settings.SIMPLE_JWT['ALGORITHM'],
                verify=True
            )
        except jwt.PyJWTError as ex:
            sentry_sdk.capture_exception(ex)
            return None

    async def __get_raw_token(self, scope) -> Union[str | None]:
        query_params = scope.get('query_string').decode('utf-8')

        parts = query_params.split('=')
        if len(parts) != 2:
            return None

        if parts[1] is None and parts[0] != 'token':
            return None
        return parts[1]
