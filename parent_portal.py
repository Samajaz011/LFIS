from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date, timedelta
from sqlalchemy import func, and_, or_
from app import app, db
from models import (Parent, Student, Grade, Attendance, Assignment, Subject, 
                   StudentEvent, ProgressReport)
import calendar

# Parent Login System
class ParentUser:
    def __init__(self, parent):
        self.id = parent.id
        self.email = parent.email
        self.first_name = parent.first_name
        self.last_name = parent.last_name
        self.is_authenticated = True
        self.is_active = parent.is_active
        self.is_anonymous = False
        
    def get_id(self):
        return str(self.id)

@app.route('/parent/login')
def parent_login():
    return render_template('parent/login.html')

@app.route('/parent/login', methods=['POST'])
def parent_login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        flash('Please enter both email and password', 'error')
        return redirect(url_for('parent_login'))
    
    # Create demo parent if it doesn't exist
    if email == 'demo@parent.com' and password == 'demo123':
        demo_parent = Parent.query.filter_by(email='demo@parent.com').first()
        if not demo_parent:
            demo_parent = Parent(
                email='demo@parent.com',
                password_hash=generate_password_hash('demo123'),
                first_name='Demo',
                last_name='Parent',
                phone='(555) 123-4567',
                is_active=True
            )
            db.session.add(demo_parent)
            db.session.commit()
        
        # Store parent info in session
        session['parent_id'] = demo_parent.id
        session['parent_name'] = f"{demo_parent.first_name} {demo_parent.last_name}"
        
        flash(f'Welcome, {demo_parent.first_name}! (Demo Account)', 'success')
        return redirect(url_for('parent_dashboard'))
    
    parent = Parent.query.filter_by(email=email).first()
    
    if not parent or not check_password_hash(parent.password_hash, password):
        flash('Invalid email or password', 'error')
        return redirect(url_for('parent_login'))
    
    if not parent.is_active:
        flash('Your account has been deactivated. Please contact school administration.', 'error')
        return redirect(url_for('parent_login'))
    
    # Store parent info in session
    session['parent_id'] = parent.id
    session['parent_name'] = f"{parent.first_name} {parent.last_name}"
    
    flash(f'Welcome, {parent.first_name}!', 'success')
    return redirect(url_for('parent_dashboard'))

@app.route('/parent/logout')
def parent_logout():
    session.pop('parent_id', None)
    session.pop('parent_name', None)
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('parent_login'))

def parent_login_required(f):
    def decorated_function(*args, **kwargs):
        if 'parent_id' not in session:
            flash('Please log in to access the parent portal', 'error')
            return redirect(url_for('parent_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/parent/dashboard')
@parent_login_required
def parent_dashboard():
    parent_id = session['parent_id']
    parent = Parent.query.get(parent_id)
    students = Student.query.filter_by(parent_id=parent_id, is_active=True).all()
    
    # Get summary data for each student
    student_summaries = []
    for student in students:
        # Latest attendance (last 7 days)
        week_ago = date.today() - timedelta(days=7)
        recent_attendance = Attendance.query.filter(
            Attendance.student_id == student.id,
            Attendance.date >= week_ago
        ).all()
        
        attendance_rate = 0
        if recent_attendance:
            present_days = sum(1 for att in recent_attendance if att.status == 'Present')
            attendance_rate = (present_days / len(recent_attendance)) * 100
        
        # Recent grades average
        recent_grades = Grade.query.filter_by(student_id=student.id).order_by(Grade.exam_date.desc()).limit(5).all()
        avg_percentage = 0
        if recent_grades:
            total_percentage = sum((g.marks_obtained / g.total_marks) * 100 for g in recent_grades)
            avg_percentage = total_percentage / len(recent_grades)
        
        # Pending assignments
        pending_assignments = Assignment.query.filter(
            Assignment.student_id == student.id,
            Assignment.status == 'assigned',
            Assignment.due_date >= date.today()
        ).count()
        
        # Recent events
        recent_events = StudentEvent.query.filter_by(student_id=student.id).order_by(StudentEvent.event_date.desc()).limit(3).all()
        
        student_summaries.append({
            'student': student,
            'attendance_rate': round(attendance_rate, 1),
            'avg_percentage': round(avg_percentage, 1),
            'pending_assignments': pending_assignments,
            'recent_events': recent_events
        })
    
    return render_template('parent/dashboard.html', 
                         parent=parent, 
                         student_summaries=student_summaries)

@app.route('/parent/student/<int:student_id>')
@parent_login_required
def student_detail(student_id):
    parent_id = session['parent_id']
    student = Student.query.filter_by(id=student_id, parent_id=parent_id).first_or_404()
    
    # Get current academic year and term
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    # Determine current term (assuming quarters)
    if current_month <= 3:
        current_term = "Quarter 3"
        academic_year = f"{current_year-1}-{current_year}"
    elif current_month <= 6:
        current_term = "Quarter 4"
        academic_year = f"{current_year-1}-{current_year}"
    elif current_month <= 9:
        current_term = "Quarter 1"
        academic_year = f"{current_year}-{current_year+1}"
    else:
        current_term = "Quarter 2"
        academic_year = f"{current_year}-{current_year+1}"
    
    return render_template('parent/student_detail.html', 
                         student=student,
                         current_term=current_term,
                         academic_year=academic_year)

@app.route('/parent/grades/<int:student_id>')
@parent_login_required
def student_grades(student_id):
    parent_id = session['parent_id']
    student = Student.query.filter_by(id=student_id, parent_id=parent_id).first_or_404()
    
    # Get all subjects for this student's class
    subjects = Subject.query.filter_by(class_level=student.class_name.split('-')[0]).all()
    
    # Get grades grouped by subject
    grades_by_subject = {}
    for subject in subjects:
        grades = Grade.query.filter_by(
            student_id=student.id, 
            subject_id=subject.id
        ).order_by(Grade.exam_date.desc()).all()
        
        if grades:
            avg_percentage = sum((g.marks_obtained / g.total_marks) * 100 for g in grades) / len(grades)
            grades_by_subject[subject] = {
                'grades': grades,
                'average': round(avg_percentage, 1)
            }
    
    return render_template('parent/grades.html', 
                         student=student,
                         grades_by_subject=grades_by_subject)

@app.route('/parent/attendance/<int:student_id>')
@parent_login_required
def student_attendance(student_id):
    parent_id = session['parent_id']
    student = Student.query.filter_by(id=student_id, parent_id=parent_id).first_or_404()
    
    # Get current month attendance
    current_date = date.today()
    start_of_month = current_date.replace(day=1)
    
    attendance_records = Attendance.query.filter(
        Attendance.student_id == student.id,
        Attendance.date >= start_of_month
    ).order_by(Attendance.date.desc()).all()
    
    # Calculate statistics
    total_days = len(attendance_records)
    present_days = sum(1 for att in attendance_records if att.status == 'Present')
    absent_days = sum(1 for att in attendance_records if att.status == 'Absent')
    late_days = sum(1 for att in attendance_records if att.status == 'Late')
    
    attendance_rate = (present_days / total_days * 100) if total_days > 0 else 0
    
    # Get monthly view data for calendar
    cal = calendar.monthcalendar(current_date.year, current_date.month)
    attendance_calendar = {}
    for record in attendance_records:
        attendance_calendar[record.date.day] = record.status
    
    return render_template('parent/attendance.html',
                         student=student,
                         attendance_records=attendance_records,
                         attendance_rate=round(attendance_rate, 1),
                         present_days=present_days,
                         absent_days=absent_days,
                         late_days=late_days,
                         calendar_data=cal,
                         attendance_calendar=attendance_calendar,
                         current_month=current_date.strftime('%B %Y'))

@app.route('/parent/assignments/<int:student_id>')
@parent_login_required
def student_assignments(student_id):
    parent_id = session['parent_id']
    student = Student.query.filter_by(id=student_id, parent_id=parent_id).first_or_404()
    
    # Get assignments by status
    pending_assignments = Assignment.query.filter(
        Assignment.student_id == student.id,
        Assignment.status == 'assigned',
        Assignment.due_date >= date.today()
    ).order_by(Assignment.due_date.asc()).all()
    
    submitted_assignments = Assignment.query.filter(
        Assignment.student_id == student.id,
        Assignment.status.in_(['submitted', 'graded'])
    ).order_by(Assignment.submission_date.desc()).all()
    
    overdue_assignments = Assignment.query.filter(
        Assignment.student_id == student.id,
        Assignment.status == 'assigned',
        Assignment.due_date < date.today()
    ).order_by(Assignment.due_date.desc()).all()
    
    return render_template('parent/assignments.html',
                         student=student,
                         pending_assignments=pending_assignments,
                         submitted_assignments=submitted_assignments,
                         overdue_assignments=overdue_assignments,
                         today=date.today())

@app.route('/parent/events/<int:student_id>')
@parent_login_required
def student_events(student_id):
    parent_id = session['parent_id']
    student = Student.query.filter_by(id=student_id, parent_id=parent_id).first_or_404()
    
    # Get recent events
    events = StudentEvent.query.filter_by(student_id=student.id).order_by(StudentEvent.event_date.desc()).all()
    
    # Group events by type
    events_by_type = {
        'Achievement': [],
        'Discipline': [],
        'Health': [],
        'General': []
    }
    
    for event in events:
        if event.event_type in events_by_type:
            events_by_type[event.event_type].append(event)
    
    return render_template('parent/events.html',
                         student=student,
                         events_by_type=events_by_type)

@app.route('/parent/progress-report/<int:student_id>')
@parent_login_required
def progress_report(student_id):
    parent_id = session['parent_id']
    student = Student.query.filter_by(id=student_id, parent_id=parent_id).first_or_404()
    
    # Get latest progress report
    latest_report = ProgressReport.query.filter_by(student_id=student.id).order_by(ProgressReport.generated_date.desc()).first()
    
    # Get all available reports
    all_reports = ProgressReport.query.filter_by(student_id=student.id).order_by(ProgressReport.generated_date.desc()).all()
    
    return render_template('parent/progress_report.html',
                         student=student,
                         latest_report=latest_report,
                         all_reports=all_reports)

@app.route('/parent/api/attendance-chart/<int:student_id>')
@parent_login_required
def attendance_chart_data(student_id):
    parent_id = session['parent_id']
    student = Student.query.filter_by(id=student_id, parent_id=parent_id).first_or_404()
    
    # Get last 6 months of attendance data
    six_months_ago = date.today() - timedelta(days=180)
    attendance_records = Attendance.query.filter(
        Attendance.student_id == student.id,
        Attendance.date >= six_months_ago
    ).all()
    
    # Group by month
    monthly_data = {}
    for record in attendance_records:
        month_key = record.date.strftime('%Y-%m')
        if month_key not in monthly_data:
            monthly_data[month_key] = {'present': 0, 'absent': 0, 'late': 0, 'total': 0}
        
        monthly_data[month_key]['total'] += 1
        if record.status == 'Present':
            monthly_data[month_key]['present'] += 1
        elif record.status == 'Absent':
            monthly_data[month_key]['absent'] += 1
        elif record.status == 'Late':
            monthly_data[month_key]['late'] += 1
    
    # Format for chart
    chart_data = {
        'labels': [datetime.strptime(month, '%Y-%m').strftime('%B %Y') for month in sorted(monthly_data.keys())],
        'present': [monthly_data[month]['present'] for month in sorted(monthly_data.keys())],
        'absent': [monthly_data[month]['absent'] for month in sorted(monthly_data.keys())],
        'late': [monthly_data[month]['late'] for month in sorted(monthly_data.keys())]
    }
    
    return jsonify(chart_data)

@app.route('/parent/api/grades-chart/<int:student_id>')
@parent_login_required
def grades_chart_data(student_id):
    parent_id = session['parent_id']
    student = Student.query.filter_by(id=student_id, parent_id=parent_id).first_or_404()
    
    # Get recent grades by subject
    subjects = Subject.query.filter_by(class_level=student.class_name.split('-')[0]).all()
    
    chart_data = {
        'labels': [],
        'data': []
    }
    
    for subject in subjects:
        recent_grades = Grade.query.filter_by(
            student_id=student.id,
            subject_id=subject.id
        ).order_by(Grade.exam_date.desc()).limit(5).all()
        
        if recent_grades:
            avg_percentage = sum((g.marks_obtained / g.total_marks) * 100 for g in recent_grades) / len(recent_grades)
            chart_data['labels'].append(subject.name)
            chart_data['data'].append(round(avg_percentage, 1))
    
    return jsonify(chart_data)

# Helper function for templates
@app.context_processor
def inject_parent_students():
    def get_parent_students(parent_id):
        return Student.query.filter_by(parent_id=parent_id, is_active=True).all()
    return dict(get_parent_students=get_parent_students)