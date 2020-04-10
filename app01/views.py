from django.shortcuts import render

# Create your views here.
from app01 import models
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
import uuid
from utils.response import *
from django.forms.models import model_to_dict


# 定义一个序列化类
class TimeSerilizers(serializers.ModelSerializer):
    class Meta:
        model = models.Time
        fields = "__all__"


# 时间管理模块
class TmeView(APIView):
    def get(self, request, *args, **kwargs):
        # 定义状态码
        ret = {"code": 200, "data": None}
        try:
            nowtime = kwargs.get('nowtime')
            token = kwargs.get('token')
            if token:
                userid = models.UserAuthToken.objects.filter(token=token).first().user_id
                alltime = models.Time.objects.filter(user_id=userid, createtime=nowtime).values()

                ret['data'] = []

                for i in alltime:
                    ret['data'].append(i)


            else:
                # 如果是请求单条数据
                pk = kwargs.get("pk")
                if pk:
                    obj = models.Time.objects.filter(id=pk).first()
                    ser = TimeSerilizers(instance=obj, many=False)
                    # 查询数据库
                else:
                    # 否则我就查询所有的数据
                    queryset = models.Time.objects.all()
                    # 使用序列化类进行序列化数据疯子在data里面
                    ser = TimeSerilizers(instance=queryset, many=True)
                ret["data"] = ser.data
        except Exception as e:
            ret["code"] = 400
            # 新建一个error 返回给后端
            ret["error"] = "获取时间列表失败"
        return Response(ret)



    def post(self, request):
        # 定义状态码
        ret = {"code": 200, "data": None}
        try:
            bs = models.Time.objects.create(quest=request.data['quest'],startime=request.data['startime'],
                                            endtime=request.data['endtime'],status=request.data['status'],
                                            total=request.data['total'],
                                            user_id=request.data['user']) # post不需要定义many=Ture

            if bs:
                ret['data'] = '添加数据成功'
                return Response(ret)
            else:
                ret['code'] = 400
                ret['data'] = '添加数据失败'

        except Exception as e:
            ret["code"] = 400
            # 新建一个error 返回给后端
            ret["data"] = "服务器错误"
        return Response(ret)


        # 删除数据

    def delete(self, *args, **kwargs):

        pk = kwargs.get("pk")
        print(pk)
        ret = {"code": 200, "data": None}
        models.Time.objects.filter(id=pk).delete()
        ret['data'] = '删除数据成功'
        return Response(ret)

        # #  修改数据（前端指定id值后，在data中输入k：v即可change数据）

    def put(self, request, *args, **kwargs):
          # 定义状态码
        ret = {"code": 200, "data": None}
        pk = kwargs.get("pk")
        try:
            publish = models.Time.objects.filter(pk=pk)
            # data=  form request.data client
            ps = publish.update(quest=request.data['quest'],startime=request.data['startime'],
                                                endtime=request.data['endtime'],status=request.data['status'],
                                                total=request.data['total'],
                                                user_id=request.data['user']) # many=True多个对象

        except Exception as e:
            ret['code'] = 400
            ret['data'] = '服务器错误'
            return Response(ret)

        # if ps pass verify
        if ps:
            ret['code'] = 200
            ret['data'] = '修改数据成功'
            return Response(ret)
        else:
            ret['code'] = 400
            ret['data'] = '修改数据失败'
            return Response(ret)


# 处理登录验证
class LoginView(APIView):
    """
    Interface for user authentication
    """

    def post(self, request, *args, **kwargs):
        """
        Authentification of user
        :param request: request correlation data
        :param args: URL transmit args
        :param kwargs: URL transmit kwargs
        """
        # acquire status object
        ret = TokenResponse()
        try:
            user = request.data.get('user')
            pwd = request.data.get('pwd')
            new_user = models.Account.objects.filter(username=user, password=pwd).first()
            ret.data = new_user.id
            if not new_user:
                ret.code = 400
                ret.error = '用户名密码错误'
            else:
                uid = str(uuid.uuid4())
                models.UserAuthToken.objects.update_or_create(user=new_user, defaults={'token': uid})
                ret.token = uid

        except Exception as e:
            ret.code = 404
            ret.data = '服务器错误'

            # ret.dict == return class init attr of dict
        return Response(ret.dict)


# 处理注册模块
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Authentification of user
        :param request: request correlation data
        :param args: URL transmit args
        :param kwargs: URL transmit kwargs
        """
        # acquire status object
        ret = BaseResponse()
        try:
            user = request.data.get('user')
            pwd = request.data.get('pwd')
            new_user = models.Account.objects.filter(username=user, password=pwd).first()
            if not new_user:
                models.Account.objects.create(username=user, password=pwd)
                ret.code = 200
                ret.data = '创建用户成功'
            else:
                ret.code = 400
                ret.data = '用户名已经存在'

        except Exception as e:
            ret.code = 404
            ret.data = '服务器错误'

        # ret.dict == return class init attr of dict
        return Response(ret.dict)
