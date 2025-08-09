
Flask Login Dictabase Blueprint
==============================

A Flask blueprint for user authentication (login, registration, password reset, magic link login) using [flask_dictabase](https://github.com/GrantGMiller/flask_dictabase) and [flask_login](https://flask-login.readthedocs.io/en/latest/). This blueprint provides a simple, extensible way to add user authentication to your Flask app with a dictionary-based database backend.

Features
--------
- User login/logout
- User registration
- Password reset (with token)
- Magic link login
- Admin user support
- Customizable template rendering
- Callbacks for user events (new user, forgot password, magic link, sign in)

Install with
------------

.. code-block:: bash

    pip install flask-login-dictabase-blueprint

Usage
-----

1. Initialize Flask and Dictabase
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from flask import Flask, render_template, flash
    import flask_dictabase
    from flask_login_dictabase_blueprint import (
        bp,
        verify_is_user,
        verify_is_admin,
        new_user,
        forgot_password,
        on_magic_link_created,
        add_admin,
        get_users,
        get_current_user,
        on_signin
    )

    app = Flask('Test')
    app.db = flask_dictabase.Dictabase(app)
    app.config["SECRET_KEY"] = "randomUnguessableString"
    app.register_blueprint(bp)

    @app.route('/')
    def index():
        # This page is visible to anyone (logged in or not)
        return render_template('index.html', user=get_current_user())

    @app.route('/private')
    @verify_is_user
    def private():
        # This page is only viewable to logged-in users.
        return render_template('private.html', user=get_current_user())

    add_admin('grant@grant-miller.com')  # You can add one or more "admins"

    @app.route('/admin')
    @verify_is_admin
    def admin():
        # This page is only viewable by the admins
        return render_template(
            'admin.html',
            users=get_users(),
            user=get_current_user(),
        )

    @new_user
    def new_user_callback(user):
        # Called whenever a new user is created
        print('new_user_callback(user=', user)
        flash(f'Welcome new user {user["email"]}')

    @forgot_password
    def forgot_password_callback(user, forgot_url):
        # Called when a user requests to reset their password.
        # You should email the forgot_url to the user
        print('forgot_password_callback(user=', user, forgot_url)
        flash('Send an email with the forgot_url to the user', 'info')

    @on_magic_link_created
    def magic_link_callback(user, magic_link):
        # Used to simplify login. Email the magic_link to the user.
        # If they click on the magic_link, they will be logged in.
        print('magic_link_callback(user=', user, magic_link)
        flash('Send an email with the magic link to the user', 'info')

    @on_signin
    def signed_in_callback(user):
        print(f'signed_in {user["email"]}')

    if __name__ == '__main__':
        app.run(debug=True)

API Reference
-------------

All functions are imported from ``flask_login_dictabase_blueprint``:

- ``get_current_user(email=None)`` — Returns the current user object, or user by email.
- ``verify_is_user(func)`` — Decorator to require login.
- ``verify_is_admin(func)`` — Decorator to require admin.
- ``add_admin(email)`` — Add an admin by email.
- ``get_admins()`` — Get a set of admin emails.
- ``get_users()`` — Get all users (deprecated: use ``get_users()`` not ``GetUsers``).
- ``is_admin()`` — Returns True if current user is admin.
- ``logout_user()`` — Log out the current user.
- ``get_hash(strng, salt='')`` — Hash a password with salt.
- ``new_user(func)`` — Register a callback for new users.
- ``forgot_password(func)`` — Register a callback for password reset.
- ``on_magic_link_created(func)`` — Register a callback for magic link creation.
- ``on_signin(func)`` — Register a callback for user sign in.
- ``do_render_template(func)`` — Register a callback for custom template rendering.

Routes Provided
---------------

- ``/login`` — Login page
- ``/logout`` — Logout
- ``/register`` — Register new user
- ``/forgot`` — Forgot password
- ``/reset_password/<resetToken>`` — Password reset
- ``/magic_link`` — Request magic link
- ``/magic_link_login`` — Login with magic link

Templates
---------

Override the templates in ``flask_login_dictabase_blueprint/templates/`` as needed:
- ``login.html``
- ``register.html``
- ``forgot.html``
- ``magic_link.html``
- ``base.html``

License
-------
MIT
