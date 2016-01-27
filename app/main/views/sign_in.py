from flask import (
    render_template,
    redirect,
    url_for,
    session,
    abort
)

from app.main import main
from app.main.dao import users_dao
from app.main.forms import LoginForm


@main.route('/sign-in', methods=(['GET', 'POST']))
def sign_in():
    form = LoginForm()
    if form.validate_on_submit():
        user = users_dao.get_user_by_email(form.email_address.data)
        if user:
            if not user.is_locked() and user.is_active() and users_dao.verify_password(user, form.password.data):
                users_dao.send_verify_code(user.id, 'sms')
                session['user_details'] = {"email": user.email_address, "id": user.id}
                return redirect(url_for('.two_factor'))
            else:
                # TODO re wire this increment to api
                users_dao.increment_failed_login_count(user.id)
        # Vague error message for login
        form.password.errors.append('Username or password is incorrect')

    return render_template('views/signin.html', form=form)
