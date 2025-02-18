from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from kim_gallery.main import bp
from kim_gallery.models import Image, Tag

@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    images = Image.query.order_by(Image.upload_date.desc()).paginate(
        page=page, per_page=12, error_out=False)
    return render_template('main/index.html', title='Home', images=images)

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