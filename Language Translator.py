
from tkinter import *
import os
import pymysql
import hashlib
import googletrans
from googletrans import Translator, LANGUAGES
from gtts import gTTS
from tkinter import messagebox
from tkinter import ttk

# Initialize Tkinter window
root = Tk()
root.title("Language Translator")
root.geometry("700x700")
root.config(bg="#a8ebe3")
root.resizable(False, False)

# Get languages
languages = googletrans.LANGUAGES
language_list = list(languages.values())

# Database connection
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        database="language_translator"
    )

# Function to hash passwords securely
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to save user details
def save():
    username = entry1.get()
    email = entry2.get()
    password_hash = entry3.get()
    re_password = entry4.get()

    if username == "" or email == "" or password_hash == "" or re_password == "":
        messagebox.showerror("Error", "Enter all details")
    elif password_hash != re_password:
        messagebox.showerror("Error", "Passwords do not match")
    else:
        try:
            connection = connect_db()
            cursor = connection.cursor()

            # Hash the password before storing it
            hashed_password = hash_password(password_hash)
            query = "INSERT INTO users (user_name, email_address, password_hash,re_password) VALUES (%s, %s, %s,%s)"
            cursor.execute(query, (username, email, password_hash,hashed_password))
            connection.commit()
            cursor.close()
            connection.close()

            messagebox.showinfo("Info", "Successfully Registered!")
            open_page2()
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", f"Failed to save data: {e}")

# Function to translate text
def translate_now():
    global tts_audio

    try:
        text_ = text1.get(1.0, END).strip()
        source_lang = combo1.get()
        target_lang = combo2.get()

        if text_:
            translator = Translator()
            detected_lang = translator.detect(text_).lang

            target_code = None
            for code, lang in LANGUAGES.items():
                if lang.lower() == target_lang.lower():
                    target_code = code
                    break

            if target_code:
                translated_text = translator.translate(text_, src=detected_lang, dest=target_code).text
                text2.delete(1.0, END)
                text2.insert(END, translated_text)

                # Convert translated text to speech
                tts_audio = "translated_audio.mp3"
                tts = gTTS(text=translated_text, lang=target_code)
                tts.save(tts_audio)

            return

        messagebox.showerror("Error", "Please enter text to translate.")
    
    except Exception as e:
        messagebox.showerror("Error", f"Translation failed! {e}")

# Function to play translated text as audio
def play_audio():
    global tts_audio
    if tts_audio and os.path.exists(tts_audio):
        os.system(f"start {tts_audio}")  # Play audio
    else:
        messagebox.showerror("Error", "No audio found. Translate first!")

# Function to copy translated text
def copy_text():
    root.clipboard_clear()
    root.clipboard_append(text2.get(1.0, END))
    root.update()
    messagebox.showinfo("Copied", "Translated text copied!")

# Function to paste text
def paste_text():
    text1.delete(1.0, END)
    text1.insert(INSERT, root.clipboard_get())

# Function to clear text boxes
def clear():
    text1.delete(1.0, END)
    text2.delete(1.0, END)

# Function to open translator page
def open_page2():
    global text1, text2, combo1, combo2
    root.withdraw()
    page2 = Toplevel(root)
    page2.title("Language Translator")
    page2.geometry("900x700")
    page2.config(bg="#a8ebe3")
    page2.resizable(False, False)

    Label(page2, text="LANGUAGE TRANSLATOR", font=('Graphique Pro', 20, "bold"), fg="black", bg="#a8ebe3").place(x=270, y=80)

    text1 = Text(page2, height=15, width=45)
    text1.grid(row=1, column=0, pady=150, padx=10)

    text2 = Text(page2, height=15, width=45)
    text2.grid(row=1, column=2, pady=20, padx=10)

    Button(page2, text="Translate", font=("Arial", 15, "bold"), bg="#a1ef69", command=translate_now).grid(row=1, column=1, padx=10, pady=20)

    combo1 = ttk.Combobox(page2, width=31, values=language_list, font=("Arial", 14))
    combo1.set("English")
    combo1.place(x=10, y=430)

    combo2 = ttk.Combobox(page2, width=31, values=language_list, font=("Arial", 14))
    combo2.set("Select Language")
    combo2.place(x=522, y=430)

    Button(page2, text="Clear", font=("Arial", 12, "bold"), bg="red", command=clear).place(x=422, y=430)
    Button(page2, text="Copy", font=("Arial", 12, "bold"), bg="blue", command=copy_text).place(x=670, y=500)
    Button(page2, text="Paste", font=("Arial", 12, "bold"), bg="orange", command=paste_text).place(x=150, y=500)
    Button(page2, text="Play Audio", font=("Arial", 12, "bold"), bg="purple", command=play_audio).place(x=400, y=500)

# UI for Login Page
Label(root, text="LANGUAGE TRANSLATOR", font=('Graphique Pro', 20, "bold"), fg="black", bg="#a8ebe3").place(x=160, y=100)
Label(root, text="User Name", font=('Montserrat', 15, "bold"), fg="black", bg="#a8ebe3").place(x=150, y=200)
entry1 = Entry(root, font=('Montserrat', 15, "bold"), relief="solid")
entry1.place(x=350, y=200)

Label(root, text="Email Address", font=('Montserrat', 15, "bold"), fg="black", bg="#a8ebe3").place(x=150, y=270)
entry2 = Entry(root, font=('Montserrat', 15, "bold"), relief="solid")
entry2.place(x=350, y=270)

Label(root, text="Password", font=('Montserrat', 15, "bold"), fg="black", bg="#a8ebe3").place(x=150, y=340)
entry3 = Entry(root, font=('Montserrat', 15, "bold"), show="*", relief="solid")
entry3.place(x=350, y=340)

Label(root, text="Re-Enter Password", font=('Montserrat', 15, "bold"), fg="black", bg="#a8ebe3").place(x=150, y=410)
entry4 = Entry(root, font=('Montserrat', 15, "bold"), show="*", relief="solid")
entry4.place(x=350, y=410)

Button(root, text='Submit', command=save, bg="white", fg="black", font=("Montserrat", 15, "bold"), height="1", width="13", bd=0).place(x=250, y=530)

root.mainloop()
