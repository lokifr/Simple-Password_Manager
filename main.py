from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import os
import json

# Initialize the global file_path variable
file_path = os.path.join(os.path.expanduser("~/Desktop"), "data.json")

# PASSWORD GENERATOR
def gen_passwd():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    passwd_letters = [choice(letters) for _ in range(randint(8, 10))]
    passwd_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    passwd_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = passwd_numbers + passwd_symbols + passwd_letters

    shuffle(password_list)

    password = "".join(password_list)
    Passwd_entry.delete(0, END)  # Clear the entry field before inserting
    Passwd_entry.insert(0, password)
    pyperclip.copy(password)

# SAVE PASSWORD
def save():
    website = Website_entry.get()
    usname = Username_entry.get()
    passwd = Passwd_entry.get()
    new_data = {
        website: {
            "email": usname,
            "passwd": passwd
        }
    }
    if len(website) == 0 or len(passwd) == 0:
        messagebox.showwarning(title="Empty", message="Field Empty")
    else:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
        else:
            data = {}

        # update data
        data.update(new_data)

        with open(file_path, "w") as data_file:
            json.dump(data, data_file, indent=4)

        Website_entry.delete(0, END)
        Username_entry.delete(0, END)
        Passwd_entry.delete(0, END)

# SEARCH FUNCTION
def search():
    website = Website_entry.get()
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "r") as f:
            try:
                data = json.load(f)
                if website in data:
                    info = data[website]
                    messagebox.showinfo(title=website, message=f"Email: {info['email']}\nPassword: {info['passwd']}")
                else:
                    messagebox.showwarning(title="Not Found", message="No details for the website exist.")
            except json.JSONDecodeError:
                messagebox.showwarning(title="Error", message="Error reading data file.")
    else:
        messagebox.showwarning(title="Error", message="Data file not found.")

# UI SETUP
window = Tk()
window.title("Password Manager")
window.minsize(width=600, height=400)
window.config(padx=30, pady=30)

canvas = Canvas(width=256, height=256)
photo = PhotoImage(file="password-manager_optimized.png")
canvas.create_image(132, 132, image=photo)
canvas.grid(column=1, row=0)

# labels
website_txt = Label(text="Website", font=("Montserrat", 10, "bold"))
website_txt.grid(column=0, row=1)
email_txt = Label(text="Email/Username", font=("Montserrat", 10, "bold"))
email_txt.grid(column=0, row=2)
passwd_txt = Label(text="Password", font=("Montserrat", 10, "bold"))
passwd_txt.grid(column=0, row=3)

Website_entry = Entry(width=60)
Website_entry.grid(column=1, row=1, columnspan=3)
Website_entry.focus()
Username_entry = Entry(width=60)
Username_entry.grid(column=1, row=2, columnspan=3)
Username_entry.insert(0, "@gmail.com")
Passwd_entry = Entry(width=60)
Passwd_entry.grid(column=1, row=3, columnspan=3)

# buttons
generate_button = Button(text="Generate Password", width=30, command=gen_passwd)
generate_button.grid(column=1, row=4, columnspan=1)
add_button = Button(text="Add", width=10, command=save)
add_button.grid(column=2, row=4, columnspan=1)
search_button = Button(text="Search", width=10, command=search)
search_button.grid(column=5, row=1, columnspan=1)

window.mainloop()
