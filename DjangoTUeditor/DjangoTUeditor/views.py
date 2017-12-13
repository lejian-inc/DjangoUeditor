# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from action_dealer import default_action_dealer as editor_dealer
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def action_controller(request):
    return editor_dealer.deal(request)
    
