#coding=utf-8
from rest_framework.fields import CharField 
from django.utils import six, timezone
from lxml import etree, html
import urlparse


class TUEditorField(CharField):
    """
    用于在rest 框架中使用的SerializerField，他会对文本中的域名做
    替换操作，适用于富文本中的图片被CDN部署的情景。命名参数的格式，
    domain_from: 替换前的域名，str或list 
    domain_to: 替换后的域名，str或list，与domain_from一一对应
    """
    def __init__(self, **kwargs):
        self.domain_from = kwargs.pop("domain_from") if "domain_from" in kwargs else None
        self.domain_to = kwargs.pop("domain_to") if "domain_to" in kwargs else ""
        super(TUEditorField, self).__init__(**kwargs)

    def to_representation(self, value):
        value = six.text_type(value)
        if self.domain_from:
            value = self.html_domain_replace(value, self.domain_from, self.domain_to)
        return value


    def html_domain_replace(self, content, domain_from, domain_to):
        """
        功能：对content内容进行src或href的domain信息替换
        参数：
        from_domain: string或list，替换前的domain
        to_domain: string或list，替换后的domain
        """
        if isinstance(domain_from, list) and isinstance(domain_to, list):
            assert len(domain_from) == len(domain_to), u"domain_from和domain_to的长度应当相同"
        elif isinstance(domain_from, str) and isinstance(domain_to, str):
            domain_from, domain_to = [domain_from], [domain_to]
        elif isinstance(domain_from, unicode) and isinstance(domain_to, unicode):
            domain_from, domain_to = [domain_from], [domain_to]
        else:
            assert True==False, u"传递参数类型不正确，应都为str或都为list"

        tree  = html.fragment_fromstring(content, create_parent=True)
        for node in tree.xpath('//*[@src]'):
            src = node.get('src')
            for f_d, t_d in zip(domain_from, domain_to):
                src = src.replace(f_d, t_d)
                node.set('src', src)
        # 当前不做href属性替换
        # for node in tree.xpath('//*[@href]'):
        #     href = node.get('href')
        #     for f_d, t_d in zip(domain_from, domain_to):
        #         href = href.replace(f_d, t_d)
        #     node.set('href', href)
        data =  etree.tostring(tree, encoding="utf-8")
        return data

