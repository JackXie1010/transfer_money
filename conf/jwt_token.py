import jwt
import time
from conf.op_conf import get_conf


def gen_token(id, username):
    payload = {
        "exp": int(time.time()) + get_conf()['jwt_expire'],
        "id": id,
        "nick_name": username,
    }
    token = jwt.encode(payload, get_conf()['secret_key'], algorithm='HS256')
    return token.decode('utf-8')


def validate_token(token):
    try:
        payload = jwt.decode(
            token,
            get_conf()["secret_key"],
            leeway=get_conf()["jwt_expire"],
            options={"verify_exp": True}
        )
        if payload:
            return {'res': 1, 'msg': token, 'req_uid': payload['id'], 'user_name': payload['nick_name']}
        return {'res': 0, 'msg': token}
    except:
        return {'res': 0, 'msg': 'token超时或被篡改，请重新登陆'}


if __name__ == '__main__':
    token = gen_token(1, 'root')
    print(token)
    ret = validate_token(token)
    print(ret)