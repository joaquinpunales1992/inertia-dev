from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from llama_cpp import Llama
import asyncio

def home(request):
    return render(request, "hello.html")



# Initialize the Llama model
async def load_model():
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None, 
        lambda: Llama.from_pretrained(
            repo_id="Qwen/Qwen2-0.5B-Instruct-GGUF",
            filename="qwen2-0_5b-instruct-q4_0.gguf",
            verbose=False,
            max_seq_len=512
        )
    )

async def main():
    print("Loading model asynchronously...")
    global llm
    llm = await load_model()
    print("Model loaded!")


asyncio.run(main())

@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)

        # Define domain-specific context
        domain_context = (
            "We are representing a software company."
            "Provide concise and relevant responses regarding project proposals and company capabilities."
            "We create custom Web Applications, AI integrations, Machine learning solutions for businesses, chatbots, recommendation systems, and more." 
            "if the user wants to contact us, please redirect them to our contact page."
            "Always talk about US/Our not I/my"
            "We develop software in Python (Django)."
            "Our main clients are: Australian museum, University of Sydney, Art gallery of South Australia and more"
        )
        # Construct the prompt
        prompt = f"{domain_context}\nUser: {user_message}\nBot:"

        # Generate response using the Llama model
        output = llm(prompt, max_tokens=50)
        response_text = output["choices"][0]["text"].strip()

        return JsonResponse({"response": response_text})
    else:
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)