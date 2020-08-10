#! /usr/bin/env python
# -*- coding: utf-8 -*-

import jwt
import datetime
from jwt import exceptions

app_token = 'AT_ZnmHbwWYzrxjIEyQni4miU72dcLy43WW'
JWT_SALT = 'helloworld'


def create_token():


    # 构造header
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }

    # 构造payload
    payload = {
        'user_id': 1,
        'username': 'admin',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5)
    }
    result = jwt.encode(payload=payload, key=JWT_SALT, algorithm='HS256', headers=headers).decode('utf8')
    return result


def parse_payload(token):
    result = {'status': False, 'data': None, 'error': None}

    try:
        verified_payload = jwt.decode(token, JWT_SALT, True)
        result['status'] = True
        result['data'] = verified_payload
    except exceptions.ExpiredSignatureError:
        result['error'] = 'token已失效 '
    except jwt.DecodeError:
        result['error'] = 'token认证失败'
    except jwt.InvalidTokenError:
        result['error'] = '非法的token'
    return result

if __name__ == '__main__':
    token = create_token()
    print(token)
    print()

    print(parse_payload(token))

