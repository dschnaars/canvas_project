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

def current_users(current_course):
    """Create a list of all current users and get a count. Count used for progress bars/feedback when iterating through all users."""
    count = 0 #resets the count if one had been previously made
    all_users = current_course.get_users(enrollment_type=['student'])
    for user in all_users:
        count += 1
    return count, all_users

def update_course(current_course):
    """Method for updating various course parameters, such as name, start/end date, etc..."""
    #new_name = input("Provide the new course name: ").strip()
    #print(current_course.name)
    #current_course.update(current_course={'name':'Python Project'})
    #print(current_course.name)
'''
    print(current_course.start_at)
    current_course.update(current_course={'start_at':'2020-12-20T00:01Z'})
    print(current_course.start_at)
    '''