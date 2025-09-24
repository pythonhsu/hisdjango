#解決修改資料(update),staus 為 none 的問題，方法三：
def session_user(request):
    return {
        'status':request.session.get('is_login'),
        'uname':request.session.get('uname'),
        'email':request.session.get('email'),
    }