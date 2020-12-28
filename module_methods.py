import canvasapi

def display_modules(current_course):
    """Method for displaying all of the current modules for the selected course."""
    modules = current_course.get_modules()
    for module in modules:
        print("Module ID:", str(module.id).ljust(10, '.'), module.name)

def set_module(current_course):
    """Method to set the current module in use."""
    #TODO: add a check to verify that the module number added is actually in the teacher's list of modules. 
    valid = True
    while valid:
        module_number = int(input("Please enter the module number of interest.\n>>> ").strip())
        try:
            module = current_course.get_module(module_number)
            valid = False
        except (canvasapi.exceptions.Unauthorized, canvasapi.exceptions.ResourceDoesNotExist):
            print("Invalid Module Number")
        except ValueError:
            print("Invalid Module Number")
    return module

def display_module_items(current_module):
    """Method for displaying all of the items in the selected module."""
    all_items = current_module.get_module_items()
    for item in all_items:
        print(item)

def new_module(current_course):
    """Method for creating a new module from scratch."""
    module_name = input("Provide a name for the new module:\n>>>").strip()
    current_course.create_module(module={'name':module_name})

def edit_module(current_course, current_module):
    """Method for updating module parameters."""
    done = False
    while not done:
        user_choice = input("\nChoose module parameter to update:\n\n" +
        "1. Module Name\n" + 
        "2. Module Position\n" +
        "3. Published Status\n" +
        "4. Require Sequential Progress\n" +
        ">>> ").strip()
        if user_choice in ["1"]:
            print("Current module name:", current_module.name)
            new_name = input("Provide the new module name: ").strip()
            current_module.edit(module={'name':new_name})
            current_module = current_course.get_module(current_module.id) #have to reload the module in order to confirm the change
            print("Module name changed to", current_module.name)
        elif user_choice in ["2"]:
            print("Current module position:", current_module.position)
            new_position = int(input("Provide the new module position: ").strip())
            current_module.edit(module={'position':new_position})
            current_module = current_course.get_module(current_module.id)
            print("Module position changed to", current_module.position)
        elif user_choice in ["3"]:
            print("Current publication status:", current_module.published)
            pub_status = input("Would you like the current module published? (Y/N):\n>>> ").strip().upper()
            if pub_status == 'Y':
                current_module.edit(module={'published':True})
            elif pub_status == 'N':
                current_module.edit(module={'published':False})
            else:
                print("Please enter only 'y' or 'n' for publishing the current module.")
            current_module = current_course.get_module(current_module.id)
            print("New publication status:", current_module.published)
        elif user_choice in ["4"]:
            print("Sequential progress required:", current_module.require_sequential_progress)
            req_seq_progress = input("Would you like to require sequential progress of module items? (Y/N):\n>>> ").strip().upper()
            if req_seq_progress == 'Y':
                current_module.edit(module={'require_sequential_progress':True})
            elif req_seq_progress == 'N':
                current_module.edit(module={'require_sequential_progress':False})
            else:
                print("Please enter only 'y' or 'n' for requiring sequential progress.")
            current_module = current_course.get_module(current_module.id)
            print("Sequential progress required:", current_module.require_sequential_progress)
            '''
            elif user_choice in ["4"]:
                print("Current end date:", current_course.end_at)
                print("End date must follow format YYYY-MM-DD")
                new_end = input("Provide the new end date: ").strip()
                new_end += "T23:59Z"
                current_course.update(course={'end_at':new_end})
                print("New end date:", current_course.end_at)
            '''
        elif user_choice == "":
            break
        else:
            print("Not a valid parameter.")
        
def copy_module(current_course):
    """Method for copying a module and modifying it. Junior's Method"""

    #TODO: create a module object of the template module to be copied
    display_modules(current_course)
    template_module = set_module(current_course) #runs the set_module method from above allowing the user to set the module # to copy from

    #TODO: create a new module and edit the attributes to match those of the template module
    new_module = current_course.create_module(module={'name':template_module.name + ' copy'}) 

    #TODO: iterate through the module_items() from the template module and create a new assignment with the same attributes each time
    old_items = template_module.get_module_items()

    for item in old_items:
        #print(item.type, item.content_id, type(item.id), item.title)
        old_assignment = current_course.get_assignment(item.content_id)
        #print(old_assignment.points_possible)
        if item.type == 'Assignment':
            assignment = current_course.create_assignment(
                assignment={
                    'name':old_assignment.name, 
                    'position':old_assignment.position, 
                    'points_possible':old_assignment.points_possible, 
                    'grading_type':old_assignment.grading_type, 
                    'due_at':old_assignment.due_at, 
                    'lock_at':old_assignment.lock_at, 
                    'unlock_at':old_assignment.unlock_at, 
                    'assignment_group_id':old_assignment.assignment_group_id, 
                    'published':old_assignment.published, 
                    'omit_from_final_grade':old_assignment.omit_from_final_grade, 
                    'allowed_attempts':old_assignment.allowed_attempts
                    }) 
            new_module.create_module_item(
                module_item={
                    'title':item.title, 
                    'type':'Assignment', 
                    'content_id':assignment.id, 
                    'position':item.position, 
                    'indent':item.indent, 
                    #'new_tab':item.new_tab, 
                    'completion_requirement':{
                        'type':'must_mark_done'}, #item.completion_requirement.type}, 
                    #'completion_requirement':{
                        #'min_score':item.completion_requirement.min_score},
                    'module_item':item.published,
                    })
    
    new_module.edit(module={'unlock_at':template_module.unlock_at, 'position':template_module.position + 1, 'require_sequential_progress':template_module.require_sequential_progress, 'publish_final_grade':template_module.publish_final_grade, 'published':template_module.published})

    #That seems like it...?