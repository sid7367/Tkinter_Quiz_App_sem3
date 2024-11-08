import mysql.connector as ms
import tkinter as tk
from tkinter import font

#establishing the connection
conn = ms.connect(host='localhost',
                               user='root',
                               password='SIDsql@2005#', 
                               database='Quiz_Questions')

cursor = conn.cursor()

# Global variable to track first start
first_start = True

#global variable to keep track of question index
question_index = 0

def get_questions(category):
    query = "SELECT question_text, option1, option2, option3, option4 FROM questions WHERE category = %s"
    cursor.execute(query, (category,))
    return cursor.fetchall()
    
def start_quiz(category): 

    global first_start, question_index # Declare the global variable

    questions = get_questions(category) # based on category
    #using tk alias name for tkinter module and creating a application window where all widgets will reside
    root = tk.Tk()   
    root.title("Quiz App")  #setting the title of the window
    root.geometry("500x400")  #setting the size of the window
    root.configure(bg="lightblue")  #setting the background color of the window

    title_font = font.Font(family="Helvetica", size=16, weight="bold")
    question_font = font.Font(family="Helvectica", size=14, weight = "bold")
    option_font = font.Font(family="Arial", size=12)
    button_font = font.Font(family="Arial", size=12, weight="bold")


    # creates a label widget for question text
    question_label = tk.Label(root, text="", font = question_font)  

    # adds the q. label widget into the window
    question_label.pack(pady=(20,20)) 

    # Radiobuttons for options
    # variable for holding value of selected option and updates automatically when user selects option 👇
    var = tk.StringVar(value = "None of the options... Select one")  # by default a value is given 
    # creates a radio button widget for options
    """
    variable = var is used to link all radio buttons to the same variable, 
    meaning selecting one will deselect the others.

    text = "" label for each radio button which will be populated later
    """
    option_frame = tk.Frame(root,bg = "#f0f8ff")
    option_frame.pack()

    option1_radio = tk.Radiobutton(option_frame, variable=var, font = option_font,text="",bg="#f0f8ff",activebackground="#f0f8ff")
    option2_radio = tk.Radiobutton(option_frame, variable=var, font = option_font,text="",bg="#f0f8ff",activebackground="#f0f8ff")
    option3_radio = tk.Radiobutton(option_frame, variable=var, font = option_font,text="",bg="#f0f8ff",activebackground="#f0f8ff")
    option4_radio = tk.Radiobutton(option_frame, variable=var, font = option_font,text="",bg="#f0f8ff",activebackground="#f0f8ff")


    #adds each radio button to the application window 
    option1_radio.pack(anchor="w",pady = 5)
    option2_radio.pack(anchor="w",pady = 5)
    option3_radio.pack(anchor="w",pady = 5)
    option4_radio.pack(anchor="w",pady = 5)

    # to print the submitted option
    def submit_answer():
        selected_option = var.get()  # Get the selected option
        print(f"You selected: {selected_option}")

# loading the question data into the widgets
    def load_question(question_data):
        question_text, opt1, opt2, opt3, opt4 = question_data #unpacking the tuple
        question_label.config(text=question_text) #setting question text to widget label
        # sets option_1 text to widget 1 text and value is the part that will be assigned to var if selected
        option1_radio.config(text=opt1, value=opt1)  
        option2_radio.config(text=opt2, value=opt2)
        option3_radio.config(text=opt3, value=opt3)
        option4_radio.config(text=opt4, value=opt4)

    load_question(questions[0])  #loading the first question 

    submit_button = tk.Button(root, text="Submit", width=10,command=submit_answer, font=button_font, bg ="#ffa07a", fg="white")
    submit_button.pack(pady=10)  #adds the submit button to the application window

    # Add Go Back button for the first selection only 👇
    if first_start:
        first_start = False  # Set to False after the first start
        go_back_button = tk.Button(root, text="Go Back",font=button_font, bg="#ffa07a", fg="white", command=lambda: [root.destroy(), select_category()])
        go_back_button.pack(pady=10)

    root.mainloop() # for keeping window open always


# Function to create the category selection window
def select_category():
    category_window = tk.Tk()
    category_window.title("Select Quiz Category")
    category_window.geometry("400x300")
    category_window.configure(bg="#f5f5f5")

    # Styling title and button fonts
    label_font = font.Font(family="Helvetica", size=14, weight="bold")
    button_font = font.Font(family="Arial", size=12)

    tk.Label(category_window, text="Choose a Category",font=label_font,bg="#f5f5f5", fg="navy").pack(pady = 20)


    # List of categories
    categories = ["Science", "Mathematics", "Literature", "Geography"]

    # Function to handle category selection
    def handle_selection(category):
        category_window.destroy()  # Close the category selection window
        start_quiz(category)  # Open the quiz window for the selected category

    # Create a button for each category in the category window
    for cat in categories:
        button = tk.Button(category_window, text=cat, font=button_font, bg="#4682b4", fg="white",width=20,command=lambda c=cat: handle_selection(c))
        button.pack(pady = 10)

    category_window.mainloop()

# Start the app with category selection window
select_category()

# Close the database connection
conn.close()