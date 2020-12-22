import canvasapi

def list_courses(canvas):
    """Method for listing all of a teacher's courses along with ID numbers
    and course codes. Can be used later to add to the shelf file."""
    all_courses = canvas.get_courses()
    for course in all_courses:
        print("Course ID: " + str(course.id).ljust(10, '.') + course.name)

def set_course(canvas_object):
    """Method to set the current course in use."""
    course_number = int(input("Please enter the course number of the class.\n>>> ").strip())
    course = canvas_object.get_course(course_number)
    return course

def current_students(current_course):
    """Create a list of all current students and get a count. Count used for progress bars/feedback when iterating through all users."""
    count = 0 #resets the count if one had been previously made
    all_students = current_course.get_users(enrollment_type=['student'])
    for user in all_students:
        count += 1
    return count, all_students

def update_course(current_course):
    """Method for updating various course parameters, such as name, start/end date, etc..."""
    done = False
    while not done:
        user_choice = input("Choose course parameter to update:\n\n" +
        "1. Course Name\n" + 
        "2. Course Code\n" +
        "3. Start Date\n" +
        "4. End Date\n").strip()
        if user_choice in ["1"]:
            print("Current course name:", current_course.name)
            new_name = input("Provide the new course name: ").strip()
            current_course.update(course={'name':new_name})
            print("Course name changed to", current_course.name)
        elif user_choice in ["2"]:
            print("Current course code:", current_course.course_code)
            new_name = input("Provide the new course code: ").strip()
            current_course.update(course={'course_code':new_name})
            print("Course code changed to", current_course.course_code)
        elif user_choice in ["3"]:
            pass
            '''
                print(current_course.start_at)
                current_course.update(current_course={'start_at':'2020-12-20T00:01Z'})
                print(current_course.start_at)
                '''
        elif user_choice == "":
            break
        else:
            print("Not a valid parameter.")
