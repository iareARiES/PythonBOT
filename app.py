

from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai  # Ensure this is the correct import for the genai library you are using
import config as config  # Assuming you have a config file where the API key is stored

app = Flask(__name__,template_folder='templates')

print("Current Working Directory:", os.getcwd())

template_dir = os.path.join(os.getcwd(), 'templates')
print("Templates Directory Files:", os.listdir(template_dir))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form.get("msg", "")  # Use get() to handle missing key scenarios
    response = get_Chat_response(msg)
    return jsonify({"response": response})

def get_Chat_response(text):
    # Set the API key from your config file
    os.environ["GEMINI_API_KEY"] = config.apikey
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    # Enhanced settings for a career counselor AI
    generation_config = {
        "temperature": 0.9,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 8000,  # Adjusted to a more reasonable value
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "You are a career counselor. Your role is to provide personalized advice on career paths based on the user's interests, skills, and market trends."
                    " Start by asking the user about their interests, skills, work environment preferences, and career goals. Use this information to offer detailed career guidance,"
                    " including current job market trends and a roadmap to achieve their career goals. Provide examples of potential career paths and ensure your advice is actionable and up-to-date.",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Hello! I’m here to assist you with career counseling. To provide the best advice, I need to understand your interests and goals."
                    " Please answer the following questions so I can help you further:"
                    "\n 1. What are your key interests and passions? (e.g., technology, teaching, art, medical)"
                    "\n 2. What skills and talents do you have? (e.g., problem-solving, communication, technical skills)"
                    "\n 3. What type of work environment do you prefer? (e.g., remote, team-based, fast-paced)"
                    "\n 4. What are your career goals? (e.g., financial success, making an impact, work-life balance)\n"
                    "Based on your responses, I’ll provide tailored advice on career paths, market trends, and a roadmap to achieve your career aspirations.",
                ],
            },
        ]
    )

    # Send user input to the chat session and receive a response
    response = chat_session.send_message(text)

 # Convert numbered lists to bullet points
    bullet_response = response.text.replace(r'\d+\.', '-')

    # Return the modified response with bullet points
    return bullet_response

if __name__ == "__main__":
    app.run(debug=True)
