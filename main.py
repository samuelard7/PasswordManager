from tkinter import *
from tkinter import messagebox
from random import *
import pyperclip
import json


def close():
    window.destroy()

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    pass_letters = [choice(letters) for _ in range(randint(5, 7))]
    pass_numbers = [choice(numbers) for _ in range(randint(3, 4))]
    pass_symbols = [choice(symbols) for _ in range(randint(3, 4))]

    e = messagebox.askquestion(title="Select", message="Do you want to generate an easy password?")
    if e == 'no':
        h = messagebox.askquestion(title="Select", message="Do you want to generate an hard password?")
        if h == 'yes':
            let1 = []
            hard_pass = ""

            let1 = pass_letters + pass_numbers + pass_symbols
            shuffle(let1)
            hard_pass = "".join(let1)
            password_entry.insert(0, hard_pass)
            pyperclip.copy(hard_pass)
    elif e == 'yes':
        let2 = []
        easy_pass = ""
        let2 = pass_letters + pass_numbers + pass_symbols
        easy_pass = "".join(let2)
        password_entry.insert(0, easy_pass)
        pyperclip.copy(easy_pass)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 and len(password) == 0:
        messagebox.showerror(title="Oops", message="Fields are empty.")
    elif len(website) == 0:
        messagebox.showerror(title="Error", message="Please enter the website!!!")
    elif len(password) == 0:
        messagebox.showerror(title="Error", message="Please enter the password!!!")
    else:
        is_ok = messagebox.askokcancel(title=website,
                                       message=f"These are the details entered: \nEmail: {email}\nPassword: "
                                               f"{password}\nIs it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)

            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    cap = website.capitalize()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found.")
    else:
        if cap in data:
            email = data[cap]["email"]
            password = data[cap]["password"]
            messagebox.showinfo(title=cap, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showerror(title="Error", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()

window.title("Password Manager")
window.config(padx=50, pady=50, bg="white")

canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)

pass_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=pass_img)
canvas.grid(row=0, column=1)

# labels
website_label = Label(text="Website:", bg="white")
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:", bg="white")
email_label.grid(column=0, row=2)
password_label = Label(text="Password:", bg="white")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=22)
website_entry.grid(column=1, row=1)
website_entry.focus()
email_entry = Entry(width=36, borderwidth=1)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "samuelrichard214@gmail.com")
password_entry = Entry(width=22)
password_entry.grid(row=3, column=1)

# Buttons
pass_button = Button(text="Gen Password", command=generate_password, borderwidth=1, width=10, bg="white")
pass_button.grid(row=3, column=2)
add_button = Button(text="Add", width=33, command=save, borderwidth=0, bg="white")
add_button.grid(row=4, column=1, columnspan=2)
close_button = Button(text="Exit", command=close, bg="white")
close_button.grid(row=0, column=2)
search_button = Button(text="Search", borderwidth=1, width=10, bg="white", command=find_password)
search_button.grid(row=1, column=2)
window.mainloop()


