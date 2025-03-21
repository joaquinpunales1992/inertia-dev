from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from transformers import GPT2LMHeadModel, GPT2Tokenizer

import threading

def home(request):
    return render(request, "hello.html")

llm_model = None
tokenizer = None

# Load model in a separate thread
def load_model_sync():
    global llm_model, tokenizer

    # Load the model and tokenizer
    model_name = "gpt2"
    llm_model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)


# Run model loading in a separate thread
threading.Thread(target=load_model_sync, daemon=True).start()

@csrf_exempt
def chat(request):

    if llm_model is None:
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
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        outputs = llm_model.generate(inputs, max_length=120)
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return JsonResponse({"response": response_text})
    else:
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)
