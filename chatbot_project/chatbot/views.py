import requests
from django.http import HttpResponse, JsonResponse #Helps to return data in json format
import json
from django.views.decorators.csrf import csrf_exempt


# from django.template import loader

# def chatbot(request):
#     template = loader.get_template('base.html') #loader the template u want
#     return HttpResponse(template.render()) #render the template u loaded

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')
