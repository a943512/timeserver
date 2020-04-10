# 后端登录认证

from rest_framework import exceptions
from app01 import models
from rest_framework.authentication import BaseAuthentication


class TokenAuth(BaseAuthentication):
    def authenticate(self, request):
        # 取到 request里面的 token值
        totken = request.GET.get('token')
        token_obj = models.UserAuthToken.objects.filter(token=totken).first()
        if not token_obj:
            # 抛认证字段的异常
            raise exceptions.AuthenticationFailed("验证失败")
        else:
            return token_obj.user.user, token_obj.token