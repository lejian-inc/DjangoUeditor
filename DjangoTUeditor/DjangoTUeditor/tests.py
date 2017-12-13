# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys 
from django.test import TestCase

from lxml import etree, html
import urlparse

# Create your tests here.

"""
测试html属性替换
"""
def test_html_parse(content, from_domain, to_domain):
    """
    功能：对content内容进行src或href的domain信息替换
    参数：
    from_domain: string或list，替换前的domain
    to_domain: string或list，替换后的domain
    """
    if isinstance(from_domain, list) and isinstance(to_domain, list):
        assert len(from_domain) == len(to_domain), u"from_domain和to_domain的长度应当相同"
    elif isinstance(from_domain, str) and isinstance(to_domain, str):
        from_domain, to_domain = [from_domain], [to_domain]
    elif isinstance(from_domain, unicode) and isinstance(to_domain, unicode):
        from_domain, to_domain = [from_domain], [to_domain]
    else:
        # import pdb; pdb.set_trace()
        assert True==False, u"传递参数类型不正确，应都为str或都为list"

    tree  = html.fragment_fromstring(content, create_parent=True)
    for node in tree.xpath('//*[@src]'):
        src = node.get('src')
        for f_d, t_d in zip(from_domain, to_domain):
            src = src.replace(f_d, t_d)
        node.set('src', src)

    for node in tree.xpath('//*[@href]'):
        href = node.get('href')
        for f_d, t_d in zip(from_domain, to_domain):
            href = href.replace(f_d, t_d)
        node.set('href', href)

    data =  etree.tostring(tree, pretty_print=False) 　
    return data


if __name__ == "__main__":
    with open(sys.argv[1]) as in_f:
        content = in_f.read()
    content = test_html_parse(content, ["baidu.com", "www.sina.com"], ["google.com", "www.163.com:80"])
    with open("./out.html", "wb") as out_f:
        out_f.write(content)

