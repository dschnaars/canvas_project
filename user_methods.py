import canvasapi, time 

def get_assignments(current_course):
    """Method for viewing the list of assignments for a given user."""
    user_id = int(input("Enter the ID number for the user you wish to retrieve:\n>>> "))
    user = current_course.get_user(user_id)

    assignments = user.get_assignments(current_course.id)

    attributes = vars(assignments[14])
    for item in attributes.items():
        print(item)