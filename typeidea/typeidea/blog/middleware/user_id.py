import uuid

USER_KEY = "uid"
TEN_YEARS = 60 * 60 * 24 * 365 * 10

class UserIDMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        uid = self.generate_uid(request)
        request.uid = uid
        response = self.get_response(request)
        # httponly 只能在服务端才能访问
        response.set_cookie(USER_KEY,uid,max_age=TEN_YEARS,httponly=True)
        return response

    def generate_uid(self,request):
        try:
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            # 生成唯一id
            uid = uuid.uuid4().hex
        return uid
