import tkinter as tk
import math

# Sample data
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

# Function to load the selected question
def load_question(index):
    question_label.config(text=f"Question {index + 1}: {questions[index]}")
    feedback_label.config(text="")

# Initial setup for the main window
root = tk.Tk()
root.title("Circular Navigation Menu")
root.geometry("600x600")
root.configure(bg="lightblue")

# Center coordinates for the circle
center_x = 300
center_y = 300
radius = 150

# Create a frame for the question display
quiz_frame = tk.Frame(root, bg="lightblue")
quiz_frame.pack(side="top", pady=20)

question_label = tk.Label(quiz_frame, text="", font=("Helvetica", 16), bg="lightblue")
question_label.pack(pady=10)

feedback_label = tk.Label(quiz_frame, text="", font=("Arial", 12), bg="lightblue")
feedback_label.pack(pady=10)

# Create buttons in a circular pattern
num_buttons = len(questions)
angle_increment = 2 * math.pi / num_buttons  # Divide the circle evenly

buttons = []
for i in range(num_buttons):
    angle = i * angle_increment
    x = center_x + int(radius * math.cos(angle))
    y = center_y - int(radius * math.sin(angle))
    
    # Create a button for each question
    button = tk.Button(root, text=f"Q{i + 1}", command=lambda i=i: load_question(i))
    button.place(x=x, y=y, anchor="center")
    buttons.append(button)

# Load the first question by default
load_question(0)

root.mainloop()
