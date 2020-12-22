import canvasapi

def display_modules(current_course):
    """Method for displaying all of the current modules for the selected course."""
    modules = current_course.get_modules()
    for module in modules:
        print(module)

def update_module(current_course):
    """Method for updating module parameters."""
    module_num = int(input("Module number: ").strip())
    current_module = current_course.get_module(module_num)
    print(current_module.name)
    current_module.edit(module={'name':'New Name'})
    print(current_module.name)