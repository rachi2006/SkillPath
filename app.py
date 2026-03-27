from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# ---------------- MONGODB ATLAS CONNECTION ---------------- #
client = MongoClient(os.getenv("MONGO_URI"))
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
    
    elif "python" in skill_lower:
        return {
            "course_link": "https://docs.python.org/3/",
            "topics": [
            {"title": "Python Basics", "link": "https://docs.python.org/3/tutorial/", "status": "pending"},
            {"title": "Control Flow", "link": "https://docs.python.org/3/tutorial/controlflow.html", "status": "pending"},
            {"title": "Functions", "link": "https://docs.python.org/3/tutorial/functions.html", "status": "pending"},
            {"title": "OOP", "link": "https://docs.python.org/3/tutorial/classes.html", "status": "pending"},
            {"title": "Error Handling", "link": "https://docs.python.org/3/tutorial/errors.html", "status": "pending"},
            {"title": "Decorators", "link": "https://docs.python.org/3/glossary.html#term-decorator", "status": "pending"},
            {"title": "Async Programming", "link": "https://docs.python.org/3/library/asyncio.html", "status": "pending"},
            {"title": "Testing (PyTest)", "link": "https://docs.python.org/3/library/unittest.html", "status": "pending"},
            {"title": "Project: CLI Tool", "link": "https://docs.python.org/3/library/argparse.html", "status": "pending"},
            ]
        }
    
    elif "sql" in skill_lower:
        return {
            "course_link": "https://www.postgresql.org/docs/",
            "topics": [
            {"title": "SQL Basics", "link": "https://www.postgresql.org/docs/current/sql-syntax.html", "status": "pending"},
            {"title": "Data Types", "link": "https://www.postgresql.org/docs/current/datatype.html", "status": "pending"},
            {"title": "CRUD Operations", "link": "https://www.postgresql.org/docs/current/dml.html", "status": "pending"},
            {"title": "Joins", "link": "https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN", "status": "pending"},
            {"title": "Indexes", "link": "https://www.postgresql.org/docs/current/sql-createindex.html", "status": "pending"},
            {"title": "Transactions", "link": "https://www.postgresql.org/docs/current/tutorial-transactions.html", "status": "pending"},
            {"title": "Project: Simple Database", "link": "https://www.postgresql.org/docs/current/tutorial.html", "status": "pending"}
            ]
        }
    
    elif "mongodb" in skill_lower:
        return {
            "course_link": "https://www.mongodb.com/docs/",
            "topics": [
                {"title": "MongoDB Basics", "link": "https://www.mongodb.com/docs/manual/introduction/", "status": "pending"},
                {"title": "CRUD Operations", "link": "https://www.mongodb.com/docs/manual/crud/", "status": "pending"},
                {"title": "Indexes", "link": "https://www.mongodb.com/docs/manual/indexes/", "status": "pending"},
                {"title": "Aggregation", "link": "https://www.mongodb.com/docs/manual/aggregation/", "status": "pending"},
                {"title": "Replication & Sharding", "link": "https://www.mongodb.com/docs/manual/replication/", "status": "pending"},
                {"title": "Project: NoSQL Database", "link": "https://www.mongodb.com/docs/manual/tutorial/", "status": "pending"}
            ]
        }
    
    elif "data science" in skill_lower:
        return {
            "course_link": "https://www.coursera.org/specializations/data-science-python",
            "topics": [
                {"title": "Python for Data Science", "link": "https://www.coursera.org/learn/python-for-applied-data-science-ai", "status": "pending"},
                {"title": "Data Analysis with Pandas", "link": "https://pandas.pydata.org/docs/", "status": "pending"},
                {"title": "Data Visualization", "link": "https://matplotlib.org/stable/contents.html", "status": "pending"},
                {"title": "Machine Learning Basics", "link": "https://scikit-learn.org/stable/tutorial/basic/tutorial.html", "status": "pending"},
                {"title": "Project: Data Science Pipeline", "link": "https://www.kaggle.com/learn/data-science-projects", "status": "pending"}
            ]
        }

    elif "machine learning" in skill_lower:
        return {
            "course_link": "https://www.coursera.org/learn/machine-learning",
            "topics": [
                {"title": "ML Basics", "link": "https://www.coursera.org/learn/machine-learning", "status": "pending"},
                {"title": "Supervised Learning", "link": "https://scikit-learn.org/stable/supervised_learning.html", "status": "pending"},
                {"title": "Unsupervised Learning", "link": "https://scikit-learn.org/stable/unsupervised_learning.html", "status": "pending"},
                {"title": "Neural Networks", "link": "https://www.tensorflow.org/guide/keras/sequential_model", "status": "pending"},
                {"title": "Project: ML Model", "link": "https://www.kaggle.com/learn/machine-learning-projects", "status": "pending"}
            ]
        },

    elif "html" in skill_lower:
        return {
            "course_link": "https://developer.mozilla.org/en-US/docs/Web/HTML",
            "topics": [
                {"title": "HTML Basics", "link": "https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/HTML_basics", "status": "pending"},
                {"title": "HTML Document Structure", "link": "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/html", "status": "pending"},
                {"title": "Forms & Inputs", "link": "https://developer.mozilla.org/en-US/docs/Learn/Forms", "status": "pending"},
                {"title": "Semantic HTML", "link": "https://developer.mozilla.org/en-US/docs/Web/HTML/Element", "status": "pending"},
                {"title": "Meta Tags & SEO", "link": "https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/The_head_metadata_in_HTML", "status": "pending"},
                {"title": "Accessibility (a11y)", "link": "https://developer.mozilla.org/en-US/docs/Web/Accessibility", "status": "pending"},
                {"title": "Multimedia Elements", "link": "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio", "status": "pending"},
                {"title": "Project: Personal Website", "link": "https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/Howto_build_a_website", "status": "pending"}
            ]
        }

    elif "css" in skill_lower:
        return {
            "course_link": "https://developer.mozilla.org/en-US/docs/Web/CSS",
            "topics": [
                {"title": "CSS Basics", "link": "https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/CSS_basics", "status": "pending"},
                {"title": "Selectors & Specificity", "link": "https://developer.mozilla.org/en-US/docs/Web/CSS/Specificity", "status": "pending"},
                {"title": "Box Model", "link": "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Box_Model", "status": "pending"},
                {"title": "Flexbox", "link": "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Basic_Concepts_of_Flexbox", "status": "pending"},
                {"title": "Grid Layout", "link": "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout", "status": "pending"},
                {"title": "Responsive Design", "link": "https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design", "status": "pending"},
                {"title": "Animations & Transitions", "link": "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations/Using_CSS_animations", "status": "pending"},
                {"title": "Project: Portfolio Website", "link": "https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/Howto_build_a_website", "status": "pending"}
            ]
        }

    elif "javascript" in skill_lower:   
        {
            "course_link": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
            "topics": [
                {"title": "JS Basics", "link": "https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/JavaScript_basics", "status": "pending"},
                {"title": "Variables & Data Types", "link": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_types", "status": "pending"},
                {"title": "Functions", "link": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Functions", "status": "pending"},
                {"title": "Objects & Arrays", "link": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_with_Objects", "status": "pending"},
                {"title": "DOM Manipulation", "link": "https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction", "status": "pending"},
                {"title": "Event Handling", "link": "https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener", "status": "pending"},
                {"title": "ES6+ Features", "link": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import", "status": "pending"},
                {"title": "Asynchronous JS", "link": "https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous", "status": "pending"},
                {"title": "Promises & Callbacks", "link": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise", "status": "pending"},
                {"title": "Fetch API & AJAX", "link": "https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API", "status": "pending"},
                {"title": "JSON", "link": "https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON", "status": "pending"},
                {"title": "Project: Interactive Website", "link": "https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/Howto_build_a_website", "status": "pending"}
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