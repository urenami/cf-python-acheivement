num1 = int(input("Enter a number: "))
num2 = int(input("Enter another number: "))
operator = input("Enter an operator (+ or -): ")

if operator == "+":
    result = num1 + num2
    print("The sum of", num1, "and", num2, "is", result)
elif operator == "-":
    result = num1 - num2
    print(num1, "minus", num2, "is", result)
else:
    print("Invalid operator. Please enter + or -.")
