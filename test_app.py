from flask import Flask, render_template, flash
from flask_login_dictabase_blueprint import (
    bp,
    VerifyLogin,
    VerifyAdmin,
    NewUser,
    ForgotPassword,
    MagicLink,
    AddAdmin,
    GetUsers,
    GetUser,
)
import flask_dictabase

app = Flask('Test')
app.db = flask_dictabase.Dictabase(app)
app.config["SECRET_KEY"] = "randomUnguessableString"
app.register_blueprint(bp)


@app.route('/')
def Index():
    return render_template('index.html', user=GetUser())


@app.route('/private')
@VerifyLogin
def Private():
    return render_template('private.html', user=GetUser())


AddAdmin('grant@grant-miller.com')


@app.route('/admin')
@VerifyAdmin
def Admin():
    return render_template(
        'admin.html',
        users=GetUsers(),
        user=GetUser(),
    )


@NewUser
def NewUserCallback(user):
    print('NewUserCallback(user=', user)
    flash(f'Welcome new user {user["email"]}')


@ForgotPassword
def ForgotPasswordCallback(user, forgotURL):
    print('ForgotPasswordCallback(user=', user, forgotURL)
    flash('Send an email with the forgotURL to the user', 'info')


@MagicLink
def MagicLinkCallback(user, magicLink):
    print('MagicLinkCallback(user=', user, magicLink)
    flash('Send an email with the magic link to the user', 'info')


if __name__ == '__main__':
    app.run(debug=True)
