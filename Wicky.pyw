import tkinter as tk
import json
import random
import customtkinter as CTk
from tkinter import messagebox
import datetime
import speech_recognition as sr


with open('src/settings.json', 'r')as f:
    settings = json.load(f)
version = settings['Version']
theme = settings['Theme']

if theme == 'Dark':
    CTk.set_appearance_mode('dark')
else:
    CTk.set_appearance_mode('light')

app = CTk.CTk()
app.configure(bg="#D1FFF3")
app.title(f"Wicky v{version}")
app.geometry('500x560')
app.resizable(False, False)
response_text = CTk.CTkTextbox(app, width=420, height=420, state='disabled')
response_text.place(x=50, y=10)

with open('src/responses.json') as json_file:
    intents = json.load(json_file)


def submit():
    user_input = user_input_field.get()
    get_response(user_input)
    user_input_field.delete(0, "end")


def get_response(event=None):
    user_input = user_input_field.get()
    user_input_field.delete(0, "end")
    if user_input == '':
        empty_input = messagebox.showinfo(
            'Empty request', 'Please type your request in the text field to the left.')
    else:
        send_button.configure(state='disabled')
        export_chatlog_button.configure(state='disabled')
        clear_button.configure(state='disabled')
        response_text.configure(state='normal')
        response_text.insert("end", "You: " + user_input + "\n\n" + "Wicky: ")
        user_input_field.delete(0, "end")
        response = "I'm sorry, I don't understand what you're saying."

        for intent in intents['intents']:
            if user_input.lower() in intent['patterns']:
                response = random.choice(intent['responses'])
                break

        for i, c in enumerate(response):
            response_text.insert("end", c)
            response_text.update()
            response_text.after(50)

        response_text.insert(
            "end", "\n\n"+"-"*101+"\n\n")
        response_text.configure(state='disabled')
        send_button.configure(state='normal')
        export_chatlog_button.configure(state='normal')
        clear_button.configure(state='normal')


def clear_all():
    is_ok = messagebox.askokcancel(
        title='Clear All?', message="Are you sure you want to clear the response and the input text fields?")
    if is_ok:
        response_text.configure(state='normal')

        response_text.delete("1.0", "end")
        user_input_field.delete(0, "end")
        response_text.configure(state='disabled')


def show_commands():
    pass

# TODO: Better filtering of feeling lucky


def feeling_lucky():
    with open('src/responses.json') as f:
        data = json.load(f)
        commands = []
        for intent in data['intents']:
            if intent['tag'] not in ['greetings', 'goodbye']:
                for pattern in intent['patterns']:
                    commands.append(pattern)
        command = random.choice(commands)
        users = user_input_field.get()
        if users == "":
            user_input_field.insert('end', command)
        else:
            user_input_field.delete(0, "end")
            user_input_field.insert(0, command)


def voice_recognition():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio_text = r.listen(source)
    try:
        transcribed_text = r.recognize_google(audio_text)
        user_input_field.configure(state='normal')
        user_input_field.delete(0, "end")
        user_input_field.insert(tk.END, transcribed_text)
    except sr.UnknownValueError:
        user_input_field.configure(state='normal')
        user_input_field.delete(0, "end")
        user_input_field.insert(
            tk.END, 'Could not understand audio. Please Try again.')
    except sr.RequestError as e:
        user_input_field.configure(state='normal')
        user_input_field.delete(0, "end")
        user_input_field.insert(
            tk.END, 'Not able to request data. Please Try again.')


def export_chatlog():
    log = response_text.get("1.0", "end-1c")
    if log == '':
        empty_box = messagebox.showinfo(
            'Empty textbox', 'Nothing to be exported.')
    else:
        now = datetime.datetime.now()
        filename = f"chat_logs/chatlog_{now.strftime('%m-%d-%Y_%H-%M-%S')}.txt"
        with open(filename, 'w')as f:
            f.write(log)
        print(f'Chat log saved to {filename}')


def toggle_theme():
    with open('src/settings.json', 'r')as f:
        settings = json.load(f)
        theme = settings['Theme']
        if theme == 'Dark':
            CTk.set_appearance_mode('light')
            toggle_theme_button.configure(text='\u26ee')
            settings['Theme'] = 'Light'
        if theme == 'Light':
            CTk.set_appearance_mode('Dark')
            toggle_theme_button.configure(text='\u2600')
            settings['Theme'] = 'Dark'
        with open('src/settings.json', 'w')as f:
            json.dump(settings, f)


user_input_field = CTk.CTkEntry(app, width=280)
user_input_field.focus()
user_input_field.bind("<Return>", get_response)
user_input_field.place(x=120, y=450)
listen_button = CTk.CTkButton(
    app, text='\U0001F3A4', command=voice_recognition, width=20)
listen_button.place(x=405, y=450)
send_button = CTk.CTkButton(app, text='\u21e8', command=submit, width=20)
send_button.place(x=440, y=450)
clear_button = CTk.CTkButton(
    app, text="Clear All", command=clear_all, width=50)
clear_button.place(x=50, y=450)
commands_button = CTk.CTkButton(
    app, text="What Can I Do?", command=show_commands, width=50)
commands_button.place(x=50, y=490)
feeling_lucky_button = CTk.CTkButton(
    app, text="Feeling Lucky", command=feeling_lucky, width=50)
feeling_lucky_button.place(x=155, y=490)
export_chatlog_button = CTk.CTkButton(
    app, text="Export Chat Log", command=export_chatlog, width=70)
export_chatlog_button.place(x=265, y=490)
toggle_theme_button = CTk.CTkButton(
    app, text='\u2600', width=3, command=toggle_theme)
toggle_theme_button.place(x=380, y=490)
exit_button = CTk.CTkButton(app, text="Exit", command=exit, width=50)
exit_button.place(x=418, y=490)

app.mainloop()
