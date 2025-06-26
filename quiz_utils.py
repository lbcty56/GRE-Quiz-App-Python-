# quiz_utils.py
import re

def check_answer(question_data, user_answer_str):
    """
    Checks if a user's answer is correct, with flexible parsing.

    Args:
        question_data (dict): The dictionary for the question.
        user_answer_str (str): The raw string input from the user.

    Returns:
        bool: True if the answer is correct, False otherwise.
    """
    q_type = question_data.get('type')
    correct_answer_str = question_data.get('answer', '')

    # --- FIX FOR "INCORRECT" BUG ---
    # The original logic was not robust enough. This new logic extracts the
    # capital letter from BOTH the user's answer and the correct answer string
    # and compares them directly. This is the most reliable method.
    if q_type == 'Multiple Choice - Single Answer' or q_type == 'Quantitative Comparison':
        user_match = re.search(r'[A-Z]', user_answer_str.strip().upper())
        correct_match = re.search(r'[A-Z]', correct_answer_str.strip().upper())

        if user_match and correct_match:
            user_letter = user_match.group()
            correct_letter = correct_match.group()
            return user_letter == correct_letter
        return False # Return false if a letter couldn't be found in one of the strings

    elif q_type == 'Numeric Entry':
        try:
            if re.fullmatch(r'-?\d+(\.\d+)?', user_answer_str.strip()):
                user_num = float(user_answer_str)
                correct_num = float(correct_answer_str)
                return user_num == correct_num
        except (ValueError, TypeError):
            clean_user = user_answer_str.replace(" ", "").lower()
            clean_correct = correct_answer_str.replace(" ", "").lower()
            return clean_user == clean_correct

    elif q_type == 'Multiple Choice - Multiple Answers':
        correct_set = {char for char in correct_answer_str if char.isalpha()}
        normalized_user_str = re.sub(r'[\s;/-]+', ',', user_answer_str.strip().upper())
        user_set = {ans.strip() for ans in normalized_user_str.split(',') if ans.strip()}
        return correct_set == user_set

    return False