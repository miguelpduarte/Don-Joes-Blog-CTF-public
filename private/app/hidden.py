from flask import Blueprint, render_template, request, abort, make_response, redirect, url_for

import utils.auth as auth
import utils.sessions as sessions
from utils.flag import flag

hidden = Blueprint('hidden', __name__, static_folder='')

def get_redirect_to_hidden_index():
    # Ugly but the heroku ssl stuff is breaking so let's hope this works
    return make_response(redirect("/m4st3rfully_h1dd3n/"))

@hidden.route("/admin")
def admin_flag():
    if not auth.is_admin(request):
        abort(403)
    return render_template("admin.html", flag=flag)

@hidden.route("/login", methods=["GET"])
def hidden_login():
    return render_template("login.html")

@hidden.route("/login", methods=["POST"])
def hidden_post_login():
    data = auth.try_login(request.form)
    if data:
        # Redirect back to the hidden homepage
        # resp = make_response(redirect(url_for(".hidden_index")))
        resp = get_redirect_to_hidden_index()
        # create new cookie session to authenticate user
        session = sessions.create_session(data)
        cookie = sessions.create_cookie(session)
        resp.set_cookie("auth", cookie)
        return resp
    return render_template("login.html", msg="Invalid user and/or password"), 401

@hidden.route("/")
def hidden_index():
    # TODO: Maybe have some sort of middleware for this "router" to redirect to the homepage in case of invalid session signature so that users notice some sort of redirection to know that the cookie is broken.
    session = auth.get_session(request)
    print(session)
    if session:
        user = auth.get_user_from_session(session)
        print(user)
        return render_template("hidden_home.html", user=user)
    return render_template("hidden_home.html")

@hidden.route("/logout")
def logout():
    # Redirect back to the hidden homepage
    # resp = make_response(redirect(url_for(".hidden_index")))
    resp = get_redirect_to_hidden_index()
    resp.set_cookie("auth", "", expires=0)
    return resp

# Get the application source code since we're so cool that the app is even open source!
@hidden.route("/source")
def source():
    return hidden.send_static_file("source.zip")

