from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from kim_gallery.main import bp
from kim_gallery.models import Image, Tag, User
from kim_gallery import db
from kim_gallery.main.forms import EditProfileForm

@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    images = Image.query.order_by(Image.upload_date.desc()).paginate(
        page=page, per_page=12, error_out=False)
    return render_template('main/index.html', title='Home', images=images)

@bp.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    images = user.images.order_by(Image.upload_date.desc()).paginate(
        page=page, per_page=12, error_out=False)
    return render_template('main/profile.html', user=user, images=images)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('main.profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('main/edit_profile.html', title='Edit Profile', form=form)

@bp.route('/about')
def about():
    return render_template('main/about.html', title='About')

@bp.route('/contact')
def contact():
    return render_template('main/contact.html', title='Contact')

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    if query:
        images = Image.query.filter(
            (Image.title.ilike(f'%{query}%')) |
            (Image.description.ilike(f'%{query}%'))
        ).order_by(Image.upload_date.desc()).paginate(
            page=page, per_page=12, error_out=False)
    else:
        images = Image.query.none().paginate(page=page, per_page=12, error_out=False)
    
    return render_template('main/search.html', title='Search', images=images, query=query)

@bp.route('/tag/<name>')
def tag(name):
    page = request.args.get('page', 1, type=int)
    tag = Tag.query.filter_by(name=name).first_or_404()
    images = tag.images.order_by(Image.upload_date.desc()).paginate(
        page=page, per_page=12, error_out=False)
    return render_template('main/tag.html', title=f'Tag: {name}', tag=tag, images=images) 