import google.generativeai as genai
from django.conf import settings


def generate_ai_response(prompt: str) -> str:
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # ✅ SAFE MODEL (WORKING)
        model = genai.GenerativeModel("gemini-1.5-flash-latest")

        response = model.generate_content(prompt)

        if hasattr(response, "text"):
            return response.text

        return str(response)

    except Exception as e:
        return f"AI Error: {str(e)}"