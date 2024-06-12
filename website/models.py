from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import timedelta, datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('student', 'teacher', 'admin'), name='role', nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())

    quizzes = db.relationship('Quiz')
    results = db.relationship('Result')


class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())

    questions = db.relationship('Question')

    def __repr__(self):
        repr_str = (
                f'{self.id = }\n' +
                f'{self.title = }\n' +
                f'{self.description = }\n' +
                f'{self.author_id = }\n' +
                f'{self.created_at = }\n' +
                f'Questions:'
        )
        for q_number, question in enumerate(self.questions):
            repr_str += f'\n Question nr {q_number + 1}: {question.text}'
            for a_number, answer in enumerate(question.answers):
                repr_str += f'\n\tAnswer nr {a_number + 1}: {answer.text}, {answer.is_correct}'

        return repr_str


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())

    answers = db.relationship('Answer')

    def get_correct_answer_text(self):
        return next((answer.text for answer in self.answers if answer.is_correct), None)


class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())


class QuizAccessCode(db.Model):
    __tablename__ = 'quiz_access_codes'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    access_code = db.Column(db.String(50), nullable=False)
    expires_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now() + timedelta(minutes=10))
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())


class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    correct_answers = db.Column(db.Integer, default=0)
    all_answers = db.Column(db.Integer, default=0)
    score_percentage = db.Column(db.Float, default=0)
    started_at = db.Column(db.DateTime(timezone=True), default=func.now())
    completed_at = db.Column(db.DateTime(timezone=True), default=None)
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())

    user = db.relationship('User')
    quiz = db.relationship('Quiz')
    user_answers = db.relationship('UserAnswer')

    def __repr__(self):
        repr_str = (
                f'{self.id = }\n' +
                f'{self.user_id = }\n' +
                f'{self.quiz_id = }\n' +
                f'{self.correct_answers = }\n' +
                f'{self.all_answers = }\n' +
                f'{self.score_percentage = }\n' +
                f'{self.started_at = }\n' +
                f'{self.completed_at = }\n' +
                f'Answers:'
        )
        for a_number, answer in enumerate(self.user_answers):
            repr_str += f"\nAnswer nr {a_number + 1}: {answer.is_correct}"

        return repr_str


class UserAnswer(db.Model):
    __tablename__ = 'user_answers'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey('answers.id'))
    result_id = db.Column(db.Integer, db.ForeignKey('results.id'), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())

    result = db.relationship('Result')
    question = db.relationship('Question')
    answer = db.relationship('Answer')