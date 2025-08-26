"""
Input: Name 
Output: Hello {Name}, Your name has {n} characters
"""

def name_count(name):
    number_of_chars = len(name)
    return f"Hello {name}, Your name has {number_of_chars} characters"


name_local = "Anurup"
response = name_count(name_local)
print(response)