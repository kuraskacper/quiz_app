from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Quiz, Question, Answer, QuizAccessCode, Result, UserAnswer
from datetime import datetime
from pprint import pprint
from . import db

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    if current_user.role == 'student':
        return redirect(url_for('views.enter_quiz_code'))
    elif current_user.role == 'teacher':
        return redirect(url_for('views.quizzes'))
    elif current_user.role == 'admin':
        return redirect(url_for('views.results'))


@views.route('/enter-quiz-code')
@login_required
def enter_quiz_code():
    if current_user.role == 'student' or current_user.role == 'admin':
        return render_template("enter-quiz-code.html", user=current_user)
    else:
        return redirect(url_for('views.home'))


@views.route('/take-quiz', methods=['GET', 'POST'])
@login_required
def take_quiz():
    if request.method == 'POST':
        access_code = request.form.get('access-code')
        quiz_access_code = QuizAccessCode.query.filter_by(access_code=access_code).first()
        print(quiz_access_code)
        if quiz_access_code is None:
            flash(f"Kod dostępu: \"{access_code}\" nie istnieje!", category='error')
        elif quiz_access_code.expires_at < datetime.now():
            flash(f"Kod dostępu: \"{access_code}\" jest przeterminowany!", category='error')
        else:
            quiz = Quiz.query.get(quiz_access_code.quiz_id)
            flash(f'Pomyślnie rozpoczęto quiz \"{quiz.title}\"!')
            new_result = Result(user_id=current_user.id, quiz_id=quiz.id)
            db.session.add(new_result)
            db.session.commit()
            return render_template('take-quiz.html', user=current_user, quiz=quiz, result_id=new_result.id)
    return redirect(url_for('views.home'))


@views.route('/submit-quiz', methods=['GET', 'POST'])
@login_required
def submit_quiz():
    if request.method == 'POST':
        quiz_results = request.form.to_dict()
        pprint(quiz_results)

        quiz: Quiz = Quiz.query.get(quiz_results['quiz-id'])
        result: Result = Result.query.get(quiz_results['result-id'])
        all_answers = 0
        correct_answers = 0
        for question_number, question in enumerate(quiz.questions):
            all_answers += 1
            for answer_number, answer in enumerate(question.answers):
                correct_answer = False
                if int(request.form.get(f'{question_number + 1}')) == answer_number + 1:
                    if answer.is_correct:
                        correct_answers += 1
                        correct_answer = True
                    new_user_answer = UserAnswer(user_id=current_user.id, question_id=question.id, answer_id=answer.id,
                                                 result_id=result.id, is_correct=correct_answer)
                    db.session.add(new_user_answer)
                    break
            else:
                new_user_answer = UserAnswer(user_id=current_user.id, question_id=question.id, answer_id=None,
                                             result_id=result.id, is_correct=False)
                db.session.add(new_user_answer)

        pprint(quiz)
        pprint(result)
        result.all_answers = all_answers
        result.correct_answers = correct_answers
        result.score_percentage = round((correct_answers / all_answers) * 100, 2)
        result.completed_at = datetime.now()
        db.session.commit()
        flash(f'Zakończono quiz \"{quiz.title}\" z wynikiem: {result.score_percentage}%!', category='success')
        return redirect(url_for('views.results'))

    return redirect(url_for('views.home'))


class UserResult:
    def __init__(self, result: Result):

        quiz: Quiz = Quiz.query.get(result.quiz_id)
        self.id = result.id
        self.title = quiz.title
        self.description = quiz.description
        day_names_pl = {
            '0': "Niedziela",
            '1': "Poniedziałek",
            '2': "Wtorek",
            '3': "Środa",
            '4': "Czwartek",
            '5': "Piątek",
            '6': "Sobota"
        }
        self.started_at = f'{day_names_pl[f"{result.started_at:%w}"]} {result.started_at:%H:%M %d-%m-%Y}'
        self.completed_at = f'{day_names_pl[f"{result.started_at:%w}"]} {result.started_at:%H:%M %d-%m-%Y}'
        self.questions = []

        for quiz_question in quiz.questions:
            question = {'text': quiz_question.text}
            temp_answers = {}
            for number, quiz_answer in enumerate(quiz_question.answers):
                user_answer = UserAnswer.query.filter_by(user_id=current_user.id, question_id=quiz_question.id,
                                                         answer_id=quiz_answer.id, result_id=result.id).first()

                # print(f'{current_user.id = }')
                # print(f'{quiz_question.id = }')
                # print(f'{quiz_answer.id = }')
                # print(f'{result.id = }')
                #
                # print(f'{user_answer = }')

                temp_value = 'neutral'
                if user_answer is not None:
                    question['check_answer'] = number + 1
                    if user_answer.is_correct:
                        temp_value = 'correct'
                    else:
                        temp_value = 'wrong'
                else:
                    if quiz_answer.is_correct:
                        temp_value = 'correct'

                temp_answers[f'{quiz_answer.text}'] = temp_value
            question['answers'] = temp_answers
            self.questions.append(question)
        self.score = result.score_percentage
        self.correct_answer = result.correct_answers
        self.all_answer = result.all_answers
        if result.score_percentage <= 30:
            self.score_percentage_color = 'red'
        elif 30 < result.score_percentage <= 50:
            self.score_percentage_color = '#FF5F1F'
        elif 50 < result.score_percentage <= 80:
            self.score_percentage_color = 'gold'
        else:
            self.score_percentage_color = 'lime'


@views.route('/results')
@login_required
def results():
    if current_user.role == 'student' or current_user.role == 'admin':

        results_query = Result.query.filter(
            Result.user_id == current_user.id,
            Result.completed_at.isnot(None)
        ).all()
        print("__________________________________________________________")
        print(results_query)
        print("__________________________________________________________")
        sorted_results = sorted(results_query, key=lambda r: r.completed_at, reverse=True)

        results = [UserResult(result) for result in sorted_results]

        return render_template("results.html", user=current_user, results=results)
    else:
        return redirect(url_for('views.home'))


@views.route('/create-quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    if request.method == 'POST':
        quiz = handle_posted_quiz(request)
        pprint(quiz)

        if not check_quiz_validity(quiz):
            return render_template('create-quiz.html', user=current_user, quiz=quiz)
        else:
            title = quiz['info']['title']
            description = quiz['info']['description']
            author_id = current_user.id
            new_quiz = Quiz(title=title, description=description, author_id=author_id)
            db.session.add(new_quiz)
            db.session.commit()
            quiz_id = new_quiz.id
            for question in quiz['questions']:
                text = question['text']
                new_question = Question(quiz_id=quiz_id, text=text, )
                db.session.add(new_question)
                db.session.commit()
                question_id = new_question.id
                for index, answer in enumerate(question['answers']):
                    is_correct = True if question['correct_answer'] == index + 1 else False
                    text = answer[0]
                    new_answer = Answer(question_id=question_id, text=text, is_correct=is_correct)
                    db.session.add(new_answer)
                    db.session.commit()
            flash(f'Quiz o nazwie \"{quiz['info']['title']}\" został pomyślnie utworzony!', category='success')
            return redirect(url_for('views.home'))
    else:
        if current_user.role == 'teacher' or current_user.role == 'admin':
            return render_template("create-quiz.html", user=current_user, quiz=0)
        else:
            return redirect(url_for('views.home'))


@views.route('/quizzes')
@login_required
def quizzes():
    quizzes = Quiz.query.filter_by(author_id=current_user.id).all()
    quizzes = sorted(quizzes, key=lambda q: q.created_at, reverse=True)

    if current_user.role == 'teacher' or current_user.role == 'admin':
        return render_template("quizzes.html", user=current_user, quizzes=quizzes)
    else:
        return redirect(url_for('views.home'))


@views.route('/access-code', methods=["POST"])
@login_required
def access_code():
    quiz_id = request.form.get('quiz-id')
    quiz_title = request.form.get('quiz-title')
    access_code = request.form.get('access-code')

    if len(access_code) < 4:
        flash("Kod dostępu musi mieć minimum 4 znkai!", category='error')
    elif QuizAccessCode.query.filter_by(access_code=access_code).count() > 0:
        flash("Podany kod jest już w użytku!", category='error')
    else:
        new_access_code = QuizAccessCode(quiz_id=quiz_id, access_code=access_code)
        db.session.add(new_access_code)
        db.session.commit()
        flash(
            f'Quiz o nazwie \"{quiz_title}\" został uruchominy do {new_access_code.expires_at:%H:%M:%S} z kodem dostępu: \"{access_code}\"!',
            category='success')

    return redirect(url_for('views.quizzes'))


@views.route('/students-results')
@login_required
def students_results():
    if current_user.role == 'teacher' or current_user.role == 'admin':
        quizzes = Quiz.query.filter_by(author_id=current_user.id).all()
        results = {}
        for quiz in quizzes:
            results[quiz.id] = Result.query.filter_by(quiz_id=quiz.id).all()

        return render_template('students-results.html', user=current_user, quizzes=quizzes, results=results)
    else:
        return redirect(url_for('views.home'))


def check_quiz_validity(quiz):
    message = ''
    if quiz['info']['title'] == '':
        message = "Tytuł quizu nie może być pusty!"
    elif quiz['info']['question_count'] == 0:
        message = "Quiz musi mieć conajmniej 1 pytanie!"
    else:
        for question_number, question in enumerate(quiz['questions']):
            if question['text'] == "":
                message = f"Pytanie nr {question_number + 1} nie posiada treści!"
                break
            elif question['answer_count'] < 2:
                message = f"Pytanie nr {question_number + 1} nie ma wystarczjącej ilości odpowiedzi. Minimalna liczba to 2!"
                break
            elif question['correct_answer'] is None:
                message = f"Pytani nr {question_number + 1} nie ma wybranej poprawnej odpowiedz!"
                break
            else:
                for answer_number, answer in enumerate(question['answers']):
                    if answer[0] == "":
                        message = f"Odpowiedź nr {answer_number + 1} w pytaniu nr {question_number + 1} jest pusta!"
                        break
    if message != '':
        flash(message, category='error')
        return False
    else:
        return True


def handle_posted_quiz(request):
    quiz_info = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'question_count': int(request.form.get('question-counter'))
    }
    questions = []
    for i in range(1, quiz_info['question_count'] + 1):
        questions_text = request.form.get(f'question-{i}-text')
        answer_count = int(request.form.get(f'question-{i}-answer-counter'))
        correct_answer = request.form.get(f'correct-question-{i}')
        if correct_answer is not None:
            correct_answer = int(correct_answer.split('-')[1])
        answers = [[request.form.get(f'question-{i}-answer-{j}')] for j in range(1, answer_count + 1)]
        question = {
            'text': questions_text,
            'answer_count': answer_count,
            'correct_answer': correct_answer,
            'answers': answers
        }

        questions.append(question)

    quiz = {
        'info': quiz_info,
        'questions': questions
    }

    return quiz
