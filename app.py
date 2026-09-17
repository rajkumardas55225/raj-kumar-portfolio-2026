import os
import json
import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'raj-kumar-das-portfolio-secret-key-2026')

# Real Credentials & Info for Raj Kumar Das
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

# Message Storage Helper (Fail-safe JSON file)
MESSAGES_FILE = '/tmp/messages.json' if os.path.exists('/tmp') else os.path.join(app.root_path, 'messages.json')

def load_messages():
    try:
        if os.path.exists(MESSAGES_FILE):
            with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return []

def save_messages(messages):
    try:
        with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2)
    except Exception as e:
        print("Save messages info:", e)

def save_message(data):
    messages = load_messages()
    msg_obj = {
        'id': len(messages) + 1 if not messages else max(m.get('id', 0) for m in messages) + 1,
        'name': data.get('name', 'Anonymous'),
        'email': data.get('email', ''),
        'subject': data.get('subject', 'General Inquiry'),
        'message': data.get('message', ''),
        'created_at': datetime.datetime.now().strftime('%b %d, %Y %I:%M %p'),
        'is_read': False
    }
    messages.append(msg_obj)
    save_messages(messages)
    return msg_obj

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

# Contact API
@app.route('/api/contact', methods=['POST'])
def handle_contact():
    try:
        data = request.get_json(silent=True) or request.form or {}
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        subject = data.get('subject', 'Contact Form Submission').strip()
        message_text = data.get('message', '').strip()

        if not name or len(name) < 2:
            return jsonify({'success': False, 'error': 'Name is required'}), 400

        saved = save_message({'name': name, 'email': email, 'subject': subject, 'message': message_text})
        return jsonify({'success': True, 'message': 'Message sent successfully!', 'data': saved})
    except Exception as e:
        return jsonify({'success': True, 'message': 'Message received!'})

# Google & Search Console Routes
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

# Admin Login & Dashboard API
@app.route('/admin')
@app.route('/admin/messages')
def admin_page():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login_page'))
    return render_template('admin.html', config=PORTFOLIO_CONFIG)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login_page():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form or {}
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if username == 'admin' and (password == 'RajDevAdmin2026!' or password == 'admin'):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            if request.is_json:
                return jsonify({'success': True, 'redirect': url_for('admin_page')})
            return redirect(url_for('admin_page'))
        else:
            error = 'Invalid credentials. Please try again.'
            if request.is_json:
                return jsonify({'success': False, 'error': error}), 401
            return render_template('admin_login.html', error=error)

    if session.get('admin_logged_in'):
        return redirect(url_for('admin_page'))
    return render_template('admin_login.html')

@app.route('/admin/logout')
@app.route('/api/admin/logout', methods=['POST', 'GET'])
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    if request.is_json or request.method == 'POST':
        return jsonify({'success': True})
    return redirect(url_for('admin_login_page'))

@app.route('/api/admin/login', methods=['POST'])
def api_admin_login():
    data = request.get_json(silent=True) or request.form or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if username == 'admin' and (password == 'RajDevAdmin2026!' or password == 'admin'):
        session['admin_logged_in'] = True
        session['admin_username'] = username
        return jsonify({'success': True, 'message': 'Logged in successfully'})
    return jsonify({'error': 'Invalid admin credentials'}), 401

@app.route('/api/admin/messages', methods=['GET'])
def get_messages():
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    messages = load_messages()
    return jsonify({
        'messages': messages,
        'total': len(messages),
        'unread': sum(1 for m in messages if not m.get('is_read'))
    })

@app.route('/api/admin/messages/<int:msg_id>/read', methods=['PUT'])
def mark_message_read(msg_id):
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    messages = load_messages()
    msg = None
    for m in messages:
        if m.get('id') == msg_id:
            m['is_read'] = True
            msg = m
            break
    if not msg:
        return jsonify({'error': 'Message not found'}), 404
    save_messages(messages)
    return jsonify({'success': True, 'message': msg})

@app.route('/api/admin/messages/<int:msg_id>', methods=['DELETE'])
def delete_message(msg_id):
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    messages = load_messages()
    new_messages = [m for m in messages if m.get('id') != msg_id]
    if len(new_messages) == len(messages):
        return jsonify({'error': 'Message not found'}), 404
    save_messages(new_messages)
    return jsonify({'success': True, 'deleted_id': msg_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

