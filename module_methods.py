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

def edit_module(current_module):
    """Method for updating module parameters."""
    done = False
    while not done:
        user_choice = input("Choose module parameter to update:\n\n" +
        "1. Module Name\n" + 
        "2. Module Position\n" +
        "3. Published Status\n" +
        "4. Require Sequential Progress\n" +
        ">>> ").strip()
        if user_choice in ["1"]:
            print("Current module name:", current_module.name)
            new_name = input("Provide the new module name: ").strip()
            current_module.edit(module={'name':new_name})
            print("Module name changed to", current_module.name)
        elif user_choice in ["2"]:
            print("Current module position:", current_module.position)
            new_position = input("Provide the new module position: ").strip()
            current_module.edit(module={'position':new_position})
            print("Module position changed to", current_module.position)
        elif user_choice in ["3"]:
            print("Current publication status:", current_module.published)
            pub_status = input("Would you like the current module published? (Y/N):\n>>> ").strip().upper()
            if pub_status == 'Y':
                current_module.edit(module={'published':True})
            elif pub_status == 'N':
                current_module.edit(module={'published':True})
            else:
                print("Please enter only 'y' or 'n' for publishing the current module.")
            print("New publication status:", current_module.published)
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
