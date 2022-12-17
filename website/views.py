import base64

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from . import db
from .models import Photo, User

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return render_template("base.html", user=current_user)


@views.route("/discoverphotos")
@login_required
def discover():
    posts = Photo.query.all()
    return render_template("discover.html", user=current_user, posts=posts)


@views.route("/userphotos")
@login_required
def posts():
    user = User.query.filter_by(username=current_user.username).first()

    if not user:
        flash("No user with that username exists.", category="error")
        return redirect(url_for("views.discover"))

    posts = Photo.query.filter_by(author=user.id).all()
    return render_template(
        "posts.html", user=current_user, posts=posts, username=current_user.username
    )


@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        img = request.files["image"]
        if not img:
            return "No photo uploaded!", 400
        image_b64 = base64.b64encode(img.read()).decode("utf-8")
        post = Photo(img=image_b64, author=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("Post created!", category="success")
        return redirect(url_for("views.discover"))

    return render_template("create_post.html", user=current_user)


@views.route("/update-post/<id>", methods=["GET", "POST"])
@login_required
def update_post(id):
    post = Photo.query.filter_by(id=id).first()
    if request.method == "POST":
        img = request.files["image"]
        if not img:
            return "No photo uploaded!", 400
        image_b64 = base64.b64encode(img.read()).decode("utf-8")
        post.img = image_b64
        db.session.commit()
        flash("Post updated!", category="success")
        return redirect(url_for("views.discover"))
    return render_template("update_post.html", user=current_user)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Photo.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category="error")
    elif current_user.id != post.id:
        print(current_user.id, post.id)
        flash("You do not have permission to delete this post.", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted.", category="success")

    return redirect(url_for("views.discover"))
