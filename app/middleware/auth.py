from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 排除不需要登录就能访问的界面
        if request.path_info in ['/sign-in/', '/sign-up/', '/code/']:
            return

        # 读取当前访问的用户的session信息，如果能读到，说明已经登录过了，继续向后走
        info_dict = request.session.get('info')
        if info_dict:
            return

        # 如果读不到，说明没有登录，跳转到登录界面
        return redirect('/sign-in/')
