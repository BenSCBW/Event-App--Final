from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from eventapp import db
from eventapp.models import EventPost
from eventapp.models import Comment
from eventapp.event_posts.forms import EventPostForm, CommentForm
import os
from flask import url_for, current_app


event_posts = Blueprint('event_posts',__name__)

@event_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = EventPostForm()

    if form.validate_on_submit():
        f = form.pic.data
        f.save(os.path.join(
            current_app.root_path, 'static/photos', f.filename
        ))
        event_post = EventPost(title=form.title.data,
                             text=form.text.data,
                             city=form.city.data,
                             address=form.address.data,
                             time_start=form.time_start.data,
                             time_end=form.time_end.data,
                             contact=form.contact.data,
                             user_id=current_user.id,
                             pic=f.filename
        )
        db.session.add(event_post)
        db.session.commit()
        flash("Event Post Created")
        return redirect(url_for('core.index'))

    return render_template('create_post.html',form=form)


# int: event_post:id se prenosi kao intiger
# umjesto stringaaaaa.
@event_posts.route('/<int:event_post_id>',methods=['GET','POST'])
def event_post(event_post_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment_post = Comment(
		                    user_id=current_user.id,
							post_id=event_post_id,
                            body=form.comment.data
        )
        db.session.add(comment_post)
        db.session.commit()
        flash("Comment Created")
    # uzmi zatrazeni event post po id broju ili izbaci error 404
    event_post = EventPost.query.get_or_404(event_post_id)
    return render_template('event_post.html',title=event_post.title,
                            city=event_post.city,
                            address=event_post.address,
                            date=event_post.date,
                            contact=event_post.contact,
                            time_start=event_post.time_start,
                            time_end=event_post.time_end,
                            post=event_post,
                            pic=event_post.pic,
							form=form
                            )

@event_posts.route("/<int:event_post_id>/update", methods=['GET', 'POST'])
@login_required
def update(event_post_id):
    event_post = EventPost.query.get_or_404(event_post_id)
    if event_post.author != current_user:
        # nema pristupa
        abort(403)

    form = EventPostForm()
    if form.validate_on_submit():
        f = form.pic.data
        f.save(os.path.join(
            current_app.root_path, 'static/photos', f.filename
        ))
        event_post.city=form.city.data
        event_post.address=form.address.data
        event_post.title = form.title.data
        event_post.text = form.text.data
        event_post.contact = form.contact.data
        event_post.time_start = form.time_start.data
        event_post.time_end = form.time_end.data
        event_post.pic = f.filename
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('event_posts.event_post', event_post_id=event_post.id))
    #  predaj postojeci info event posta da se moze ponovno pokrenuti
    # postojeci text i title.
    elif request.method == 'GET':
        form.title.data = event_post.title
        form.text.data = event_post.text
        form.city.data = event_post.city
        form.contact.data = event_post.contact
        form.address.data = event_post.address
        form.time_start.data = event_post.time_start
        form.time_end.data = event_post.time_end
    return render_template('update_post.html', title='Update', form=form)


@event_posts.route("/<int:event_post_id>/delete", methods=['POST'])
@login_required
def delete_post(event_post_id):
    event_post = EventPost.query.get_or_404(event_post_id)
    if event_post.author != current_user:
        abort(403)
    db.session.delete(event_post)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.index'))

@event_posts.route("/<int:event_post_id>/<int:comment_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_comment(event_post_id, comment_id):
    comment = Comment.query.get_or_404(comment_id)
    event_post = EventPost.query.get_or_404(event_post_id)
    if comment.author != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('event_posts.event_post', event_post_id=event_post.id))

@event_posts.route("/<int:event_post_id>/<int:comment_id>/update", methods=['GET', 'POST'])
@login_required
def update_comment(event_post_id, comment_id):
    event_post = EventPost.query.get_or_404(event_post_id)
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        # nema pristupa
        abort(403)

    form = CommentForm()
    if form.validate_on_submit():
        comment.body=form.comment.data
        db.session.commit()
        flash('Comment Updated')
        return redirect(url_for('event_posts.event_post', event_post_id=event_post.id))
    #  predaj postojeci info event posta da se moze ponovno pokrenuti
    # postojeci text i title.
    elif request.method == 'GET':
        form.comment.data = comment.body
    return render_template('update_comment.html', title='Update', form=form)
