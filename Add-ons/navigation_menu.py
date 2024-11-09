import tkinter as tk
from tkinter import font

# Sample questions for demonstration
questions = [
    "What is the capital of France?",
    "What is 2 + 2?",
    "Who wrote 'Hamlet'?",
    "What is the boiling point of water?",
    "Which planet is known as the Red Planet?"
]

options = [
    ["Paris", "London", "Berlin", "Madrid"],
    ["2", "3", "4", "5"],
    ["Shakespeare", "Tolkien", "Hemingway", "Poe"],
    ["100°C", "90°C", "80°C", "110°C"],
    ["Mars", "Venus", "Jupiter", "Saturn"]
]

correct_answers = ["Paris", "4", "Shakespeare", "100°C", "Mars"]

# Function to load a selected question
def load_question(index):
    question_label.config(text=questions[index])
    for i, option in enumerate(option_buttons):
        option.config(text=options[index][i], value=options[index][i])
    feedback_label.config(text="")

# Initial setup for the main window
root = tk.Tk()
root.title("Quiz App with Navigation Menu")
root.geometry("600x400")
root.configure(bg="lightblue")

# Create a listbox for question navigation
question_listbox = tk.Listbox(root, height=10, width=30, font=("Arial", 12))
question_listbox.pack(side="left", fill="y", padx=10, pady=10)

# Populate the listbox with question numbers
for i in range(len(questions)):
    question_listbox.insert(tk.END, f"Question {i + 1}")

# Bind the listbox to navigate between questions
def navigate_to_question(event):
    selected_index = int(question_listbox.curselection()[0])
    load_question(selected_index)

question_listbox.bind("<<ListboxSelect>>", navigate_to_question)

# Create a frame to hold the question and options
quiz_frame = tk.Frame(root, bg="lightblue")
quiz_frame.pack(side="right", expand=True, fill="both")

# Create widgets for displaying the question
question_label = tk.Label(quiz_frame, text="", font=("Helvetica", 16), bg="lightblue")
question_label.pack(pady=20)

# Create option buttons
option_var = tk.StringVar(value="")

option_buttons = []
for i in range(4):
    option = tk.Radiobutton(quiz_frame, variable=option_var, value="", font=("Arial", 12), bg="lightblue")
    option.pack(anchor="w", pady=5)
    option_buttons.append(option)

feedback_label = tk.Label(quiz_frame, text="", font=("Arial", 12), bg="lightblue")
feedback_label.pack(pady=10)

# Load the first question by default
load_question(0)

root.mainloop()
