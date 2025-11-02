num1 = input("Enter first number: ")
try:
    num1 = int(num1)
except ValueError:
    print("Invalid input. Please enter an integer.")
    exit()

num2 = input("Enter second number: ")
try:
    num2 = int(num2)
except ValueError:
    print("Invalid input. Please enter an integer.")
    exit()

sum = num1 + num2
print(sum)