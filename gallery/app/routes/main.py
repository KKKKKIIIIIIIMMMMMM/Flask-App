from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models.image import Image, Tag
from app.models.user import User
from app import db
from sqlalchemy import desc
from app.models.comment import Comment

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 12
    images = Image.query.order_by(desc(Image.upload_date)).paginate(
        page=page, per_page=per_page, error_out=False)
    return render_template('main/index.html', images=images)

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    if query:
        images = Image.query.filter(
            (Image.title.ilike(f'%{query}%')) |
            (Image.description.ilike(f'%{query}%')) |
            (Image.tags.any(Tag.name.ilike(f'%{query}%')))
        ).order_by(desc(Image.upload_date)).paginate(
            page=page, per_page=per_page, error_out=False)
    else:
        images = Image.query.paginate(page=page, per_page=per_page, error_out=False)
        
    return render_template('main/search.html', images=images, query=query)

@bp.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = 12
    images = Image.query.filter_by(user_id=user.id).order_by(
        desc(Image.upload_date)).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('main/profile.html', user=user, images=images)

@bp.route('/tag/<tag_name>')
def tag(tag_name):
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = 12
    images = tag.images.order_by(desc(Image.upload_date)).paginate(
        page=page, per_page=per_page, error_out=False)
    return render_template('main/tag.html', tag=tag, images=images)

@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        current_user.bio = request.form.get('bio', '')
        current_user.website = request.form.get('website', '')
        
        # Handle password change
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        if current_password and new_password:
            if current_user.check_password(current_password):
                current_user.set_password(new_password)
                flash('Password updated successfully')
            else:
                flash('Current password is incorrect')
                return redirect(url_for('main.settings'))
        
        db.session.commit()
        flash('Settings updated successfully')
        return redirect(url_for('main.profile', username=current_user.username))
        
    return render_template('main/settings.html')

@bp.route('/image/<int:image_id>/like', methods=['POST'])
@login_required
def like_image(image_id):
    image = Image.query.get_or_404(image_id)
    if image in current_user.liked_images:
        current_user.liked_images.remove(image)
        message = 'unliked'
    else:
        current_user.liked_images.append(image)
        message = 'liked'
    db.session.commit()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'status': 'success',
            'message': message,
            'likes': len(image.liked_by.all())
        })
    return redirect(url_for('images.view', image_id=image_id))

from app.models.comment import Comment

@bp.route('/image/<int:image_id>/comment', methods=['POST'])
@login_required
def add_comment(image_id):
    image = Image.query.get_or_404(image_id)
    content = request.form.get('content', '').strip()
    
    if content:
        comment = Comment(
            content=content,
            user_id=current_user.id,
            image_id=image_id
        )
        db.session.add(comment)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(comment.to_dict())
            
    return redirect(url_for('images.view', image_id=image_id))

@bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        flash('You cannot delete this comment')
        return redirect(url_for('images.view', image_id=comment.image_id))
        
    db.session.delete(comment)
    db.session.commit()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'status': 'success'})
        
    return redirect(url_for('images.view', image_id=comment.image_id))