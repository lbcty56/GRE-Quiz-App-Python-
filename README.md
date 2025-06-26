GRE Quant Practice Quiz
This is a command-line interface (CLI) application built in Python to help students prepare for the GRE Quantitative Reasoning section. The application provides a customizable and interactive quiz experience using a comprehensive, difficulty-rated question bank.
The core goal is to offer a more effective study tool than static lists of questions by providing adaptive difficulty, immediate feedback, and detailed performance analytics to help users identify and improve on their weak areas.
Key Features:
Comprehensive Question Bank: Includes 200 questions, each with a unique ID, difficulty level, topic, question type, answer, and detailed explanation.
Adaptive Quiz Levels: Users can choose from 5 quiz levels, each with a unique mix of question difficulties, from Novice (mostly simple questions) to Expert (mostly hard and challenging questions).
Immediate Feedback: After every question, the user is told whether their answer was correct and is immediately shown the correct answer and a step-by-step explanation.
Detailed Performance Analysis: At the end of the quiz, a full report is generated, showing:
Overall raw and weighted scores.
A percentage breakdown of performance by difficulty level.
A percentage breakdown of performance by topic (Algebra, Geometry, etc.).
A final qualitative assessment of the user's performance level.
Skills & Concepts Demonstrated
This project showcases several key Python programming skills and best practices:
Object-Oriented Programming (OOP): The entire application is structured around a central Quiz class, which encapsulates the state (score, results) and behavior (preparing, running, checking answers) of a quiz session. This promotes code that is reusable, organized, and easy to maintain.
Data Structures:
Use of list and dict to structure the question bank.
Effective use of collections.defaultdict to efficiently group questions by topic and difficulty without extra boilerplate code.
Application of set for robust, order-independent checking of multiple-choice-multiple-answer questions.
Modularity and File Handling:
The question data (question_bank.py) is decoupled from the application logic (main.py).
A try...except ImportError block is used to ensure the application handles a missing data file gracefully.
Algorithmic Logic: The _prepare_quiz method contains a specific algorithm to select a balanced and randomized set of unique questions based on user-defined parameters, using random.sample and random.shuffle.
Robust User Input and Validation: The main() function uses while True loops and try...except ValueError blocks to ensure the user provides valid input for the quiz setup, preventing crashes from incorrect entries.
Python Best Practices:
Adherence to the if __name__ == "__main__": convention to make the script safely importable and executable.
Use of f-strings for clean, readable string formatting.
Clear separation of configuration (constants) from logic (classes).
How to Run the Project
Follow these steps to run the GRE Quant Practice Quiz on your local machine.
1. Prerequisites:
You must have Python 3 installed.
2. File Setup:
Create a directory for the project.
Inside this directory, create two files:
question_bank.py
main.py
3. Populate the Files:
Copy the entire gre_quant_bank list (containing all 200 questions) and paste it into the question_bank.py file.
Copy the application code (including the Quiz class and main function) and paste it into the main.py file.
4. Execute the Application:
Open a terminal or command prompt.
Navigate to the directory where you saved the two files.
Run the following command:
python3 main.py
