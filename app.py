"""Feedback Flask app."""

from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedBackForm, UpdateFeedBackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///flask-feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhhh"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route("/")
def homepage():
    """Homepage of site; redirect to register."""

    return redirect("/register")


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user: produce form and handle form submission."""


    if "username" in session:
        return redirect("/secret")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)

        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{user.username}")
        

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """Homepage of site, redirect to register."""

    if "username" in session:
        return redirect("/secret")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)  # <User> or False
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)
    # return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    """Logout route."""

    session.pop("username")
    return redirect("/login")



# @app.route('/secret', methods=['GET', 'POST'])
# def secret():
#     if "username" in session:
#         return 'You made it!'
    
#     else:
#         form = LoginForm()
#         return render_template("login.html", form=form)

@app.route("/users/<username>")
def show_user(username):
    """Example page for logged-in-users."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)

    return render_template("show.html", user=user)


@app.route("/users/<username>/delete", methods={'POST'})
def delete_user(username):
    
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")


@app.route("/users/<username>/feedback/add", methods={'GET', 'POST'})
def feedbac_form(username):
    
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedBackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
        
    else:
        form = FeedBackForm()
        return render_template("feedback.html", form=form)



# Just started this

@app.route("/feedback/<feedback_id>/update", methods={'GET', 'POST'})
def update_feedback(feedback_id):



    feedback = Feedback.query.get_or_404(feedback_id)
    
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()



    form = UpdateFeedBackForm(obj=feedback)


    if form.validate_on_submit():
        
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.add(feedback)
        db.session.commit()
        
        return redirect(f"/users/{feedback.username}")


    else:
        return render_template('update.html', feedback=feedback, form=form)



@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
        

    feedback = Feedback.query.get(feedback_id)
    
    db.session.delete(feedback)
    db.session.commit()

    return redirect(f"/users/{feedback.username}")






        
