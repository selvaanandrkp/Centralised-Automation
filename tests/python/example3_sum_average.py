# Program 3: Sum and Average (static list)

numbers = [10, 20, 30, 40, 50]
print("numbers =", numbers)

total = sum(numbers)
average = total / len(numbers) if len(numbers) != 0 else 0

print("Sum =", total)
print("Average =", average)