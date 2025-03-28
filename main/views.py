from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from thefuzz import process


# Define chatbot intents and responses
INTENTS = {
    "website": ["website", "web development", "build site", "web application"],
    "app": ["app", "mobile app", "application"],
    "AI": ["AI", "artificial intelligence", "machine learning"],
    "pricing": ["price", "cost", "budget"],
}

RESPONSES = {
    "website": "We can help build your website! <input type='submit' value='Book a 30-minute call for FREE' class='small'/>",
    "app": "Are you looking for a mobile or web application?",
    "AI": "We specialize in AI solutions! What problem are you trying to solve? <input type='submit' value='Book a 30-minute call for FREE' class='small'/>",
    "pricing": "Our pricing depends on project complexity. <input type='submit' value='Book a 30-minute call for FREE' class='small'/>",
}

def detect_intent(user_message):
    best_match = None
    best_score = 0
    
    for intent, keywords in INTENTS.items():
        match, score = process.extractOne(user_message, keywords)
        if score > best_score:
            best_match = intent
            best_score = score
    
    return best_match if best_score > 70 else None


def home(request):
    return render(request, "hello.html")


@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").lower()
            
            # Detect intent using fuzzy matching
            intent = detect_intent(user_message)
            if intent:
                return JsonResponse({"response": RESPONSES[intent]})
            
            return JsonResponse({"response": "Can you provide more details about your project?"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)
