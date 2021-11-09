from tkinter import *
from random import choice
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"

global words_to_learn
try:
    words_to_learn = pd.read_csv("data/words_to_learn.csv").to_dict(orient="records")
except FileNotFoundError:
    words_to_learn = pd.read_csv("data/french_words.csv").to_dict(orient="records")
else:
    words_to_learn = words_to_learn

current_card = {}


def next_word():
    global current_card, flip_timer
    current_card = choice(words_to_learn)

    window.after_cancel(flip_timer)
    canvas.itemconfig(image, image=card_front)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(image, image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


def is_known():
    words_to_learn.remove(current_card)
    pd.DataFrame(words_to_learn).to_csv("data/words_to_learn.csv", index=False)
    next_word()


window = Tk()
window.title("Flash Card")
window.config(bg=BACKGROUND_COLOR, pady=30, padx=30)
flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=910, height=570, bg=BACKGROUND_COLOR, highlightthickness=0)
card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")
image = canvas.create_image(470, 285, image=card_front)

card_title = canvas.create_text(420, 100, text="Title", font=("Arial", 40, "italic"))
card_word = canvas.create_text(420, 270, text="word", font=("Arial", 40, "bold"))

canvas.grid(column=0, row=0, columnspan=2)

unknown_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=unknown_image, highlightthickness=0, border=0, command=next_word)
unknown_button.grid(column=0, row=1, pady=10)

known_image = PhotoImage(file="images/right.png")
known_button = Button(image=known_image, highlightthickness=0, border=0, command=is_known)
known_button.grid(column=1, row=1, pady=20)

next_word()
window.mainloop()
