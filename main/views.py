from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from llama_cpp import Llama
import threading
import asyncio

def home(request):
    return render(request, "hello.html")

llm = None  # Global variable for the model

# Load model in a separate thread (Django is synchronous by default)
def load_model_sync():
    global llm
    llm = Llama(
        model_path="qwen2-0_5b-instruct-q4_0.gguf",  
        verbose=False,
        max_seq_len=512
    )
    print("Model loaded!")

# Run model loading in a separate thread
threading.Thread(target=load_model_sync, daemon=True).start()

@csrf_exempt
def chat(request):
    global llm

    if llm is None:
        print("Model is still loading, please try again later.")

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)

        # Define domain-specific context
        domain_context = (
            "We are representing a software company."
            "Limit your response to 50 characters."
            "Provide concise and relevant responses regarding project proposals and company capabilities."
            "We create custom Web Applications, AI integrations, Machine learning solutions for businesses, chatbots, recommendation systems, and more." 
            "If the user wants to contact us, please redirect them to our contact page."
            "Always talk about US/Our not I/my."
            "We develop software in Python (Django)."
            "Our main clients are: Australian Museum, University of Sydney, Art Gallery of South Australia, and more."
        )

        # Construct the prompt
        prompt = f"{domain_context}\nUser: {user_message}\nBot:"

        # Generate response using the Llama model
        output = llm(prompt, max_tokens=150)
        response_text = output["choices"][0]["text"].strip()
        print (response_text)

        return JsonResponse({"response": response_text})
    else:
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)