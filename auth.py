from rest_framework.authentication import BaseAuthentication
import jwt
from jwt import exceptions
from rest_framework.exceptions import AuthenticationFailed


class jwtauthen(BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            _, token = authorization_header.split(' ')
            salt = 'asdfghjkl123qwe'
            try:
                payload = jwt.decode(token, salt, algorithms=['HS256'])
                return payload, token
            except exceptions.ExpiredSignatureError:
                raise AuthenticationFailed({'code': 400, 'error': "token已超时"})
            except jwt.DecodeError:
                raise AuthenticationFailed({'code': 400, 'error': "token认证失败"})
            except jwt.InvalidTokenError:
                raise AuthenticationFailed({'code': 400, 'error': "非法的token"})
