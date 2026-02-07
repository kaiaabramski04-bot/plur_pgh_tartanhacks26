try:
    from flask import Flask, render_template, request, redirect, url_for, session
except ImportError:
    print("Flask is not installed. Please install it with: pip install flask")
    exit(1)

import os
import csv
import json
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for sessions

# Database (SQLite) configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Reuse the data loading and scoring logic from the original script
def load_data(filepath='plurpgh.csv'):
    data = []
    try:
        with open(filepath, mode='r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data
    except FileNotFoundError:
        return []

def calculate_scores(data, user_zip, user_budget, user_types, user_prefs):
    price_rank = {'$': 1, '$$': 2, '$$$': 3}
    user_rank = price_rank.get(user_budget, 1)
    
    scored_results = []
    
    for row in data:
        score = 0
        
        # 1. Preferences (+50 points each - HIGHEST PRIORITY)
        for pref in user_prefs:
            val = row.get(pref, '').strip()
            if val and val != '0':
                score += 50
        
        # 2. Type Match (+30 points - SECOND PRIORITY)
        if row.get('type', '').strip() in user_types:
            score += 30
            
        # 3. Zip Code Match (+20 points - THIRD PRIORITY)
        if row.get('Zip Code', '').strip() == user_zip:
            score += 20
            
        # 4. Budget Weighting (LOWER PRIORITY)
        v_price = row.get('price', '').strip()
        
        if v_price in price_rank:
            v_rank = price_rank[v_price]
            diff = user_rank - v_rank
            
            if diff < 0:
                # Venue is more expensive than budget -> Huge Penalty
                score -= 1000
            else:
                # 15 pts for exact match, -5 for every step cheaper
                weight_score = 15 - (diff * 5)
                score += max(0, weight_score)
        
        # Store result if it's not totally excluded
        if score > -100:
            row['match_score'] = score
            scored_results.append(row)
            
    # Sort by score descending (highest first)
    scored_results.sort(key=lambda x: x['match_score'], reverse=True)
    
    return scored_results[:3]


# --- Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    results = db.relationship('Result', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_zip = db.Column(db.String(20))
    user_budget = db.Column(db.String(10))
    user_types = db.Column(db.String(200))
    user_prefs = db.Column(db.String(200))
    venues_json = db.Column(db.Text)


# --- Posts / Comments / Chat Models ---
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='post', lazy=True)

    @property
    def user(self):
        return User.query.get(self.user_id)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def user(self):
        return User.query.get(self.user_id)


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            return render_template('register.html', error='Username and password required')

        existing = User.query.filter_by(username=username).first()
        if existing:
            return render_template('register.html', error='Username already exists')

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        session['username'] = user.username
        return redirect(url_for('quiz'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('quiz'))
        return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    results = Result.query.filter_by(user_id=user_id).order_by(Result.timestamp.desc()).all()
    parsed = []
    for r in results:
        try:
            venues = json.loads(r.venues_json or '[]')
        except Exception:
            venues = []
        parsed.append({'id': r.id, 'timestamp': r.timestamp, 'user_zip': r.user_zip, 'venues': venues})

    return render_template('dashboard.html', results=parsed, username=session.get('username'))


# --- Posts & Comments routes ---
@app.route('/posts')
def posts():
    data = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('posts.html', posts=data)


@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        body = request.form.get('body', '').strip()
        if not title or not body:
            return render_template('new_post.html', error='Title and body required')
        p = Post(user_id=user_id, title=title, body=body)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('post_detail', post_id=p.id))

    return render_template('new_post.html')


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    p = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login'))
        body = request.form.get('body', '').strip()
        if body:
            c = Comment(post_id=post_id, user_id=user_id, body=body)
            db.session.add(c)
            db.session.commit()
            return redirect(url_for('post_detail', post_id=post_id))

    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp.asc()).all()
    return render_template('post_detail.html', post=p, comments=comments)


# --- Simple chat endpoints (polling-based) ---
@app.route('/chat')
def chat():
    return render_template('chat.html')


@app.route('/chat/messages')
def chat_messages():
    # return last 100 messages
    msgs = ChatMessage.query.order_by(ChatMessage.timestamp.asc()).limit(200).all()
    out = []
    for m in msgs:
        out.append({
            'id': m.id,
            'user': User.query.get(m.user_id).username if User.query.get(m.user_id) else 'unknown',
            'body': m.body,
            'timestamp': m.timestamp.isoformat()
        })
    return jsonify(out)


@app.route('/chat/send', methods=['POST'])
def chat_send():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error':'login required'}), 403
    data = request.get_json() or {}
    body = data.get('message', '').strip()
    if not body:
        return jsonify({'error':'empty'}), 400
    m = ChatMessage(user_id=user_id, body=body)
    db.session.add(m)
    db.session.commit()
    return jsonify({'ok':True, 'id': m.id, 'timestamp': m.timestamp.isoformat()})

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Process form data
        user_zip = request.form.get('zip', '').strip()
        user_budget = request.form.get('budget', '$')
        user_types = request.form.getlist('types')
        user_prefs = request.form.getlist('prefs')
        
        # Store in session
        session['user_zip'] = user_zip
        session['user_budget'] = user_budget
        session['user_types'] = user_types
        session['user_prefs'] = user_prefs
        
        return redirect(url_for('results'))
    
    # GET request - show the quiz form
    data = load_data()
    if not data:
        return "Error: CSV file not found", 500
    
    # Extract unique types and define preferences
    unique_types = sorted(list(set(row.get('type', '').strip() for row in data if row.get('type'))))
    preferences = ['LGBT +', 'Adult Club', 'Activity']
    
    return render_template('quiz.html', types=unique_types, prefs=preferences)

@app.route('/results')
def results():
    # Get data from session
    user_zip = session.get('user_zip', '')
    user_budget = session.get('user_budget', '$')
    user_types = session.get('user_types', [])
    user_prefs = session.get('user_prefs', [])
    
    if not user_zip:
        return redirect(url_for('quiz'))
    
    # Load data and calculate results
    data = load_data()
    if not data:
        return "Error: CSV file not found", 500
    
    venues = calculate_scores(data, user_zip, user_budget, user_types, user_prefs)

    # If user is logged in, save the result snapshot
    user_id = session.get('user_id')
    if user_id:
        try:
            r = Result(user_id=user_id,
                       user_zip=user_zip,
                       user_budget=user_budget,
                       user_types=','.join(user_types) if user_types else '',
                       user_prefs=','.join(user_prefs) if user_prefs else '',
                       venues_json=json.dumps(venues))
            db.session.add(r)
            db.session.commit()
        except Exception:
            db.session.rollback()

    return render_template('results.html', venues=venues)

@app.route('/about')
def about():
    # Load venue data for the map
    data = load_data()
    if not data:
        venues = []
    else:
        # Filter out venues without coordinates
        venues = [row for row in data if row.get('latitude') and row.get('longitude')]
    
    return render_template('about.html', venues=venues)

if __name__ == '__main__':
    print("=" * 60)
    print("🎮 PITTSBURGH VENUE FINDER - PLUR PGH 🎮")
    print("=" * 60)
    print("🚀 Starting Flask development server...")
    print("📱 Your app will be available at:")
    print("   http://127.0.0.1:5000")
    print("=" * 60)
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 60)
    # Ensure DB tables exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)