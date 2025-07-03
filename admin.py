from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from app import app, db
from models import *
from forms import *
from utils import allowed_file, save_uploaded_file
from werkzeug.utils import secure_filename
import os
from datetime import datetime

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data) and user.is_admin:
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    # Get statistics
    stats = {
        'total_news': News.query.count(),
        'total_faculty': Faculty.query.count(),
        'total_documents': Document.query.count(),
        'total_contacts': Contact.query.count(),
        'unread_contacts': Contact.query.filter_by(is_read=False).count(),
        'pending_admissions': Admission.query.filter_by(status='pending').count(),
        'total_gallery': Gallery.query.count(),
        'total_events': Event.query.count(),
        'total_transfer_certificates': TransferCertificate.query.count(),
        'issued_transfer_certificates': TransferCertificate.query.filter_by(is_issued=True).count()
    }

    # Get recent activity
    recent_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(5).all()
    recent_admissions = Admission.query.order_by(Admission.created_at.desc()).limit(5).all()

    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         recent_contacts=recent_contacts,
                         recent_admissions=recent_admissions)

@app.route('/admin/content')
@login_required
def admin_content():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    section = request.args.get('section', 'about')
    content_items = SchoolInfo.query.filter_by(section=section).order_by(SchoolInfo.order_index.asc()).all()

    return render_template('admin/manage_content.html', 
                         content_items=content_items, 
                         current_section=section)

@app.route('/admin/content/add', methods=['GET', 'POST'])
@login_required
def admin_add_content():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    form = SchoolInfoForm()

    if form.validate_on_submit():
        content = SchoolInfo(
            section=form.section.data,
            title=form.title.data,
            content=form.content.data,
            image_url=form.image_url.data,
            order_index=form.order_index.data,
            is_active=form.is_active.data
        )
        db.session.add(content)
        db.session.commit()
        flash('Content added successfully!', 'success')
        return redirect(url_for('admin_content', section=form.section.data))

    return render_template('admin/add_content.html', form=form)

@app.route('/admin/content/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_content(id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    content = SchoolInfo.query.get_or_404(id)
    form = SchoolInfoForm(obj=content)

    if form.validate_on_submit():
        form.populate_obj(content)
        content.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Content updated successfully!', 'success')
        return redirect(url_for('admin_content', section=content.section))

    return render_template('admin/edit_content.html', form=form, content=content)

@app.route('/admin/content/delete/<int:id>')
@login_required
def admin_delete_content(id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    content = SchoolInfo.query.get_or_404(id)
    section = content.section
    db.session.delete(content)
    db.session.commit()
    flash('Content deleted successfully!', 'success')
    return redirect(url_for('admin_content', section=section))

@app.route('/admin/news')
@login_required
def admin_news():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    news_items = News.query.order_by(News.publish_date.desc()).all()
    return render_template('admin/manage_news.html', news_items=news_items)

@app.route('/admin/news/add', methods=['GET', 'POST'])
@login_required
def admin_add_news():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    form = NewsForm()

    if form.validate_on_submit():
        image_url = form.image_url.data

        # Handle file upload for main image
        if form.image.data:
            file = form.image.data
            if allowed_file(file.filename):
                filename = save_uploaded_file(file, 'news')
                image_url = f'/uploads/news/{filename}'

        news = News(
            title=form.title.data,
            content=form.content.data,
            summary=form.summary.data,
            image_url=image_url,
            category=form.category.data,
            is_featured=form.is_featured.data,
            is_active=form.is_active.data
        )
        db.session.add(news)
        db.session.commit()
        flash('News added successfully!', 'success')
        return redirect(url_for('admin_news'))

    return render_template('admin/add_news.html', form=form)

@app.route('/admin/news/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_news(id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    news = News.query.get_or_404(id)
    form = NewsForm(obj=news)

    if form.validate_on_submit():
        # Handle file upload for main image
        if form.image.data:
            file = form.image.data
            if allowed_file(file.filename):
                filename = save_uploaded_file(file, 'news')
                news.image_url = f'/uploads/news/{filename}'
        elif form.image_url.data:
            news.image_url = form.image_url.data



        news.title = form.title.data
        news.content = form.content.data
        news.summary = form.summary.data
        news.category = form.category.data
        news.is_featured = form.is_featured.data
        news.is_active = form.is_active.data

        db.session.commit()
        flash('News updated successfully!', 'success')
        return redirect(url_for('admin_news'))

    return render_template('admin/edit_news.html', form=form, news=news)

@app.route('/admin/news/delete/<int:id>')
@login_required
def admin_delete_news(id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    news = News.query.get_or_404(id)
    db.session.delete(news)
    db.session.commit()
    flash('News deleted successfully!', 'success')
    return redirect(url_for('admin_news'))

@app.route('/admin/faculty')
@login_required
def admin_faculty():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    faculty_members = Faculty.query.order_by(Faculty.department.asc(), Faculty.order_index.asc()).all()
    return render_template('admin/manage_faculty.html', faculty_members=faculty_members)

@app.route('/admin/faculty/add', methods=['GET', 'POST'])
@login_required
def admin_add_faculty():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    form = FacultyForm()

    if form.validate_on_submit():
        image_url = form.image_url.data

        # Handle file upload
        if form.image.data:
            file = form.image.data
            if allowed_file(file.filename):
                filename = save_uploaded_file(file, 'faculty')
                image_url = f'/uploads/faculty/{filename}'

        faculty = Faculty(
            name=form.name.data,
            position=form.position.data,
            department=form.department.data,
            qualification=form.qualification.data,
            experience=form.experience.data,
            bio=form.bio.data,
            image_url=image_url,
            email=form.email.data,
            phone=form.phone.data,
            order_index=form.order_index.data,
            is_active=form.is_active.data
        )
        db.session.add(faculty)
        db.session.commit()
        flash('Faculty member added successfully!', 'success')
        return redirect(url_for('admin_faculty'))

    return render_template('admin/add_faculty.html', form=form)

@app.route('/admin/gallery', methods=['GET', 'POST'])
@login_required
def admin_gallery():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    form = GalleryForm()

    if form.validate_on_submit():
        image_url = form.image_url.data

        # Handle file upload
        if form.image.data:
            file = form.image.data
            if allowed_file(file.filename):
                filename = save_uploaded_file(file, 'gallery')
                image_url = f'/uploads/gallery/{filename}'

        if image_url:
            gallery_item = Gallery(
                title=form.title.data,
                description=form.description.data,
                image_url=image_url,
                category=form.category.data,
                is_featured=form.is_featured.data,
                is_active=form.is_active.data
            )
            db.session.add(gallery_item)
            db.session.commit()
            flash('Gallery image added successfully!', 'success')
            return redirect(url_for('admin_gallery'))
        else:
            flash('Please provide either an image file or image URL', 'error')

    gallery_items = Gallery.query.order_by(Gallery.created_at.desc()).all()
    return render_template('admin/manage_gallery.html', gallery_items=gallery_items, form=form)

@app.route('/admin/gallery/delete/<int:id>')
@login_required
def admin_delete_gallery(id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    gallery_item = Gallery.query.get_or_404(id)
    db.session.delete(gallery_item)
    db.session.commit()
    flash('Gallery image deleted successfully!', 'success')
    return redirect(url_for('admin_gallery'))

@app.route('/admin/documents')
@login_required
def admin_documents():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    documents = Document.query.order_by(Document.created_at.desc()).all()
    return render_template('admin/manage_files.html', documents=documents)

@app.route('/admin/contacts')
@login_required
def admin_contacts():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/manage_contacts.html', contacts=contacts)

@app.route('/admin/admissions')
@login_required
def admin_admissions():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    admissions = Admission.query.order_by(Admission.created_at.desc()).all()
    return render_template('admin/manage_admissions.html', admissions=admissions)

@app.route('/admin/banners')
@login_required
def admin_banners():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    banners = Banner.query.order_by(Banner.created_at.desc()).all()
    return render_template('admin/manage_banners.html', banners=banners)

@app.route('/admin/banners/add', methods=['GET', 'POST'])
@login_required
def admin_add_banner():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    form = BannerForm()

    if form.validate_on_submit():
        image_url = form.image_url.data

        # Handle file upload
        if form.image.data:
            file = form.image.data
            if allowed_file(file.filename):
                filename = save_uploaded_file(file, 'banners')
                image_url = f'/uploads/banners/{filename}'

        banner = Banner(
            title=form.title.data,
            message=form.message.data,
            banner_type=form.banner_type.data,
            style=form.style.data,
            image_url=image_url,
            order_index=form.order_index.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            is_active=form.is_active.data
        )
        db.session.add(banner)
        db.session.commit()
        flash('Banner added successfully!', 'success')
        return redirect(url_for('admin_banners'))

    return render_template('admin/add_banner.html', form=form)

@app.route('/admin/banners/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_banner(id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    banner = Banner.query.get_or_404(id)
    form = BannerForm(obj=banner)

    if form.validate_on_submit():
        # Handle file upload
        if form.image.data:
            file = form.image.data
            if allowed_file(file.filename):
                filename = save_uploaded_file(file, 'banners')
                banner.image_url = f'/uploads/banners/{filename}'
        elif form.image_url.data:
            banner.image_url = form.image_url.data

        banner.title = form.title.data
        banner.message = form.message.data
        banner.banner_type = form.banner_type.data
        banner.style = form.style.data
        banner.order_index = form.order_index.data
        banner.start_date = form.start_date.data
        banner.end_date = form.end_date.data
        banner.is_active = form.is_active.data

        db.session.commit()
        flash('Banner updated successfully!', 'success')
        return redirect(url_for('admin_banners'))

    return render_template('admin/edit_banner.html', form=form, banner=banner)

@app.route('/admin/banners/delete/<int:id>')
@login_required
def admin_delete_banner(id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    banner = Banner.query.get_or_404(id)
    db.session.delete(banner)
    db.session.commit()
    flash('Banner deleted successfully!', 'success')
    return redirect(url_for('admin_banners'))

@app.route('/admin/transfer-certificates')
@login_required
def admin_transfer_certificates():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    tcs = TransferCertificate.query.order_by(TransferCertificate.uploaded_at.desc()).all()
    return render_template('admin/manage_transfer_certificates.html', tcs=tcs)

@app.route('/admin/transfer-certificates/add', methods=['GET', 'POST'])
@login_required
def admin_add_transfer_certificate():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    form = TransferCertificateForm()

    if form.validate_on_submit():
        admission_number = form.admission_number.data
        
        # Handle file upload
        file = form.tc_file.data
        if file and file.filename:
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{filename}"

            file_path = os.path.join('uploads', 'transfer_certificates', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)

            # Create transfer certificate record
            tc = TransferCertificate(
                admission_number=admission_number,
                file_path=file_path,
                filename=file.filename,
                is_issued=form.is_issued.data,
                uploaded_at=datetime.now()
            )

            db.session.add(tc)
            db.session.commit()

            flash('Transfer certificate uploaded successfully!', 'success')
            return redirect(url_for('admin_transfer_certificates'))
        else:
            flash('Please select a file to upload', 'error')

    return render_template('admin/add_transfer_certificate.html', form=form)

@app.route('/admin/transfer-certificates/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_transfer_certificate(id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    tc = TransferCertificate.query.get_or_404(id)
    form = TransferCertificateForm(obj=tc)

    if form.validate_on_submit():
        form.populate_obj(tc)
        db.session.commit()
        flash('Transfer Certificate updated successfully!', 'success')
        return redirect(url_for('admin_transfer_certificates'))

    return render_template('admin/edit_transfer_certificate.html', form=form, tc=tc)

@app.route('/admin/transfer-certificates/delete/<int:id>')
@login_required
def admin_delete_transfer_certificate(id):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    tc = TransferCertificate.query.get_or_404(id)
    db.session.delete(tc)
    db.session.commit()
    flash('Transfer Certificate deleted successfully!', 'success')
    return redirect(url_for('admin_transfer_certificates'))

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Handle form submissions for different settings
        for key, value in request.form.items():
            if key.startswith('setting_'):
                setting_key = key.replace('setting_', '')
                setting = Setting.query.filter_by(key=setting_key).first()
                if setting:
                    setting.value = value
                    setting.updated_at = datetime.utcnow()
                else:
                    setting = Setting(key=setting_key, value=value)
                    db.session.add(setting)
            else:
                # Handle settings without 'setting_' prefix
                setting = Setting.query.filter_by(key=key).first()
                if setting:
                    setting.value = value
                    setting.updated_at = datetime.utcnow()
                else:
                    setting = Setting(key=key, value=value)
                    db.session.add(setting)

        db.session.commit()
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('admin_settings'))

    # Get all settings as a dictionary for easier template access
    settings_query = Setting.query.all()
    settings = {}
    for setting in settings_query:
        settings[setting.key] = setting.value

    # Get stats for the settings page
    stats = {
        'total_news': News.query.count(),
        'total_faculty': Faculty.query.count(),
        'total_contacts': Contact.query.count(),
        'total_admissions': Admission.query.count(),
        'total_gallery': Gallery.query.count(),
        'total_documents': Document.query.count(),
        'total_transfer_certificates': TransferCertificate.query.count()
    }

    return render_template('admin/settings.html', settings=settings, stats=stats)

# Add password checking method to User model
def check_password(self, password):
    from werkzeug.security import check_password_hash
    return check_password_hash(self.password_hash, password)

User.check_password = check_password