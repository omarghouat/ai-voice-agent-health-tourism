import openai

# Replace with your own key
openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a health tourism assistant helping users with medical travel queries."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
