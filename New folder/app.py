from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Function to generate a study plan
def generate_study_plan(subjects, deadlines, free_time):
    study_plan = []
    for subject, deadline in zip(subjects, deadlines):
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
        days_remaining = (deadline_date - datetime.now()).days
        if days_remaining <= 0:
            study_plan.append({
                "subject": subject,
                "deadline": deadline,
                "hours_per_day": "Deadline has passed",
                "days_remaining": 0
            })
        else:
            hours_per_day = free_time / len(subjects)
            study_plan.append({
                "subject": subject,
                "deadline": deadline,
                "hours_per_day": round(hours_per_day, 2),
                "days_remaining": days_remaining
            })
    return study_plan

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-plan', methods=['POST'])
def generate_plan():
    data = request.json
    subjects = data.get('subjects', [])
    deadlines = data.get('deadlines', [])
    free_time = data.get('freeTime', 0)

    if not subjects or not deadlines or free_time <= 0:
        return jsonify({'error': 'Invalid input. Please provide subjects, deadlines, and free time.'}), 400

    study_plan = generate_study_plan(subjects, deadlines, free_time)
    return jsonify({'plan': study_plan})

if __name__ == '__main__':
    app.run(debug=True)