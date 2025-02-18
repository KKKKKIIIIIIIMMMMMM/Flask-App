import os
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from kim_gallery import db
from kim_gallery.gallery import bp
from kim_gallery.gallery.forms import UploadForm, EditImageForm
from kim_gallery.models import Image, Tag

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            # Create unique filename
            base, ext = os.path.splitext(filename)
            filename = f"{base}_{current_user.id}{ext}"
            
            # Save the file
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            
            # Create image record
            image = Image(
                title=form.title.data,
                description=form.description.data,
                filename=filename,
                author=current_user
            )
            
            # Handle tags
            tag_names = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
            for tag_name in tag_names:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                image.tags.append(tag)
            
            db.session.add(image)
            db.session.commit()
            
            flash('Your image has been uploaded!', 'success')
            return redirect(url_for('gallery.image', id=image.id))
    
    return render_template('gallery/upload.html', title='Upload Image', form=form)

@bp.route('/image/<int:id>')
def image(id):
    image = Image.query.get_or_404(id)
    return render_template('gallery/image.html', title=image.title, image=image)

@bp.route('/image/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_image(id):
    image = Image.query.get_or_404(id)
    if image.author != current_user:
        flash('You cannot edit this image.', 'error')
        return redirect(url_for('gallery.image', id=id))
    
    form = EditImageForm()
    if form.validate_on_submit():
        image.title = form.title.data
        image.description = form.description.data
        
        # Update tags
        image.tags.clear()
        tag_names = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            image.tags.append(tag)
        
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('gallery.image', id=id))
    elif request.method == 'GET':
        form.title.data = image.title
        form.description.data = image.description
        form.tags.data = ', '.join(tag.name for tag in image.tags)
    
    return render_template('gallery/edit_image.html', title='Edit Image', form=form, image=image)

@bp.route('/image/<int:id>/delete', methods=['POST'])
@login_required
def delete_image(id):
    image = Image.query.get_or_404(id)
    if image.author != current_user:
        flash('You cannot delete this image.', 'error')
        return redirect(url_for('gallery.image', id=id))
    
    # Delete the file
    try:
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename))
    except Exception as e:
        flash(f'Error deleting image file: {str(e)}', 'error')
    
    # Delete the database record
    db.session.delete(image)
    db.session.commit()
    
    flash('Image has been deleted.', 'success')
    return redirect(url_for('main.index')) 