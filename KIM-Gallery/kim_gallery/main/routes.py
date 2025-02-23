import os
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from kim_gallery.main import bp
from kim_gallery.models import Image, Tag, User, Contact, image_tags
from kim_gallery import db
from kim_gallery.main.forms import EditProfileForm, ContactForm
from datetime import datetime
from flask_mail import Message
from kim_gallery import mail

def save_profile_picture(form_picture):
    if form_picture:
        filename = secure_filename(form_picture.filename)
        # Create unique filename using username and timestamp
        _, ext = os.path.splitext(filename)
        picture_filename = f"profile_{current_user.username}_{int(datetime.utcnow().timestamp())}{ext}"
        
        # Ensure profile_pics directory exists
        profile_pics_path = os.path.join(current_app.root_path, 'static', 'profile_pics')
        os.makedirs(profile_pics_path, exist_ok=True)
        
        # Save the picture
        picture_path = os.path.join(profile_pics_path, picture_filename)
        form_picture.save(picture_path)
        
        # Delete old profile picture if it exists
        if current_user.profile_image:
            old_picture_path = os.path.join(profile_pics_path, current_user.profile_image)
            if os.path.exists(old_picture_path):
                try:
                    os.remove(old_picture_path)
                except Exception as e:
                    current_app.logger.error(f"Error deleting old profile picture: {e}")
        
        return picture_filename
    return None

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
        try:
            if form.profile_image.data:
                picture_filename = save_profile_picture(form.profile_image.data)
                if picture_filename:
                    current_user.profile_image = picture_filename
            
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.about_me = form.about_me.data
            db.session.commit()
            flash('Your changes have been saved.', 'success')
            return redirect(url_for('main.profile', username=current_user.username))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while saving your changes. Please try again.', 'error')
            current_app.logger.error(f"Error updating profile: {e}")
            
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    
    return render_template('main/edit_profile.html', title='Edit Profile', form=form)

@bp.route('/about')
def about():
    return render_template('main/about.html', title='About')

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data,
            user_id=current_user.id if current_user.is_authenticated else None
        )
        db.session.add(contact)
        
        try:
            # Send email notification to admin
            msg = Message(
                subject=f'New Contact Form Submission: {form.subject.data}',
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[current_app.config['ADMIN_EMAIL']],
                body=f'''New contact form submission from {form.name.data} ({form.email.data}):

Subject: {form.subject.data}

Message:
{form.message.data}

Submitted at: {datetime.utcnow()}
'''
            )
            mail.send(msg)
            
            # Send confirmation email to user
            user_msg = Message(
                subject='Thank you for contacting KIM Gallery',
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[form.email.data],
                body=f'''Dear {form.name.data},

Thank you for contacting KIM Gallery. We have received your message and will get back to you as soon as possible.

Best regards,
KIM Gallery Team
'''
            )
            mail.send(user_msg)
            
            db.session.commit()
            flash('Your message has been sent successfully! We will get back to you soon.', 'success')
            return redirect(url_for('main.contact'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error sending contact form: {str(e)}')
            flash('An error occurred while sending your message. Please try again later.', 'error')
    
    return render_template('main/contact.html', title='Contact Us', form=form)

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    search_type = request.args.get('type', 'all')  # all, images, users, tags
    
    if query:
        # Base query for images
        image_query = Image.query.join(User, Image.user_id == User.id)

        if search_type == 'images' or search_type == 'all':
            # Search in image titles and descriptions
            images = image_query.filter(
                db.or_(
                    Image.title.ilike(f'%{query}%'),
                    Image.description.ilike(f'%{query}%'),
                    User.username.ilike(f'%{query}%')
                )
            )
            # Add tag search if there are any matching tags
            matching_tags = Tag.query.filter(Tag.name.ilike(f'%{query}%')).all()
            if matching_tags:
                tag_images = Image.query.join(image_tags).join(Tag).filter(
                    Tag.id.in_([tag.id for tag in matching_tags])
                )
                images = images.union(tag_images)
        elif search_type == 'users':
            # Search for users
            images = image_query.filter(User.username.ilike(f'%{query}%'))
        elif search_type == 'tags':
            # Search for tags
            tag_images = Image.query.join(image_tags).join(Tag).filter(
                Tag.name.ilike(f'%{query}%')
            )
            images = tag_images
        
        # Order and paginate results
        images = images.order_by(Image.upload_date.desc()).paginate(
            page=page, per_page=12, error_out=False)
        
        # Get related tags for search suggestions
        related_tags = Tag.query.filter(Tag.name.ilike(f'%{query}%')).limit(5).all()
        
        # Get matching users for search suggestions
        matching_users = User.query.filter(User.username.ilike(f'%{query}%')).limit(5).all()
    else:
        images = Image.query.none().paginate(page=page, per_page=12, error_out=False)
        related_tags = []
        matching_users = []
    
    return render_template(
        'main/search.html',
        title='Search',
        images=images,
        query=query,
        search_type=search_type,
        related_tags=related_tags,
        matching_users=matching_users
    )

@bp.route('/tag/<name>')
def tag(name):
    page = request.args.get('page', 1, type=int)
    tag = Tag.query.filter_by(name=name).first_or_404()
    images = tag.images.order_by(Image.upload_date.desc()).paginate(
        page=page, per_page=12, error_out=False)
    return render_template('main/tag.html', title=f'Tag: {name}', tag=tag, images=images) 