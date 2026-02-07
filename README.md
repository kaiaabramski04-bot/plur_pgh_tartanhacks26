# 🎮 PLUR PGH - Pittsburgh Venue Finder

A retro-electronic web application that helps users discover their perfect nightlife venue in Pittsburgh using intelligent matching algorithms and a cyberpunk-inspired interface.

## 📋 Table of Contents

- [Overview](#overview)
- [What is P.L.U.R.?](#what-is-plur)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Scoring Algorithm](#scoring-algorithm)
- [Data](#data)
- [Development History](#development-history)

---

## 🎯 Overview

**PLUR PGH** transforms a command-line Python script into a modern, interactive web application. It combines venue data (200+ Pittsburgh establishments) with an advanced scoring system to recommend venues that match your preferences, budget, location, and venue type preferences.

The application features:
- A retro electronic aesthetic with lime green/black color scheme
- Flask backend with user authentication and database persistence
- Interactive Leaflet map showing all venue locations
- Community features including posts, comments, and user search history
- Responsive design that works across all devices

---

## 🌈 What is P.L.U.R.?

P.L.U.R. is the core philosophy behind the venue finder:

| Letter | Meaning | Description |
|--------|---------|-------------|
| **P** | PEACE | Letting go of aggression, embracing calm and harmony |
| **L** | LOVE | Fostering deep connection, friendship, and acceptance |
| **U** | UNITY | Creating a collective experience, feeling one with the music and crowd |
| **R** | RESPECT | Acknowledging individuality, boundaries, and looking out for one another |

---

## ✨ Features

### 🎯 Smart Matching Algorithm
- Advanced weighted scoring system that prioritizes user preferences
- Considers venue type, location proximity, and budget compatibility
- Returns top 3 personalized venue recommendations

### 🎨 Retro Electronic Design
- Cyberpunk-inspired visual theme with authentic 80s/90s electronic aesthetic
- Lime green text (#8ACE00) on black background
- Pixel fonts (Press Start 2P) for authentic retro feel
- Custom styled Leaflet popups and controls

### 📍 Interactive Mapping
- Leaflet-based map showing all 200+ venue locations
- Color-coded markers by venue type
- Legend showing venue type color scheme
- Clickable popups with venue information

### 📊 Venue Analytics
- Bar chart showing venue distribution by type
- Statistics dashboard on about page
- Historical view of past search results

### 👥 Community Features
- **Posts System**: Share reviews, tips, and venue recommendations
- **Comments**: Discuss venues and experiences with other users
- **User Dashboard**: Track your search history and past recommendations

### 🔐 User System
- User registration and login with password hashing
- Session management
- Personalized user dashboards
- Search history persistence

### 📱 Responsive Layout
- Side-by-side venue cards with images
- Works seamlessly on desktop, tablet, and mobile
- Clean grid layouts for all UI components

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Python Flask (>=2.0)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Werkzeug (password hashing)
- **Templating**: Jinja2

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Custom styling with cyberpunk theme
- **JavaScript**: Map visualization, chart rendering
- **Mapping Library**: Leaflet.js (1.9.4)
- **Charting Library**: Chart.js

### Data Processing
- CSV data loading and processing
- JSON serialization for results storage
- Web scraping for venue metadata

---

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone/Download the Project
```bash
cd c:\Users\kaiaa\OneDrive\Desktop\Personal_Projects
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:
- Flask>=2.0 - Web framework
- Flask-SQLAlchemy>=3.0 - ORM and database
- Werkzeug>=2.0 - Utilities and security

### Step 3: Verify Data File
Ensure `plurpgh.csv` exists in the project root directory. This file contains all venue data.

---

## 🚀 Usage

### Running the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

### Using the App

1. **Home Page** (`/`)
   - Landing page with navigation to all features

2. **Register** (`/register`)
   - Create a new user account
   - Username and password required

3. **Login** (`/login`)
   - Sign in with existing credentials
   - Maintains session for personalized experience

4. **Quiz** (`/quiz`)
   - Enter your zip code
   - Select budget level ($, $$, $$$)
   - Choose venue types
   - Select preferences (LGBT friendly, Adult Club, Activities)

5. **Results** (`/results`)
   - View your top 3 matched venues
   - See detailed venue information with images
   - Save results to dashboard (if logged in)

6. **Dashboard** (`/dashboard`)
   - View all your past search results
   - Revisit previous recommendations
   - Track your venue exploration history

7. **Posts** (`/posts`)
   - Browse community posts about venues
   - Create new posts with reviews and tips
   - Comment on other users' posts

8. **About** (`/about`)
   - Project information and philosophy
   - Interactive venue map with all locations
   - Bar chart of venues by type
   - Technical architecture details
   - Scoring algorithm breakdown

---

## 📁 Project Structure

```
c:\Users\kaiaa\OneDrive\Desktop\Personal_Projects\
├── app.py                          # Main Flask application
├── plurpgh.csv                     # Venue database (200+ venues)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── app.db                          # SQLite database (created on first run)
├── templates/                      # HTML templates
│   ├── home.html                  # Landing page
│   ├── register.html              # Registration page
│   ├── login.html                 # Login page
│   ├── quiz.html                  # Preference form
│   ├── results.html               # Matched venues display
│   ├── dashboard.html             # User search history
│   ├── posts.html                 # Community posts feed
│   ├── new_post.html              # Create new post
│   ├── post_detail.html           # View post with comments
│   ├── chat.html                  # Community chat
│   └── about.html                 # Project information & map
├── __pycache__/                   # Python cache (auto-generated)
└── Archive/                       # Previous versions and test files
    ├── plur_pgh.py               # Original CLI version
    ├── test_scoring.py           # Scoring tests
    ├── venue_finder_launcher.py  # GUI launcher
    └── Kaggle_Repo_Uber/         # Additional data resources
```

---

## 🧮 Scoring Algorithm

The intelligent matching system uses a **weighted priority-based scoring approach**:

### Priority Levels

| Priority | Factor | Points | Description |
|----------|--------|--------|-------------|
| **1** (Highest) | User Preferences | +50 each | LGBT Friendly, Adult Club, Activity |
| **2** | Venue Type Match | +30 | Bar & Grill, Night Club, Live Music, etc. |
| **3** | Zip Code Match | +20 | Exact location proximity |
| **4** (Lowest) | Budget Compatibility | 0-15 | Price tier alignment |

### Budget Penalty System
- **More Expensive Than Budget**: -1000 points (automatic disqualification)
- **Exact Price Match**: +15 points
- **Cheaper Than Budget**: -5 points per price tier

### Example
A user in zip code 15213, with budget $$, interested in Night Clubs with LGBT and Adult Club preferences:

```
Venue: Underground Lounge
- LGBT Friendly (Yes):           +50
- Adult Club (Yes):              +50
- Night Club match:              +30
- Zip Code match (15213):        +20
- Price ($$):                    +15
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Score:                     165 points ✓
```

The top 3 venues are returned sorted by total score.

---

## 📊 Data

### CSV Structure
The `plurpgh.csv` file contains venue data with the following columns:

| Column | Example | Description |
|--------|---------|-------------|
| title | "Smoke Stack" | Venue name |
| type | "Bar & grill" | Venue category |
| price | "$$" | Price tier ($ / $$ / $$$) |
| Zip Code | "15213" | Pittsburgh zip code |
| latitude | 40.4425 | GPS latitude |
| longitude | -79.9584 | GPS longitude |
| LGBT + | "1" | LGBT friendly (1=yes, 0=no) |
| Adult Club | "1" | Adult-oriented venue |
| Activity | "0" | Activity focus |
| image_url | "https://..." | Venue image URL |

### Database Schema

The application uses SQLite with the following models:

```
User
  ├── id (primary key)
  ├── username (unique)
  └── password_hash
        └── Results (one-to-many)

Result
  ├── id (primary key)
  ├── user_id (foreign key)
  ├── timestamp
  ├── user_zip
  ├── user_budget
  ├── user_types
  ├── user_prefs
  └── venues_json

Post
  ├── id (primary key)
  ├── user_id (foreign key)
  ├── title
  ├── body
  ├── timestamp
  └── Comments (one-to-many)

Comment
  ├── id (primary key)
  ├── post_id (foreign key)
  ├── user_id (foreign key)
  ├── body
  └── timestamp

ChatMessage
  ├── id (primary key)
  ├── user_id (foreign key)
  ├── body
  └── timestamp
```

---

## 📜 Development History

PLUR PGH has evolved through multiple iterations:

1. **Phase 1: Command-Line Tool** (`plur_pgh.py`)
   - Original Python script with CSV parsing
   - Basic scoring algorithm
   - CLI interface

2. **Phase 2: GUI Application** (`venue_finder_launcher.py`)
   - Tkinter-based graphical interface
   - Popup window for user input
   - Local venue matching

3. **Phase 3: Web Application** (`app.py`)
   - Flask web framework
   - SQLAlchemy database integration
   - User authentication system

4. **Phase 4: Design Enhancement**
   - Cyberpunk/electronic aesthetic
   - Retro 80s/90s visual theme
   - Color-coded venue type system

5. **Phase 5: Feature Expansion**
   - Venue thumbnail images
   - Advanced scoring algorithm
   - Community features (posts, comments)
   - Interactive mapping

6. **Phase 6: Analytics & Visualization**
   - Leaflet map with color-coded markers
   - Bar charts for venue distribution
   - User dashboard with history tracking
   - About page with comprehensive info

---

## 🔧 Configuration

### Secret Key
The Flask app uses a secret key for session management. For production deployment, change:

```python
app.secret_key = 'your-secret-key-here'
```

To a strong, random value.

### Database Location
Database is created at:
```
app.db
```

This is an SQLite database stored in the project root.

### Debug Mode
By default, debug mode is enabled:
```python
app.run(debug=True)
```

For production, set `debug=False`.

---

## 📝 Testing

Test files are included in the project:
- `test_flow.py` - Main application flow testing
- `test_posts_chat.py` - Community features testing
- `Archive/test_scoring.py` - Scoring algorithm validation

Run tests:
```bash
python test_flow.py
python test_posts_chat.py
```

---

## 🎮 Example Workflow

1. **Start the server**
   ```bash
   python app.py
   ```

2. **Open browser** to `http://127.0.0.1:5000`

3. **Register** a new account
   - Username: `evan`
   - Password: `password123`

4. **Complete the quiz**
   - Zip Code: `15213`
   - Budget: `$$`
   - Types: Night Club, Live Music
   - Preferences: LGBT +, Activity

5. **View results**
   - Get top 3 personalized venue matches
   - See detailed venue cards with images

6. **Explore**
   - Visit the interactive map on the About page
   - Check out venue statistics
   - Browse community posts
   - View your search history on Dashboard

---

## 🌐 Key Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| Flask | >=2.0 | Web framework and routing |
| Flask-SQLAlchemy | >=3.0 | Database ORM |
| Werkzeug | >=2.0 | Security utilities |
| Jinja2 | (included) | Template rendering |
| Leaflet.js | 1.9.4 | Interactive mapping |
| Chart.js | Latest | Data visualization |
| Google Fonts | N/A | Press Start 2P font |

---

## 🎨 Design Philosophy

PLUR PGH embraces a retro-electronic, cyberpunk aesthetic:

- **Color Scheme**: Lime green (#8ACE00) on pure black (#000000)
- **Typography**: Press Start 2P for headings, Courier New for body
- **Visual Elements**: CRT monitor borders, pixel-perfect styling
- **Interactions**: Glowing effects, sharp angles, neon-inspired shadows
- **Theme**: 80s/90s electronic music culture meets modern web tech

---

## 📮 Features Wishlist

Potential future enhancements:
- [ ] Real-time chat with WebSockets
- [ ] User ratings and reviews system
- [ ] Venue photo gallery
- [ ] Event calendar integration
- [ ] Social media sharing
- [ ] Advanced filtering options
- [ ] Mobile app version
- [ ] User recommendations algorithm
- [ ] Venue analytics for owners
- [ ] API for third-party integration

---

## 📄 License

This project is created for personal/educational purposes.

---

## 👨‍💻 Author

Created as a portfolio project showcasing:
- Full-stack web development
- Database design and ORM usage
- Algorithm development (scoring system)
- UI/UX design with retro aesthetic
- Community feature implementation

---

## 🚀 Quick Start Checklist

- [ ] Python 3.7+ installed
- [ ] `requirements.txt` dependencies installed
- [ ] `plurpgh.csv` file present in project root
- [ ] Run `python app.py`
- [ ] Open `http://127.0.0.1:5000` in browser
- [ ] Register a new account
- [ ] Take the quiz and get venue recommendations
- [ ] Explore all features!

---

## 💡 Tips & Tricks

1. **Map Navigation**: Use the interactive map to explore venue locations visually
2. **Preferences Matter**: User preferences are weighted highest in the scoring (50 pts each)
3. **Budget Matters**: Expensive venues for budget users are heavily penalized
4. **Exact Zip Match**: Using your actual Pittsburgh zip code gives an immediate 20-point boost
5. **Save Results**: Sign in to track your search history and revisit past recommendations
6. **Community Posts**: Check community posts for real user experiences and tips

---

For questions or issues, check the About page in the application for detailed technical information.

Enjoy discovering your perfect Pittsburgh venue! 🎉
