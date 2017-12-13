#coding=utf-8
from django import forms 
from django.contrib.admin import widgets as admin_widgets
from settings import UEditorTotalSettings

class TUEditorWidget(forms.Textarea):

    template_name = "django-tueditor/ueditor.html"

    def __init__(self, *args, **kwargs):
        default_attrs = {}
        if kwargs:
            default_attrs.update(kwargs)

        super(TUEditorWidget, self).__init__(default_attrs)

    def get_context(self, name, value, attrs):
        context = super(TUEditorWidget, self).get_context(name, value, attrs)
        context.update(settings=UEditorTotalSettings)
        return context

    def render(self, name, value, attrs=None, renderer=None):
        return super(TUEditorWidget, self).render(name, value, attrs=attrs, renderer=renderer)

    class Media: 
        js = ("ueditor/ueditor.config.js",
              "ueditor/ueditor.all.js")


class AdminTUEditorWidget(admin_widgets.AdminTextareaWidget, TUEditorWidget):
    pass


