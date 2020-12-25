import canvasapi
from progress.bar import ChargingBar

def set_assignment(current_module):
    """Method to set the current assignment in use."""

    valid = True
    while valid:
        assignment_number = int(input("Please enter the assignment number of interest.\n>>> ").strip())
        try:
            assignment = current_module.get_module_item(assignment_number)
            valid = False
        except (canvasapi.exceptions.Unauthorized, canvasapi.exceptions.ResourceDoesNotExist):
            print("Invalid Assignment Number")
        except ValueError:
            print("Invalid Assignment Number")
    return assignment 

def add_points(current_course, count):
    """Method to add points to all student scores, such as when curving a test."""
    added_points = int(input("Please specify the number of points to be added to the assignment.\n>>> ").strip())
    assignment_number = int(input("Please specify the assignment number for the assignment you would like to modify.\n>>> ").strip()) 

    current_assignment = current_course.get_assignment(assignment_number)

    submissions = current_assignment.get_submissions()
    bar = ChargingBar('Modifying Scores', max=count)

    for submission in submissions:
        if submission.score != None:
            score = submission.score + added_points
        else:
            pass

        submission.edit(submission={'posted_grade':score})
        bar.next()

    bar.finish()