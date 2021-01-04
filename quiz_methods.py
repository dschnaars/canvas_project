import canvasapi

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
