from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def chatbot(request):
    template = loader.get_template('base.html') #loader the template u want
    return HttpResponse(template.render()) #render the template u loaded