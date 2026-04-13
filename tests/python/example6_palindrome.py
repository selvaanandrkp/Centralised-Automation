# Program 6: Palindrome using while loop (simple)

text = "madam"
rev = ""
i = len(text) - 1

while i >= 0:
    rev = rev + text[i]
    i -= 1

print("text =", text)
print("reverse =", rev)

if text == rev:
    print("Palindrome")
else:
    print("Not a Palindrome")
