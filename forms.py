from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, BooleanField, PasswordField, IntegerField, DateTimeField, DateField
from wtforms.validators import DataRequired, Email, Length, Optional
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=5, max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])

class AdmissionForm(FlaskForm):
    student_name = StringField('Student Name', validators=[DataRequired(), Length(min=2, max=100)])
    parent_name = StringField('Parent Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=20)])
    class_applying = SelectField('Class Applying For', validators=[DataRequired()], 
                                choices=[('nursery', 'Nursery'), ('lkg', 'LKG'), ('ukg', 'UKG'),
                                        ('class-1', 'Class I'), ('class-2', 'Class II'), ('class-3', 'Class III'),
                                        ('class-4', 'Class IV'), ('class-5', 'Class V'), ('class-6', 'Class VI'),
                                        ('class-7', 'Class VII'), ('class-8', 'Class VIII'), ('class-9', 'Class IX'),
                                        ('class-10', 'Class X'), ('class-11', 'Class XI'), ('class-12', 'Class XII')])
    previous_school = StringField('Previous School', validators=[Optional(), Length(max=200)])
    message = TextAreaField('Additional Message', validators=[Optional(), Length(max=1000)])

class SchoolInfoForm(FlaskForm):
    section = StringField('Section', validators=[DataRequired(), Length(max=50)])
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()], widget=TextArea())
    image_url = StringField('Image URL', validators=[Optional(), Length(max=200)])
    order_index = IntegerField('Order Index', validators=[Optional()], default=0)
    is_active = BooleanField('Active', default=True)

class NewsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()], widget=TextArea())
    summary = StringField('Summary', validators=[Optional(), Length(max=500)])
    image = FileField('Featured Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    image_url = StringField('Image URL (alternative)', validators=[Optional(), Length(max=200)])
    category = SelectField('Category', validators=[DataRequired()], 
                          choices=[('general', 'General'), ('announcement', 'Announcement'), 
                                  ('achievement', 'Achievement'), ('event', 'Event')])
    is_featured = BooleanField('Featured', default=False)
    is_active = BooleanField('Active', default=True)

class FacultyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    position = StringField('Position', validators=[DataRequired(), Length(max=100)])
    department = StringField('Department', validators=[DataRequired(), Length(max=100)])
    qualification = StringField('Qualification', validators=[Optional(), Length(max=200)])
    experience = StringField('Experience', validators=[Optional(), Length(max=100)])
    bio = TextAreaField('Bio', validators=[Optional()])
    image = FileField('Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    image_url = StringField('Image URL (alternative)', validators=[Optional(), Length(max=200)])
    email = StringField('Email', validators=[Optional(), Email()])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    order_index = IntegerField('Order Index', validators=[Optional()], default=0)
    is_active = BooleanField('Active', default=True)

class GalleryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    image_url = StringField('Image URL (alternative)', validators=[Optional(), Length(max=200)])
    category = SelectField('Category', validators=[DataRequired()], 
                          choices=[('general', 'General'), ('events', 'Events'), 
                                  ('facilities', 'Facilities'), ('activities', 'Activities')])
    is_featured = BooleanField('Featured', default=False)
    is_active = BooleanField('Active', default=True)

class DocumentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional()])
    file = FileField('File', validators=[DataRequired(), FileAllowed(['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt'])])
    category = SelectField('Category', validators=[DataRequired()], 
                          choices=[('general', 'General'), ('forms', 'Forms'), 
                                  ('policies', 'Policies'), ('resources', 'Resources')])
    is_active = BooleanField('Active', default=True)

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional()])
    event_date = DateTimeField('Event Date', validators=[DataRequired()], format='%Y-%m-%d')
    location = StringField('Location', validators=[Optional(), Length(max=200)])
    image_url = StringField('Image URL', validators=[Optional(), Length(max=200)])
    is_active = BooleanField('Active', default=True)

class BannerForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired()])
    banner_type = SelectField('Banner Type', validators=[DataRequired()], 
                             choices=[('flash', 'Flash Banner'), ('popup', 'Popup Banner'), ('slider', 'Slider Banner')])
    style = SelectField('Style', validators=[DataRequired()], 
                       choices=[('info', 'Info'), ('warning', 'Warning'), 
                               ('success', 'Success'), ('danger', 'Danger')])
    image = FileField('Banner Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    image_url = StringField('Image URL (alternative)', validators=[Optional(), Length(max=200)])
    order_index = IntegerField('Order Index', validators=[Optional()], default=0)
    start_date = DateTimeField('Start Date', validators=[Optional()], format='%Y-%m-%d')
    end_date = DateTimeField('End Date', validators=[Optional()], format='%Y-%m-%d')
    is_active = BooleanField('Active', default=True)

class TransferCertificateForm(FlaskForm):
    admission_number = StringField('Admission Number', validators=[DataRequired(), Length(max=20)])
    tc_file = FileField('Transfer Certificate File', validators=[DataRequired(), FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Only PDF and image files allowed!')])
    is_issued = BooleanField('Issued', default=True)

class TCSearchForm(FlaskForm):
    admission_number = StringField('Admission Number', validators=[DataRequired(), Length(max=20)])
