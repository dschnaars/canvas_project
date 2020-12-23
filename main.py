import canvasapi, time 
import assignment_methods, course_methods, module_methods

token = '5593~yT5hxNeSPWoWVirrMP8DZBbSr10nkIXaUJJRVoybQfO7lvFlh4RlMVtGHutBdQr4'
url_API = 'https://sacs.instructure.com'

#create a Canvas object for the given user; provides access to courses, assignments, users, etc...
canvas = canvasapi.Canvas(url_API, token)

print("\nWelcome to the SACS Canvas Interface.\nPlease enter the course number for the course you would like to work with today.\n")
time.sleep(2)
course_methods.list_courses(canvas)

#create a course object for the specified course number
current_course = course_methods.set_course(canvas)
course_methods.update_course(current_course)

count, all_students = course_methods.current_students(current_course)
print(count)

#course_methods.update_course(current_course)
#module_methods.display_modules(current_course)
#module_methods.update_module(current_course)


#assignment_methods.add_points(current_course, count)

#creates a Paginated List of all courses
#courses = canvas.get_courses()

#create course objects for specific, singular courses
#acad_bio = canvas.get_course(35855)
#h_bio = canvas.get_course(36134)
'''Useful attributes for each course include the following. Use for loop to review all attributes.
    course.id
    course.name
    course.sis_course_id

courses = canvas.get_courses()
course_attributes = vars(courses[0])
for item in course_attributes.items():
    print(item)
'''

#useful loop for listing all courses of a certain name along with ID numbers
'''
for course in courses:
    if 'Schnaars' in course.name:
        #print(type(course))
        print(course.name)
        print(course.course_code)
        print(course.sis_course_id)
'''

#creates a paginated list of all assignments for a specific class 
#assignments = acad_bio.get_assignments()
'''Useful attributes for these objects include the following. Use the for loop to review all attributes.
    assignment.due_at
    assignment.unlock_at
    assignment.lock_at
    assignment.points_possible
    assignment.assignment_group_id
    assignment.course_id
    assignment.name
    assignment.muted
    assignment.needs_grading_count

attributes = vars(assignments[0])
for item in attributes.items():
    print(item)
'''

'''
for assignment in assignments:
    if assignment.id == 541828:
        print(assignment.name)
    if assignment.name == "Indiana's Least Wanted Poster":
        print(assignment.id)
'''

#Need to learn information about users, getting list of all users for a course,
#what attributes they have, methods, etc...

#creates a paginated list of all users for the given course. The example below will return only students.
#all_users = acad_bio.get_users(enrollment_type=['student'])
'''Useful attributes for students include the following.
    student.id
    student.name
    student.sortable_name
    student.login_id
    student.email

user_vars = vars(all_users[0])
for item in user_vars.items():
    print(item)
'''

#get a single assignment and print the student's score or a message that they did not submit the assignment
#inv_species = acad_bio.get_assignment(541828)

'''
ass_attributes = vars(inv_species)
for item in ass_attributes.items():
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
