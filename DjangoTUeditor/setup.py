#coding=utf-8
from setuptools import setup, find_packages 

def readme():
    with open("README.rst") as f:
        return f.read()
 
setup(
    name = "lejian_django_tueditor",
    version = "1.0",
    description='this package is for a ueditor backend to django',
    author="tianyuan.jiang",
    author_email="weiwotianyuan@163.com",
    license="MIT",
    packages = find_packages(),
    zip_safe = False,
    include_package_data=True, # for at install stage,copy all files in MANIFEST.in to install path
)


