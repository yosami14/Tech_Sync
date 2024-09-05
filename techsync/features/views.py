# myapp/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import os
from dotenv import load_dotenv

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        try:
            # Load environment variables
            load_dotenv()
            genai.configure(api_key=os.environ["GEMINI_API_KEY"])
            
            # Create the model and chat session
            generation_config = {
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }
            model = genai.GenerativeModel(
                model_name="gemini-1.5-pro",
                generation_config=generation_config
            )
            chat_session = model.start_chat(
                history=[
                    {"role": "user", "parts": [user_message]},
                ]
            )
            response = chat_session.send_message(user_message)
            return JsonResponse({'response': response.text})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
