# app/main_window.py
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from .app_logic import AppLogic, QuizData
from .widgets.welcome_screen import WelcomeScreen
from .widgets.quiz_screen import QuizScreen
from .widgets.results_screen import ResultsScreen

class QuizApp(QMainWindow):
    """The main application window and controller."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GRE Quantitative Practice Quiz")
        self.setGeometry(100, 100, 950, 750)
        self.setMinimumSize(800, 600)
        
        self.app_logic = AppLogic()
        self.show_welcome_screen()

    def show_welcome_screen(self):
        """Shows the welcome screen, re-using last settings from AppLogic."""
        welcome_widget = WelcomeScreen(
            self.start_quiz,
            self.app_logic.last_level,
            self.app_logic.last_num_questions,
            self.app_logic.last_auto_advance
        )
        self.setCentralWidget(welcome_widget)

    def start_quiz(self, level, num_questions, auto_advance):
        """Starts a new quiz session."""
        self.app_logic.last_level = level
        self.app_logic.last_num_questions = num_questions
        self.app_logic.last_auto_advance = auto_advance

        questions, intended_counts, bank_was_reset = self.app_logic.select_questions(level, num_questions)
        
        if bank_was_reset:
            QMessageBox.information(self, "Question Bank Reset", "You have completed all available questions. The question bank has been reset.")

        if not questions:
            self.show_welcome_screen()
            return

        quiz_data = QuizData(questions, level, intended_counts)
        for q in questions:
            self.app_logic.used_qids.add(q['qid'])

        quiz_widget = QuizScreen(quiz_data, self.show_results, auto_advance)
        self.setCentralWidget(quiz_widget)

    def show_results(self, quiz_data):
        """Shows the results screen."""
        results_widget = ResultsScreen(quiz_data, self.show_welcome_screen, self.close)
        self.setCentralWidget(results_widget)