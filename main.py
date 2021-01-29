import canvasapi, time 
import assignment_methods, course_methods, module_methods, quiz_methods, user_methods

token = '5593~yT5hxNeSPWoWVirrMP8DZBbSr10nkIXaUJJRVoybQfO7lvFlh4RlMVtGHutBdQr4'
url_API = 'https://sacs.instructure.com'

#create a Canvas object for the given user; provides access to courses, assignments, users, etc...
canvas = canvasapi.Canvas(url_API, token)

#create a course object for the specified course number
print("\nWelcome to the SACS Canvas Interface.\n\nPlease enter the course number for the course you would like to work with today.\n")
course_methods.list_courses(canvas)
current_course = course_methods.set_course(canvas)
count, all_students = course_methods.current_students(current_course)

user_choice = ''    #create an initial empty string for the user choice that will be 
                    #modified to indicate what the user would like to do within the program today

while user_choice not in ['q', 'Q', 'quit', 'Quit']:
    print("\n\nPlease indicate what you would like to do today:" +
        "\n\nCourse Methods" +
        "\n\t1a. List Courses" +
        "\n\t1b. Set Current Course" +
        "\n\t1c. Create .csv for Current Course Student Users" +
        "\n\t1d. Update Course" +
        "\n\nModule Methods" +
        "\n\t2a. Display Modules in Current Course" +
        "\n\t2b. Set Current Module" +
        "\n\t2c. Display Module Items" +
        "\n\t2d. Edit Module" +
        "\n\t2e. Copy Module (Junior's Method)" +
        "\n\t2f. Get Missing Assignments Report"
        "\n\nQuiz Methods" +
        "\n\t3a. Report Checkpoint Results to Parents" +
        "\n\t3b. Excuse Lower Score Checkpoint A/B" +
        "\n\nUser Methods" +
        "\n\t4a. List Assignments for a User"
        )
    user_choice = input("\n>>> ").strip().lower()

    if user_choice == '1a':
        pass

    elif user_choice == '1c':
        """Create a .csv file including student sortable name, name, ID, email, and fields that can be filled for parent names and emails."""
        course_methods.create_users_CSV(current_course)

    elif user_choice == '2c':
        """Display the items within a particular module."""
        module_methods.display_modules(current_course)
        current_module = module_methods.set_module(current_course)
        module_methods.display_module_items(current_module)

    elif user_choice == '2f':
        """Generate a missing assignment report for the current module and have it emailed to the teacher."""
        module_methods.display_modules(current_course)
        current_module = module_methods.set_module(current_course)
        module_methods.missing_assignment_report(current_course, count, all_students, current_module)
        #pass

    elif user_choice == '3a':
        """Generate an email to parents of students following a checkpoint
        in order to report whether their student passed, failed, or achieved
        mastery."""
        module_methods.display_modules(current_course)
        current_module = module_methods.set_module(current_course)
        quiz_methods.parent_test_report(current_course, current_module)

    elif user_choice == '3b':
        """Iterate through Checkpoint A and B submissions, excusing the lower of the two scores."""
        module_methods.display_modules(current_course)
        current_module = module_methods.set_module(current_course)
        quiz_methods.keep_high_checkpoint(current_course, current_module, count, all_students)

    elif user_choice == '4a':
        """Display all of the assignments for a given student in a course."""
        user_methods.get_assignments(current_course)

'''
courses = canvas.get_courses()
course_attributes = vars(courses[0])
for item in course_attributes.items():
    print(item)
'''

'''
submission = inv_species.get_submission(18313)
for student in all_users:
    submission = inv_species.get_submission(student.id)
    if submission.score == None:
        print(student.name, "Did not turn in this assignment.")
        print(submission.score)
    elif submission.score == 0:
        print(student.name, "scored a zero out of {} on this assignment.".format(inv_species.points_possible))
    else:
        pass
'''
