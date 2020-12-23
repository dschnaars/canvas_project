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

def update_module(current_course):
    """Method for updating module parameters."""
    module_num = int(input("Module number: ").strip())
    current_module = current_course.get_module(module_num)
    print(current_module.name)
    current_module.edit(module={'name':'New Name'})
    print(current_module.name)