# config.py

# Defines the mix of questions for each quiz level
DIFFICULTY_PROPORTIONS = {
    1: {'Simple': 0.50, 'Middle': 0.30, 'Hard': 0.15, 'Challenging': 0.05}, # Novice
    2: {'Simple': 0.30, 'Middle': 0.40, 'Hard': 0.20, 'Challenging': 0.10}, # Beginner
    3: {'Simple': 0.20, 'Middle': 0.30, 'Hard': 0.30, 'Challenging': 0.20}, # Intermediate
    4: {'Simple': 0.10, 'Middle': 0.20, 'Hard': 0.40, 'Challenging': 0.30}, # Advanced
    5: {'Simple': 0.05, 'Middle': 0.15, 'Hard': 0.40, 'Challenging': 0.40}  # Expert
}

# Defines the points awarded for correct answers by difficulty
SCORE_WEIGHTS = {
    'Simple': 1,
    'Middle': 2,
    'Hard': 4,
    'Challenging': 6
}

# Defines the performance levels based on the final weighted score percentage
PERFORMANCE_LEVELS = {
    0.90: ("Expert", "Outstanding performance, comparable to the top tier of test-takers."),
    0.75: ("Advanced", "Strong command of GRE Quant concepts with solid problem-solving skills."),
    0.60: ("Intermediate", "Good foundation, but focus on consistency and tackling harder problems."),
    0.40: ("Beginner", "Building a foundation. Focus on mastering core concepts in each topic."),
    0.00: ("Novice", "This is a starting point. Review fundamental arithmetic and algebra concepts.")
}