from flask import Flask, render_template, request
from datetime import datetime
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="YOUR_GEMINI_API_KEY")  # Replace with your Gemini API key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-plan', methods=['POST'])
def generate_plan():
    # Get form data
    subject = request.form.get('subject')
    study_time = int(request.form.get('study_time'))
    deadline = request.form.get('deadline')

    # Calculate days left until the deadline
    deadline_date = datetime.strptime(deadline, '%Y-%m-%d')
    today = datetime.today()
    days_left = (deadline_date - today).days

    # Validate inputs
    if days_left <= 0:
        error_message = "Invalid deadline. Please choose a future date."
        return render_template('index.html', error_message=error_message)

    if study_time <= 0:
        error_message = "Study time must be greater than 0."
        return render_template('index.html', error_message=error_message)

    # Generate study plan using Gemini API
    study_plan = generate_study_plan_with_gemini(subject, study_time, days_left)

    return render_template('plan.html', study_plan=study_plan)

def generate_study_plan_with_gemini(subject, study_time, days_left):
    # Create a prompt for Gemini
    prompt = f"""
    Create a detailed study plan for the subject: {subject}.
    Total study time: {study_time} hours.
    Days left until the deadline: {days_left}.
    Provide actionable steps, time allocation, and tips for effective studying.
    """

    # Use Gemini to generate the study plan
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)

    # Return the generated study plan
    return response.text

if __name__ == '__main__':
    app.run(debug=True)