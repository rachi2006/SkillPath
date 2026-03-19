from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- MONGODB ATLAS CONNECTION ---------------- #
client = MongoClient("mongodb+srv://rachirachith8_db_user:CoNTW3p0h3l3LNiz@cluster0.xpnndxx.mongodb.net/?appName=Cluster0")
db = client["logindata"]
users = db["users"]
roadmaps = db["roadmaps"]

bcrypt = Bcrypt(app)

# ---------------- ROADMAP GENERATOR ---------------- #
def generate_roadmap(skill):
    skill_lower = skill.lower()

    if "django" in skill_lower:
        return {
            "course_link": "https://docs.djangoproject.com/en/stable/",
            "topics": [
                {"title": "Python Basics", "link": "https://docs.python.org/3/", "status": "pending"},
                {"title": "Django Introduction", "link": "https://docs.djangoproject.com/en/stable/intro/", "status": "pending"},
                {"title": "Project Setup", "link": "https://docs.djangoproject.com/en/stable/intro/tutorial01/", "status": "pending"},
                {"title": "Models & Database", "link": "https://docs.djangoproject.com/en/stable/topics/db/models/", "status": "pending"},
                {"title": "Views & URLs", "link": "https://docs.djangoproject.com/en/stable/topics/http/views/", "status": "pending"},
                {"title": "Templates", "link": "https://docs.djangoproject.com/en/stable/topics/templates/", "status": "pending"},
                {"title": "Authentication", "link": "https://docs.djangoproject.com/en/stable/topics/auth/", "status": "pending"},
                {"title": "Deployment", "link": "https://docs.djangoproject.com/en/stable/howto/deployment/", "status": "pending"}
            ]
        }

    elif "flask" in skill_lower:
        return {
            "course_link": "https://flask.palletsprojects.com/",
            "topics": [
                {"title": "Python Basics", "link": "https://docs.python.org/3/", "status": "pending"},
                {"title": "Flask Basics", "link": "https://flask.palletsprojects.com/en/stable/quickstart/", "status": "pending"},
                {"title": "Routing", "link": "https://flask.palletsprojects.com/en/stable/quickstart/#routing", "status": "pending"},
                {"title": "Templates", "link": "https://jinja.palletsprojects.com/", "status": "pending"},
                {"title": "Forms", "link": "https://wtforms.readthedocs.io/", "status": "pending"},
                {"title": "Authentication", "link": "https://flask-login.readthedocs.io/", "status": "pending"},
                {"title": "REST API", "link": "https://flask-restful.readthedocs.io/", "status": "pending"},
                {"title": "Deployment", "link": "https://render.com/", "status": "pending"}
            ]
        }

    else:
        return {
            "course_link": f"https://www.google.com/search?q={skill}+documentation",
            "topics": [
                {"title": f"Introduction to {skill}", "link": f"https://www.google.com/search?q={skill}+introduction", "status": "pending"},
                {"title": "Core Concepts", "link": f"https://www.google.com/search?q={skill}+core+concepts", "status": "pending"},
                {"title": "Projects", "link": f"https://www.google.com/search?q={skill}+projects", "status": "pending"}
            ]
        }

# ---------------- AUTH ROUTES ---------------- #
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier')
        password = request.form.get('password')

        user = users.find_one({
            "$or": [{"email": identifier}, {"username": identifier}]
        })

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid Credentials ❌")

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user already exists
        if users.find_one({"$or": [{"email": email}, {"username": username}]}):
            return render_template('register.html', error="User already exists ❌")

        hashed = bcrypt.generate_password_hash(password).decode('utf-8')

        users.insert_one({
            "username": username,
            "email": email,
            "password": hashed,
            "bio": "No bio yet",
            "education": "Not added",
            "college": "Not added"
        })

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------------- DASHBOARD ---------------- #
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        skill = request.form.get('skill')
        data = generate_roadmap(skill)

        roadmaps.insert_one({
            "user": session['user'],
            "skill": skill,
            "course_link": data["course_link"],
            "topics": data["topics"]
        })

    user_data = users.find_one({"username": session['user']})
    user_roadmaps = list(roadmaps.find({"user": session['user']}))
    count = roadmaps.count_documents({"user": session['user']})

    total_topics = 0
    completed_topics = 0

    for r in user_roadmaps:
        for t in r['topics']:
            total_topics += 1
            if t['status'] == "completed":
                completed_topics += 1

    progress = int((completed_topics / total_topics) * 100) if total_topics > 0 else 0

    return render_template(
        'dashboard.html',
        roadmaps=user_roadmaps,
        user=user_data,
        count=count,
        progress=progress
    )

# ---------------- UPDATE TOPIC ---------------- #
@app.route('/update_status/<roadmap_id>/<int:index>')
def update_status(roadmap_id, index):
    roadmap = roadmaps.find_one({"_id": ObjectId(roadmap_id)})

    topics = roadmap['topics']
    topics[index]['status'] = "completed" if topics[index]['status'] == "pending" else "pending"

    roadmaps.update_one(
        {"_id": ObjectId(roadmap_id)},
        {"$set": {"topics": topics}}
    )

    return redirect(url_for('dashboard'))

# ---------------- DELETE ---------------- #
@app.route('/delete/<roadmap_id>')
def delete(roadmap_id):
    roadmaps.delete_one({"_id": ObjectId(roadmap_id)})
    return redirect(url_for('dashboard'))

# ---------------- EDIT PROFILE ---------------- #
@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    if 'user' not in session:
        return redirect(url_for('login'))

    users.update_one(
        {"username": session['user']},
        {"$set": {
            "bio": request.form.get('bio'),
            "education": request.form.get('education'),
            "college": request.form.get('college')
        }}
    )

    return redirect(url_for('dashboard'))

# ---------------- RUN ---------------- #
if __name__ == '__main__':
    app.run(debug=True)