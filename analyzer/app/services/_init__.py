import google.generativeai as genai
from django.conf import settings


def generate_ai_response(prompt: str) -> str:
    """
    Central AI handler.
    All AI features use this function.
    """

    if not settings.GEMINI_API_KEY:
        raise Exception("GEMINI_API_KEY not configured.")

    genai.configure(api_key=settings.GEMINI_API_KEY)

    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(prompt)

    return response.text