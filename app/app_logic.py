# app/app_logic.py
import random
from collections import defaultdict

# --- Import from root project modules ---
from question_bank import gre_quant_bank
from config import DIFFICULTY_PROPORTIONS, SCORE_WEIGHTS

class QuizData:
    """A non-GUI class to hold the data for a single quiz instance."""
    def __init__(self, questions, level, intended_counts):
        self.questions = questions
        self.level = level
        self.intended_counts = intended_counts
        self.results = []
        self.current_score = 0
        self.max_score = sum(SCORE_WEIGHTS[q['difficulty']] for q in self.questions)

class AppLogic:
    """Manages the application state and quiz creation logic."""
    def __init__(self):
        self.full_bank = gre_quant_bank
        self.used_qids = set()
        self.last_level = 1
        self.last_num_questions = 10
        self.last_auto_advance = False

    def select_questions(self, level, num_questions):
        """Selects a unique set of questions from the available bank."""
        bank_was_reset = False
        available_questions = [q for q in self.full_bank if q['qid'] not in self.used_qids]

        if not available_questions:
            self.used_qids.clear()
            bank_was_reset = True
            available_questions = self.full_bank

        if len(available_questions) < num_questions:
            num_questions = len(available_questions)

        grouped_questions = defaultdict(list)
        for q in available_questions:
            grouped_questions[q['difficulty']].append(q)

        proportions = DIFFICULTY_PROPORTIONS[level]
        counts = {d: num_questions * p for d, p in proportions.items()}
        base_counts = {d: int(c) for d, c in counts.items()}
        remainders = {d: c - base_counts[d] for d, c in counts.items()}
        num_to_distribute = num_questions - sum(base_counts.values())
        sorted_by_remainder = sorted(remainders.items(), key=lambda item: item[1], reverse=True)
        for i in range(num_to_distribute):
            base_counts[sorted_by_remainder[i][0]] += 1
        
        intended_counts = base_counts.copy()
        questions_for_quiz = []

        for diff, num in base_counts.items():
            actual_to_select = min(num, len(grouped_questions[diff]))
            if actual_to_select > 0:
                questions_for_quiz.extend(random.sample(grouped_questions[diff], actual_to_select))

        if len(questions_for_quiz) < num_questions:
            current_qids = {q['qid'] for q in questions_for_quiz}
            spillover_pool = [q for q in available_questions if q['qid'] not in current_qids]
            num_needed = num_questions - len(questions_for_quiz)
            if num_needed > 0 and spillover_pool:
                questions_for_quiz.extend(random.sample(spillover_pool, min(num_needed, len(spillover_pool))))
        
        random.shuffle(questions_for_quiz)
        return questions_for_quiz, intended_counts, bank_was_reset
