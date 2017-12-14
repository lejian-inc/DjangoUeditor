# DjangoTUeditor
代码参考了DjangoUeditor，为了和DjangoUeditor区分开来，这里命名为DjangoTUeditor。前端ueditor版本为1.4.3。

# 使用
进入DjangoTUeditor中，执行
```bash
python setup sdist
```
在DjangoTUeditor中dist文件夹下生成了一个tar文件，然后使用pip进行安装  
```bash
pip install lejian_django_tueditor-xxx.tar.gz  
```

在settings中添加app
```python
INSTALLED_APPS = [
    ...
    'DjangoTUeditor',
]
```
在urls文件中加入路由  
```python
import DjangoTUeditor  

urlpatterns = [
    url(r'^admin/', admin.site.urls), 
    url(r'^ueditor/', include("DjangoTUeditor.urls")),  
]
```
在model对应的字段上使用ueditor富文本编辑器，如下models.py文件 
```python
from DjangoTUeditor.models import TUEditorField

class Book(models.Model):
    description = TUEditorField(null=True, blank=True)
    public = TUEditorField(null=True, blank=True)
```

如果不希望直接影响models文件，可以在admin文件中指定使用富文本的字段，如下admin.py文件  
```python
from models import Book
from DjangoTUeditor.widgets import AdminTUEditorWidget

class BookForm(forms.ModelForm):
     class Meta:
         model = Book
         fields = '__all__'
         widgets = {
             "description": AdminTUEditorWidget,
         }
 
 
@admin.register(Menu)                                                                                                                                                                                      
class BookAdmin(admin.ModelAdmin):  
    form = BookForm
```

如果你期望在rest-framework中对富文本字段做一些特殊处理（典型的是域名替换），可以在serializers文件如下使用 
```python
from rest_framework import serializers
from DjangoTUeditor.rest.serializers import TUEditorField

class BookSerializer(serializers.Serializer):
    description = TUEditorField(domain_from="www.baidu.com", domain_to="www.cdn.com")
```
（这里的domain_from和domain_to可以将富文本中的domain_from指定的域名替换为domain_to中的域名，两个参数为str或list类型）


# 存储基于storage
DjangoTUeditor的存储方式依赖于django项目所使用的storage，当你需要使用其他存储方式对文件进行存储时（如ftp），仅需要在django项目的
settings文件中指定相应的storage，DjangoTUeditor会默认使用该storage对文件进行存储操作。

django的storage相关信息：https://docs.djangoproject.com/en/2.0/ref/files/storage/  

# 存储文件重命名
在settings文件中可以指定对文件进行重命名的函数，默认使用原有文件名
```python
TUEDITOR_FILE_NAME_FUN=rename_fun
```
该函数接收一个原文件名参数

# 域名设置及域名替换
DjangoTUeditor存储时服务器返回的路径为相对路径，如果需要设置存储路径的域名信息，可以在后台进行配置，前端获得配置后将会将域名和服务器返回的相对地址进行拼接
如我在settings文件中设置如下内容：
```python
TUEDITOR_UPLOAD_SETTINGS={
   #上传图片配置项
    "imageActionName": "uploadimage", #执行上传图片的action名称
    "imageMaxSize": 10485760, #上传大小限制，单位B,10M
    "imageFieldName": "upfile", #* 提交的图片表单名称 */
    "imageUrlPrefix": "www.baidu.com",
     .....  
}    
```
那么富文本中存储的图片地址将都会带有"www.baidu.com"这个域名。某些情景下需要对域名进行替换，比如图片进行了CDN部署时，需要在客户端展示的域名替换为
CDN域名，DjangoTUeditor提供了一个domain_cv过滤器，可以在template模板中进行使用，如下：
```html
{% load tueditor %}

<body>
{{ s | domain_cv:d }}
</body>
```
这里s为富文本内容，domain_cv为过滤器，d为域名转换信息，格式如下"原始域名,替换域名|原始域名,替换域名",例如将baidu替换为google，将sina替换为163，
d的内容就应该为  
"www.baidu.com,www.google.com|www.sina.com:8000,www.163.com:80"  

在rest-framework中，对应的SerializerField可以使用domain_from和domain_to参数指定替换，如上面的代码：  
```python
from rest_framework import serializers
from DjangoTUeditor.rest.serializers import TUEditorField

class BookSerializer(serializers.Serializer):
    description = TUEditorField(domain_from="www.baidu.com", domain_to="www.cdn.com")
```
这将"www.baidu.com"替换为"www.cdn.com"

注意：替换时仅仅将标签的src属性进行替换，而不会对文本内容中的对应字符进行替换。


# 详细设置 
以下内容均在django settings文件中设置

文件存储路径设置  
该路径是将storage的根目录作为存储根目录，默认存储在ueditor目录下
```python
TUEDITOR_UPLOAD_PATH = 'richtext/'
```

文件访问路径设置  
服务器后端存储文件时返回的是相对路径，但是这个相对路径会加上一个路径访问前缀，如果没有设置的话，将会使用settings.MEDIA_URL
```python
TUEDITOR_MEDIA_URL = '/media/'
```

常规设置
```python
TUEDITOR_GENERAL_SETTINGS=
{ # ueditor的通用设置，暂未对其全部配置进行处理，这里仅仅拿出几个配置作为例子，详细请查看ueditor.cofnig.js中的详细配置
    "html_width" : "800px", # 组件展示宽度，为自定义，ueditor中无该设置
    "html_height" : "500px", # 组件展示高度，为自定义，ueditor中无该设置，设置了该属性，那么autoHeightEnabled配置则为false
    "isShow" : True,    # 默认显示编辑器
    "textarea" : "editorValue", # 提交表单时，服务器获取编辑器提交内容的所用的参数，多实例时可以给容器name属性，会将name给定的值最为每个实例的键值，不用每次实例化的时候都设置这个值
    "initialContent":'欢迎使用ueditor!',    # 初始化编辑器的内容,也可以通过textarea/script给值，看官网例子
}
```

工具栏按钮设置  
```python
TUEDITOR_TOOLBARS_SETTINGS = 
[[  # ueditor的工具栏设置, 
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
```

文件上传设置
```python  
TUEDITOR_UPLOAD_SETTINGS = # 具体配置内容可以参考ueditor的config.js文件
{
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

```















