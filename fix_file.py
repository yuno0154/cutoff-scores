
import re

file_path = r'd:\Antigravity\추정분할점수\나이스 학기말 추정분할점수 산출.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix broken html += ' pattern (single quote followed by newline)
# Example: html += ' \n <table>
fixed_content = re.sub(r"html \+= '(?!\s*`)[\s\n]*", "html += '", content)

# Also fix cases where a single quote is missing its closing counterpart before a newline in html concatenation
# This is a bit complex, but essentially we want to make sure strings are closed.
# However, a simpler way is to replace the whole problematic sections from a known good state.

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("Cleanup attempt 1 finished.")
