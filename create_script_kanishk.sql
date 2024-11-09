CREATE DATABASE quiz_questions;

USE quiz_questions;

CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_text VARCHAR(255) NOT NULL,
    option1 VARCHAR(100) NOT NULL,
    option2 VARCHAR(100) NOT NULL,
    option3 VARCHAR(100),
    option4 VARCHAR(100),
    correct_answer VARCHAR(100) NOT NULL,
    category VARCHAR(50) DEFAULT 'General'
);

INSERT INTO questions (question_text, option1, option2, option3, option4, correct_answer, category)
VALUES 
    ("What is the capital of France?", "Paris", "Berlin", "Rome", "Madrid", "Paris", "Geography"),
    ("Which planet is known as the Red Planet?", "Earth", "Mars", "Jupiter", "Venus", "Mars", "Science"),
    ("What is 5 + 7?", "10", "11", "12", "13", "12", "Mathematics"),
    ("Who wrote 'To Kill a Mockingbird'?", "Harper Lee", "Mark Twain", "J.K. Rowling", "Ernest Hemingway", "Harper Lee", "Literature"),
    ("Which element has the chemical symbol 'O'?", "Gold", "Oxygen", "Osmium", "Oganesson", "Oxygen", "Science");

INSERT INTO questions (question_text, option1, option2, option3, option4, correct_answer, category)
VALUES 
    ("What is the largest desert in the world?", "Sahara", "Arctic", "Antarctic", "Gobi", "Antarctic", "Geography"),
    ("Which country has the most natural lakes?", "Canada", "USA", "India", "Brazil", "Canada", "Geography"),
    ("What is the longest river in the world?", "Amazon", "Nile", "Yangtze", "Mississippi", "Nile", "Geography"),
    ("Which country is known as the Land of the Rising Sun?", "China", "South Korea", "Japan", "Vietnam", "Japan", "Geography"),
    ("What is the smallest country in the world?", "Monaco", "San Marino", "Vatican City", "Liechtenstein", "Vatican City", "Geography"),
    ("Which city is known as the Big Apple?", "Los Angeles", "Chicago", "New York", "Miami", "New York", "Geography"),
    ("What is the highest waterfall in the world?", "Niagara Falls", "Victoria Falls", "Angel Falls", "Yosemite Falls", "Angel Falls", "Geography"),
    ("Which continent is known as the Dark Continent?", "Asia", "South America", "Africa", "Australia", "Africa", "Geography"),
    ("Which US state is the largest by area?", "Texas", "California", "Alaska", "Montana", "Alaska", "Geography"),
    
    ("What is the chemical symbol for gold?", "Go", "Gd", "Ga", "Au", "Au", "Science"),
    ("What is the most abundant gas in Earth's atmosphere?", "Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen", "Nitrogen", "Science"),
    ("What is the speed of light?", "300,000 km/s", "150,000 km/s", "299,792 km/s", "299,999 km/s", "299,792 km/s", "Science"),
    ("What planet is closest to the sun?", "Venus", "Earth", "Mercury", "Mars", "Mercury", "Science"),
    ("What is the powerhouse of the cell?", "Nucleus", "Ribosome", "Mitochondria", "Chloroplast", "Mitochondria", "Science"),
    ("What is the chemical formula for water?", "H2O", "O2", "H2", "CO2", "H2O", "Science"),
    ("Who developed the theory of relativity?", "Isaac Newton", "Galileo Galilei", "Albert Einstein", "Nikola Tesla", "Albert Einstein", "Science"),
    ("What is the main gas found in the air we breathe?", "Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen", "Nitrogen", "Science"),
    ("Which planet has the most moons?", "Earth", "Jupiter", "Saturn", "Mars", "Saturn", "Science"),
    
    ("What is 15 + 9?", "23", "24", "22", "25", "24", "Mathematics"),
    ("What is the value of pi?", "3.14", "3.15", "3.13", "3.16", "3.14", "Mathematics"),
    ("What is the square root of 64?", "6", "7", "8", "9", "8", "Mathematics"),
    ("What is 9 x 8?", "71", "72", "73", "74", "72", "Mathematics"),
    ("What is 100 / 4?", "25", "24", "26", "23", "25", "Mathematics"),
    ("What is the result of 6 cubed?", "216", "126", "136", "226", "216", "Mathematics"),
    ("What is the value of 12^2?", "144", "124", "134", "154", "144", "Mathematics"),
    ("What is the smallest prime number?", "0", "1", "2", "3", "2", "Mathematics"),
    ("What is 11 x 11?", "111", "121", "131", "141", "121", "Mathematics"),
    
    ("Who wrote 'Pride and Prejudice'?", "Jane Austen", "Emily Bronte", "Mark Twain", "Charles Dickens", "Jane Austen", "Literature"),
    ("Who is the author of the Harry Potter series?", "J.K. Rowling", "J.R.R. Tolkien", "George R.R. Martin", "C.S. Lewis", "J.K. Rowling", "Literature"),
    ("What is the first book of the Old Testament?", "Genesis", "Exodus", "Leviticus", "Numbers", "Genesis", "Literature"),
    ("Who wrote '1984'?", "George Orwell", "Aldous Huxley", "Ray Bradbury", "Arthur C. Clarke", "George Orwell", "Literature"),
    ("Who wrote 'The Catcher in the Rye'?", "J.D. Salinger", "Ernest Hemingway", "F. Scott Fitzgerald", "John Steinbeck", "J.D. Salinger", "Literature"),
    ("What is the name of the hobbit played by Elijah Wood in the Lord of the Rings movies?", "Samwise", "Frodo", "Bilbo", "Pippin", "Frodo", "Literature"),
    ("Who wrote 'The Great Gatsby'?", "Ernest Hemingway", "F. Scott Fitzgerald", "William Faulkner", "John Steinbeck", "F. Scott Fitzgerald", "Literature"),
    ("Who is the author of 'Moby-Dick'?", "Herman Melville", "Mark Twain", "Nathaniel Hawthorne", "Henry James", "Herman Melville", "Literature"),
    ("Who wrote 'War and Peace'?", "Leo Tolstoy", "Fyodor Dostoevsky", "Anton Chekhov", "Ivan Turgenev", "Leo Tolstoy", "Literature");
