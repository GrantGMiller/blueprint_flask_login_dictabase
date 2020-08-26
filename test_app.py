from flask import Flask
from blueprint_flask_login_dictabase import (
    bp,
    VerifyLogin,
    NewUser,
    ForgotPassword,
    MagicLink
)
import flask_dictabase

app = Flask('Test')
app.db = flask_dictabase.Dictabase(app)
app.config["SECRET_KEY"] = "randomUnguessableString"
app.register_blueprint(bp)


@app.route('/')
def Index():
    return 'Index<br><a href="/private">Private Page</a>'


@app.route('/private')
@VerifyLogin
def Private():
    return 'Private Page<br><a href="/">Index Page</a>'


@NewUser
def NewUserCallback(user):
    print('NewUserCallback(user=', user)


@ForgotPassword
def ForgotPasswordCallback(user, forgotURL):
    print('ForgotPasswordCallback(user=', user, forgotURL)


@MagicLink
def MagicLinkCallback(user, magicLink):
    print('MagicLinkCallback(user=', user, magicLink)


if __name__ == '__main__':
    app.run(debug=True)
