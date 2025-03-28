from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from thefuzz import process


# Define chatbot intents and responses
INTENTS = {
    "greeting": ["hi", "hello", "hey", "how are you", "what's up", "howdy"],
    "website": ["website", "web development", "build site", "web application"],
    "app": ["app", "mobile app", "application"],
    "AI": ["AI", "artificial intelligence", "machine learning"],
    "pricing": ["price", "cost", "budget", "how much", "rates", "rate", "pricing"],
    "portfolio": ["portfolio", "projects", "previous work", "examples", "client", "clients"],
    "contact": ["contact", "get in touch", "reach out", "how to contact", "how to reach"],
    "about": ["about", "who are you", "who we are", "company", "team"],
    "location": ["location", "where are you", "where is your office", "address"],
    "hours": ["hours", "working hours", "business hours", "when are you open"],
    "services": ["services", "what do you offer", "offerings", "what can you do", "service", "what do you provide", "what services"],
    "thanks": ["thank you", "thanks", "appreciate it", "grateful"],
    "goodbye": ["bye", "goodbye", "see you later", "take care"],

}

RESPONSES = {
    "greeting": "Hello! Do you have a project in mind? ",
    "website": "We can help you build your website! <input type='submit' value='Book a 30-minute call for FREE' class='small'/>",
    "app": "Are you looking for a mobile or web application?",
    "AI": "We specialize in AI solutions! What problem are you trying to solve? <input type='submit' value='Book a 30-minute call for FREE' class='small'/>",
    "pricing": "Our pricing depends on project complexity. <input type='submit' value='Book a 30-minute call for FREE' class='small'/>",
    "portfolio": "We have a diverse portfolio! <input type='submit' value='Check out our Clients section' class='small'/>",
    "contact": "Just fill the contact form and we'll get back to you! <input type='submit' value='Contact Us' class='small'/>",
    "about": "We are a team of passionate Software Engineers! What is your project about?",
    "location": "We've been working remotely since 2018! So don't worry we get you cover",
    "hours": "We work 24/7! So you can reach us anytime.",
    "services": "We offer web development, API development and AI solutions  <input type='submit' value='Book a 30-minute call for FREE' class='small'/>",
    "thanks": "You're welcome! If you have any more questions, feel free to ask.",
    "goodbye": "Goodbye! Have a great day!",
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
