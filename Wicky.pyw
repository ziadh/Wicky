import tkinter as tk
import json
import random
import customtkinter as CTk

version = '0.10'
app = CTk.CTk()
app.configure(bg="#D1FFF3")
app.title(f"Wicky v{version}")
app.geometry('500x510')
app.resizable(False, False)
response_text = CTk.CTkTextbox(app, width=420, height=420,state='disabled')
response_text.place(x=50, y=10)

with open('responses.json') as json_file:
    intents = json.load(json_file)


def submit():
    user_input = user_input_field.get()
    get_response(user_input)
    user_input_field.delete(0, "end")


def get_response(event=None):
    response_text.configure(state='normal')
    user_input = user_input_field.get()
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
        "end", "\n\n-----------------------------------------------------------------------------------------------------\n\n")
    response_text.configure(state='disabled')
    


def clear_all():
    response_text.delete("1.0", "end")
    user_input_field.delete(0, "end")


user_input_field = CTk.CTkEntry(app, width=280)
user_input_field.bind("<Return>", get_response)
user_input_field.place(x=120, y=450)
send_button = CTk.CTkButton(app, text="Send", command=submit, width=50)
send_button.place(x=420, y=450)
clear_button = CTk.CTkButton(app, text="Clear", command=clear_all, width=50)
clear_button.place(x=50, y=450)
app.mainloop()
