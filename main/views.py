from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Define chatbot intents and responses
INTENTS = {
    "website": ["website", "web development", "build site"],
    "app": ["app", "mobile app", "application"],
    "AI": ["AI", "artificial intelligence", "machine learning"],
    "pricing": ["price", "cost", "budget"],
}

RESPONSES = {
    "website": "We can help build your website! What features do you need?",
    "app": "Are you looking for a mobile or web application?",
    "AI": "We specialize in AI solutions! What problem are you trying to solve?",
    "pricing": "Our pricing depends on project complexity. Can you describe your requirements?",
}

def detect_intent(user_message):
    doc = nlp(user_message)
    for intent, keywords in INTENTS.items():
        for keyword in keywords:
            if keyword in user_message:
                return intent
    return None

def home(request):
    return render(request, "hello.html")


@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").lower()
            
            # Detect intent using NLP
            intent = detect_intent(user_message)
            if intent:
                return JsonResponse({"response": RESPONSES[intent]})
            
            return JsonResponse({"response": "Can you provide more details about your project?"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)