class Height:
    def __init__(self, feet, inches):
        self.feet = feet
        self.inches = inches

    def __sub__(self, other):
        total_inches_self = self.feet * 12 + self.inches
        total_inches_other = other.feet * 12 + other.inches

        result_inches = total_inches_self - total_inches_other

        # Ensure the result is non-negative
        if result_inches < 0:
            raise ValueError("Result cannot be negative")

        result_feet, result_inches = divmod(result_inches, 12)
        return Height(result_feet, result_inches)

    def __str__(self):
        return f"{self.feet} feet and {self.inches} inches"


person_a = Height(5, 10)
person_b = Height(3, 9)
height_diff = person_a - person_b

print(f"Height difference: {height_diff}")
