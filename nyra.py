import pyttsx3
import speech_recognition as sr
import os
import webbrowser
import openai
import tkinter as tk
from tkinter import ttk

# OpenAI API Key (Replace with your own)
openai.api_key = "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"

# Initialize Text-to-Speech engine
def initialize_tts():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Female voice
    return engine

tts_engine = initialize_tts()

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def chat_with_ai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are Nyra, a virtual assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def open_application(command):
    command = command.lower()
    if "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
    elif "open spotify" in command:
        webbrowser.open("https://open.spotify.com")
        speak("Opening Spotify")
    elif "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        speak("Opening WhatsApp")

    elif "open notepad" in command:
        os.system("notepad.exe")
        speak("Opening Notepad")
    elif "open college" in command or "open srm" in command:
        webbrowser.open("https://sp.srmist.edu.in/srmiststudentportal/students/loginManager/youLogin.jsp")
        speak("Opening SRM Student Portal")
    else:
        speak("I am not sure how to open that.")

def handle_command(command):
    if "open" in command:
        open_application(command)
    else:
        response = chat_with_ai(command)
        speak(response)

def start_listening():
    command = listen()
    if command:
        handle_command(command)

def create_gui():
    root = tk.Tk()
    root.title("Nyra - AI Assistant")
    root.geometry("500x600")

    label = tk.Label(root, text="Nyra - Your AI Assistant", font=("Arial", 18))
    label.pack(pady=20)

    text_area = tk.Text(root, height=15, width=50)
    text_area.pack(pady=10)
    
    def ask_nyra():
        user_input = text_area.get("1.0", tk.END).strip()
        if user_input:
            handle_command(user_input)
            output_label.config(text="✅ Done: " + user_input)
    
    button = ttk.Button(root, text="Ask Nyra", command=ask_nyra)
    button.pack(pady=10)
    
    output_label = tk.Label(root, text="", wraplength=400, font=("Arial", 12))
    output_label.pack(pady=10)
    
    mic_button = ttk.Button(root, text="🎤 Speak", command=start_listening)
    mic_button.pack(pady=10)
    
    root.mainloop()

# Run the GUI
create_gui()
