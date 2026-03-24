# learn_skills
🚀 Project Overview: learn_skills (Login + Roadmap Generator)

This project is a full-stack web application built using Flask and MongoDB that allows users to register, log in, and generate personalized learning roadmaps based on their skills.

It is designed to help users track their learning journey and follow structured paths for technologies like Django, Python, and more.

🔥 Key Features
🔐 Authentication System
User registration and login
Passwords are securely stored using bcrypt hashing
Session-based authentication using Flask
🧠 Smart Roadmap Generator
Users can enter a skill (e.g., Django)
The system generates a structured learning roadmap
Includes:
📚 Topics to learn
🔗 Resource links
📊 Progress status (pending/completed)
📊 Dashboard
Displays user-specific data after login
Shows generated roadmaps
Tracks learning progress
🗄️ Database Integration
Uses MongoDB
Stores:
User data
Roadmaps
Progress tracking
🛠️ Tech Stack
Backend: Flask (Python)
Database: MongoDB
Frontend: HTML, CSS
Authentication: Flask sessions + Bcrypt
Libraries Used:
pymongo
flask-bcrypt
bson
📁 Project Structure
<img width="545" height="222" alt="image" src="https://github.com/user-attachments/assets/76a49f58-5d23-4030-b569-27bf1357946d" />
⚙️ How It Works
User registers → data stored in MongoDB
User logs in → session is created
User enters a skill → roadmap is generated
Roadmap is saved → displayed on dashboard
User can track progress of each topic
