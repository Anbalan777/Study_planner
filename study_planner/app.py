from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Store subjects and topics in a dictionary
subjects_data = {}

@app.route("/")
def index():
    return render_template("index.html", subjects=subjects_data)

@app.route("/add_subject", methods=["POST"])
def add_subject():
    subject = request.form.get("subject")
    topics = request.form.getlist("topics[]")
    difficulty_levels = request.form.getlist("difficulty[]")

    if not subject or not topics or not difficulty_levels:
        return jsonify({"success": False, "error": "All fields are required"}), 400

    # Store topics and difficulty levels for the subject
    subjects_data[subject] = []
    for topic, difficulty in zip(topics, difficulty_levels):
        subjects_data[subject].append({"topic": topic, "difficulty": difficulty})

    return redirect(url_for("index"))

@app.route("/get_study_plan", methods=["POST"])
def get_study_plan():
    data = request.json
    subject = data.get("subject")
    deadline = data.get("deadline")
    study_time = data.get("study_time")

    # Validate input
    if not subject or not deadline or not study_time:
        return jsonify({"success": False, "error": "All fields are required"}), 400

    try:
        # Convert study_time to float
        study_time = float(study_time)

        # Convert deadline to a datetime object
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
        current_date = datetime.now()

        # Calculate the number of days until the deadline
        days_until_deadline = (deadline_date - current_date).days

        if days_until_deadline < 0:
            return jsonify({"success": False, "error": "Deadline has already passed"}), 400

        # Generate study advice and schedule
        advice = generate_study_advice(subject, study_time, days_until_deadline)
        schedule = generate_study_schedule(subject, study_time, days_until_deadline)

        return jsonify({
            "success": True,
            "advice": advice,
            "schedule": schedule
        })
    except ValueError as e:
        return jsonify({"success": False, "error": f"Invalid input: {str(e)}"}), 400

def generate_study_advice(subject, study_time, days_until_deadline):
    """
    Generate detailed study advice based on subject, study time, and days until deadline.
    """
    if days_until_deadline == 0:
        return f"Your deadline for {subject} is today! Focus on quick revision and key concepts."

    # Calculate daily study time
    daily_study_time = study_time / days_until_deadline

    # Get topics for the subject
    topics = subjects_data.get(subject, [])

    # Sort topics by difficulty (hard -> medium -> easy)
    topics.sort(key=lambda x: {"hard": 0, "medium": 1, "easy": 2}[x["difficulty"]])

    # Generate study plan
    study_plan = (
        f"For the subject '{subject}', you have {days_until_deadline} days until your deadline. "
        f"Allocate approximately {daily_study_time:.1f} hours per day.\n\n"
        f"**Where to Start**: Begin with the most challenging topics.\n"
        f"**Topics to Study First**:\n"
    )

    # Add topics to the study plan
    for i, topic_data in enumerate(topics, 1):
        study_plan += f"{i}. {topic_data['topic']} ({topic_data['difficulty'].capitalize()})\n"

    # Add study techniques
    study_plan += (
        "\n**How to Study**:\n"
        "1. **Understand Concepts**: Read the theory and make notes.\n"
        "2. **Practice Problems**: Solve problems related to each topic.\n"
        "3. **Revise Regularly**: Review your notes and key concepts daily.\n"
        "4. **Take Breaks**: Study in chunks of 25-30 minutes with 5-minute breaks.\n"
        "5. **Use Flashcards**: For memorizing key terms and formulas.\n"
        "6. **Teach Someone**: Explain concepts to a friend or yourself to reinforce learning."
    )

    return study_plan

def generate_study_schedule(subject, study_time, days_until_deadline):
    """
    Generate a daily study schedule for the given subject.
    """
    if days_until_deadline == 0:
        return []

    # Get topics for the subject
    topics = subjects_data.get(subject, [])

    # Sort topics by difficulty (hard -> medium -> easy)
    topics.sort(key=lambda x: {"hard": 0, "medium": 1, "easy": 2}[x["difficulty"]])

    # Calculate daily study time
    daily_study_time = study_time / days_until_deadline

    # Distribute topics across days
    schedule = []
    for day in range(1, days_until_deadline + 1):
        day_schedule = {
            "day": day,
            "topics": [],
            "study_time": daily_study_time
        }

        # Assign topics to the day
        if topics:
            day_schedule["topics"].append(topics.pop(0))  # Assign one topic per day

        schedule.append(day_schedule)

    return schedule

if __name__ == "__main__":
    app.run(debug=True)