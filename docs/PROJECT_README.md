# Cohort Web Application

A comprehensive platform connecting students, mentors, and institutions in a structured journey of academic and personal excellence through five pillars of holistic development.

**Version:** 1.0.0  
**Status:** Active Development  
**Last Updated:** January 29, 2026

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [User Roles and Permissions](#user-roles-and-permissions)
5. [Five Development Pillars](#five-development-pillars)
6. [Gamification System](#gamification-system)
7. [Key Features](#key-features)
8. [Project Structure](#project-structure)
9. [Installation and Setup](#installation-and-setup)
10. [Running the Application](#running-the-application)
11. [API Documentation](#api-documentation)
12. [Testing Guide](#testing-guide)
13. [Deployment](#deployment)
14. [Security Features](#security-features)
15. [Communication Systems](#communication-systems)
16. [Contributing](#contributing)

---

## Project Overview

Cohort Web Application is a unified platform designed to track and manage student development across multiple dimensions. It provides a complete ecosystem for students, mentors, floor/wing representatives, and administrators to collaborate effectively.

### Purpose

- Track and manage student development across five pillars of holistic growth
- Connect students with mentors for personalized guidance
- Monitor institutional performance with real-time dashboards
- Facilitate communication between all stakeholders
- Analyze progress with comprehensive analytics and gamification

### Key Highlights

- Multi-role authentication system (Student, Mentor, Floor Wing, Admin)
- Five-pillar development tracking (CLT, SRI, CFC, IIPC, SCD)
- Campus and floor-based hierarchical organization
- Real-time notifications and messaging
- Comprehensive analytics and reporting
- Hackathon registration and tracking with countdown reminders
- LeetCode profile integration with automated streak tracking
- Season-based gamification system with 1500-point scoring
- Professional development logging

---

## System Architecture

### Component Architecture

```
CLIENT LAYER (React 19.2.0)
├── Student UI
├── Mentor UI
├── Floor Wing UI
└── Admin UI
    ↓
API GATEWAY (Django REST Framework)
├── JWT Authentication
├── CORS Handling
├── Rate Limiting
└── API Documentation
    ↓
BACKEND SERVICES (Django 4.2.7)
├── Main Backend (Pillars, Profiles)
├── Admin Backend (Management)
├── Mentor Backend (Reviews)
└── Communication Services
    ↓
DATABASE LAYER (PostgreSQL)
├── Users & Profiles
├── Submissions & Reviews
├── Analytics & Statistics
└── Gamification & Logs
```

### Data Flow

1. **User Authentication** → JWT token generation → Role-based route access
2. **Student Submission** → Validation → File upload → Status tracking → Mentor review
3. **Mentor Review** → Submission evaluation → Status update → Student notification
4. **Analytics** → Data aggregation → Cache layer → Real-time dashboard updates

---

## Technology Stack

### Frontend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 19.2.0 | UI Framework |
| Vite | 7.2.4 | Build tool and dev server |
| React Router DOM | 6.20.0 | Client-side routing |
| Framer Motion | 11.15.0 | Animations |
| GSAP | 3.14.2 | Advanced animations |
| Three.js | 0.181.0 | 3D graphics |
| Lucide React | 0.559.0 | Icon library |
| Recharts | 3.5.1 | Data visualization |
| Zustand | 5.0.9 | State management |
| Axios | 1.13.2 | HTTP client |

### Backend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Django | 4.2.7 | Web framework |
| Django REST Framework | 3.14.0 | API framework |
| djangorestframework-simplejwt | 5.3.0 | JWT authentication |
| PostgreSQL | psycopg2-binary 2.9.9 | Database |
| Pillow | 10.1.0 | Image processing |
| django-cors-headers | 4.3.1 | CORS handling |
| python-dotenv | 1.0.0 | Environment variables |
| cryptography | 41.0.7 | Security utilities |
| argon2-cffi | 23.1.0 | Password hashing |
| gunicorn | 21.2.0 | Production server |
| whitenoise | 6.6.0 | Static file serving |

---

## User Roles and Permissions

### 1. Student

**Access Level:** Basic  
**Primary Dashboard:** Student Home

**Permissions:**
- View personal dashboard with progress tracking
- Submit activities across all five pillars
- Upload certificates and evidence files
- View submission status and mentor feedback
- Register for hackathons and competitions
- Manage LinkedIn profile verification
- Receive notifications from mentors and floor wing
- View floor announcements
- Track personal analytics and progress

**Restricted From:**
- Viewing other students' submissions
- Accessing mentor/admin dashboards
- Modifying system settings

### 2. Mentor

**Access Level:** Intermediate  
**Primary Dashboard:** Mentor Dashboard

**Permissions:**
- View assigned students list
- Review and approve/reject submissions
- Provide feedback on student work
- Track student progress across pillars
- Send messages to students (General, Completion, Pending Review)
- Access student analytics
- View month-wise submission history
- Generate mentor reports

**Restricted From:**
- Accessing admin functions
- Viewing unassigned students outside scope
- Modifying system configurations

### 3. Floor Wing Representative

**Access Level:** Floor-Level Management  
**Primary Dashboard:** Floor Wing Dashboard

**Permissions:**
- View all students on assigned floor
- Monitor floor-level statistics
- Create and manage floor announcements
- Assign students to mentors (individual and bulk)
- View mentor workload analytics
- Track floor-wide pillar progress
- Manage student assignments
- View floor-specific reports

**Data Scope:** Strictly limited to assigned campus and floor

**Restricted From:**
- Accessing other floors or campuses
- Admin system configurations
- Direct submission review

### 4. Administrator

**Access Level:** Full System Access  
**Primary Dashboard:** Admin Campus Selection to Floor Management

**Permissions:**
- Full access to all campuses and floors
- Student profile management
- Mentor assignment and management
- Floor and wing representative management
- System-wide analytics and reporting
- Communication center access
- Leaderboard management
- System configuration
- User role management
- Database administration

---

## Five Development Pillars

### 1. CLT (Continuous Learning Track)

**Purpose:** Track continuous learning and skill development through online courses

**Features:**
- Course completion tracking
- Platform integration (Udemy, Coursera, edX, etc.)
- Certificate upload and validation
- Progress monitoring
- Statistics dashboard

**Submission Workflow:**
1. Enter course details (title, platform, description)
2. Upload completion certificate
3. Submit for mentor review
4. Receive approval or feedback
5. Track learning outcomes

**Points:** 100 points per season

### 2. SRI (Social Responsibility Initiative)

**Purpose:** Document social service and community engagement activities

**Features:**
- Event participation tracking
- Impact measurement
- Photo documentation
- Hour logging
- Organization partnerships

**Key Metrics:**
- Hours contributed
- Events participated
- Community impact
- Leadership roles

**Points:** 300 points (outcome-based)

### 3. CFC (Career, Future & Competency)

**Purpose:** Professional development and career preparation

**Features:**
- **Hackathon Management:**
  - Registration system with countdown timers
  - Participation tracking
  - Motivational reminders based on urgency
  - Submission linking with GitHub repos
  - Certificate upload
- **LinkedIn Integration:**
  - Profile verification
  - Post tracking
  - Professional networking documentation

**Sub-components:**
- Business Model Canvas (200 points)
- GenAI Project (200 points)
- Hackathon Participation (200 points)
- Patent/Journal Publication (200 points)

**Total Points:** 800 points per season

### 4. IIPC (Industry Interaction & Professional Connect)

**Purpose:** Industry exposure and professional networking

**Features:**
- Industry visit documentation
- Guest lecture attendance
- Company interaction tracking
- Networking events
- Mentorship programs

**Components:**
- LinkedIn Connect (100 points)
- LinkedIn Post/Article (100 points)

**Total Points:** 200 points per season

### 5. SCD (Self-Code Development)

**Purpose:** Technical skill development and coding practice

**Features:**
- **LeetCode Integration:**
  - Profile linking with username
  - Daily streak tracking (automated)
  - Problem-solving analytics
  - Consistency monitoring

**Implementation:**
- Student links LeetCode username
- Daily cron job syncs streak data via LeetCode GraphQL API
- Full uninterrupted streak = 100 points
- Partial streaks reduce points but don't fail season

**Critical Note:** SCD scoring based ONLY on daily streak verification, NOT problem count

**Points:** 100 points per season

---

## Gamification System

### Core Structure

**System Name:** COHORT GAMIFICATION SYSTEM  
**Type:** Level-Based, Episode-Driven Quest System  
**Scoring:** 1500 Point System per Season

### Season Structure

```
Season (1 Month)
├── Episode 1 (Week 1 - Kickoff)
├── Episode 2 (Week 2 - Build)
├── Episode 3 (Week 3 - Intensity)
└── Episode 4 (Week 4 - Finale)
```

### Episode Distribution

**Episode 1 (Week 1 - Kickoff)**
- CLT: 1 task (course completion)
- SCD: Start daily LeetCode streak

**Episode 2 (Week 2 - Build)**
- CFC: Task 1 (e.g., BMC Video)
- IIPC: Task 1 (e.g., LinkedIn Connect)
- SCD: Continue streak

**Episode 3 (Week 3 - Intensity)**
- CFC: Task 2 (e.g., GenAI Project)
- IIPC: Task 2 (e.g., LinkedIn Post)
- SCD: Continue streak

**Episode 4 (Week 4 - Finale)**
- CFC: Task 3 (e.g., Hackathon)
- SRI: 1 task (social responsibility)
- SCD: Full-month streak completion

**Rules:**
- Episode N unlocks ONLY after Episode N-1 is completed
- Episode completion requires mentor approval of ALL tasks
- Partial season completion = NO score, NO leaderboard, NO vault credits

### Scoring System

| Pillar | Max Points | Components |
|--------|-----------|------------|
| CLT | 100 | AI Certification |
| IIPC | 200 | LinkedIn Connect (100) + Post/Article (100) |
| SCD | 100 | Daily LeetCode streak (full month) |
| CFC | 800 | BMC (200) + GenAI (200) + Hackathon (200) + Patent (200) |
| Outcome | 300 | Internship/Placement >= 10 LPA |
| **TOTAL** | **1500** | **Season Maximum** |

### Score Types

**1. Season Score**
- Monthly performance (max 1500)
- Resets every season
- Calculated ONLY after full season completion

**2. Legacy Score**
- Lifetime cumulative score
- NEVER resets
- Includes: Season Scores + Ascension Bonus + Achievements

**3. Vault Credits**
- Redeemable currency
- Earned ONLY after full season completion
- Formula: Season Score ÷ 10 = Credits
- Used for: Titles, OD/WFH, Tech tools
- Spending does NOT reduce Legacy Score

### Ascension Bonus

**Value:** +5 Legacy Score points  
**Rule:** If Current Season Score > Previous Season Score → Add +5 to Legacy Score

- No penalty for score decrease
- Applies ONLY after full season completion
- Encourages self-improvement over peer competition

### Leaderboard (Champions Podium)

**Public Display (Top 3 Only):**
- Rank 1: Season Champion
- Rank 2 & 3: Elite Runners

**Private View (For Others):**
- Season Score
- Legacy Score
- Vault Credits
- Percentile Bracket (Top 10%, 25%, 50%, Below 50%)

**Note:** Only students who completed full season are ranked

### Title System

Students redeem Vault Credits to unlock titles displayed next to their name.

**Sample Titles:**

| Title | Cost | Rarity | Description |
|-------|------|--------|-------------|
| The Consistent | 50 | Rare | Completed all episodes without breaking streak |
| The Ascender | 100 | Epic | Ascension Bonus in 3 consecutive seasons |
| The Finisher | 30 | Common | First season 100% completion |
| The Quality Champion | 150 | Legendary | Season Score above 1400 |
| Code Warrior | 80 | Epic | Perfect LeetCode streak |
| Season Champion | 200 | Legendary | Achieved Rank 1 |

---

## Key Features

### Student Features

- Personal dashboard with progress tracking
- Submit activities across five pillars (CLT, SRI, CFC, IIPC, SCD)
- Visual progress indicators and analytics
- Hackathon registration with countdown reminders
- Professional development logging
- LinkedIn profile and post verification
- Responsive design for mobile access
- Real-time notifications from mentors
- Floor announcements with read tracking

### Mentor Features

- Student list management
- Submission review and approval system
- Pillar-wise progress tracking
- Direct messaging with students (3 message types)
- Performance analytics
- Month-wise submission reviews
- Mentor dashboard with statistics

### Floor Wing Features

**Enhanced Dashboard (4 Tabs):**

**Tab 1: Dashboard Overview**
- 6 live stats cards (total students, active mentors, assigned/unassigned, avg completion, pending reviews)
- Pillar progress overview (CLT, CFC, SRI, IIPC, SCD)
- Mentor workload visualization with status indicators
- Animated hover effects

**Tab 2: Student Management**
- Filter system (All, Unassigned, At Risk, Low Progress)
- Real-time search functionality
- Bulk selection with checkboxes
- Bulk mentor assignment
- Status badges (On Track, At Risk, Moderate)
- Individual progress bars
- Student detail drawer

**Tab 3: Mentor Overview**
- Mentor list with workload status
- Student count per mentor
- Pending review statistics
- Approval rates
- Last active tracking

**Tab 4: Announcements**
- Create floor-scoped announcements
- Priority levels (Normal, Important, Urgent)
- Status management (Draft, Published, Expired)
- Expiry date setting
- Read tracking per student
- Read statistics display
- CRUD operations
- Strict campus + floor data isolation

### Admin Features

- Institutional dashboard
- Campus selection interface
- Floor management per campus
- Student profile management
- Mentor assignment and management
- Floor and wing management
- Comprehensive analytics and reporting
- Communication center
- Leaderboard system
- System configuration

---

## Project Structure

```
cohort/
├── backend/                      # Django Backend
│   ├── apps/                     # Django Applications
│   │   ├── profiles/            # User profiles, floor wing features
│   │   ├── clt/                 # Continuous Learning Track
│   │   ├── sri/                 # Social Responsibility Initiative
│   │   ├── cfc/                 # Career, Future & Competency
│   │   ├── iipc/                # Industry Interaction
│   │   ├── scd/                 # Self-Code Development
│   │   ├── hackathons/          # Hackathon Management
│   │   ├── gamification/        # Gamification Engine
│   │   └── dashboard/           # Analytics Dashboard
│   │
│   ├── config/                  # Django Configuration
│   │   ├── settings.py          # Main settings
│   │   ├── urls.py              # URL routing
│   │   ├── wsgi.py              # WSGI config
│   │   └── asgi.py              # ASGI config
│   │
│   ├── media/                   # User Uploaded Files
│   │   ├── certificates/        # Course certificates
│   │   ├── submissions/         # Submission files
│   │   └── profiles/            # Profile pictures
│   │
│   ├── static/                  # Static Files
│   ├── manage.py                # Django CLI
│   ├── requirements.txt         # Python dependencies
│   └── README.md                # Backend documentation
│
├── src/                         # React Frontend
│   ├── assets/                  # Static Assets
│   │   ├── images/
│   │   ├── fonts/
│   │   └── icons/
│   │
│   ├── components/              # Reusable Components
│   │   ├── Button.jsx
│   │   ├── GlassCard.jsx
│   │   ├── Input.jsx
│   │   ├── ProgressBar.jsx
│   │   ├── ProtectedRoute.jsx
│   │   ├── ThemeToggle.jsx
│   │   ├── Navigation.jsx
│   │   ├── HackathonRegistrationModal.jsx
│   │   ├── UpcomingHackathonsWidget.jsx
│   │   └── admin/               # Admin components
│   │
│   ├── context/                 # React Context
│   │   └── AuthContext.jsx      # Authentication state
│   │
│   ├── pages/                   # Page Components
│   │   ├── Login.jsx            # Login page
│   │   ├── ParallaxIntro.jsx    # Landing page
│   │   │
│   │   ├── student/             # Student Pages
│   │   │   ├── Home.jsx         # Student dashboard
│   │   │   ├── CLT.jsx          # Learning track
│   │   │   ├── SRI.jsx          # Social responsibility
│   │   │   ├── CFC.jsx          # Career & competency
│   │   │   ├── IIPC.jsx         # Industry interaction
│   │   │   ├── SCD.jsx          # Code development
│   │   │   ├── Hackathons.jsx   # Hackathon registration
│   │   │   ├── MonthlyReport.jsx
│   │   │   └── ProfileSettings.jsx
│   │   │
│   │   ├── mentor/              # Mentor Pages
│   │   │   ├── MentorLayout.jsx
│   │   │   ├── MentorHome.jsx
│   │   │   ├── MentorDashboard.jsx
│   │   │   ├── SubmissionReview.jsx
│   │   │   └── PillarReview.jsx
│   │   │
│   │   ├── floorwing/           # Floor Wing Pages
│   │   │   ├── FloorWingDashboard.jsx
│   │   │   └── FloorWingDashboard.css
│   │   │
│   │   └── admin/               # Admin Pages
│   │       ├── AdminLayout.jsx
│   │       ├── AdminDashboard.jsx
│   │       ├── CampusSelect.jsx
│   │       ├── CampusDetail.jsx
│   │       └── FloorDetail.jsx
│   │
│   ├── services/                # API Services
│   │   ├── api.js               # Base API configuration
│   │   ├── auth.js              # Authentication
│   │   ├── clt.js               # CLT pillar
│   │   ├── sri.js               # SRI pillar
│   │   ├── cfc.js               # CFC pillar
│   │   ├── iipc.js              # IIPC pillar
│   │   ├── scd.js               # SCD pillar
│   │   ├── messageService.js    # Messaging
│   │   ├── adminService.js      # Admin operations
│   │   └── announcement.js      # Announcements
│   │
│   ├── store/                   # State Management
│   │   └── adminStore.js        # Admin state (Zustand)
│   │
│   ├── theme/                   # Theming
│   │   ├── theme.js
│   │   └── ThemeContext.jsx
│   │
│   ├── App.jsx                  # Main app component
│   ├── main.jsx                 # Entry point
│   └── index.css                # Global styles
│
├── public/                      # Public Assets
│   └── index.html
│
├── tests/                       # Test Files
│
├── Documentation Files          # 34 markdown files
├── package.json                 # Node dependencies
├── vite.config.js              # Vite configuration
├── eslint.config.js            # ESLint rules
├── pytest.ini                  # Pytest configuration
└── README.md                    # This file
```

---

## Installation and Setup

### Prerequisites

- **Node.js** 18.x or higher
- **Python** 3.10 or higher
- **PostgreSQL** 14.x or higher
- **Git**

### Clone Repository

```bash
git clone <repository-url>
cd cohort
```

### Frontend Setup

```bash
# Install dependencies
npm install

# Create .env file for frontend
# Windows PowerShell:
@"
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_LINKEDIN_CLIENT_ID=your_linkedin_client_id
VITE_LINKEDIN_REDIRECT_URI=http://localhost:5173/iipc/callback
"@ | Out-File -FilePath .env -Encoding utf8

# Linux/Mac:
cat > .env << EOF
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_LINKEDIN_CLIENT_ID=your_linkedin_client_id
VITE_LINKEDIN_REDIRECT_URI=http://localhost:5173/iipc/callback
EOF
```

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file for backend
# Update with your actual values
DEBUG=True
SECRET_KEY=your-secret-key-here-minimum-50-characters-long
DATABASE_NAME=cohort_db
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174
JWT_SECRET_KEY=your-jwt-secret-key-minimum-50-characters
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

### Database Setup

```bash
# Create PostgreSQL database
psql -U postgres

# In PostgreSQL shell:
CREATE DATABASE cohort_db;
CREATE USER your_db_user WITH PASSWORD 'your_db_password';
ALTER ROLE your_db_user SET client_encoding TO 'utf8';
ALTER ROLE your_db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_db_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE cohort_db TO your_db_user;
\q
```

### Run Migrations

```bash
# Still in backend directory with virtual environment activated
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Create Test Users (Optional)

```bash
# Create role-based test users
python create_role_users.py

# Or create basic test users
python create_test_users.py
```

### Setup Gamification (Optional)

```bash
# Create sample titles
python manage.py create_sample_titles

# Setup cron job for LeetCode sync (runs daily at midnight)
# Windows Task Scheduler or Linux crontab:
0 0 * * * cd /path/to/backend && python manage.py sync_leetcode_streaks
```

---

## Running the Application

### Development Mode

**Terminal 1 - Frontend:**
```bash
# From project root directory
npm run dev
# Frontend runs on http://localhost:5173 or http://localhost:5174
```

**Terminal 2 - Backend:**
```bash
cd backend
# Activate virtual environment
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac

# Run Django development server
python manage.py runserver
# Backend runs on http://127.0.0.1:8000
```

### Access Points

- **Frontend Application:** http://localhost:5174
- **Backend API:** http://127.0.0.1:8000/api/
- **Django Admin:** http://127.0.0.1:8000/admin/
- **API Documentation (Swagger):** http://127.0.0.1:8000/api/docs/
- **API Documentation (ReDoc):** http://127.0.0.1:8000/api/redoc/

### Test Credentials

**Student:**
- Email: `student@test.com`
- Password: `student123`

**Mentor:**
- Email: `mentor@test.com`
- Password: `mentor123`

**Floor Wing:**
- Email: `fw.tech.floor1@college.edu`
- Password: `Test123!`

**Admin:**
- Email: `admin@college.edu`
- Password: `Test123!`

---

## API Documentation

### Authentication Endpoints

```
POST /api/auth/token/              # Get JWT tokens
POST /api/auth/token/refresh/      # Refresh access token
POST /api/auth/register/           # Register new user
```

### Profile Endpoints

```
GET    /api/profiles/me/           # Get current user profile
PATCH  /api/profiles/me/           # Update current user profile
```

### CLT (Continuous Learning Track) Endpoints

```
GET    /api/clt/submissions/                    # List all submissions
POST   /api/clt/submissions/                    # Create new submission
GET    /api/clt/submissions/{id}/               # Get submission details
PATCH  /api/clt/submissions/{id}/               # Update submission
DELETE /api/clt/submissions/{id}/               # Delete submission
POST   /api/clt/submissions/{id}/upload_files/  # Upload files
POST   /api/clt/submissions/{id}/submit/        # Submit for review
DELETE /api/clt/submissions/{id}/delete_file/   # Delete file
GET    /api/clt/submissions/stats/              # Get statistics
```

### CFC (Career, Future & Competency) Endpoints

```
GET    /api/cfc/hackathon-registrations/                # List registrations
POST   /api/cfc/hackathon-registrations/                # Register hackathon
GET    /api/cfc/hackathon-registrations/upcoming/       # Get upcoming
POST   /api/cfc/hackathon-registrations/{id}/mark_completed/     # Mark complete
POST   /api/cfc/hackathon-registrations/{id}/create_submission/  # Create submission
PUT    /api/cfc/hackathon-registrations/{id}/           # Update registration
DELETE /api/cfc/hackathon-registrations/{id}/           # Delete registration
```

### Floor Wing Endpoints

```
GET  /api/profiles/floor-wing/dashboard/        # Dashboard stats
GET  /api/profiles/floor-wing/students/         # List students
POST /api/profiles/floor-wing/assign-mentor/    # Assign mentor
GET  /api/profiles/floor-wing/mentors/          # List mentors
```

### Announcement Endpoints

**Floor Wing:**
```
GET    /api/profiles/floor-wing/announcements/       # List announcements
POST   /api/profiles/floor-wing/announcements/       # Create announcement
GET    /api/profiles/floor-wing/announcements/stats/ # Get statistics
PATCH  /api/profiles/floor-wing/announcements/{id}/  # Update announcement
DELETE /api/profiles/floor-wing/announcements/{id}/  # Delete announcement
```

**Student:**
```
GET  /api/profiles/student/announcements/              # List announcements
POST /api/profiles/student/announcements/{id}/mark_read/  # Mark as read
GET  /api/profiles/student/announcements/unread_count/    # Get unread count
```

### Messaging Endpoints

```
GET  /api/communication/messages/               # List messages
POST /api/communication/messages/               # Send message
GET  /api/communication/messages/unread/        # Get unread messages
POST /api/communication/messages/{id}/mark_read/  # Mark message as read
POST /api/communication/messages/mark_all_read/   # Mark all as read
```

### Gamification Endpoints

```
GET  /api/gamification/seasons/                 # List seasons
GET  /api/gamification/seasons/current/         # Get current season
GET  /api/gamification/episodes/                # List episodes
GET  /api/gamification/leaderboard/             # Get leaderboard
GET  /api/gamification/student-progress/        # Get student progress
```

---

## Testing Guide

### Running Tests

**Frontend Tests:**
```bash
npm run test
```

**Backend Tests:**
```bash
cd backend
python manage.py test
```

**End-to-End Tests:**
```bash
python run_tests.py
```

### Manual Testing Flow

#### 1. Admin Flow

1. Login as admin at http://localhost:5174/login
2. Navigate to campus selection screen
3. Select Technology Campus
4. View floor cards (Floors 1-4)
5. Click Floor 1 to view details
6. Test Students, Mentors, and Floor Wing tabs
7. Verify data displays correctly

#### 2. Floor Wing Flow

1. Login as floor wing representative
2. View dashboard with 4 tabs
3. Test Dashboard tab (stats, pillar progress, mentor workload)
4. Test Students tab (filtering, search, bulk assignment)
5. Test Mentors tab (list with statistics)
6. Test Announcements tab (create, edit, delete)
7. Create announcement and verify it appears for students

#### 3. Mentor Flow

1. Login as mentor
2. View assigned students list
3. Click on a student to view details
4. Navigate to submission review
5. Approve/reject a submission with feedback
6. Send message to student (General/Completion/Pending)
7. View student analytics

#### 4. Student Flow

1. Login as student
2. View home dashboard with progress tracking
3. Check upcoming hackathons widget
4. Navigate to CLT page
5. Create new course submission
6. Upload certificate file
7. Submit for review
8. Check notifications for mentor messages
9. View floor announcements
10. Register for a hackathon in CFC page
11. Return to home and verify countdown reminder appears

### Test Data Creation

**Create Test Users:**
```bash
cd backend
python create_test_users.py
```

**Create E2E Test Users:**
```bash
python create_e2e_test_users.py
```

**Import Dummy Students:**
```bash
python import_dummy_users.py
```

---

## Deployment

### Recommended Deployment Setup

**Backend:** Render (with PostgreSQL)  
**Frontend:** Vercel  
**Estimated Cost:** $10-15/month for PostgreSQL

### Backend Deployment (Render)

1. Push code to GitHub repository
2. Create New Web Service on Render
3. Connect GitHub repository
4. Configure build settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn config.wsgi:application`
5. Create PostgreSQL database on Render
6. Add environment variables
7. Deploy and run migrations

### Frontend Deployment (Vercel)

1. Connect GitHub repository to Vercel
2. Configure project:
   - **Framework Preset:** Vite
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
3. Add environment variable:
   - `VITE_API_URL` = Backend URL
4. Deploy

### Environment Variables

**Backend (.env):**
```
SECRET_KEY=<50-character-random-string>
DEBUG=False
ALLOWED_HOSTS=.onrender.com,your-frontend-domain.vercel.app
DATABASE_URL=<postgres-url>
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
JWT_SECRET_KEY=<50-character-random-string>
JWT_ALGORITHM=HS256
```

**Frontend (.env.production):**
```
VITE_API_URL=https://your-backend.onrender.com/api
```

### Post-Deployment Steps

1. Run database migrations
2. Create superuser account
3. Create test users and roles
4. Setup gamification system
5. Configure LeetCode sync cron job
6. Test all API endpoints
7. Verify CORS configuration
8. Test file upload functionality

---

## Security Features

### Authentication and Authorization

- JWT token-based authentication
- Token refresh mechanism
- Role-based access control (RBAC)
- Password hashing with Argon2
- Session management

### Data Protection

- CORS protection configured
- CSRF protection enabled
- Rate limiting on API endpoints
- SQL injection prevention (Django ORM)
- XSS protection
- Input validation and sanitization

### Access Control

- Strict data isolation by campus and floor
- Permission classes for all endpoints
- User-scoped queries (students see only their data)
- Floor Wing data restricted to assigned floor
- Admin access logging

### File Upload Security

- File type validation (PDF, images only)
- File size limits (10MB max per file)
- Secure file storage
- Virus scanning recommended for production

---

## Communication Systems

### Mentor-Student Chat

**Features:**
- Three message types: General, Completion, Pending Review
- Real-time notifications on student home page
- Auto-refresh every 30 seconds
- Mark as read functionality
- Message history tracking

**API Endpoints:**
```
POST /api/communication/messages/
GET  /api/communication/messages/
GET  /api/communication/messages/unread/
POST /api/communication/messages/{id}/mark_read/
```

### Floor Announcements

**Features:**
- Priority levels: Normal, Important, Urgent
- Status management: Draft, Published, Expired
- Expiry date configuration
- Read tracking per student
- Read statistics display
- Strict campus + floor data scoping

**Priority Color Coding:**
- Normal: Blue
- Important: Orange
- Urgent: Red

**API Endpoints:**
```
# Floor Wing
POST   /api/profiles/floor-wing/announcements/
GET    /api/profiles/floor-wing/announcements/
PATCH  /api/profiles/floor-wing/announcements/{id}/
DELETE /api/profiles/floor-wing/announcements/{id}/

# Student
GET  /api/profiles/student/announcements/
POST /api/profiles/student/announcements/{id}/mark_read/
```

---

## Contributing

### Development Workflow

1. Always work in feature branches, never push directly to `main`
2. Create descriptive branch names (e.g., `feature/hackathon-reminders`)
3. Write clear commit messages
4. Test thoroughly before pushing
5. Create pull requests for review
6. Update documentation for new features

### Code Standards

**Frontend (React):**
- Use functional components with hooks
- Follow ESLint configuration
- Use meaningful variable names
- Add comments for complex logic
- Keep components modular and reusable

**Backend (Django):**
- Follow PEP 8 style guide
- Write docstrings for all functions
- Use Django best practices
- Add proper validation and error handling
- Write unit tests for new features

### Testing Requirements

- Write unit tests for all new features
- Ensure all existing tests pass
- Test edge cases and error conditions
- Verify API endpoints with Swagger
- Test cross-browser compatibility

### Documentation

- Update README.md for major changes
- Document new API endpoints
- Add comments for complex code
- Update environment variable documentation
- Create user guides for new features

---

## Troubleshooting

### Common Issues

**CORS Errors:**
- Verify `CORS_ALLOWED_ORIGINS` in backend settings
- Check frontend is using correct API URL
- Ensure no trailing slashes in URLs

**Authentication Errors:**
- Check JWT tokens are stored in localStorage
- Verify token is sent in Authorization header
- Test login at Django admin panel

**File Upload Errors:**
- Maximum file size: 10MB per file
- Maximum files per request: 10 files
- Allowed types: PDF, images (PNG, JPG, JPEG)

**Database Errors:**
- Verify PostgreSQL is running
- Check database credentials in .env
- Ensure migrations are up to date

**Frontend Build Errors:**
- Clear node_modules and reinstall: `npm install`
- Clear Vite cache: `npm run clean`
- Check Node.js version compatibility

### Getting Help

- Check documentation files in the repository
- Review API documentation at `/api/docs/`
- Check Django admin panel for data verification
- Review browser console for frontend errors
- Check Django server logs for backend errors

---

## License

This project is proprietary and confidential. All rights reserved.

---

## Contact and Support

For questions, issues, or contributions, please contact the development team.

**Project Maintainers:**
- Backend Development Team
- Frontend Development Team
- DevOps Team

**Last Updated:** January 29, 2026  
**Version:** 1.0.0
