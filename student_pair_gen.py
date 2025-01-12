import random
from datetime import datetime

def write_pairs(pairs, students, special_students):
    with open("student_pairs.txt", "w") as file:
        formatted_datetime = datetime.now().strftime("%B %d, %Y %H:%M:%S")
        file.write(f"Generated on: {formatted_datetime}")
        file.write("\n")
        for pair in pairs:
            if pair[1] == True:
                file.write(f"{special_students[pair[0][0]]} , {special_students[pair[0][1]]}")
            else:
                file.write(f"{students[pair[0][0]]} , {students[pair[0][1]]}")
            file.write("\n")

def gen_pairs(list, is_special):
    if len(list) <= 3:
        pairs = [(tuple(list), is_special)]
    else:
        pairs = [((list[0], list[1]), is_special)] + gen_pairs(list[2:], is_special)
    return pairs

def create_indices_pairs(n, is_special):
    numbers = list(range(n))
    random.shuffle(numbers)
    return gen_pairs(numbers, is_special)

def parse_file(file):
    students = []
    for line in file:
        # Remove leading spaces and newline characters
        line = line.strip()

        # Append to List
        students.append("\"" + line + "\"")
    return students

def get_students(filename):
    try:
        with open(filename, "r") as file:
            students = parse_file(file)
    except FileNotFoundError:
        print("File not found!")
    except PermissionError:
        print("You don't have permission to open this file.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return students

def get_special_students(filename):
    try:
        with open(filename, "r") as file:
            special_students = parse_file(file)
    except FileNotFoundError:
        pass # file doesn't have to exist
    except PermissionError:
        print("You don't have permission to open this file.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return special_students

def main():
    students = get_students("students.txt")
    special_students = get_special_students("special_students.txt")

    # can't make a pair with one student
    if (len(special_students) == 1):
        students += special_students
        special_students.clear()

    if special_students:
        # remove special students from students
        students = list(filter(lambda item: item not in set(special_students), students))

        # create one combined shuffled list of indicies pair
        combined_pairs = create_indices_pairs(len(students), False) + create_indices_pairs(len(special_students), True)
        random.shuffle(combined_pairs)

        write_pairs(combined_pairs, students, special_students) 
    else:
        student_pairs = create_indices_pairs(len(students), False)
        write_pairs(student_pairs, students, special_students)

if __name__ == "__main__":
    main()