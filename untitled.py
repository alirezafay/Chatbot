#################################################
from flask import Flask, request, jsonify, render_template
import requests
import json
import os



app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"


#### DATA

def load_json_from_google_drive(file_id):
    # Google Drive direct download link format
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            raise Exception("The file is not a valid JSON format.")
    else:
        raise Exception(f"Failed to download JSON: {response.status_code}")
file_id = "1kqCbNDU_Lfld9YRXTdaSX-4h8LaObDdV"  
user_data = load_json_from_google_drive(file_id)

# Example: Access personal details
#print("Name:", user_data["Personal Information"]["name"])
#print("Job Title:", user_data["career"]["job title"])

context = f"""
User Profile:
- Name: {user_data['Personal Information']['name']}
- Age: {user_data['Personal Information']['age']}
- Occupation: {user_data['career']['job title']}
- Industry: {user_data['career']['Current job']}
- Skills: {", ".join(user_data['career']['skills'])}
- Achievements: {", ".join(user_data['career']['achievements'])}

Instructions:
- Use this profile when answering any question.
- Respond with business-related insights based on the user's expertise.
- Provide personalized guidance using their past achievements.

User Question: INSERT_USER_QUESTION_HERE
"""

def generate_response(user_question):
    # Inject user profile context into the request
    prompt = context.replace("INSERT_USER_QUESTION_HERE", user_question)
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}

    response = requests.post(URL, json=payload, headers=headers)
    
    #Check if AI response contains valid output
    response_json = response.json()
    if "candidates" in response.json():
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return "Error: No AI response received."
        
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_question = data["question"]
    response = generate_response(user_question)
    return jsonify({"response": response})
    
@app.route("/")    
def home():
    return render_template("index.html")
#print(app.url_map)
#
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
