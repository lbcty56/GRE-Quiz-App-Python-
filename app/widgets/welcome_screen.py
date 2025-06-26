# app/widgets/welcome_screen.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QSpinBox, QFrame, QCheckBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class WelcomeScreen(QWidget):
    """The initial screen for selecting quiz settings."""
    def __init__(self, start_callback, last_level, last_num, last_auto_advance):
        super().__init__()
        self.start_callback = start_callback
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        title = QLabel("GRE Quantitative Practice")
        title.setFont(QFont("Helvetica", 32, QFont.Weight.Bold))
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        settings_frame = QFrame()
        settings_frame.setFrameShape(QFrame.Shape.StyledPanel)
        settings_layout = QHBoxLayout(settings_frame)
        settings_layout.addWidget(QLabel("Difficulty Level:"))
        self.level_combo = QComboBox()
        self.level_combo.addItems([str(i) for i in range(1, 6)])
        self.level_combo.setCurrentIndex(last_level - 1)
        settings_layout.addWidget(self.level_combo)
        settings_layout.addSpacing(40)
        settings_layout.addWidget(QLabel("Number of Questions:"))
        self.num_questions_spin = QSpinBox()
        self.num_questions_spin.setRange(5, 50)
        self.num_questions_spin.setValue(last_num)
        settings_layout.addWidget(self.num_questions_spin)
        layout.addWidget(settings_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        self.auto_advance_check = QCheckBox("Auto-advance to next question (3s delay)")
        self.auto_advance_check.setChecked(last_auto_advance)
        layout.addWidget(self.auto_advance_check, alignment=Qt.AlignmentFlag.AlignCenter)

        start_button = QPushButton("Start Quiz")
        start_button.setMinimumSize(200, 50)
        start_button.setFont(QFont("Helvetica", 16, QFont.Weight.Bold))
        start_button.clicked.connect(self.on_start)
        layout.addWidget(start_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def on_start(self):
        self.start_callback(
            int(self.level_combo.currentText()),
            self.num_questions_spin.value(),
            self.auto_advance_check.isChecked()
        )