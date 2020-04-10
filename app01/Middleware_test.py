from django.utils.deprecation import MiddlewareMixin


class Alloriven(MiddlewareMixin):
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods '] = 'PUT,DELETE,POST,GET'

        if request.method == 'OPTIONS':
            print(123123123)
            # 我只响应你 content-type 如果你定义了其他的头，浏览器就不会返回给你数据
            response['Access-Control-Allow-Headers '] = '*'
            response['Access-Control-Allow-Origin'] = '*'
            # 如果是put 或者是delete请求就需要 加方法响应
            response['Access-Control-Allow-Methods '] = 'PUT,DELETE,POST,GET'
        return response