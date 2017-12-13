#coding=utf-8
from django import forms
from widgets import TUEditorWidget
from models import TUEditorField as ModelTUEditorField

class TUEditorField(forms.CharField):
    def __init__(self, *args,**kwargs):
        super(TUEditorField,self).__init__(*args, **kwargs)


