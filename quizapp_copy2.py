import mysql.connector as ms
import tkinter as tk
from tkinter import font
import time
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# Establishing the connection
conn = ms.connect(host='localhost',
                  user='root',
                  password='SIDsql@2005#', 
                  database='Quiz_Questions')

cursor = conn.cursor()

# Global variables to track the current question index, score, and answers
question_index = 0
score = 0
correct_count = 0
incorrect_count = 0
start_time = 0  # For tracking quiz start time

# Function to get questions based on the category and number of questions
def get_questions(category, num_questions):
    query = "SELECT question_text, option1, option2, option3, option4, correct_answer FROM questions WHERE category = %s LIMIT %s"
    cursor.execute(query, (category, num_questions))
    return cursor.fetchall()

# Function to start the quiz and load questions
def start_quiz(category, num_questions):
    global question_index, score, correct_count, incorrect_count, start_time
    score = 0
    question_index = 0
    correct_count = 0
    incorrect_count = 0
    start_time = time.time()  # Start time of the quiz

    questions = get_questions(category, num_questions)

    def load_question(index):
        if 0 <= index < len(questions):
            question_data = questions[index]
            question_text, opt1, opt2, opt3, opt4, correct_ans = question_data
            question_label.config(text=question_text)
            option1_radio.config(text=opt1, value=opt1)
            option2_radio.config(text=opt2, value=opt2)
            option3_radio.config(text=opt3, value=opt3)
            option4_radio.config(text=opt4, value=opt4)
            feedback_label.config(text="")
        else:
            feedback_label.config(text=f"Quiz completed! Your score: {score}/{len(questions)}", fg="green")
            submit_button.config(state=tk.DISABLED)
            next_button.config(state=tk.DISABLED)
            back_button.config(state=tk.DISABLED)
            generate_report_button.pack()  # Show the report generation button

    def submit_answer():
        global score, correct_count, incorrect_count
        selected_option = var.get()
        correct_answer = questions[question_index][5]

        if selected_option == correct_answer:
            score += 1
            correct_count += 1
            feedback_label.config(text="Correct!", fg="green")
        else:
            incorrect_count += 1
            feedback_label.config(text=f"Incorrect! The correct answer is: {correct_answer}", fg="red")

        submit_button.config(state=tk.DISABLED)

    def next_question():
        global question_index
        if question_index < len(questions) - 1:
            question_index += 1
            load_question(question_index)
            submit_button.config(state=tk.NORMAL)
        else:
            feedback_label.config(text="You have reached the last question.", fg="blue")

    def previous_question():
        global question_index
        if question_index > 0:
            question_index -= 1
            load_question(question_index)
            submit_button.config(state=tk.NORMAL)
        else:
            feedback_label.config(text="You are on the first question.", fg="blue")

    # Function to generate the quiz report
    def generate_report():
        end_time = time.time()
        time_taken = end_time - start_time

        # Create pie chart
        labels = ['Correct', 'Incorrect']
        sizes = [correct_count, incorrect_count]
        colors = ['#4CAF50', '#FF6347']
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        chart_path = 'quiz_chart.png'
        plt.savefig(chart_path)
        plt.close()

        # Create PDF report
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.cell(200, 10, txt="Quiz Report", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Total Score: {score}/{len(questions)}", ln=True)
        pdf.cell(200, 10, txt=f"Time Taken: {time_taken:.2f} seconds", ln=True)

        pdf.image(chart_path, x=60, y=50, w=90)
        report_path = 'quiz_report.pdf'
        pdf.output(report_path)
        
        if os.path.exists(chart_path):
            os.remove(chart_path)

        feedback_label.config(text=f"Report generated: {report_path}", fg="blue")

    root = tk.Tk()
    root.title("Quiz App")
    root.geometry("500x450")
    root.configure(bg="lightblue")

    title_font = font.Font(family="Helvetica", size=16, weight="bold")
    question_font = font.Font(family="Arial", size=14)
    option_font = font.Font(family="Arial", size=12)
    button_font = font.Font(family="Arial", size=12, weight="bold")

    question_label = tk.Label(root, text="", font=question_font)
    question_label.pack(pady=(20, 20))

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

    feedback_label = tk.Label(root, text="", font=button_font, bg="lightblue")
    feedback_label.pack(pady=10)

    submit_button = tk.Button(root, text="Submit", command=submit_answer, font=button_font, bg="#ffa07a", fg="white")
    submit_button.pack(pady=10)

    next_button = tk.Button(root, text="Next", command=next_question, font=button_font, bg="#4682b4", fg="white")
    next_button.pack(side="right", padx=20, pady=10)

    back_button = tk.Button(root, text="Go Back", command=previous_question, font=button_font, bg="#4682b4", fg="white")
    back_button.pack(side="left", padx=20, pady=10)

    generate_report_button = tk.Button(root, text="Download Report", command=generate_report, font=button_font, bg="#00CED1", fg="white")
    generate_report_button.pack_forget()  # Initially hidden until quiz is completed

    load_question(question_index)
    root.mainloop()

def select_question_number(category):
    number_window = tk.Tk()
    number_window.title("Select Number of Questions")
    number_window.geometry("400x300")
    number_window.configure(bg="#C9E9D2")

    label_font = font.Font(family="Helvetica", size=14, weight="bold")
    button_font = font.Font(family="Arial", size=12)

    tk.Label(number_window, text="Choose Number of Questions", font=label_font, bg="#f5f5f5", fg="navy").pack(pady=20)

    question_numbers = [5, 10, 15, 20]

    def handle_selection(num_questions):
        number_window.destroy()
        start_quiz(category, num_questions)

    for num in question_numbers:
        button = tk.Button(number_window, text=f"{num} Questions", font=button_font, bg="#FFE3E3", fg="black", width=20, command=lambda n=num: handle_selection(n))
        button.pack(pady=10)

    number_window.mainloop()

def select_category():
    category_window = tk.Tk()
    category_window.title("Select Quiz Category")
    category_window.geometry("400x300")
    category_window.configure(bg="#C9E9D2")

    label_font = font.Font(family="Helvetica", size=14, weight="bold")
    button_font = font.Font(family="Arial", size=12)

    tk.Label(category_window, text="Choose a Category", font=label_font, bg="#f5f5f5", fg="navy").pack(pady=20)

    categories = ["Science", "Mathematics", "Literature", "Geography"]

    def handle_selection(category):
        category_window.destroy()
        select_question_number(category)

    for cat in categories:
        button = tk.Button(category_window, text=cat, font=button_font, bg="#FFE3E3", fg="black", width=20, command=lambda c=cat: handle_selection(c))
        button.pack(pady=10)

    category_window.mainloop()

# Start the app with category selection window
select_category()
conn.close()
