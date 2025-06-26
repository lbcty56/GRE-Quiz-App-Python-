# app/widgets/results_screen.py
from collections import defaultdict
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFormLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from config import SCORE_WEIGHTS, PERFORMANCE_LEVELS
from .results_chart import ResultsChart

class ResultsScreen(QWidget):
    """The final screen showing results and the performance graph, with an improved layout."""
    def __init__(self, quiz_data, restart_callback, quit_callback):
        super().__init__()
        layout = QVBoxLayout(self)
        summary_layout = QHBoxLayout()
        
        text_results_widget = QWidget()
        # --- UI/UX ENHANCEMENT ---
        # Using QFormLayout for a much cleaner, two-column presentation of results.
        text_results_layout = QFormLayout(text_results_widget)
        text_results_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        text_results_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        self._generate_text_results(quiz_data, text_results_layout)
        summary_layout.addWidget(text_results_widget, stretch=1)
        
        # Topic statistics calculation
        topic_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
        for r in quiz_data.results:
            topic = r['question']['topic']
            topic_stats[topic]['total'] += 1
            if r['is_correct']:
                topic_stats[topic]['correct'] += 1
                
        self.chart = ResultsChart(self, width=6, height=5, dpi=100)
        self.chart.plot(topic_stats)
        summary_layout.addWidget(self.chart, stretch=2)
        
        layout.addLayout(summary_layout)
        
        button_layout = QHBoxLayout()
        restart_button = QPushButton("Take Another Quiz")
        quit_button = QPushButton("Quit")
        restart_button.clicked.connect(restart_callback)
        quit_button.clicked.connect(quit_callback)
        button_layout.addStretch()
        button_layout.addWidget(restart_button)
        button_layout.addWidget(quit_button)
        layout.addLayout(button_layout)

    def _generate_text_results(self, quiz_data, layout):
        """Generates all the textual result information using the new QFormLayout."""
        title = QLabel("Quiz Results")
        title.setFont(QFont("Helvetica", 24, QFont.Weight.Bold))
        layout.addRow(title)
        
        total_correct = sum(1 for r in quiz_data.results if r['is_correct'])
        total_q = len(quiz_data.results)
        score_percent = quiz_data.current_score / quiz_data.max_score if quiz_data.max_score > 0 else 0
        
        layout.addRow(QLabel(""), QLabel("")) # Spacer
        layout.addRow("Correct Questions:", QLabel(f"<b>{total_correct}/{total_q} ({total_correct/total_q:.1%})</b>"))
        layout.addRow("Weighted Score:", QLabel(f"<b>{quiz_data.current_score}/{quiz_data.max_score} ({score_percent:.1%})</b>"))
        
        diff_title = QLabel("\n--- Performance by Difficulty ---")
        diff_title.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        layout.addRow(diff_title)
        
        diff_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
        for r in quiz_data.results:
            diff = r['question']['difficulty']
            diff_stats[diff]['total'] += 1
            if r['is_correct']:
                diff_stats[diff]['correct'] += 1
                
        for diff, num_planned in sorted(quiz_data.intended_counts.items(), key=lambda item: list(SCORE_WEIGHTS.keys()).index(item[0])):
            stats = diff_stats[diff]
            percent = (stats['correct'] / stats['total']) if stats['total'] > 0 else 0
            layout.addRow(f"{diff}:", QLabel(f"{stats['correct']}/{stats['total']} ({percent:.0%})  (Planned: {num_planned})"))
            
        assessment_title = QLabel("\n--- Final Assessment ---")
        assessment_title.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        layout.addRow(assessment_title)
        
        assessment_label = QLabel()
        for threshold, (level, desc) in sorted(PERFORMANCE_LEVELS.items(), reverse=True):
            if score_percent >= threshold:
                assessment_label.setText(f"<b>{level}:</b> {desc}")
                break
        assessment_label.setWordWrap(True)
        layout.addRow(assessment_label)