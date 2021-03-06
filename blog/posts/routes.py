from flask_login import login_required, current_user
from flask import render_template, redirect, url_for,Blueprint
from blog.posts.forms import CommentForm, CreatePostForm
from blog.posts.db_model import CommentDB, BlogPost
from blog.users.db_model import User
from blog import db
from datetime import date

posts = Blueprint('posts', __name__)

@posts.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html",
                           all_posts=posts,
                           logged_in=current_user.is_authenticated)

@posts.route("/post/<int:id>", methods=['GET', 'POST'])
def show_post(id):
    comments_form = CommentForm()
    requested_post = BlogPost.query.get(id)
    comments = CommentDB.query.filter_by(post_id=id).all()
    rights = False
    if current_user.is_authenticated:
        rights = True if current_user.id == requested_post.post_id else False
    if comments_form.validate_on_submit() and current_user.is_authenticated:
        new_comment = CommentDB(comment=comments_form.comment.data)
        user = User.query.filter_by(user_name=current_user.user_name).first()
        user.comments_id.append(new_comment)
        requested_post.comment_id.append(new_comment)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('posts.show_post', id=id))
    return render_template("post.html",
                           post=requested_post,
                           all_comments=comments,
                           logged_in=current_user.is_authenticated,
                           have_rights=rights,
                           form=comments_form)

@posts.route("/new_post", methods=["GET", "POST"])
@login_required
def add_new_post():
    new_post_form = CreatePostForm()
    user_id = current_user.id
    if new_post_form.validate_on_submit():
        new_post_db = BlogPost(
            title=new_post_form.title.data,
            subtitle=new_post_form.subtitle.data,
            img_url=new_post_form.img_url.data,
            date=date.today().strftime("%B %d, %Y"),
            body=new_post_form.body.data,
            author=current_user.user_name)
        user = User.query.filter_by(user_name=current_user.user_name).first()
        user.posts.append(new_post_db)
        db.session.add(new_post_db)
        db.session.commit()
        return redirect(url_for('posts.get_all_posts'))
    return render_template("make-post.html", form=new_post_form, logged_in=current_user.is_authenticated)


@posts.route("/edit_post/<post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    to_edit_post_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body, )
    if to_edit_post_form.validate_on_submit():
        post.title = to_edit_post_form.title.data
        post.subtitle = to_edit_post_form.subtitle.data
        post.author = current_user.user_name
        post.img_url = to_edit_post_form.img_url.data
        post.body = to_edit_post_form.body.data
        db.session.commit()
        return redirect(url_for("posts.show_post", id=post.id))
    return render_template("make-post.html", form=to_edit_post_form, logged_in=current_user.is_authenticated)

@posts.route("/delete/<int:id>")
@login_required
def delete(id):
    delete_post = BlogPost.query.get(id)
    db.session.delete(delete_post)
    db.session.commit()
    return redirect(url_for('posts.get_all_posts'))
