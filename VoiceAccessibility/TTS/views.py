from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import os
import subprocess
import shutil
import datetime
import urllib.parse
import requests
import pyttsx3
import pywhatkit
import webbrowser
import pyjokes
import pyautogui
import speech_recognition as sr
from bs4 import BeautifulSoup
from django.shortcuts import render
import re

# ========== CONFIGURATION ==========
GEMINI_API_KEY = "AIzaSyD5eAYRj9Db29f4KCzCv5CMxEh5K2GIdwY"
GEMINI_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}'
WEATHER_API_KEY = "0d7f551109ba7c4d548985f2e8cea6f8"

# System and additional app paths
system_apps = {
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "files": r"explorer.exe",
    "v s code": r"C:\Users\selen\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "notepad": "notepad.exe",
    "explorer": "explorer.exe",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "camera": "start microsoft.windows.camera:",
    "microsoft store": "start ms-windows-store:",
    "settings": "start ms-settings:",
    "spotify": r"C:\Users\selenAppData\Roaming\Spotify\Spotify.exe",
    "whatsapp": r"C:\Users\selen\AppData\Local\WhatsApp\WhatsApp.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "vlc": r"C:\Program Files\VideoLAN\VLC\vlc.exe"
}

web_links = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
    "whatsapp": "https://web.whatsapp.com",
    "gmail": "https://mail.google.com",
    "reddit": "https://www.reddit.com",
    "spotify": "https://open.spotify.com",
    "stackoverflow": "https://stackoverflow.com",
    "twitter": "https://twitter.com",
    "facebook": "https://facebook.com",
    "copilot": "https://copilot.microsoft.com",
    "amazon": "https://www.amazon.in",
    "flipkart": "https://www.flipkart.com",
    "meesho": "https://www.meesho.com",
    "ajio": "https://www.ajio.com",
    "myntra": "https://www.myntra.com",
    "nykaa": "https://www.nykaa.com",
    "snapdeal": "https://www.snapdeal.com",
    "jiomart": "https://www.jiomart.com",
    "bigbasket": "https://www.bigbasket.com",
    "grofers": "https://blinkit.com",
     "dmart": "https://www.dmart.in",
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
    "whatsapp": "https://web.whatsapp.com",
    "gmail": "https://mail.google.com",
    "reddit": "https://www.reddit.com",
    "spotify": "https://open.spotify.com",
    "stackoverflow": "https://stackoverflow.com",
    "twitter": "https://twitter.com",
    "facebook": "https://facebook.com",
    "youtube": "https://www.youtube.com",
    "hotstar": "https://www.hotstar.com/in",
    "netflix": "https://www.netflix.com",
    "prime video": "https://www.primevideo.com",
    "sonyliv": "https://www.sonyliv.com",
    "zee5": "https://www.zee5.com",
    "mx player": "https://www.mxplayer.in",
    "voot": "https://www.voot.com",
    "aha": "https://www.aha.video",
    "movierulz": "https://www.movierulz.vc",  
    "ibomma": "https://www.ibomma.day" ,
    "spotify": "https://open.spotify.com",
    "youtube music": "https://music.youtube.com",
    "gaana": "https://gaana.com",
    "wynk": "https://wynk.in/music",
    "jiosaavn": "https://www.jiosaavn.com",
    "coursera": "https://www.coursera.org",
    "udemy": "https://www.udemy.com",
    "edx": "https://www.edx.org",
    "nptel": "https://nptel.ac.in",
    "khan academy": "https://www.khanacademy.org",
    "w3schools": "https://www.w3schools.com",
    "geeks for geeks": "https://www.geeksforgeeks.org",
    "stackoverflow": "https://stackoverflow.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://twitter.com",
    "telegram": "https://web.telegram.org",
    "whatsapp": "https://web.whatsapp.com",
    "linkedin": "https://www.linkedin.com",
    "threads": "https://www.threads.net"

    
}

contacts = {
    "varshi": "+919876543210",
    "anjali": "+917654321098"
}

engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass

def listen():
    recog = sr.Recognizer()
    with sr.Microphone() as source:
        recog.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recog.listen(source, timeout=5, phrase_time_limit=6)
            command = recog.recognize_google(audio).lower().strip()
            return command
        except:
            return ""

def get_path(location):
    user = os.environ['USERPROFILE']
    one = os.path.join(user, 'OneDrive')
    folders = {
        "desktop": "Desktop",
        "documents": "Documents",
        "downloads": "Downloads",
        "pictures": "Pictures",
        "gallery": "Pictures",
        "music": "Music",
        "videos": "Videos"
    }
    name = folders.get(location.lower().strip(), "Desktop")
    path = os.path.join(user, name)
    alt = os.path.join(one, name)
    return path if os.path.exists(path) else alt if os.path.exists(alt) else user

def gemini_generate(prompt):
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        res = requests.post(GEMINI_URL, headers={"Content-Type": "application/json"}, json=payload, timeout=15)
        if res.status_code == 200:
            candidates = res.json().get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "⚠️ No response.")
            return "⚠️ Empty response."
        else:
            return f"⚠️ Gemini error: {res.text}"
    except Exception as e:
        return f"⚠️ Gemini exception: {e}"

def open_app(app_name):
    app_name = app_name.lower()
    if app_name in system_apps:
        path = system_apps[app_name]
        try:
            if path.startswith("start "):
                subprocess.run(path, shell=True)
            else:
                subprocess.Popen([path])
            speak(f"Opening {app_name}")
            return True
        except Exception as e:
            speak(f"Failed to open {app_name}: {e}")
            return False
    speak(f"App {app_name} not found.")
    return False

def open_file_or_folder(target, location="desktop", app=None):
    base_path = get_path(location)
    for root, dirs, files in os.walk(base_path):
        for dir in dirs:
            if dir.lower() == target.lower():
                full = os.path.join(root, dir)
                try:
                    if app and app in system_apps:
                        app_path = system_apps[app]
                        subprocess.Popen([app_path, full])
                        speak(f"Opened folder {target} in {app}")
                    else:
                        os.startfile(full)
                        speak(f"Opened folder {target}")
                    return True
                except Exception as e:
                    speak(f"Could not open folder: {e}")
                    return False
        break
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.lower() == target.lower() or file.lower().startswith(target.lower()):
                full = os.path.join(root, file)
                try:
                    if app and app in system_apps:
                        app_path = system_apps[app]
                        subprocess.Popen([app_path, full])
                        speak(f"Opened file {target} in {app}")
                    else:
                        os.startfile(full)
                        speak(f"Opened file {target}")
                    return True
                except Exception as e:
                    speak(f"Could not open file: {e}")
                    return False
        break
    speak(f"{target} does not exist in {location}.")
    return False

def create_folder(folder, location="desktop"):
    path = get_path(location)
    full = os.path.join(path, folder)
    try:
        if os.path.exists(full):
            speak(f"Folder {folder} already exists.")
            return False
        os.makedirs(full)
        speak(f"Created folder {folder}")
        return True
    except Exception as e:
        speak(f"Failed to create folder: {e}")
        return False

def create_file(filename, location="desktop"):
    path = get_path(location)
    full = os.path.join(path, filename)
    try:
        if os.path.exists(full):
            speak(f"File {filename} already exists.")
            return False
        with open(full, "w") as f:
            f.write("Voice created file.")
        speak(f"Created file {filename}")
        return True
    except Exception as e:
        speak(f"Failed to create file: {e}")
        return False

def delete_item(item, location="desktop"):
    path = get_path(location)
    for root, dirs, files in os.walk(path):
        for name in files + dirs:
            if name.lower() == item.lower():
                full_path = os.path.join(root, name)
                try:
                    if os.path.isfile(full_path):
                        os.remove(full_path)
                    elif os.path.isdir(full_path):
                        shutil.rmtree(full_path)
                    speak(f"Deleted {item}.")
                    return True
                except Exception as e:
                    speak("Couldn't delete the item.")
                    return False
        break
    speak("Item not found to delete.")
    return False

def get_weather_google(city="guntur"):
    try:
        url = f"https://www.google.com/search?q=weather+{city}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        temp_elem = soup.find("span", {"id": "wob_tm"})
        if temp_elem is None:
            raise ValueError("Temperature element not found")
        print(f"Current temperature in {city}: {temp_elem.text}°C")
    except Exception as e:
        print(f"Could not fetch weather data: {e}")
        # Redirect to Google weather page
        webbrowser.open(f"https://www.google.com/search?q=weather+{city}")

def google_search(command):
    search = command.replace("google", "").replace("search", "").strip()
    if search:
        webbrowser.open(f"https://www.google.com/search?q={search}")
        speak(f"Searching for {search}")
    else:
        speak("What do you want me to search?")

def take_note():
    speak("What should I write?")
    note = listen()
    if note:
        filename = f"note_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = os.path.join(os.getcwd(), filename)
        with open(filepath, "w") as f:
            f.write(note)
        speak(f"Note saved as {filename}")

def set_reminder():
    speak("What should I remind you about?")
    msg = listen()
    speak("In how many minutes?")
    try:
        minutes = int(listen())
        speak(f"Reminder set for {minutes} minutes.")
        import threading
        def remind_later():
            import time
            time.sleep(minutes * 60)
            speak(f"🔔 Reminder: {msg}")
        threading.Thread(target=remind_later).start()
    except:
        speak("Could not set reminder.")

def play_music():
    music_folder = get_path("music")
    found = False
    for file in os.listdir(music_folder):
        if file.endswith(".mp3"):
            os.startfile(os.path.join(music_folder, file))
            speak(f"Playing {file}")
            found = True
            break
    if not found:
        speak("No MP3 found.")

def open_camera():
    try:
        subprocess.run("start microsoft.windows.camera:", shell=True)
        speak("Camera opened.")
    except:
        speak("Couldn't open camera.")

def send_whatsapp_message():
    speak("Who should I message?")
    person = listen()
    number = contacts.get(person)
    if not number:
        speak("Number not found. Say the number with +91")
        number = listen()
    speak("What is the message?")
    msg = listen()
    try:
        pywhatkit.sendwhatmsg_instantly(number, msg)
        speak("Message sent.")
    except:
        speak("Something went wrong.")

def whatsapp_call(command):
    for name in contacts:
        if name in command:
            webbrowser.open(f"https://wa.me/{contacts[name]}")
            speak(f"Calling {name} on WhatsApp")
            return True
    return False

def open_any(command):
    # First check websites
    for name, url in web_links.items():
        if name in command:
            webbrowser.open(url)
            speak(f"Opening {name}")
            return True
    # Check hardcoded apps
    for name, path in system_apps.items():
        if name in command:
            try:
                if path.startswith("start "):
                    subprocess.run(path, shell=True)
                else:
                    subprocess.Popen([path])
                speak(f"Opening {name}")
                return True
            except:
                speak(f"Failed to open {name}")
                return False
    speak("I couldn’t find or open that.")
    return False

# MAIN DJANGO VIEW
def result2(request):
    recognized_text = ""
    generated_code = ""
    suggestion_prompt = ""
    ask_app = False
    pending_target = ""
    pending_location = ""

    if request.method == "POST":
        try:
            recog = sr.Recognizer()
            with sr.Microphone() as source:
                recog.adjust_for_ambient_noise(source)
                audio = recog.listen(source, timeout=5)
            recognized_text = recog.recognize_google(audio).lower().strip()

            # Session follow-up for app choice
            if "pending_open" in request.session:
                pending = request.session["pending_open"]
                app = recognized_text.strip()
                target = pending["target"]
                location = pending["location"]
                opened = open_file_or_folder(target, location, app)
                if not opened:
                    suggestion_prompt = f"{target} does not exist in {location}."
                del request.session["pending_open"]
                return render(request, "result2.html", {
                    "recognized_text": recognized_text,
                    "generated_code": generated_code,
                    "suggestion_prompt": suggestion_prompt,
                    "ask_app": False
                })

            # Shutdown system
            if "shutdown" in recognized_text:
                speak("Shutting system.")
                os.system("shutdown /s /t 5")
                return render(request, "result2.html", {
                    "recognized_text": recognized_text,
                    "generated_code": generated_code,
                    "suggestion_prompt": "System shutdown initiated.",
                    "ask_app": ask_app,
                })

            # Stop or exit
            if "exit" in recognized_text or "stop" in recognized_text:
                speak("Goodbye")
                return render(request, "result2.html", {
                    "recognized_text": recognized_text,
                    "generated_code": generated_code,
                    "suggestion_prompt": "Session ended.",
                    "ask_app": ask_app,
                })

            # Take note
            if "note" in recognized_text or "write" in recognized_text:
                take_note()
                return render(request, "result2.html", {
                    "recognized_text": recognized_text,
                    "generated_code": generated_code,
                    "suggestion_prompt": "Note saved.",
                    "ask_app": ask_app,
                })

            # Set reminder
            if "remind" in recognized_text or "reminder" in recognized_text:
                set_reminder()
                return render(request, "result2.html", {
                    "recognized_text": recognized_text,
                    "generated_code": generated_code,
                    "suggestion_prompt": "Reminder set.",
                    "ask_app": ask_app,
                })

            # Play music
            if "music" in recognized_text or "song" in recognized_text:
                play_music()
                return render(request, "result2.html", {
                    "recognized_text": recognized_text,
                    "generated_code": generated_code,
                    "suggestion_prompt": "Playing music.",
                    "ask_app": ask_app,
                })

            # Camera
            if "camera" in recognized_text:
                open_camera()
                return render(request, "result2.html", {
                    "recognized_text": recognized_text,
                    "generated_code": generated_code,
                    "suggestion_prompt": "Camera opened.",
                    "ask_app": ask_app,
                })

            # WhatsApp message
            if "message" in recognized_text:
                send_whatsapp_message()
                return render(request, "result2.html", {
                    "recognized_text": recognized_text,
                    "generated_code": generated_code,
                    "suggestion_prompt": "Message sent.",
                    "ask_app": ask_app,
                })

            # WhatsApp call
            if "call" in recognized_text:
                if not whatsapp_call(recognized_text):
                    speak("Contact not found.")
                return render(request, "result2.html", {
                    "recognized_text": recognized_text,
                    "generated_code": generated_code,
                    "suggestion_prompt": "Call initiated." if whatsapp_call(recognized_text) else "Contact not found.",
                    "ask_app": ask_app,
                })

            # Code generation
            if recognized_text.startswith("generate code"):
                prompt = recognized_text.replace("generate code", "").strip()
                if prompt:
                    generated_code = gemini_generate(f"Generate a single Python code for: {prompt} without any explanation")
                    suggestion_prompt = "💡 Try: 'Generate code to check prime number.'"
                    speak("Here is the code generated.")
                else:
                    generated_code = "⚠️ Specify what code to generate."
                    speak(generated_code)

            # Gemini joke
            elif "joke" in recognized_text:
                joke = gemini_generate(recognized_text)
                speak(joke)
                return render(request, "result2.html", {
                    "recognized_text": recognized_text,
                    "generated_code": generated_code,
                    "suggestion_prompt": suggestion_prompt,
                    "ask_app": ask_app,
                })

          

            # Weather
            elif "weather" in recognized_text:
                # Try to extract city from the recognized_text, fallback to Hyderabad
                city_match = re.search(r'weather in ([a-zA-Z\s]+)', recognized_text)
                city = city_match.group(1).strip() if city_match else "Hyderabad"
                weather_str = get_weather_google(city)
                speak(weather_str)  # <-- Ensures it is spoken out loud!
                return render(request, "result2.html", {
                    "recognized_text": recognized_text,
                    "generated_code": generated_code,
                    "suggestion_prompt": weather_str,
                    "ask_app": ask_app,
                })


            # Time
            elif "time" in recognized_text:
                now = datetime.datetime.now().strftime('%I:%M %p')
                speak(f"The time is {now}")
                return render(request, "result2.html", {
                    "recognized_text": recognized_text,
                    "generated_code": generated_code,
                    "suggestion_prompt": suggestion_prompt,
                    "ask_app": ask_app,
                })

            # Screenshot
            elif "screenshot" in recognized_text:
                img = pyautogui.screenshot()
                img.save(os.path.join(os.getcwd(), "screenshot.png"))
                speak("Screenshot saved.")

            # Play on YouTube
            elif recognized_text.startswith("play") and "spotify" not in recognized_text:
                song = recognized_text.replace("play", "").strip()
                pywhatkit.playonyt(song)
                speak(f"Playing {song} on YouTube.")

            # Play on Spotify
            elif recognized_text.startswith("play") and "spotify" in recognized_text:
                song = recognized_text.replace("play", "").replace("on spotify", "").strip()
                url = f"https://open.spotify.com/search/{urllib.parse.quote_plus(song)}"
                webbrowser.open(url)
                speak(f"Searching for {song} on Spotify.")

            # Open system app
            elif recognized_text.startswith("open "):
                app_name = recognized_text.replace("open", "").replace("app", "").strip()
                if open_app(app_name):
                    return render(request, "result2.html", {
                        "recognized_text": recognized_text,
                        "generated_code": generated_code,
                        "suggestion_prompt": suggestion_prompt,
                        "ask_app": ask_app,
                    })
                else:
                    # Try to open as a website if not found in system apps
                    url = f"https://www.{app_name.replace(' ', '')}.com"
                    webbrowser.open(url)
                    speak(f"Opening {app_name} in browser.")
                    return render(request, "result2.html", {
                        "recognized_text": recognized_text,
                        "generated_code": generated_code,
                        "suggestion_prompt": f"Opened {app_name} in browser.",
                        "ask_app": ask_app,
                    })


            # Open file or folder (interactive)
            match = re.match(r"open (folder|file) (.+?)(?: from ([\w\s]+))?(?: on (\w+))?$", recognized_text)
            if match:
                kind, target, location, app = match.groups()
                target = target.strip()
                location = location.strip() if location else "desktop"
                app = app.strip() if app else None
                if not app:
                    speak("Where should I open it? For example, say vscode, notepad, excel, word, or explorer.")
                    request.session["pending_open"] = {"target": target, "location": location}
                    ask_app = True
                    pending_target = target
                    pending_location = location
                else:
                    opened = open_file_or_folder(target, location, app)
                    if not opened:
                        suggestion_prompt = f"{target} does not exist in {location}."
                return render(request, "result2.html", {
                    "recognized_text": recognized_text,
                    "generated_code": generated_code,
                    "suggestion_prompt": suggestion_prompt,
                    "ask_app": ask_app,
                    "pending_target": pending_target,
                    "pending_location": pending_location,
                })

            # Create folder
            elif recognized_text.startswith("create folder"):
                folder = recognized_text.replace("create folder", "").strip()
                create_folder(folder)

            # Create file
            elif recognized_text.startswith("create file"):
                filename = recognized_text.replace("create file", "").strip()
                create_file(filename)

            # Delete item
            elif recognized_text.startswith("delete"):
                item = recognized_text.replace("delete", "").strip()
                delete_item(item)

            # Open web links (only explicit)
            elif any(site in recognized_text for site in web_links):
                for site in web_links:
                    if site in recognized_text:
                        webbrowser.open(web_links[site])
                        speak(f"Opened {site}")
                        break

            # Google search fallback and improved search/app/web handling
            elif "search" in recognized_text or "google" in recognized_text:
                google_search(recognized_text)

            # Open any mapped app or website
            else:
                open_any(recognized_text)

        except sr.UnknownValueError:
            recognized_text = "🎧 Could not understand audio."
        except sr.RequestError:
            recognized_text = "⚠️ Speech recognition service unavailable."
        except Exception as e:
            recognized_text = f"⚠️ Internal error: {str(e)}"

    else:
        recognized_text = "Press the microphone button and speak."

    return render(request, "result2.html", {
        "recognized_text": recognized_text,
        "generated_code": generated_code,
        "suggestion_prompt": suggestion_prompt,
        "ask_app": ask_app,
        "pending_target": pending_target,
        "pending_location": pending_location,
    })


































def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    extracted_text = ""
    for page in doc:
        extracted_text += page.get_text("text")
    doc.close()
    return extracted_text.strip()

def extract_text_from_image(file_path):
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img)
    return text.strip()


def home(request):
    return render(request, 'home.html')


def result(request):
    if request.method == 'POST':
        input_type = request.POST.get('input_type')
        extracted_text = ""
        if input_type == 'text':
            extracted_text = request.POST.get('input_text', '').strip()
            if not extracted_text:
                extracted_text = "No text was provided."
        elif input_type == 'pdf' and request.FILES.get('pdf_file'):
            pdf_file = request.FILES['pdf_file']
            file_path = default_storage.save('temp/' + pdf_file.name, pdf_file)
            abs_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
            try:
                extracted_text = extract_text_from_pdf(abs_file_path)
            except Exception as e:
                extracted_text = f"Error extracting text: {e}"
            if os.path.exists(abs_file_path):
                os.remove(abs_file_path)
        elif input_type == 'image' and request.FILES.get('image_file'):
            image_file = request.FILES['image_file']
            file_path = default_storage.save('temp/' + image_file.name, image_file)
            abs_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
            try:
                extracted_text = extract_text_from_image(abs_file_path)
            except Exception as e:
                extracted_text = f"Error extracting text: {e}"
            if os.path.exists(abs_file_path):
                os.remove(abs_file_path)
        else:
            extracted_text = "No valid input provided."
        return render(request, 'result.html', {'extracted_text': extracted_text})
    return redirect('home')



def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('num1')
        password = request.POST.get('num2')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('result2')
    return render(request,'login.html')
    
def registerpage(request):
    if request.method == 'POST':
        username = request.POST.get('num1')
        password = request.POST.get('num2')
        conform = request.POST.get('num3')
        if password != conform:
            return render(request,'register.html',{'result':'ERROR'})
        user=User.objects.create_user(username=username,password=password)
        return redirect('login')
    return render(request,'register.html')
def home(request):
    return render (request,'home.html')








