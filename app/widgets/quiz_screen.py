# app/widgets/quiz_screen.py
import re
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QRadioButton, QCheckBox, QLineEdit,
    QTextEdit, QButtonGroup, QFrame
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QTimer, Qt

# Import from the project's root
from config import SCORE_WEIGHTS
from quiz_utils import check_answer

class QuizScreen(QWidget):
    """The main screen where the quiz is taken, with an improved vertical layout."""
    def __init__(self, quiz_data, finish_callback, auto_advance_enabled):
        super().__init__()
        self.quiz_data = quiz_data
        self.finish_callback = finish_callback
        self.current_q_index = 0
        self.auto_advance_enabled = auto_advance_enabled
        self.auto_advance_timer = QTimer(self)
        self.auto_advance_timer.setSingleShot(True)
        self.auto_advance_timer.timeout.connect(self.next_question)
        self._setup_layout()
        self._load_question()

    def _setup_layout(self):
        """Sets up the new single-column vertical layout."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # Status Bar (Top)
        status_layout = QHBoxLayout()
        self.q_count_label, self.difficulty_label, self.score_label = QLabel(), QLabel(), QLabel()
        for label in [self.q_count_label, self.difficulty_label, self.score_label]:
            label.setFont(QFont("Helvetica", 12))
        status_layout.addWidget(self.q_count_label); status_layout.addStretch()
        status_layout.addWidget(self.difficulty_label); status_layout.addStretch()
        status_layout.addWidget(self.score_label)
        self.main_layout.addLayout(status_layout)

        # Question Text Area
        self.question_text = QTextEdit()
        self.question_text.setReadOnly(True)
        self.question_text.setFont(QFont("Helvetica", 16))
        self.question_text.setMaximumHeight(200) # Give it a max height
        self.main_layout.addWidget(self.question_text)

        # Options Area (will be populated dynamically)
        self.options_widget = QWidget()
        self.main_layout.addWidget(self.options_widget)

        self.main_layout.addStretch() # Pushes content up

        # Submit Button (always visible initially)
        self.submit_button = QPushButton("Submit Answer")
        self.submit_button.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        self.submit_button.setMinimumHeight(40)
        self.submit_button.clicked.connect(self.submit_answer)
        self.main_layout.addWidget(self.submit_button, 0, Qt.AlignmentFlag.AlignRight)

        # Feedback Area (appears after submit)
        self.feedback_frame = QFrame()
        self.feedback_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.feedback_layout = QVBoxLayout(self.feedback_frame)
        
        self.feedback_status_label = QLabel()
        self.feedback_status_label.setFont(QFont("Helvetica", 16, QFont.Weight.Bold)) # Larger, bolder status
        
        self.explanation_text = QTextEdit()
        self.explanation_text.setReadOnly(True)
        self.explanation_text.setFont(QFont("Helvetica", 12)) # Smaller font for details
        
        self.next_button = QPushButton("Next Question")
        self.next_button.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        self.next_button.setMinimumHeight(40)
        self.next_button.clicked.connect(self.next_question)

        self.feedback_layout.addWidget(self.feedback_status_label)
        self.feedback_layout.addWidget(self.explanation_text)
        self.feedback_layout.addWidget(self.next_button, 0, Qt.AlignmentFlag.AlignRight)
        
        self.main_layout.addWidget(self.feedback_frame)

    def _load_question(self):
        """Resets the UI state and loads the next question."""
        self.submit_button.setVisible(True)
        self.feedback_frame.setVisible(False)
        self.next_button.setText("Next Question")

        q_data = self.quiz_data.questions[self.current_q_index]
        self.q_count_label.setText(f"Question: {self.current_q_index + 1}/{len(self.quiz_data.questions)}")
        self.difficulty_label.setText(f"Difficulty: {q_data['difficulty']}")
        self.score_label.setText(f"Score: {self.quiz_data.current_score}")
        self.question_text.setText(q_data['question'])
        self._create_option_widgets(q_data)

    def _create_option_widgets(self, q_data):
        if self.options_widget.layout() is not None:
            QWidget().setLayout(self.options_widget.layout())
        
        layout = QVBoxLayout()
        layout.setSpacing(15) # Increased spacing for readability
        self.options_widget.setLayout(layout)
        
        self.option_inputs = []
        self.numeric_input = None
        q_type = q_data.get('type')
        
        if q_type in ["Multiple Choice - Single Answer", "Quantitative Comparison"]:
            self.answer_group = QButtonGroup(self)
            options = re.findall(r'\([A-Z]\)[^\n]*', q_data['question'])
            if not options:
                options = ["(A) Quantity A is greater.", "(B) Quantity B is greater.", "(C) The two quantities are equal.", "(D) The relationship cannot be determined..."]
            for opt in options:
                rb = QRadioButton(opt.strip()); rb.setFont(QFont("Helvetica", 12)); layout.addWidget(rb); self.option_inputs.append(rb); self.answer_group.addButton(rb)
        elif q_type == "Multiple Choice - Multiple Answers":
            options = re.findall(r'\([A-Z]\)[^\n]*', q_data['question'])
            for opt in options:
                cb = QCheckBox(opt.strip()); cb.setFont(QFont("Helvetica", 12)); layout.addWidget(cb); self.option_inputs.append(cb)
        elif q_type == "Numeric Entry":
            self.numeric_input = QLineEdit(); self.numeric_input.setFont(QFont("Helvetica", 12)); self.numeric_input.setPlaceholderText("Enter your numeric answer here"); layout.addWidget(self.numeric_input)
        else:
            error_label = QLabel("Error: This question is malformed.\nPlease click the button below to continue.")
            error_label.setStyleSheet("color: red;")
            layout.addWidget(error_label)
            self.submit_button.setVisible(False)
            self.feedback_frame.setVisible(True)
            self.feedback_status_label.setText("Question Error")
            self.explanation_text.setText("This question could not be loaded due to a data error.")
            self.next_button.setText("Skip to Next Question")
        layout.addStretch()

    def submit_answer(self):
        """Checks the answer and reveals the feedback area."""
        user_answer = ""
        q_data = self.quiz_data.questions[self.current_q_index]
        q_type = q_data.get('type')
        
        if q_type in ["Multiple Choice - Single Answer", "Quantitative Comparison"]:
            checked_button = self.answer_group.checkedButton()
            if checked_button: user_answer = checked_button.text()
        elif q_type == "Multiple Choice - Multiple Answers":
            user_answer = ",".join(sorted([btn.text()[1] for btn in self.option_inputs if btn.isChecked()]))
        elif q_type == "Numeric Entry":
            user_answer = self.numeric_input.text()

        if not user_answer.strip():
            result = {'question': q_data, 'is_correct': False}
            self.feedback_status_label.setText("❌ No answer submitted. Marked as incorrect.")
            self.feedback_status_label.setStyleSheet("color: #ff9a8c;") # A soft red
            self.explanation_text.setText(f"Correct Answer: {q_data.get('answer', 'N/A')}\n\nExplanation:\n{q_data.get('explanation', 'N/A')}")
        else:
            is_correct = check_answer(q_data, user_answer)
            result = {'question': q_data, 'is_correct': is_correct}
            if is_correct:
                self.feedback_status_label.setText("✅ Correct!")
                self.feedback_status_label.setStyleSheet("color: #a2d9a5;") # A soft green
                self.explanation_text.setText(f"Explanation:\n{q_data.get('explanation', 'N/A')}")
                self.quiz_data.current_score += SCORE_WEIGHTS[q_data['difficulty']]
            else:
                self.feedback_status_label.setText("❌ Incorrect.")
                self.feedback_status_label.setStyleSheet("color: #ff9a8c;")
                self.explanation_text.setText(f"Correct Answer: {q_data.get('answer', 'N/A')}\n\nExplanation:\n{q_data.get('explanation', 'N/A')}")
        
        self.quiz_data.results.append(result)
        self.score_label.setText(f"Score: {self.quiz_data.current_score}")
        
        self.submit_button.setVisible(False)
        self.feedback_frame.setVisible(True)

        if self.auto_advance_enabled:
            self.next_button.setText("Next Question (3...)")
            self.auto_advance_timer.start(3000)

    def next_question(self):
        self.auto_advance_timer.stop()
        self.current_q_index += 1
        if self.current_q_index < len(self.quiz_data.questions):
            self._load_question()
        else:
            self.finish_callback(self.quiz_data)
