from utils import analyze_clause_with_llm

# Fake legal text for testing
sample_text = """
The company reserves the right to terminate the account at any time without notice.
The user data will be sold to third-party advertisers for revenue generation.
Disputes will be resolved in the court of Mars.
"""

print("AI Analysis chal raha hai... Wait karo...")
result = analyze_clause_with_llm(sample_text)
print("\n--- RESULT AA GAYA --- \n")
print(result)