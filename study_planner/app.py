from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

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

    # Generate study plan
    study_plan = generate_study_plan(subject, study_time, days_left)

    return render_template('plan.html', study_plan=study_plan)

def generate_study_plan(subject, study_time, days_left):
    # Calculate daily study time
    daily_study_time = study_time / days_left

    # Generate actionable steps
    plan = f"""
    <h2>Study Plan for {subject}</h2>
    <p><strong>Days Left:</strong> {days_left}</p>
    <p><strong>Total Study Time:</strong> {study_time} hours</p>
    <p><strong>Daily Study Time:</strong> {daily_study_time:.2f} hours/day</p>
    <h3>Actionable Steps:</h3>
    <ol>
        <li>Divide the syllabus into {days_left} parts.</li>
        <li>Spend {daily_study_time:.2f} hours each day studying {subject}.</li>
        <li>Focus on understanding key concepts and practicing problems.</li>
        <li>Revise the entire syllabus at least once before the exam.</li>
        <li>Take short breaks every 45 minutes to stay focused.</li>
    </ol>
    """
    return plan

if __name__ == '__main__':
    app.run(debug=True)