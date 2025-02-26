import requests #to send api requests
from django.http import HttpResponse,JsonResponse #Helps to return dchatbot responses in json format
import json
from django.views.decorators.csrf import csrf_exempt


from django.template import loader

def chatbot(request):
    template = loader.get_template('base.html') #loader the template u want
    return HttpResponse(template.render()) 

import re

def extract_chatbot_thought_and_reply(response):
    """
    Extracts both the AI's thought process and final reply.
    - Thought process is before `</think>`.
    - Reply is after `</think>`.
    """
    response = response.strip() 

    if "</think>" in response:
        thought, reply = response.split("</think>", 1)  # Split at </think>
    else:
        thought = "No thought process provided."
        reply = response  # If </think> is missing, use the full response

    return thought.strip(), reply.strip()

@csrf_exempt
def chatbot_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            DEEPSEEK_API_URL = "https://r1-prod-swecoab-new-res.germanywestcentral.inference.ml.azure.com/v1/chat/completions"
            API_KEY = "W8zGgBDxoHsvreZCkHkhcDuRmHS1j20a"

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "messages": [{"role": "user", "content": user_message}],
                "model": "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"
            }

            response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
            deepseek_response = response.json()

            #Extract AI response content correctly
            assistant_message = deepseek_response["choices"][0]["message"]["content"]

            # Extract thought process and actual reply
            thought, reply = extract_chatbot_thought_and_reply(assistant_message)

            return JsonResponse({"thought": thought, "reply": reply})  # Send both

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=400)

