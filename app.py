import os
import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'raj-kumar-das-portfolio-secret-key-2026')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'portfolio.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'created_at': self.created_at.strftime('%b %d, %Y %I:%M %p'),
            'is_read': self.is_read
        }

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

# Site Info Configuration (Fully Verified Real Credentials for Raj Kumar Das)
PORTFOLIO_CONFIG = {
    "name": "Raj Kumar Das",
    "degree": "B.Tech – Computer Science & Engineering",
    "institute": "Amity University Jharkhand",
    "campus": "Ranchi Campus, Jharkhand",
    "batch": "2025–2029",
    "current_semester": "3rd Semester",
    "location": "Ranchi, Jharkhand, India",
    "phone": "+91 82529 75401",
    "phone_alt": "+91 92048 19351",
    "whatsapp": "https://wa.me/918252975401?text=Hello%20Raj%20Kumar%20Das,%20I%20visited%20your%20portfolio%20website%20and%20I'd%20like%20to%20connect%20with%20you!",
    "telegram": "https://t.me/rajjjjjj_52627",
    "github": "https://github.com/rajkumardas552",
    "linkedin": "https://www.linkedin.com/in/raj-kumar-das-b444a127b",
    "email": "rajk4881169@gmail.com",
    "email_alt": "dasrajkumar2908@gmail.com",
    "student_email": "rajkumar.das@student.amity.edu",
    "resume_url": "/resume",
    "sih_team": "UNCODED.SIH",
    "sih_problem": "SIH26153",
    "status": "Building & Learning",
    "photo_url": "/static/images/raj-profile.jpg"
}

# Ensure Database Tables Exist & Default Admin User Created
with app.app_context():
    db.create_all()
    if not AdminUser.query.filter_by(username='admin').first():
        default_admin = AdminUser(
            username='admin',
            password_hash=generate_password_hash('RajDevAdmin2026!')
        )
        db.session.add(default_admin)
        db.session.commit()

# Public Routes
@app.route('/')
def index():
    return render_template('index.html', config=PORTFOLIO_CONFIG)

@app.route('/resume')
def resume():
    return render_template('resume.html', config=PORTFOLIO_CONFIG)

@app.route('/api/config')
def get_config():
    return jsonify(PORTFOLIO_CONFIG)

# Contact Form API Endpoint
@app.route('/api/contact', methods=['POST'])
def handle_contact():
    try:
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        subject = data.get('subject', '').strip()
        message_text = data.get('message', '').strip()

        # Validation
        if not name or len(name) < 2:
            return jsonify({'success': False, 'error': 'Please provide a valid name (at least 2 characters).'}), 400
        if not email or '@' not in email or '.' not in email:
            return jsonify({'success': False, 'error': 'Please enter a valid email address.'}), 400
        if not subject or len(subject) < 3:
            return jsonify({'success': False, 'error': 'Please provide a descriptive subject.'}), 400
        if not message_text or len(message_text) < 10:
            return jsonify({'success': False, 'error': 'Message should be at least 10 characters long.'}), 400

        # Save message to database
        new_msg = Message(
            name=name,
            email=email,
            subject=subject,
            message=message_text
        )
        db.session.add(new_msg)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Thank you! Your message has been sent successfully. Raj will get back to you soon.',
            'message_id': new_msg.id
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'An unexpected error occurred: {str(e)}'}), 500

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        data = request.form if request.form else request.get_json() or {}
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        user = AdminUser.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            if request.is_json:
                return jsonify({'success': True, 'redirect': url_for('admin_messages')})
            return redirect(url_for('admin_messages'))
        else:
            error = 'Invalid credentials. Please try again.'
            if request.is_json:
                return jsonify({'success': False, 'error': error}), 401
            return render_template('admin_login.html', error=error)

    if session.get('admin_logged_in'):
        return redirect(url_for('admin_messages'))
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
@app.route('/admin/messages')
def admin_messages():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin.html', config=PORTFOLIO_CONFIG)

# Admin API Endpoints
@app.route('/api/admin/messages', methods=['GET'])
def get_messages():
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return jsonify({
        'messages': [m.to_dict() for m in messages],
        'total': len(messages),
        'unread': sum(1 for m in messages if not m.is_read)
    })

@app.route('/api/admin/messages/<int:msg_id>/read', methods=['PUT'])
def mark_message_read(msg_id):
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    msg = Message.query.get(msg_id)
    if not msg:
        return jsonify({'error': 'Message not found'}), 404
    msg.is_read = True
    db.session.commit()
    return jsonify({'success': True, 'message': msg.to_dict()})

@app.route('/api/admin/messages/<int:msg_id>', methods=['DELETE'])
def delete_message(msg_id):
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    msg = Message.query.get(msg_id)
    if not msg:
        return jsonify({'error': 'Message not found'}), 404
    db.session.delete(msg)
    db.session.commit()
    return jsonify({'success': True, 'deleted_id': msg_id})

@app.route('/robots.txt')
def robots():
    return "User-agent: *\nAllow: /\nSitemap: https://rajkumar-das.vercel.app/sitemap.xml\n", 200, {'Content-Type': 'text/plain'}

@app.route('/sitemap.xml')
def sitemap():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://rajkumar-das.vercel.app/</loc>
    <lastmod>2026-09-17</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://rajkumar-das.vercel.app/resume</loc>
    <lastmod>2026-09-17</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>"""
    return xml, 200, {'Content-Type': 'application/xml'}

@app.route('/google24d3232dac5002f0.html')
def google_html_verification():
    return "google-site-verification: google24d3232dac5002f0.html", 200, {'Content-Type': 'text/html'}

@app.route('/google-verification')
def google_verification_check():
    return '<meta name="google-site-verification" content="ABp0Hm9K6b12oR3G-pghgfcPdTA1Y53U68bIUHk8C1w" />', 200, {'Content-Type': 'text/html'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


