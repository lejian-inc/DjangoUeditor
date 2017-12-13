#coding=utf-8
from django import template
from django.template.defaultfilters import stringfilter
from ..utils import html_domain_replace


register = template.Library()

# 定义域名过滤器
@register.filter(name="domain_cv")
def tueditor_domain_converse(value, domain_switcher):
    """
    功能：进行域名替换操作
    参数：
    domain_switcher，域名转换字符串，格式"原始域名,替换域名|原始域名,替换域名"
    """
    domain_from, domain_to = [], []
    for domain in domain_switcher.split("|"):
        if not domain:
            continue
        domain_f, domain_t = domain.split(",")
        domain_from.append(domain_f)
        domain_to.append(domain_t)

    rst_value = html_domain_replace(value, domain_from, domain_to)
    return rst_value

