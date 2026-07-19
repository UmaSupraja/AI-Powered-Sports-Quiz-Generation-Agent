import json

from google import genai

from src.config import GEMINI_API_KEY
from src.database import query_historic_facts
from src.search import get_live_news_context


def compile_quiz_data(sport, difficulty):
    """
    Generates a sports quiz using Retrieval-Augmented Generation (RAG).

    Returns:
        quiz_data (list): List of quiz questions in JSON format
        unified_context (str): Context used for generation
    """

    # -----------------------------
    # Retrieve Historical Facts
    # -----------------------------
    db_query = f"{sport} history championships records rules famous players"

    db_matches = query_historic_facts(
        sport=sport,
        query_text=db_query,
        n_results=3
    )

    db_context = (
        "\n".join(db_matches)
        if db_matches
        else "No historical sports facts available."
    )

    # -----------------------------
    # Retrieve Latest Sports News
    # -----------------------------
    web_context = get_live_news_context(sport)

    # -----------------------------
    # Merge Context
    # -----------------------------
    unified_context = f"""
========================
HISTORICAL FACTS
========================
{db_context}

========================
LATEST SPORTS NEWS
========================
{web_context}
"""

    # -----------------------------
    # Gemini Client
    # -----------------------------
    client = genai.Client(api_key=GEMINI_API_KEY)

    # -----------------------------
    # System Prompt
    # -----------------------------
    system_instruction = f"""
You are an expert Sports Quiz Generator.

Your job is to generate engaging and factually accurate sports quizzes.

IMPORTANT RULES:

1. Use ONLY the information from the retrieved context.
2. Never invent facts.
3. Generate EXACTLY 4 questions.
4. Each question must have FOUR options.
5. Only ONE option must be correct.
6. Difficulty must match the requested level.
7. Explanation should be 1-2 lines.
8. Return ONLY VALID JSON.
9. Do NOT return markdown.
10. Do NOT use ```json.

Retrieved Context:

{unified_context}
"""

    # -----------------------------
    # User Prompt
    # -----------------------------
    user_prompt = f"""
Create a {difficulty} level quiz for {sport}.

Return ONLY this JSON array.

[
  {{
    "question": "Question text",
    "options": {{
      "A": "Option A",
      "B": "Option B",
      "C": "Option C",
      "D": "Option D"
    }},
    "correct_answer": "A",
    "explanation": "Short explanation"
  }},
  {{
    "question": "...",
    "options": {{
      "A": "...",
      "B": "...",
      "C": "...",
      "D": "..."
    }},
    "correct_answer": "B",
    "explanation": "..."
  }},
  {{
    "question": "...",
    "options": {{
      "A": "...",
      "B": "...",
      "C": "...",
      "D": "..."
    }},
    "correct_answer": "C",
    "explanation": "..."
  }},
  {{
    "question": "...",
    "options": {{
      "A": "...",
      "B": "...",
      "C": "...",
      "D": "..."
    }},
    "correct_answer": "D",
    "explanation": "..."
  }}
]
"""

    # -----------------------------
    # Generate Quiz
    # -----------------------------
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=f"{system_instruction}\n\n{user_prompt}"
    )

    response_text = response.text.strip()

    # Remove markdown if Gemini accidentally returns it
    response_text = response_text.replace("```json", "")
    response_text = response_text.replace("```", "").strip()

    try:
        quiz_data = json.loads(response_text)
    except Exception:
        raise Exception(
            "Gemini did not return valid JSON.\n\n"
            f"Response:\n{response_text}"
        )

    return quiz_data, unified_context