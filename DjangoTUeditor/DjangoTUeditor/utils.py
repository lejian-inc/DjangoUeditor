#coding=utf-8
from lxml import etree, html
import urlparse

def html_domain_replace(content, domain_from, domain_to):
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











