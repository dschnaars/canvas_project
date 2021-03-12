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

def keep_high_checkpoint(current_course, current_module, count, all_students):
    """Method for examining Checkpoint A and B and keeping high score while excusing low."""
    filename = input("Enter the name of the .csv file to pull data from:\n>>> ").strip()

    #create a dictionary of all users where the user ID is main key, value is a dictionary
    #of keys:values such as sortable name, checkpoint A/B scores, etc..
    students_dictionary = {}
    with open(filename, 'r') as csv_read:
            students = csv.reader(csv_read)

            next(students) #skip the header row

            for student in students:
                students_dictionary[student[2]] = {
                    'sortable_name':student[0]
                }

    #Display all tests/quizzes in this module and choose the test of interest
    all_items = current_module.get_module_items()
    for item in all_items:
        if item.type == 'Quiz':
            print(item.title, item.content_id)
    
    #Gather submissions for Checkpoint A
    checkpoint_id = int(input("Enter the Quiz ID number for Checkpoint A: ").strip())
    checkpoint_a = current_course.get_quiz(checkpoint_id)
    checkpoint_a_submissions = checkpoint_a.get_submissions()

    #Gather submissions for Checkpoint B
    checkpoint_id = int(input("Enter the Quiz ID number for Checkpoint B: ").strip())
    checkpoint_b = current_course.get_quiz(checkpoint_id)
    checkpoint_b_submissions = checkpoint_b.get_submissions()

    #Iterate through submissions and add score to each student in the dictionary
    for submission in checkpoint_a_submissions:
        if str(submission.user_id) in students_dictionary:
            students_dictionary[str(submission.user_id)]['score_a'] = submission.score

    for submission in checkpoint_b_submissions:
        if str(submission.user_id) in students_dictionary:
            students_dictionary[str(submission.user_id)]['score_b'] = submission.score

    check_a_not_taken = []
    check_b_not_taken = []
    neither_taken = []
    for student in students_dictionary:
        name = students_dictionary[student]['sortable_name']
        if 'score_a' in students_dictionary[student]: 
            if students_dictionary[student]['score_a'] == None:
                check_a_not_taken.append(name)
            else:
                print(name, students_dictionary[student]['score_a'])
        if 'score_b' in students_dictionary[student]:
            if students_dictionary[student]['score_b'] == None:
                check_b_not_taken.append(name)
            else:
                print(name, students_dictionary[student]['score_b'])
            
    print(check_a_not_taken, '\n', check_b_not_taken, '\n', neither_taken)
'''
    attributes = vars(checkpoint_b_submissions[0])
    for item in attributes.items():
        print(item)
'''

def parent_test_report(current_course, current_module):
    """Method for reporting mastery, passing, or failing test results to parents."""

    #Create a dictionary of all students and parent emails
    students_dictionary = {}
    filename = input("Enter filename to use for generating student data:\n>>> ").lower().strip()
    with open(filename, 'r') as csv_read:
        students = csv.reader(csv_read)

        next(students) #skip the header row

        for student in students:
            students_dictionary[student[2]] = {
                'sortable_name':student[0],
                'name':student[1], 
                'parent_1':student[5],
                'parent_email1':student[6], 
                'parent_2':student[7],
                'parent_email2':student[8],
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
    honors_or_acad = input("Is this report for Honors (H) or Academic (A)?\n>>> ").upper().strip()

    if honors_or_acad == 'H':
        mastery = points_possible * 0.87
        email_mastery = '87'
    elif honors_or_acad == 'A':
        mastery = points_possible * 0.85
        email_mastery = '85'
    else:
        print("No valid selection provided for 'Honors or Academic' class")
        
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
    #test_counter = 0
    no_test_taken = []
    failed_parent_emails = []

    for user in students_dictionary:
        if 'score' in students_dictionary[user]:
            score = int(students_dictionary[user]['score'])
            raw_score = score / points_possible * 100
            percent_score = round(raw_score, 1)
            if students_dictionary[user]['score'] == points_possible:
                message = (
                    f"Subject: {students_dictionary[user]['name']} Biology Test Grade\n\n"\
                    f"{students_dictionary[user]['parent_1']},"\
                    f"\n\n\tThis is Mr. Schnaars, {students_dictionary[user]['first_only']}'s Biology teacher. I wanted to follow up from our test today and "\
                    f"let you know that {students_dictionary[user]['first_only']} scored {percent_score} percent on the {current_quiz.title} test today. "\
                    f"I am of course pleased with that score and I hope {students_dictionary[user]['pro_1']} is too. Please encourage {students_dictionary[user]['pro_2']} to continue preparing for future tests in the same manner."\
                    f"\n\nThanks,\n\nDaniel Schnaars\ndschnaars@sacs.k12.in.us\nBiology Teacher, Homestead High School"
                ) 

            elif students_dictionary[user]['score'] >= mastery:
                message = (
                    f"Subject: {students_dictionary[user]['name']} Biology Test Grade\n\n"\
                    f"{students_dictionary[user]['parent_1']},"\
                    f"\n\n\tThis is Mr. Schnaars, {students_dictionary[user]['first_only']}'s Biology teacher. I wanted to follow up from our test today and "\
                    f"let you know that {students_dictionary[user]['first_only']} scored {percent_score} percent on the {current_quiz.title} test today. This means {students_dictionary[user]['pro_1']} not only passed the test, but "\
                    f"achieved the HHS standard for Mastery, {email_mastery}. {students_dictionary[user]['first_only']} may still take Checkpoint B on {check_b_date} to try and achieve a higher score, but is not required to do so. Please encourage "\
                    f"{students_dictionary[user]['pro_2']} to continue to prepare for future tests this semester the way {students_dictionary[user]['pro_1']} did for this one, and reach out to me if you have any questions or concerns."\
                    f"\n\nThanks,\n\nDaniel Schnaars\ndschnaars@sacs.k12.in.us\nBiology Teacher, Homestead High School"
                )
            
            elif students_dictionary[user]['score'] >= passing:
                message = (
                    f"Subject: {students_dictionary[user]['name']} Biology Test Grade\n\n"\
                    f"{students_dictionary[user]['parent_1']},\n\n\tThis is Mr. Schnaars, {students_dictionary[user]['first_only']}'s Biology teacher. I wanted to follow up from our test today and "\
                    f"let you know that {students_dictionary[user]['first_only']} scored {percent_score} percent on the {current_quiz.title} test today. {students_dictionary[user]['first_only']} will have a chance to "\
                    f"achieve Mastery ({email_mastery}%) and replace this score with a higher one when we take our Checkpoint B assessment on {check_b_date}. We will have a study session during class tomorrow as we work on correctives for the test, and "\
                    f"you can reach out to me if you have any questions or concerns."\
                    f"\n\nThanks,\n\nDaniel Schnaars\ndschnaars@sacs.k12.in.us\nBiology Teacher, Homestead High School"
                )

            elif students_dictionary[user]['score'] < passing:
                message = (
                    f"Subject: {students_dictionary[user]['name']} Biology Test Grade\n\n"\
                    f"{students_dictionary[user]['parent_1']},\n\n\tThis is Mr. Schnaars, {students_dictionary[user]['first_only']}'s Biology teacher. I wanted to follow up from our test today and "\
                    f"let you know that {students_dictionary[user]['first_only']} scored {percent_score} percent on the {current_quiz.title} test today, meaning that {students_dictionary[user]['pro_1']} did not pass the test. "\
                    f"{students_dictionary[user]['first_only']} will have a chance to replace this score with a higher one when we take our Checkpoint B assessment on {check_b_date}. Please encourage {students_dictionary[user]['pro_2']} to study the material from this "\
                    f"unit. We will work on the correctives assignment for this test tomorrow in class, and you can reach out to me if you have any questions or concerns."\
                    f"\n\nThanks,\n\nDaniel Schnaars\ndschnaars@sacs.k12.in.us\nBiology Teacher, Homestead High School"
                )
            
            #Send an email to the parent name 1 on file; will need to build in a check here to send to each parent if 2 listed
            try:
                smtpObj.sendmail(username, students_dictionary[user]['parent_email1'], message)
                print("successful email sent to", students_dictionary[user]['sortable_name'])
            
            except smtplib.SMTPRecipientsRefused:
                failed_parent_emails.append([students_dictionary[user]['sortable_name'], students_dictionary[user]['parent_1'], students_dictionary[user]['parent_email1']])
            #smtpObj.sendmail(username, students_dictionary[user]['parent_email1'].strip(), message)
            #test_counter += 1
        
        else:
            no_test_taken.append(students_dictionary[user]['sortable_name'])    

        #test loop to keep me from accidentally sending myself 100 emails...
        #if test_counter == 15:
            #break

    smtpObj.quit()

    print("\nThe following students have not yet taken the test:")
    for student in no_test_taken:
        print(student)
    
    print("\nThe following parent emails were invalid:")
    for parent in failed_parent_emails:
        print(parent)

def parent_notify(current_course, current_module):
    """Method to notify parent that student should attend study session."""

    #Create a dictionary of all students and parent emails
    students_dictionary = {}
    filename = input("Enter filename to use for generating student data:\n>>> ").lower().strip()
    with open(filename, 'r') as csv_read:
        students = csv.reader(csv_read)

        next(students) #skip the header row

        for student in students:
            students_dictionary[student[2]] = {
                'sortable_name':student[0],
                'name':student[1], 
                'parent_1':student[5],
                'parent_email1':student[6], 
                'parent_2':student[7],
                'parent_email2':student[8],
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
    test_date = input("Please enter date for upcoming Checkpoint test:\n>>>")
    session_date = input("Please enter date for upcoming study session:\n>>>")
    current_quiz = current_course.get_quiz(test_choice)
    threshold = current_quiz.points_possible * 0.67

    #Iterate through submissions and add score to each student in the dictionary
    submissions = current_quiz.get_submissions()
    for submission in submissions:
        if submission.score <= threshold:
            students_dictionary[str(submission.user_id)]['score'] = submission.score

    '''
    for user in students_dictionary:
        if 'score' in students_dictionary[user]:
            print(students_dictionary[user]['name'], students_dictionary[user]['score'])
    '''

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
    no_test_taken = []
    failed_parent_emails = []

    for user in students_dictionary:
        if 'score' in students_dictionary[user]:
            message = (
                f"Subject: Biology After-School Study Sessions\n\n"\
                f"{students_dictionary[user]['parent_1']},\n\n\tThis is Mr. Schnaars, "\
                f"{students_dictionary[user]['first_only']}'s Biology teacher. We have a Checkpoint test coming up next week, "\
                f"{test_date}, and I wanted let you know that {students_dictionary[user]['first_only']} can stay after school or join via Zoom for "\
                f"help preparing for this test if {students_dictionary[user]['pro_1']} would like or you feel {students_dictionary[user]['pro_1']} would benefit from it. "\
                f"Students can stay until about 3:10 on {session_date}, approximately half an hour, and be picked up from Door 26 outside the Freshman Academy. "\
                f"Please let me know if you have any questions or need any additional details about this study/help session for the test."\
                f"\n\nThanks,\n\nDaniel Schnaars\ndschnaars@sacs.k12.in.us\nBiology Teacher, Homestead High School"
            )
            
            #Send an email to the parent name 1 on file; will need to build in a check here to send to each parent if 2 listed
            try:
                smtpObj.sendmail(username, students_dictionary[user]['parent_email1'], message)
                #smtpObj.sendmail(username, username, message)
                print("successful email sent to", students_dictionary[user]['sortable_name'])
            
            except smtplib.SMTPRecipientsRefused:
                failed_parent_emails.append([students_dictionary[user]['sortable_name'], students_dictionary[user]['parent_1'], students_dictionary[user]['parent_email1']])
            #smtpObj.sendmail(username, students_dictionary[user]['parent_email1'].strip(), message)
            #test_counter += 1
        
        else:
            no_test_taken.append(students_dictionary[user]['sortable_name'])    

    smtpObj.quit()

    print("\nThe following students have not yet taken the test:")
    for student in no_test_taken:
        print(student)
    
    print("\nThe following parent emails were invalid:")
    for parent in failed_parent_emails:
        print(parent)

'''
attributes = vars(submissions[0])
for item in attributes.items():
    print(item)
'''