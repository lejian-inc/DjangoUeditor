#coding=utf-8
"""
事件处理器类
"""
import datetime as dt 
import os
import urllib 
import base64
import time

from django.http import JsonResponse
from django.core.files.base import ContentFile

import settings


class ActionDealerAbstract(object):
    """
    ActionDealer 抽象类，用于处理各种类型请求的处理
    """
    def __init__(self, settings):
        """
        功能：初始化
        参数：
        settings，TUEditor配置（非Django的settings）
        """
        if not settings:
            raise Exception(u"ActionDealer类初始化需要配置参数")
            if not hasattr(settings, "STORAGE"):
                raise Exception(u"ActionDealer 需要一个storage, 该storage需要继承自django.core.files.storage.Storage")    
        else:
            self.storage = settings.STORAGE
            self.settings = settings


class DefaultActionDealer(ActionDealerAbstract):
    """
    默认的ActionDealerAbastract实现类
    """

    def __init__(self, settings):
        super(DefaultActionDealer, self).__init__(settings)
        self._init_config_key_matcher() # 初始化matcher

    def _get_upload_path(self, filename, action=None):
        """
        功能：获取文件上传路径，包含文件名，并需要在这里解决不存在的文件夹的创建问题
        参数：
        action: action动作，暂时将所有文件不加区分存放在一个目录，这里的action没有用到
        filename: 原文件名称
        """
        if self.settings.TUEDITOR_FILE_NAME_FUN:
            file_name_generator = self.settings.TUEDITOR_FILE_NAME_FUN
            store_file_name = file_name_generator(filename)
        else:
            store_file_name = filename 
        upload_path = self.settings.TUEDITOR_UPLOAD_PATH 
        return os.path.join(upload_path, store_file_name)

    def _get_storage_files(self, path, url=None): 
        """
        功能：通过storage，获取path路径上的所有文件
        参数：
        storage, 获取文件信息所使用的storage
        path, 遍历路径
        url, 外部获取文件的url地址，默认不使用
        返回：
        list, 文件存储路径
        """
        files_array = []
        dirs, files = self.storage.listdir(path)
        if files:
            for file in files:
                if url:
                    files_array.append(urllib.basejoin(url, os.path.join(path, file))) # TODO
                else:
                    files_array.append(os.path.join(path, file))
        if dirs:
            for dir in dirs:
                files_array = files_array + self._get_storage_files(os.path.join(path, dir), url)
        return files_array

    def get_editor_settings(self, request):
        """
        功能：获取编辑器配置
        """
        return JsonResponse(self.settings.UEditorUploadSettings)
    
    def list_files(self, request):
        """
        功能：列出服务器所有文件
        参数：
        request，请求request对象
        """
        if request.method != "GET":
            return  JsonResponse({state:'ERROR'})

        action=request.GET.get("action","listimage")
        list_start = long(request.GET.get("start",0))
        list_size = long(request.GET.get("size", 30))
        files = self._get_storage_files(self.settings.TUEDITOR_UPLOAD_PATH, url=self.settings.TUEDITOR_MEDIA_URL)
        if files:
            rst = {
                "state":"SUCCESS",
                "list":files[list_start:list_start+list_size],
                "start":list_start,
                "total":len(files)
            }
        else:
            rst = {
                "state": "未找到匹配文件！",
                "list":[],
                "start":list_start,
                "total":0
            }
        return JsonResponse(rst)

    def upload_scrawl_file(self, request):
        """
        功能：处理涂鸦文件上传
        """
        try:
            action = request.GET.get("action", "")
            form_name = self.get_action_form_name(action)
            content=request.POST.get(form_name)
            upload_file = ContentFile(base64.decodestring(content))
            
            scrawl_default_name = "{}.png".format(str(int(time.time()))) # 默认涂鸦文件命名规则
            store_path = self._get_upload_path(scrawl_default_name)
            _file_name, upload_file_suffix = os.path.splitext(store_path)
            upload_file.name = _file_name

            self.storage.save(store_path, upload_file)
            rst = {
                'state': 'SUCCESS',
                'url': urllib.basejoin(self.settings.TUEDITOR_MEDIA_URL, store_path),
                'original': upload_file.name,
                'type': upload_file_suffix.replace(".", ""),
                'size': upload_file.size,
            }
        except Exception,E:
            rst = {
                'state': "写入图片文件错误:%s" % E.message,
            }
        return JsonResponse(rst)

    def upload_file(self, request):
        """
        功能：处理文件上传
        """
        action = request.GET.get("action", "")
        upload_form_name = self.get_action_form_name(action)
        upload_file = request.FILES.get(upload_form_name)
        upload_file_name, upload_file_suffix = os.path.splitext(upload_file.name) 

        if not self.is_size_allow(action, upload_file.size):
            return JsonResponse({"state":"文件尺寸不符合要求"})
        if not self.is_suffix_allow(action, upload_file_suffix):
            return JsonResponse({"state":"文件格式不符合要求"})

        store_path = self._get_upload_path(upload_file.name, action)
        self.storage.save(store_path, upload_file)

        rst = {
            'state': 'SUCCESS',
            'url': urllib.basejoin(self.settings.TUEDITOR_MEDIA_URL, store_path),
            'original': upload_file.name,
            'type': upload_file_suffix.replace(".", ""),
            'size': upload_file.size,
        }
        return JsonResponse(rst)

    def catcher_remote_image(self, request):
        """
        功能：远程抓图
        需要catchRemoteImageEnable为true。
        如果前端插入图片地址与当前web不在同一个域，则由本函数从远程下载图片到本地
        """
        rst = {
            "state": "后台暂时不支持该功能，敬请期待！"
        }
        return JsonResponse(rst)

    def get_action_form_name(self, action):
        """
        功能：获取某个动作上传文件所使用的表单名称
        参数：
        action:动作名称 
        """
        default_form_name = "upfile"
        config_key_matcher = self.form_name_macher
        key = config_key_matcher[action]
        form_name = config_key_matcher.get(key, default_form_name)
        return form_name

    def is_suffix_allow(self, action, suffix):
        """
        功能：检查suffix格式文件在action的处理中是否被允许。用于检查文件格式
        参数：
        action: 动作名称
        suffix: 文件格式（注意带"."字符，例如".suffix"）
        返回值：
        如果允许，返回True；不允许，返回False。
        """
        config_key_matcher = self.suffix_matcher
        config_key = config_key_matcher[action]
        allow_suffixs = self.settings.UEditorUploadSettings.get(config_key, [])
        if suffix in allow_suffixs:
            return True 
        else:
            return False

    def is_size_allow(self, action, size):
        """
        功能： 检查action动作可以处理文件的尺寸
        参数：
        action：动作名称
        size：待处理文件尺寸
        返回值：
        如果允许处理，返回Ture；否则，返回False
        """
        config_key_matcher = self.size_matcher
        config_key = config_key_matcher[action]
        allow_size = self.settings.UEditorUploadSettings.get(config_key, 0)
        if size > allow_size:
            return False 
        else:
            return True

    def _init_config_key_matcher(self):
        """
        功能： 初始化所有config_matcher，其他函数依赖此函数，该函数必须在实例初始化时调用
        参数： 
        matcher_type: matcher类型，"suffix"|"size"，分别是类型matcher和尺寸matcher
        """
        upload_settings = self.settings.UEditorUploadSettings
        self.form_name_macher = { # 根据action找到settings对应的form name设置
            upload_settings["imageActionName"]: "imageFieldName",
            upload_settings["scrawlActionName"]: "scrawlFieldName",
            upload_settings["videoActionName"]: "videoFieldName",
            upload_settings["fileActionName"]: "fileFieldName",
        }
        self.suffix_matcher = { # 根据action找到settings对应的允许文件格式设置
            upload_settings["imageActionName"]: "imageAllowFiles",
            upload_settings["videoActionName"]: "videoAllowFiles",
            upload_settings["fileActionName"]: "fileAllowFiles",
            upload_settings["fileManagerActionName"]: "fileManagerAllowFiles",
            upload_settings["imageManagerActionName"]: "imageManagerAllowFiles",
            upload_settings["catcherActionName"]: "catcherAllowFiles",
        }
        self.size_matcher = { # 根据action找到settings对应的最大文件大小设置
            upload_settings["imageActionName"]: "imageMaxSize",
            upload_settings["scrawlActionName"]: "scrawlMaxSize",
            upload_settings["videoActionName"]: "videoMaxSize",
            upload_settings["fileActionName"]: "fileMaxSize",
            upload_settings["catcherActionName"]: "catcherMaxSize",
        }
        self.fun_matcher = { # 根据action找到对应的处理函数
            "config": self.get_editor_settings, # 获取后台配置
            upload_settings["imageActionName"]: self.upload_file,
            upload_settings["scrawlActionName"]: self.upload_scrawl_file,
            upload_settings["videoActionName"]: self.upload_file,
            upload_settings["fileActionName"]: self.upload_file,
            upload_settings["catcherActionName"]: self.catcher_remote_image,
            upload_settings["imageManagerActionName"]: self.list_files,
            upload_settings["fileManagerActionName"]: self.list_files,
        }


    def deal(self, request):
        """
        功能：总的对外处理接口
        参数：
        request
        """
        action = request.GET.get("action", None)
        deal_fun = self.fun_matcher[action]
        return deal_fun(request)


# 设置ActionDealer实例，这里采用DefaultActionDealer
default_action_dealer = DefaultActionDealer(settings)

