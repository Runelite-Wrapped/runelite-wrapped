import json


def load_gradebook(filename):
    with open(filename, "r") as file:
        student_data = json.load(file)
    return student_data["StudentInformation"][0]


def save_gradebook(filename, gradebook):
    with open(filename, "w") as file:
        json.dump({"StudentInformation": [gradebook]}, file, indent=4)


def add_student(gradebook, name, grade):
    gradebook[name] = {"Grade": grade}


def update_grade(gradebook, name, grade):
    if name in gradebook:
        gradebook[name]["Grade"] = grade
    else:
        print(f"Student {name} not found.")


def delete_student(gradebook, name):
    if name in gradebook:
        del gradebook[name]
    else:
        print(f"Student {name} not found.")


def display_gradebook(gradebook):
    for name, info in gradebook.items():
        print(f"{name}: {info['Grade']}")


def main():
    filename = "data/grades.json"
    gradebook = load_gradebook(filename)

    while True:
        print("\nOptions:")
        print("1. Add student")
        print("2. Update student grade")
        print("3. Delete student")
        print("4. Display gradebook")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            name = input("Enter student name: ")
            grade = int(input("Enter student grade: "))
            add_student(gradebook, name, grade)
            save_gradebook(filename, gradebook)
        elif choice == "2":
            name = input("Enter student name: ")
            grade = int(input("Enter new grade: "))
            update_grade(gradebook, name, grade)
            save_gradebook(filename, gradebook)
        elif choice == "3":
            name = input("Enter student name: ")
            delete_student(gradebook, name)
            save_gradebook(filename, gradebook)
        elif choice == "4":
            display_gradebook(gradebook)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
