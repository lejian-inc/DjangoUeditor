#coding=utf-8
"""
tueditor的核心配置文件，在这里将会得到所有方面的配置信息
@author: tianyuan
@time: 2017年12月7号
"""
from django.conf import settings as gSettings 

UEditorGeneralSettings = { # ueditor的通用设置，暂未对其全部配置进行处理，这里仅仅拿出几个配置作为例子，详细请查看ueditor.cofnig.js中的详细配置
    "html_width" : "800px", # 组件展示宽度，为自定义，ueditor中无该设置
    "html_height" : "500px", # 组件展示高度，为自定义，ueditor中无该设置，设置了该属性，那么autoHeightEnabled配置则为false
    "isShow" : True,    # 默认显示编辑器
    "textarea" : "editorValue", # 提交表单时，服务器获取编辑器提交内容的所用的参数，多实例时可以给容器name属性，会将name给定的值最为每个实例的键值，不用每次实例化的时候都设置这个值
    "initialContent":'欢迎使用ueditor!',    # 初始化编辑器的内容,也可以通过textarea/script给值，看官网例子
}

UEditorToolbarsSettings = [[  # ueditor的工具栏设置, 
    'fullscreen', 'source', '|', 'undo', 'redo', '|',
    'bold', 'italic', 'underline', 'fontborder', 'strikethrough', 'superscript', 'subscript', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote', 'pasteplain', '|', 'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall', 'cleardoc', '|',
    'rowspacingtop', 'rowspacingbottom', 'lineheight', '|',
    'customstyle', 'paragraph', 'fontfamily', 'fontsize', '|',
    'directionalityltr', 'directionalityrtl', 'indent', '|',
    'justifyleft', 'justifycenter', 'justifyright', 'justifyjustify', '|', 'touppercase', 'tolowercase', '|',
    'link', 'unlink', 'anchor', '|', 'imagenone', 'imageleft', 'imageright', 'imagecenter', '|',
    'simpleupload', 'insertimage', 'emotion', 'scrawl', 'insertvideo', 'music', 'attachment', 'map', 'gmap', 'insertframe', 'insertcode', 'webapp', 'pagebreak', 'template', 'background', '|',
    'horizontal', 'date', 'time', 'spechars', 'snapscreen', 'wordimage', '|',
    'inserttable', 'deletetable', 'insertparagraphbeforetable', 'insertrow', 'deleterow', 'insertcol', 'deletecol', 'mergecells', 'mergeright', 'mergedown', 'splittocells', 'splittorows', 'splittocols', 'charts', '|',
    'print', 'preview', 'searchreplace', 'drafts', 'help'
]]


UEditorUploadSettings={
   #上传图片配置项
    "imageActionName": "uploadimage", #执行上传图片的action名称
    "imageMaxSize": 10485760, #上传大小限制，单位B,10M
    "imageFieldName": "upfile", #* 提交的图片表单名称 */
    "imageUrlPrefix": "",
    "imagePathFormat":"",
    "imageAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"], #上传图片格式显示

    #涂鸦图片上传配置项 */
    "scrawlActionName": "uploadscrawl", #执行上传涂鸦的action名称 */
    "scrawlFieldName": "upfile", #提交的图片表单名称 */
    "scrawlMaxSize": 10485760, #上传大小限制，单位B  10M
    "scrawlUrlPrefix":"",
    "scrawlPathFormat":"",

    #截图工具上传 */
    "snapscreenActionName": "uploadimage", #执行上传截图的action名称 */
    "snapscreenPathFormat":"",
    "snapscreenUrlPrefix":"",

    #抓取远程图片配置 */
    "catcherLocalDomain": ["127.0.0.1", "localhost", "img.baidu.com"],
    "catcherPathFormat":"",
    "catcherActionName": "catchimage", #执行抓取远程图片的action名称 */
    "catcherFieldName": "source", #提交的图片列表表单名称 */
    "catcherMaxSize": 10485760, #上传大小限制，单位B */
    "catcherAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"], #抓取图片格式显示 */
    "catcherUrlPrefix":"",
    #上传视频配置 */
    "videoActionName": "uploadvideo", #执行上传视频的action名称 */
    "videoPathFormat":"",
    "videoFieldName": "upfile", # 提交的视频表单名称 */
    "videoMaxSize": 102400000, #上传大小限制，单位B，默认100MB */
    "videoUrlPrefix":"",
    "videoAllowFiles": [
        ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
        ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid"], #上传视频格式显示 */

    #上传文件配置 */
    "fileActionName": "uploadfile", #controller里,执行上传视频的action名称 */
    "filePathFormat":"",
    "fileFieldName": "upfile",#提交的文件表单名称 */
    "fileMaxSize": 204800000, #上传大小限制，单位B，200MB */
    "fileUrlPrefix": "",#文件访问路径前缀 */
    "fileAllowFiles": [
        ".png", ".jpg", ".jpeg", ".gif", ".bmp",
        ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
        ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid",
        ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab", ".iso",
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml"
    ], #上传文件格式显示 */

    #列出指定目录下的图片 */
    "imageManagerActionName": "listimage", #执行图片管理的action名称 */
    "imageManagerListPath":"",
    "imageManagerListSize": 30, #每次列出文件数量 */
    "imageManagerAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"], #列出的文件类型 */
    "imageManagerUrlPrefix": "",#图片访问路径前缀 */

    #列出指定目录下的文件 */
    "fileManagerActionName": "listfile", #执行文件管理的action名称 */
    "fileManagerListPath":"",
    "fileManagerUrlPrefix": "",
    "fileManagerListSize": 30, #每次列出文件数量 */
    "fileManagerAllowFiles": [
        ".png", ".jpg", ".jpeg", ".gif", ".bmp",".tif",".psd"
        ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
        ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid",
        ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab", ".iso",
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml",
        ".exe",".com",".dll",".msi"
    ] #列出的文件类型 */
}


# 获取文件命名函数
if hasattr(gSettings, "TUEDITOR_FILE_NAME_FUN"):
    TUEDITOR_FILE_NAME_FUN = gSettings.TUEDITOR_FILE_NAME_FUN
else:
    TUEDITOR_FILE_NAME_FUN = None


# 获取文件存储路径设置
if hasattr(gSettings, "TUEDITOR_UPLOAD_PATH"):
    TUEDITOR_UPLOAD_PATH = gSettings.TUEDITOR_UPLOAD_PATH
else:
    TUEDITOR_UPLOAD_PATH = "ueditor/"


# 获取文件访问路径
if hasattr(gSettings, "TUEDITOR_MEDIA_URL"):
    TUEDITOR_MEDIA_URL = gSettings.TUEDITOR_MEDIA_URL
elif hasattr(gSettings, "MEDIA_URL"):
    TUEDITOR_MEDIA_URL = gSettings.MEDIA_URL 
else:
    TUEDITOR_MEDIA_URL = "/media/" # 默认使用的访问地址


# 更新editor设置
if hasattr(gSettings, "TUEDITOR_UPLOAD_SETTINGS"):
    UEditorUploadSettings.update(gSettings.TUEDITOR_UPLOAD_SETTINGS)

# 更新工具栏设置
if hasattr(gSettings, "TUEDITOR_TOOLBARS_SETTINGS"):
    UEditorToolbarsSettings = gSettings.TUEDITOR_TOOLBARS_SETTINGS

# 更新常规设置
if hasattr(gSettings, "TUEDITOR_GENERAL_SETTINGS"):
    UEditorGeneralSettings.update(gSettings.TUEDITOR_GENERAL_SETTINGS)

# 更新ServerUrl
if hasattr(gSettings, "TUEDITOR_SERVER_URL"):
    UEditorServerUrl = gSettings.TUEDITOR_SERVER_URL
else:
    UEditorServerUrl = '/ueditor/controller/'


# 获取存储使用的storage，依赖于Django的storage设置
from django.core.files.storage import default_storage # 获取默认存储方式 
STORAGE = default_storage

UEditorTotalSettings = {
    "general": UEditorGeneralSettings,
    "toolbars": UEditorToolbarsSettings,
    "upload": UEditorUploadSettings,
    "server_url": UEditorServerUrl,
}
