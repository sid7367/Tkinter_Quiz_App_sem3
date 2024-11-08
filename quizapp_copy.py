import mysql.connector as ms
import tkinter as tk
from tkinter import font

# Establishing the connection
conn = ms.connect(host='localhost',
                  user='root',
                  password='SIDsql@2005#', 
                  database='Quiz_Questions')

cursor = conn.cursor()

# Global variables to track the current question index and score
question_index = 0
score = 0  # Added to track the user's score

# Function to get questions based on the category and number of questions
def get_questions(category, num_questions):
    query = "SELECT question_text, option1, option2, option3, option4, correct_answer FROM questions WHERE category = %s LIMIT %s"
    cursor.execute(query, (category, num_questions))
    return cursor.fetchall()

# Function to start the quiz and load questions
def start_quiz(category, num_questions): 
    global question_index, score  # Declare global to modify

    # Reset score and question index for a new quiz
    score = 0
    question_index = 0

    # Fetch questions for the selected category and number of questions
    questions = get_questions(category, num_questions)
    
    # Function to load a question based on the current index
    def load_question(index):
        if 0 <= index < len(questions):  # Check if the index is within range
            question_data = questions[index]
            question_text, opt1, opt2, opt3, opt4, correct_ans = question_data
            question_label.config(text=question_text)
            option1_radio.config(text=opt1, value=opt1)
            option2_radio.config(text=opt2, value=opt2)
            option3_radio.config(text=opt3, value=opt3)
            option4_radio.config(text=opt4, value=opt4)
            feedback_label.config(text="")  # Clear previous feedback
        else:
            feedback_label.config(text=f"Quiz completed! Your score: {score}/{len(questions)}", fg="green")
            submit_button.config(state=tk.DISABLED)
            next_button.config(state=tk.DISABLED)
            back_button.config(state=tk.DISABLED)

    # Function to handle "Submit" button click
    def submit_answer():
        global score  # Allows modification of score within this scope
        selected_option = var.get()  # Get the selected option
        correct_answer = questions[question_index][5]  # Correct answer from fetched data

        if selected_option == correct_answer:
            score += 1
            feedback_label.config(text="Correct!", fg="green")
        else:
            feedback_label.config(text=f"Incorrect! The correct answer is: {correct_answer}", fg="red")

        # Disable submit button after answering until the next question is loaded
        submit_button.config(state=tk.DISABLED)

    # Function to handle "Next" button click
    def next_question():
        global question_index
        if question_index < len(questions) - 1:
            question_index += 1
            load_question(question_index)
            submit_button.config(state=tk.NORMAL)  # Re-enable the submit button for the next question
        else:
            feedback_label.config(text="You have reached the last question.", fg="blue")

    # Function to handle "Go Back" button click
    def previous_question():
        global question_index
        if question_index > 0:
            question_index -= 1
            load_question(question_index)
            submit_button.config(state=tk.NORMAL)  # Re-enable the submit button for the previous question
        else:
            feedback_label.config(text="You are on the first question.", fg="blue")

    # Setup the Tkinter root window
    root = tk.Tk()
    root.title("Quiz App")
    root.geometry("500x450")
    root.configure(bg="lightblue")

    title_font = font.Font(family="Helvetica", size=16, weight="bold")
    question_font = font.Font(family="Arial", size=14)
    option_font = font.Font(family="Arial", size=12)
    button_font = font.Font(family="Arial", size=12, weight="bold")

    # Creates a label widget for question text
    question_label = tk.Label(root, text="", font=question_font)
    question_label.pack(pady=(20, 20))

    # Radiobuttons for options
    var = tk.StringVar(value="None of the options... Select one")
    option_frame = tk.Frame(root, bg="#f0f8ff")
    option_frame.pack()

    option1_radio = tk.Radiobutton(option_frame, variable=var, font=option_font, text="", bg="#f0f8ff", activebackground="#f0f8ff")
    option2_radio = tk.Radiobutton(option_frame, variable=var, font=option_font, text="", bg="#f0f8ff", activebackground="#f0f8ff")
    option3_radio = tk.Radiobutton(option_frame, variable=var, font=option_font, text="", bg="#f0f8ff", activebackground="#f0f8ff")
    option4_radio = tk.Radiobutton(option_frame, variable=var, font=option_font, text="", bg="#f0f8ff", activebackground="#f0f8ff")

    option1_radio.pack(anchor="w", pady=5)
    option2_radio.pack(anchor="w", pady=5)
    option3_radio.pack(anchor="w", pady=5)
    option4_radio.pack(anchor="w", pady=5)

    # Label to display feedback
    feedback_label = tk.Label(root, text="", font=button_font, bg="lightblue")
    feedback_label.pack(pady=10)

    # Button to submit the answer
    submit_button = tk.Button(root, text="Submit", command=submit_answer, font=button_font, bg="#ffa07a", fg="white")
    submit_button.pack(pady=10)

    # Button to go to the next question
    next_button = tk.Button(root, text="Next", command=next_question, font=button_font, bg="#4682b4", fg="white")
    next_button.pack(side="right", padx=20, pady=10)

    # Button to go back to the previous question
    back_button = tk.Button(root, text="Go Back", command=previous_question, font=button_font, bg="#4682b4", fg="white")
    back_button.pack(side="left", padx=20, pady=10)

    load_question(question_index)  # Load the first question initially

    root.mainloop()

# Function to create the question number selection window
def select_question_number(category):
    number_window = tk.Tk()
    number_window.title("Select Number of Questions")
    number_window.geometry("400x300")
    number_window.configure(bg="#C9E9D2")

    label_font = font.Font(family="Helvetica", size=14, weight="bold")
    button_font = font.Font(family="Arial", size=12)

    tk.Label(number_window, text="Choose Number of Questions", font=label_font, bg="#f5f5f5", fg="navy").pack(pady=20)

    question_numbers = [5, 10, 15, 20]  # Example question counts

    # Function to handle question number selection
    def handle_selection(num_questions):
        number_window.destroy()
        start_quiz(category, num_questions)

    for num in question_numbers:
        button = tk.Button(number_window, text=f"{num} Questions", font=button_font, bg="#FFE3E3", fg="black", width=20, command=lambda n=num: handle_selection(n))
        button.pack(pady=10)

    number_window.mainloop()

# Function to create the category selection window
def select_category():
    category_window = tk.Tk()
    category_window.title("Select Quiz Category")
    category_window.geometry("400x300")
    category_window.configure(bg="#C9E9D2")

    label_font = font.Font(family="Helvetica", size=14, weight="bold")
    button_font = font.Font(family="Arial", size=12)

    tk.Label(category_window, text="Choose a Category", font=label_font, bg="#f5f5f5", fg="navy").pack(pady=20)

    categories = ["Science", "Mathematics", "Literature", "Geography"]

    # Function to handle category selection
    def handle_selection(category):
        category_window.destroy()
        select_question_number(category)

    #for displaying the categories as buttons
    for cat in categories:
        button = tk.Button(category_window, text=cat, font=button_font, bg="#FFE3E3", fg="black", width=20, command=lambda c=cat: handle_selection(c))
        button.pack(pady=10)

    category_window.mainloop()

# Start the app with category selection window
select_category()

# Close the database connection
conn.close()
