# data_validator.py
try:
    from question_bank import gre_quant_bank
except ImportError:
    print("Could not find question_bank.py. Make sure it's in the same directory.")
    exit()

VALID_TYPES = [
    "Multiple Choice - Single Answer",
    "Multiple Choice - Multiple Answers",
    "Numeric Entry",
    "Quantitative Comparison",
]

errors_found = 0
print("--- Starting Question Bank Validation ---")

for i, question in enumerate(gre_quant_bank):
    qid = question.get('qid', f"Unknown QID at index {i}")
    
    # Check 1: Does the 'type' key exist?
    if 'type' not in question:
        print(f"[ERROR] QID: {qid} is missing the 'type' key.")
        errors_found += 1
        continue # Skip to next question
        
    # Check 2: Is the 'type' value one of the valid strings?
    if question['type'] not in VALID_TYPES:
        print(f"[ERROR] QID: {qid} has a misspelled type: '{question['type']}'")
        errors_found += 1

print("\n--- Validation Complete ---")
if errors_found == 0:
    print("✅ No errors found in the question bank. The data is clean.")
else:
    print(f"❌ Found {errors_found} errors. Please correct these entries in question_bank.py.")