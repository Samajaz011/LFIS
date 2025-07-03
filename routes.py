from flask import render_template, request, redirect, url_for, flash, jsonify, send_file
from app import app, db
from models import *
from forms import ContactForm, AdmissionForm, TCSearchForm
import os

@app.context_processor
def inject_settings():
    """Make settings available to all templates"""
    settings = {}
    db_settings = Setting.query.all()
    for setting in db_settings:
        settings[setting.key] = setting.value
    return dict(settings=settings)

@app.route('/')
def index():
    # Get featured content
    featured_news = News.query.filter_by(is_featured=True, is_active=True).order_by(News.publish_date.desc()).limit(6).all()
    featured_gallery = Gallery.query.filter_by(is_active=True).order_by(Gallery.created_at.desc()).limit(6).all()
    about_content = SchoolInfo.query.filter_by(section='about', is_active=True).first()

    # Get active banners
    flash_banner = Banner.query.filter_by(banner_type='flash', is_active=True).first()
    popup_banner = Banner.query.filter_by(banner_type='popup', is_active=True).first()
    slider_banners = Banner.query.filter_by(banner_type='slider', is_active=True).order_by(Banner.order_index.asc()).all()

    return render_template('index.html', 
                         featured_news=featured_news, 
                         featured_gallery=featured_gallery,
                         about_content=about_content,
                         flash_banner=flash_banner,
                         popup_banner=popup_banner,
                         slider_banners=slider_banners)

@app.route('/about')
def about():
    # Get all about section content
    about_sections = SchoolInfo.query.filter_by(section='about', is_active=True).order_by(SchoolInfo.order_index.asc()).all()
    mission = SchoolInfo.query.filter_by(section='mission', is_active=True).first()
    vision = SchoolInfo.query.filter_by(section='vision', is_active=True).first()
    values = SchoolInfo.query.filter_by(section='values', is_active=True).first()
    history = SchoolInfo.query.filter_by(section='history', is_active=True).first()

    return render_template('about.html', 
                         about_sections=about_sections,
                         mission=mission,
                         vision=vision,
                         values=values,
                         history=history)

@app.route('/academics')
def academics():
    # Get academic content
    curriculum = SchoolInfo.query.filter_by(section='curriculum', is_active=True).order_by(SchoolInfo.order_index.asc()).all()
    examination = SchoolInfo.query.filter_by(section='examination', is_active=True).first()

    return render_template('academics.html', 
                         curriculum=curriculum,
                         examination=examination)

@app.route('/admissions', methods=['GET', 'POST'])
def admissions():
    form = AdmissionForm()

    if form.validate_on_submit():
        admission = Admission(
            student_name=form.student_name.data,
            parent_name=form.parent_name.data,
            email=form.email.data,
            phone=form.phone.data,
            class_applying=form.class_applying.data,
            previous_school=form.previous_school.data,
            message=form.message.data
        )
        db.session.add(admission)
        db.session.commit()
        flash('Admission application submitted successfully! We will contact you soon.', 'success')
        return redirect(url_for('admissions'))

    # Get admission content
    admission_content = SchoolInfo.query.filter_by(section='admission', is_active=True).order_by(SchoolInfo.order_index.asc()).all()

    return render_template('admissions.html', form=form, admission_content=admission_content)

@app.route('/faculty')
def faculty():
    # Get faculty by department
    departments = db.session.query(Faculty.department).filter_by(is_active=True).distinct().all()
    faculty_by_dept = {}

    for dept in departments:
        faculty_by_dept[dept[0]] = Faculty.query.filter_by(department=dept[0], is_active=True).order_by(Faculty.order_index.asc()).all()

    return render_template('faculty.html', faculty_by_dept=faculty_by_dept)

@app.route('/student-life')
def student_life():
    # Get student life content
    activities = SchoolInfo.query.filter_by(section='activities', is_active=True).order_by(SchoolInfo.order_index.asc()).all()
    clubs = SchoolInfo.query.filter_by(section='clubs', is_active=True).order_by(SchoolInfo.order_index.asc()).all()
    events = SchoolInfo.query.filter_by(section='events', is_active=True).order_by(SchoolInfo.order_index.asc()).all()

    return render_template('student_life.html', activities=activities, clubs=clubs, events=events)

@app.route('/facilities')
def facilities():
    # Get facilities content
    facilities = SchoolInfo.query.filter_by(section='facilities', is_active=True).order_by(SchoolInfo.order_index.asc()).all()

    return render_template('facilities.html', facilities=facilities)

@app.route('/news')
def news():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'all')

    query = News.query.filter_by(is_active=True)

    if category != 'all':
        query = query.filter_by(category=category)

    news = query.order_by(News.publish_date.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    return render_template('news.html', news=news, current_category=category)

@app.route('/news/<int:id>')
def news_detail(id):
    news_item = News.query.get_or_404(id)
    return render_template('news_detail.html', news=news_item)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(contact)
        db.session.commit()
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html', form=form)

@app.route('/gallery')
def gallery():
    category = request.args.get('category', 'all')

    query = Gallery.query.filter_by(is_active=True)

    if category != 'all':
        query = query.filter_by(category=category)

    gallery_items = query.order_by(Gallery.created_at.desc()).all()
    
    # Debug: print gallery items to console
    for item in gallery_items:
        print(f"Gallery item: {item.title}, Image URL: {item.image_url}")

    return render_template('gallery.html', gallery_items=gallery_items, current_category=category)

@app.route('/download-tc/<int:id>')
def download_tc(id):
    tc = TransferCertificate.query.get_or_404(id)
    return send_file(tc.file_path, as_attachment=True, download_name=tc.filename)

@app.route('/transfer-certificate', methods=['GET', 'POST'])
def transfer_certificate():
    form = TCSearchForm()
    tc = None
    
    if form.validate_on_submit():
        tc = TransferCertificate.query.filter_by(
            admission_number=form.admission_number.data,
            is_issued=True
        ).first()
        
        if not tc:
            flash('Transfer Certificate not found for the given admission number.', 'error')
    
    return render_template('transfer_certificate.html', form=form, tc=tc)

@app.route('/resources')
def resources():
    category = request.args.get('category', 'all')

    query = Document.query.filter_by(is_active=True)

    if category != 'all':
        query = query.filter_by(category=category)

    documents = query.order_by(Document.created_at.desc()).all()

    return render_template('resources.html', documents=documents, current_category=category)

@app.route('/download/<int:id>')
def download_document(id):
    document = Document.query.get_or_404(id)
    document.download_count += 1
    db.session.commit()

    return send_file(document.file_path, as_attachment=True, download_name=document.filename)



@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    from flask import send_from_directory
    return send_from_directory('uploads', filename)

@app.route('/library')
def library():
    # This is a placeholder for the library system integration
    library_url = "#"  # This will be configured in admin
    return redirect(library_url)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500