Voice Assistant (Django + Python)
A powerful and flexible Voice Assistant web application built using Django and Python. This assistant uses speech commands to perform a wide range of productivity tasks—open apps, fetch the weather, tell jokes, control files, automate reminders, and much more.

![Voice Assistant Screenshot](Screenshot-2025-07-24-065640.jpg

Natural language recognition from microphone input

Open applications (Word, Chrome, VLC, Notepad, VS Code)

Fetch weather and current time

Play music/videos (e.g., YouTube)

File and folder management (create, delete, write notes, screenshots)

WhatsApp messaging and calling (via command)

Google and AI news search

Custom reminders and task automation

Shutdown system

Easy extensibility for new commands

🛠️ Setup Instructions
Follow these commands to set up your environment (tested on Windows):

bash
# 1. Create a virtual environment
python -m venv fullstack

# 2. Activate the virtual environment
fullstack\Scripts\activate   # On Windows

# 3. Install dependencies (Django, etc.)
pip install -r requirements.txt

# 4. Start the Django development server
py manage.py runserver
If you encounter DLL load errors for TensorFlow, install the Microsoft C++ Redistributable and use Python 3.10/3.9 with TensorFlow 2.x.

💬 Example Commands
Open applications:
Open Word, Chrome, VLC, Notepad

Open a folder in VS Code:
Open folder Projects from Documents on VS Code

Check if a number is prime:
Generate code to check if a number is prime

Fun:
Tell me a joke, Crack a joke

Weather and Time:
What's the weather?, What time is it?

Media Controls:
Play Imagine Dragons on YouTube, Play music

System Utils:
Take a screenshot, Create folder NewFolder,
Create file readme.txt, Delete oldfile.txt

Reminders:
Remind me to drink water in 5 minutes

Notes:
Write a note

WhatsApp Integration:
Send a WhatsApp message, Call anyone on WhatsApp

Shutdown:
Shutdown

Search:
Google search AI news

Music Apps:
Open Spotify
