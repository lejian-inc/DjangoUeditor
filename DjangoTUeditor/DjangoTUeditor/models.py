# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.admin import widgets as admin_widgets

# Create your models here.
import widgets

class TUEditorField(models.TextField):

    def __init__(self, **kwargs):
        super(TUEditorField, self).__init__(**kwargs)


    def formfield(self, **kwargs):
        defaults = {"widget": widgets.TUEditorWidget()}
        defaults.update(kwargs)
        if defaults['widget'] == admin_widgets.AdminTextareaWidget:
            defaults['widget'] = widgets.AdminTUEditorWidget()
        return super(TUEditorField, self).formfield(**defaults)

