import mysql.connector as ms
import tkinter as tk
from tkinter import font
import time
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
import uuid
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from tkinter import messagebox

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

# Function to get questions based on the category and number of questions & in a random order 
def get_questions(category, num_questions):
    query = "SELECT question_text, option1, option2, option3, option4, correct_answer FROM questions WHERE category = %s ORDER BY RAND() LIMIT %s"
    cursor.execute(query, (category, num_questions))
    questions = cursor.fetchall()
    
    # Debugging print to check if questions are being fetched correctly
    print(f"Fetched {len(questions)} questions for category '{category}'")

    return questions

#function for checking email validity
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def send_email_with_report(to_email, report_path, feedback_label):
    from_email = "adm707quizpy@gmail.com"  # Replace with actual email
    from_password = "azkb awtc edzt fsob"  # Replace with the actual password (use environment variables or a config file for security)
    subject = "Your Quiz Report"
    
    # Creating the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    body = """Please find attached your quiz report. 
Thank you for taking the quiz 💗!

With regards,
Quiz App Team
    """
    msg.attach(MIMEText(body, 'plain'))

    # Attach the PDF report
    try:
        with open(report_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(report_path)}")
        msg.attach(part)

        # Sending the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        feedback_label.config(text="Report sent successfully!", fg="green")

    except Exception as e:
        feedback_label.config(text=f"Failed to send email: {str(e)}", fg="red")


# Function to start the quiz and load questions
def start_quiz(category, num_questions):
    global question_index, score, correct_count, incorrect_count, start_time,end_time
    score = 0
    question_index = 0
    correct_count = 0
    incorrect_count = 0
    # start_time = time.time()  # Start time of the quiz
    start_time = time.strftime("%Y-%m-%d %H:%M:%S")  # Record the quiz start time

    questions = get_questions(category, num_questions)

     # To Check if questions are available
    if not questions:
        print("No questions found. Please check the database.")
        feedback_label.config(text="No questions available for this category.", fg="red")
        return

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

        # Update the score label on each question load
            score_label.config(text=f"Score: {score}/{len(questions)}")

        else:
            feedback_label.config(text=f"Quiz completed! Your score: {score}/{len(questions)}", fg="green")
            score_label.config(text=f"Final Score: {score}/{len(questions)}")
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

        # Update the score label after submission
        score_label.config(text=f"Score: {score}/{len(questions)}")

        submit_button.config(state=tk.DISABLED)
        

    def next_question():
        global question_index
        if question_index < len(questions) - 1:
            question_index += 1
            load_question(question_index)
            submit_button.config(state=tk.NORMAL)
        else:
            feedback_label.config(text=f"Quiz completed! Your score: {score}/{len(questions)}", fg="green")
            score_label.config(text=f"Final Score: {score}/{len(questions)}")
            submit_button.config(state=tk.DISABLED)
            next_button.config(state=tk.DISABLED)
            back_button.config(state=tk.DISABLED)
            generate_report_button.pack()  # Show the report generation button when quiz ends


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
        # end_time = time.time()
        end_time = time.strftime("%Y-%m-%d %H:%M:%S")  # Record the quiz end time
        # time_taken = end_time - start_time
        # Calculate the time taken as a duration in seconds
        time_taken = (time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S")) - 
              time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S")))

        # Create pie chart
        labels = ['Correct', 'Incorrect']
        sizes = [correct_count, incorrect_count]
        colors = ['#4CAF50', '#FF6347']
        explode = (0.1,0.1)
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, explode=explode ,labels=labels, colors=colors, autopct='%1.1f%%', shadow = True,startangle=140)
        
        plt.title("Test Analysis")
        plt.axis('equal')
        chart_path = 'quiz_chart.png'
        plt.savefig(chart_path)
        plt.close()

        # Generate a unique file name for the report
        unique_id = uuid.uuid4()
        report_path = f'quiz_report_{unique_id}.pdf'
        
        # Create PDF report
        pdf = FPDF()
        pdf.add_page()
        # pdf.set_font("Arial", size=12)

        # Set the title with bold and underline formatting
        pdf.set_font("Arial", "BU", 16)  # Bold and underlined
        pdf.set_fill_color(200, 220, 255)  # Light blue color for the header
        pdf.cell(0, 10, txt="Quiz Report", ln=True, align="C")

        # Leave some space
        pdf.ln(5)

        # Set font for table headers (bold)
        pdf.set_font("Arial", "B", 12)

        # Table headers
        pdf.cell(80, 10, txt="Details", border=1, align="C")
        pdf.cell(110, 10, txt="Values", border=1, align="C")
        pdf.ln(10)  # Move to the next line

        # Set font for table content (regular)
        pdf.set_font("Arial", "", 12)

        # # Category row
        # pdf.cell(60, 10, txt="Category:", border=1)
        # pdf.cell(130, 10, txt=f"{category}", border=1)
        # pdf.ln(10)

        # # Total Score row
        # pdf.cell(60, 10, txt="Total Score:", border=1)
        # pdf.cell(130, 10, txt=f"{score}/{len(questions)}", border=1)
        # pdf.ln(10)

        # # Correct Answers row
        # pdf.cell(60, 10, txt="Correct Answers:", border=1)
        # pdf.cell(130, 10, txt=f"{correct_count}", border=1)
        # pdf.ln(10)

        # # Incorrect Answers row
        # pdf.cell(60, 10, txt="Incorrect Answers:", border=1)
        # pdf.cell(130, 10, txt=f"{incorrect_count}", border=1)
        # pdf.ln(10)

        # # Start Time row
        # pdf.cell(60, 10, txt="Start Time:", border=1)
        # pdf.cell(130, 10, txt=f"{start_time}", border=1)
        # pdf.ln(10)

        # # Finish Time row
        # pdf.cell(60, 10, txt="Finish Time:", border=1)
        # pdf.cell(130, 10, txt=f"{end_time}", border=1)
        # pdf.ln(10)

        # # Time Taken row
        # pdf.cell(60, 10, txt="Time Taken:", border=1)
        # pdf.cell(130, 10, txt=f"{time_taken:.2f} seconds", border=1)
        # pdf.ln(20)
        
        # newly added code👇 
        fields = [
            ("Category", category),
            ("Total Score", f"{score}/{len(questions)}"),
            ("Correct Answers", correct_count),
            ("Incorrect Answers", incorrect_count),
            ("Start Time", start_time),
            ("Finish Time", end_time),
            ("Time Taken", f"{time_taken:.2f} seconds")
        ]

        for i, (field, detail) in enumerate(fields):
            # Alternate color for rows
            if i % 2 == 0:
                pdf.set_fill_color(230, 240, 255)  # Light color for even rows
            else:
                pdf.set_fill_color(255, 255, 255)  # White for odd rows

            # Create cells with the fill color
            pdf.cell(80, 10, txt=field, border=1, ln=0, fill=True)
            pdf.cell(110, 10, txt=str(detail), border=1, ln=1, fill=True)

        pdf.ln(30)  # Leave some space after the table

        # pdf.cell(200, 10, txt="Quiz Report", ln=True, align="C")
        # pdf.cell(200, 10, txt=f"Category: {category}", ln=True)
        # pdf.cell(200, 10, txt=f"Total Score: {score}/{len(questions)}", ln=True)
        # pdf.cell(200, 10, txt=f"Correct Answers: {correct_count}", ln=True)
        # pdf.cell(200, 10, txt=f"Incorrect Answers: {incorrect_count}", ln=True)
        # pdf.cell(200, 10, txt=f"Start Time: {start_time}", ln=True)
        # pdf.cell(200, 10, txt=f"Finish Time: {end_time}", ln=True)
        # pdf.cell(200, 10, txt=f"Time Taken: {time_taken:.2f} seconds", ln=True)

        pdf.image(chart_path, x=60, y=100, w=90)
        pdf.output(report_path)
        
        if os.path.exists(chart_path):
            os.remove(chart_path)

        feedback_label.config(text=f"Report generated: {report_path}", fg="blue")

        # Email validation and sending report
        email = email_entry.get()
        if not is_valid_email(email):
            feedback_label.config(text="Invalid email format. Please enter a correct email.", fg="red")
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        else:
            send_email_with_report(email, report_path, feedback_label)


    root = tk.Tk()
    root.title("Quiz App")
    root.geometry("500x500")
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

    # Create a label to display the current score
    score_label = tk.Label(root, text=f"Score: {score}/{len(questions)}", font=button_font, bg="lightblue")
    score_label.pack(pady=10)

    submit_button = tk.Button(root, text="Submit", command=submit_answer, font=button_font, bg="#ffa07a", fg="white")
    submit_button.pack(pady=10)

    next_button = tk.Button(root, text="Next", command=next_question, font=button_font, bg="#4682b4", fg="white")
    next_button.pack(side="right", padx=20, pady=10)

    back_button = tk.Button(root, text="Go Back", command=previous_question, font=button_font, bg="#4682b4", fg="white")
    back_button.pack(side="left", padx=20, pady=10)

    generate_report_button = tk.Button(root, text="Download Report", command=generate_report, font=button_font, bg="#00CED1", fg="white")
    generate_report_button.pack_forget()  # Initially hidden until quiz is completed

    email_label = tk.Label(root, text="Enter your email:", font=("Arial", 12), bg="lightblue")
    email_label.pack(pady=5)
    email_entry = tk.Entry(root, font=("Arial", 12))
    email_entry.pack(pady=5)

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

    categories = ["Mathematics", "Science", "Geography", "Literature"]

    for category in categories:
        button = tk.Button(category_window, text=category, font=button_font, bg="#FFDDC1", fg="black", width=20, command=lambda c=category: [category_window.destroy(), select_question_number(c)])
        button.pack(pady=10)

    category_window.mainloop()

select_category()
conn.close()