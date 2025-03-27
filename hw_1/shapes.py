from homeworks.hw_1.main import Circle, Rectangle

while True:
        print("\nChoose a shape:")
        print("1. Circle")
        print("2. Rectangle")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            radius = float(input("Enter the radius: "))
            circle = Circle(radius)
            print(f"Area: {circle.area():.2f}")
            print(f"Perimeter: {circle.perimeter():.2f}")

        elif choice == "2":
            width = float(input("Enter the width: "))
            height = float(input("Enter the height: "))
            rectangle = Rectangle(width, height)
            print(f"Area: {rectangle.area():.2f}")
            print(f"Perimeter: {rectangle.perimeter():.2f}")

        elif choice == "3":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice! Please enter 1, 2, or 3.")