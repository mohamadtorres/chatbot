# import requests #to send api requests
# from django.http import JsonResponse #Helps to return dchatbot responses in json format
# import json
# from django.views.decorators.csrf import csrf_exempt


# # from django.template import loader

# # def chatbot(request):
# #     template = loader.get_template('base.html') #loader the template u want
# #     return HttpResponse(template.render()) #render the template u loaded

# @csrf_exempt
# def chatbot_view(request):
#     if request.method == 'POST': #chatbot receives POST request
#         try:
#             data = json.loads(request.body) #converting the body (json) to python dictionary
#             user_message = data.get('message', "")
#             DEEPSEEK_API_URL = "https://r1-prod-swecoab-new-res.germanywestcentral.inference.ml.azure.com/v1/chat/completions"
#             API_KEY = "W8zGgBDxoHsvreZCkHkhcDuRmHS1j20a"
#             headers = {
#                 "Authorization": "Bearer {API_KEY}",
#                 "Content-Type": "application/json",
#             }

#             payload = {"message" : user_message}

#             #send request to deepseel api
#             response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
#             deepseek_response = response.json() #convert response to python dictionary

#             return JsonResponse({"response" : deepseek_response}) #return the response in json format
        

#         except Exception as e:
#             return JsonResponse({"error" : str(e)}, status = 500) #return error message in json format if any error occurs
#     return JsonResponse({"error" : "Only POST requests are allowed"}, status = 400) #return error message in json format if request method is not POST

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def chatbot_view(request):
    if request.method == "POST":
        try:
            # Step 1: Print the request body to check if it's being received
            print("Raw Request Body:", request.body)

            data = json.loads(request.body)  # Convert request body (JSON) to Python dictionary
            user_message = data.get("message", "")

            # Step 2: Print the extracted message
            print("Extracted Message:", user_message)

            # DeepSeek API details
            DEEPSEEK_API_URL = "https://r1-prod-swecoab-new-res.germanywestcentral.inference.ml.azure.com/v1/chat/completions"  # Replace with actual API
            API_KEY = "W8zGgBDxoHsvreZCkHkhcDuRmHS1j20a"  # Replace with actual API key

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {"message": user_message}  # The message sent to DeepSeek

            # Step 3: Print the payload before sending the request
            payload = {
                "messages": [{"role": "user", "content": user_message}],  # DeepSeek expects "messages"
                "model": "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"  # Specify which model to use (replace if needed)
            }
            response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)

            # Step 4: Print the response from DeepSeek API
            print("Raw API Response:", response.text)

            deepseek_response = response.json()  # Convert response to JSON

            return JsonResponse({"response": deepseek_response})

        except json.JSONDecodeError as e:
            print("JSON Decode Error:", e)
            return JsonResponse({"error": "Invalid JSON format received"}, status=400)

        except Exception as e:
            print("Error:", e)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
