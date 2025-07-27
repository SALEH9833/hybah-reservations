# core/views.py
from django.shortcuts import render

def page_statique_view(request, template_name):
    return render(request, template_name)