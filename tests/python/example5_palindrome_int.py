# Program 5: Palindrome check for integer using while loop (static number)

n = 121
temp = n
rev = 0

while temp > 0:
    digit = temp % 10
    rev = rev * 10 + digit
    temp = temp // 10

print("n =", n)
print("reverse =", rev)

if n == rev:
    print("Palindrome")
else:
    print("Not a Palindrome")
