from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import re

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email').lower()
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password_hash, password):
                flash('Pomyślnie zalogowano', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Podane hasło jest błędne!", category='error')
        else:
            flash("Użytkownik o pdanym adresie email nie istnieje!", category='error')

        return render_template('login.html', user=current_user)

    else:
        if not current_user.is_authenticated:
            return render_template("login.html", user=current_user)
        else:
            return redirect(url_for('views.home'))


@auth.route('/sing-up', methods=['GET', 'POST'])
def sing_up():
    if request.method == 'POST':
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        email = request.form.get('email').lower()
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        role = request.form.get('role')

        print(f'{first_name = } {last_name = } {email = } {password1 = } {password2 = } {role = }')

        user = User.query.filter_by(email=email).first()

        if first_name == '' or first_name is None:
            flash("Pole imie nie może byc puste!", category='error')

        elif last_name == '' or last_name is None:
            flash("Pole nazwisko nie może byc puste!", category='error')

        elif email == '' or email is None:
            flash("Pole email nie może być puste!", category='error')

        elif re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) is None:
            flash("Adres email jest błędny", category='error')

        elif user:
            flash("Uzytkownik o podanym adresie email już instnieje!", category='error')

        elif password1 == '' or password1 is None:
            flash("Pole hasło nie może byc puste!", category='error')

        elif password1 != password2:
            flash("Hasła nie są takie same!", category='error')

        elif re.match(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&/])[A-Za-z\d@$!%*?&/]{8,}$', password1) is None:
            flash("Twoje hasło jest zbyt słabe", category='error')

        elif role != 'student' and role != 'teacher':
            flash("Musisz wybrać czy jesteś uczniem czy nauczycielem!", category='error')

        else:
            new_user = User(first_name=first_name, last_name=last_name, email=email, password_hash=generate_password_hash(password1), role=role)
            try:
                db.session.add(new_user)
                db.session.commit()
            except Exception as e:
                flash(f'Wystąpił nie znany błąd podczas towrzenia konta: {e}', category='error')
            else:
                flash('Konto zsotało pomyślnie stworznoe. Możesz się taraz zalogować', category='success')
                return render_template("login.html", user=current_user)

        return render_template("sing-up.html", values=request.form.to_dict(), user=current_user)
    else:
        if not current_user.is_authenticated:
            return render_template("sing-up.html", values={}, user=current_user)
        else:
            return redirect(url_for('views.home'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
