import canvasapi, csv, smtplib, getpass
import module_methods

def copy_quiz(current_course, new_module, item):
    """Method for copying a quiz and all of its attributes."""

    old_quiz = current_course.get_quiz(item.content_id)
    old_quiz_questions = old_quiz.get_questions()

    new_quiz = current_course.create_quiz(
        quiz={
            'title':old_quiz.title,
            'quiz_type':old_quiz.quiz_type,
            'assignment_group_id':old_quiz.assignment_group_id,
            'time_limit':old_quiz.time_limit,
            'shuffle_answers':old_quiz.shuffle_answers,
            'hide_results':old_quiz.hide_results,
            'show_correct_answers':old_quiz.show_correct_answers,
            'show_correct_answers_last_attempt':old_quiz.show_correct_answers_last_attempt,
            'show_correct_answers_at':old_quiz.show_correct_answers_at,
            'hide_correct_answers_at':old_quiz.hide_correct_answers_at,
            'allowed_attempts':old_quiz.allowed_attempts,
            'scoring_policy':old_quiz.scoring_policy,
            'one_question_at_a_time':old_quiz.one_question_at_a_time,
            'cant_go_back':old_quiz.cant_go_back,
            'access_code':old_quiz.access_code,
            'ip_filter':old_quiz.ip_filter,
            'due_at':old_quiz.due_at,
            'lock_at':old_quiz.lock_at,
            'unlock_at':old_quiz.unlock_at,
            'published':old_quiz.published,
            'one_time_results':old_quiz.one_time_results,
            'only_visible_to_overrides':old_quiz.only_visible_to_overrides
            })

    for quest in old_quiz_questions:
        new_quiz.create_question(question={
            'question_name':quest.question_name,
            'question_text':quest.question_text,
            'quiz_group_id':quest.quiz_group_id,
            'question_type':quest.question_type,
            'position':quest.position,
            'points_possible':quest.points_possible,
            'correct_comments':quest.correct_comments,
            'incorrect_comments':quest.incorrect_comments,
            'neutral_commens':quest.neutral_comments,
            'answers':quest.answers
        })

    new_quiz.edit()

    new_module.create_module_item(
        module_item={
            'title':item.title, 
            'type':'Quiz', 
            'content_id':new_quiz.id, 
            'position':item.position, 
            'indent':item.indent, 
            'completion_requirement':{
                'type':item.completion_requirement['type']}, 
            'module_item':item.published,
            })

def set_extensions(current_course):
    """Method for setting quiz extensions for specified students."""
    pass

def keep_high_checkpoint(current_course, count, all_students):
    """Method for examining Checkpoint A and B and keeping high score while excusing low."""

    #TODO: gather all submissions for the given quizzes in question
    current_module = module_methods.set_module(current_course)
    module_methods.display_module_items(current_module)
    checkpoint_a_id = int(input("Enter the Quiz ID number for Checkpoint A: ").strip())
    checkpoint_b_id = int(input("Enter the Quiz ID number for Checkpoint B: ").strip())

    set_checkpoint_a = current_course.get_quiz(checkpoint_a_id)
    set_checkpoint_b = current_course.get_quiz(checkpoint_b_id)

    checkpoint_a_submissions = set_checkpoint_a.get_submissions()
    checkpoint_b_submissions = set_checkpoint_b.get_submissions()

    #TODO: Iterate through each student in the class and get their scores for each test
    for student in all_students:
        checkpoint_a = 0 #assign initial value of 0 for each quiz.score
        checkpoint_b = 0

def parent_test_report(current_course, current_module):
    """Method for reporting mastery, passing, or failing test results to parents."""

    #Create a dictionary of all students and parent emails
    students_dictionary = {}
    with open('bio_acad.csv', 'r') as csv_read:
        students = csv.reader(csv_read)

        next(students) #skip the header row

        for student in students:
            students_dictionary[student[2]] = {
                'name':student[1], 
                'parent_1':student[5],
                'parent_1_email':student[6], 
                'parent_2':student[7],
                'parent_2_email':student[8],
                'first_only':student[9],
                'pro_1':student[10],
                'pro_2':student[11],
                'pro_3':student[12]
                }

    #Display all tests/quizzes in this module and choose the test of interest
    all_items = current_module.get_module_items()
    for item in all_items:
        if item.type == 'Quiz':
            print(item.title, item.content_id)
    test_choice = int(input("Please type in the Quiz ID for the test of interest:\n>>> "))
    check_b_date = input("Please enter a date for Checkpoint B:\n>>>")
    current_quiz = current_course.get_quiz(test_choice)
    points_possible = current_quiz.points_possible
    mastery = points_possible * 0.85
    passing = points_possible * 0.60

    submissions = current_quiz.get_submissions()
    
    #Iterate through submissions and add score to each student in the dictionary
    for submission in submissions:
        students_dictionary[str(submission.user_id)]['score'] = submission.score

    #Create an smtp object for emailing parents of each student
    smtpObj = smtplib.SMTP('smtp.office365.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()

    authenticated = True
    while authenticated:
        try:
            username = input("Username: ").strip().lower() + '@sacs.k12.in.us'
            password = getpass.getpass("Password: ").strip()

            smtpObj.login(username, password)

            authenticated = False

        except smtplib.SMTPAuthenticationError:
            print("Incorrect username/password")
            smtpObj.quit()

    #Determine which students achieved master, passed, failed, or have not yet taken the assessment.
    test_counter = 0
    for user in students_dictionary:
        if 'score' in students_dictionary[user]:
            percent_score = int(students_dictionary[user]['score']) / points_possible * 100
            if students_dictionary[user]['score'] >= mastery:
                message = """Subject: {} Biology Test Grade 

{},\n\nThis is Mr. Schnaars, your student's Biology teacher at HHS. I wanted to follow up from our test today
and let you know that {} scored {} percent on the {} test today, meaning {} achieved Mastery. Please encourage
them to keep up the hard work and studying in preparation for our tests, and reach out to me if you have any 
questions or concerns.\n\nThanks,\n\nDaniel Schnaars\nBiology Teacher, Homestead High School
                """.format(
                    students_dictionary[user]['name'], 
                    students_dictionary[user]['Parent Name 1'],
                    students_dictionary[user]['name'], 
                    percent_score, 
                    current_quiz.title, 
                    students_dictionary[user]['name'])
            
            elif students_dictionary[user]['score'] >= passing:
                message = """Subject: {} Biology Test Grade 

{},\n\nThis is Mr. Schnaars, your student's Biology teacher at HHS. I wanted to follow up from our test today
and let you know that {} scored {} percent on the {} test today, meaning that while {} passed the test, they failed to achieved Mastery. Please encourage
them to study the material and complete correctives for this test prior to Checkpoint B, and reach out to me if you have any 
questions or concerns.\n\nThanks,\n\nDaniel Schnaars\nBiology Teacher, Homestead High School
                """.format(
                    students_dictionary[user]['name'], 
                    students_dictionary[user]['Parent Name 1'],
                    students_dictionary[user]['name'], 
                    percent_score, 
                    current_quiz.title, 
                    students_dictionary[user]['name'])
            
            elif students_dictionary[user]['score'] < passing:
                message = f"""Subject: {students_dictionary[user]['name']} Biology Test Grade 

{students_dictionary[user]['Parent Name 1']},\n\n\tThis is Mr. Schnaars, and I am {students_dictionary[user]['first_only']}'s Biology 
teacher at HHS. I wanted to follow up from our test today and let you know that {students_dictionary[user]['first_only']} scored 
{percent_score} percent on the {current_quiz.title} test today, meaning that {students_dictionary[user]['pro_1']} did not pass the test.
{students_dictionary[user]['first_only']} will have a chance to replace this score with a higher one when we take Checkpoint B.
Please encourage {students_dictionary[user]['pro_2']} to study the material from this unit and complete correctives for this test prior 
to Checkpoint B on {check_b_date}, and reach out to me if you have any questions or concerns.
\nThanks,\n\nDaniel Schnaars\ndschnaars@sacs.k12.in.us\nBiology Teacher, Homestead High School
                """
            
            #Send an email to the parent name 1 on file; will need to build in a check here to send to each parent if 2 listed
            smtpObj.sendmail(username, username, message)
            test_counter += 1
        
        else:
            print(students_dictionary[user]['name'], "has not taken this test yet.")

        #test loop to keep me from accidentally sending myself 100 emails...
        if test_counter == 5:
            break

    smtpObj.quit()

    '''
    attributes = vars(submissions[0])
    for item in attributes.items():
        print(item)
    '''