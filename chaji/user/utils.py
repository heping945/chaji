def jwt_response_payload_handler(token, user=None, request=None):
    '''
    定制jwt返回实例
    :param token:
    :param user:
    :param request:
    :return:
    '''
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username,
        'avatar':user.avatar.url,
        'urltoken':user.urltoken,
    }

