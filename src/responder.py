import openai
from src import config

openai.api_key = config.OPENAI_API_KEY

def generate_response(prompt):

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150,
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        return f"Error generating response: {e}"
