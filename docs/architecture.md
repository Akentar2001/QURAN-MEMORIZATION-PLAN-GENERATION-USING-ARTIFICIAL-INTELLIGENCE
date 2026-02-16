# HIFZ-AI System Architecture

## Overview
This document describes the system architecture for HIFZ-AI - an intelligent, personalized Quran memorization system using AI and machine learning.

## 1. Technology Stack

### 1.1 Backend Framework
**Choice:** Django (Python)

**Justification:**
- Mature ecosystem with robust ORM (Django ORM) for efficient database operations
- Excellent Admin Panel and data management capabilities through Django Admin
- Strong community support and extensive third-party packages
- Non-blocking I/O (ideal for ML model serving and real-time predictions)
- RESTful API development is straightforward and well-documented
- Support for complex query operations needed for analytics and reporting

**Alternatives Considered:**
- Node.js (Express.js) - Mature ecosystem, but Django's ORM is superior for complex data relationships
- Python (Django/FastAPI) - Good, but Django includes Admin Panel which is critical for institutions

---

### 1.2 Frontend Framework
**Choice:** React.js

**Justification:**
- Component-based architecture (reusable UI components) accelerates development
- Large ecosystem and extensive third-party library support
- Excellent state management (Redux/Context API) for complex application state
- Strong testing infrastructure (Jest, React Testing Library) ensures code quality
- Virtual DOM enables efficient client-side rendering
- Good for responsive, mobile-first design required for student/parent access
- Mature development patterns and best practices

**Alternatives Considered:**
- Vue.js - Good, but React has larger ecosystem and better documentation
- Svelte - Fast, but smaller ecosystem and fewer learning resources
- Angular - Too opinionated with steep learning curve

---

### 1.3 Database
**Choice:** PostgreSQL

**Justification:**
- ACID compliance (critical for student progress data integrity)
- Strong performance for complex queries required by ML analytics
- Support for JSONB (for storing ML model outputs like difficulty scores)
- Excellent full-text search capabilities (for Quran verse lookup with Arabic)
- Mature and battle-tested with proven reliability and strong replication/backup support
- Relational model fits user, progress, plans, and Quran data naturally

**Alternatives Considered:**
- MongoDB - Flexible, but less structured query capabilities needed for complex analytics
- MySQL - Good, but PostgreSQL has superior advanced features and better performance for concurrent operations
- SQLite - Lightweight, but not suitable for production scale with 1000+ students

---

### 1.4 ML Framework
**Choice:** Scikit-learn (Python)

**Justification:**
- Excellent support for traditional machine learning algorithms including Spaced Repetition (SM-2, SM-5, etc.)
- Comprehensive implementation of Adaptive Scheduling algorithms needed for revision optimization
- Predictive Analytics capabilities for retention prediction and student performance forecasting
- Strong Decision Support functionality (e.g., Random Forest, Gradient Boosting) for recommending optimal memorization pace
- Integration with pandas, numpy for data preprocessing and feature engineering
- Extensive documentation and active community support
- Production-ready and widely used in industry

**Alternatives Considered:**
- PyTorch - Excellent for deep learning and RNN/LSTM, but overkill for adaptive scheduling
- TensorFlow - Mature, but Scikit-learn is more accessible and has better traditional ML support
- XGBoost - Excellent for gradient boosting, but Scikit-learn already includes it

---

## 2. System Architecture

### 2.1 High-Level Design
**Architecture Pattern:** Layered Microservices

**Layers:**
1. **Presentation Layer** - Frontend web application (React.js)
2. **API Gateway** - RESTful API with authentication, rate limiting, and request routing
3. **Business Logic Layer** - Core microservices (Plan Generation, Progress Tracking, User Management)
4. **Data Access Layer** - PostgreSQL database with connection pooling and transaction management
5. **ML Inference Layer** - Scikit-learn models with Flask/MLFlow integration for adaptive scheduling
6. **Infrastructure Layer** - Docker containers, Nginx load balancer, and Redis caching

**Component Communication:**
- All services communicate via RESTful JSON APIs
- Async communication using message queue (RabbitMQ or Redis) for non-blocking ML inference
- Circuit breaker pattern for fault tolerance and graceful degradation
- Service discovery for dynamic scaling

---

### 2.2 API Structure

#### RESTful Endpoints

**Authentication:**
- `POST /api/v1/auth/register` - User registration with role assignment
- `POST /api/v1/auth/login` - User authentication with JWT token generation
- `POST /api/v1/auth/logout` - JWT token invalidation

**User Management:**
- `GET /api/v1/users/:id` - Get user profile and preferences
- `PUT /api/v1/users/:id` - Update user profile and settings
- `GET /api/v1/users/:id/progress` - Get user progress summary and statistics
- `GET /api/v1/users/:id/preferences` - Get learning preferences (time availability, goals)

**Plan Generation (Core Feature):**
- `POST /api/v1/plans/generate` - Generate personalized memorization plan
- `GET /api/v1/plans/:userId/active` - Get active plan for current period
- `PUT /api/v1/plans/:id/adjust` - Manually adjust plan (teacher/student override)
- `POST /api/v1/plans/:id/feedback` - Submit practice performance feedback

**Progress Tracking:**
- `POST /api/v1/progress/record` - Record practice session (verses, time, mistakes)
- `GET /api/v1/progress/:userId/history` - Get progress history with pagination
- `GET /api/v1/progress/:userId/analytics` - Get performance analytics and trends
- `GET /api/v1/progress/:userId/streak` - Get current streak and consistency metrics

**Quran Data:**
- `GET /api/v1/quran/surahs` - List all Surahs with metadata (verse count, place of revelation)
- `GET /api/v1/quran/verses/:surahId` - Get verses in a Surah with details
- `GET /api/v1/quran/verses/:surahId/:verseId` - Get specific verse with Tajweed rules and difficulty
- `GET /api/v1/quran/juz` - List all Juz (30 equal parts of Quran)
- `GET /api/v1/quran/search` - Full-text search across all Quran

**Institutional:**
- `POST /api/v1/institutions/classes` - Create class/group
- `GET /api/v1/institutions/:id/analytics` - Get class-level analytics and performance
- `GET /api/v1/institutions/:id/reports` - Generate reports (Student Progress, Class Performance, Institutional Summary)
- `PUT /api/v1/institutions/:id` - Update class settings and teacher assignments

**Admin Panel Internal (Django Admin):**
- User management with role-based access control
- Database backup and restore operations
- System configuration and monitoring
- Bulk operations (student import, class creation)
- Application logs and error tracking

---

### 2.3 Database Schema

#### Core Entities

**Users:**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'teacher', 'parent', 'admin')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    time_availability_minutes INTEGER DEFAULT 60, -- Daily study time available
    language VARCHAR(10) DEFAULT 'ar', -- Preferred language
    timezone VARCHAR(50) DEFAULT 'UTC'
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

**Progress Tracking:**
```sql
CREATE TABLE progress_records (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    record_date DATE NOT NULL,
    ayah_id INTEGER NOT NULL REFERENCES quran_verses(id),
    verses_memorized INTEGER NOT NULL,
    verses_reviewed INTEGER NOT NULL,
    verses_new_to_user INTEGER NOT NULL, -- New verses assigned in plan
    mistakes_count INTEGER NOT NULL,
    confidence_level INTEGER CHECK (confidence_level BETWEEN 1 AND 10),
    time_spent_minutes INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_progress_user_date ON progress_records(user_id, record_date);
CREATE INDEX idx_progress_ayah ON progress_records(ayah_id);
CREATE INDEX idx_progress_date ON progress_records(record_date);
```

**Plans:**
```sql
CREATE TABLE plans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(20) NOT NULL CHECK (type IN ('new_memorization', 'minor_revision', 'major_revision')),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    daily_target_verses INTEGER NOT NULL,
    daily_review_verses INTEGER NOT NULL,
    plan_json JSONB NOT NULL, -- Detailed plan breakdown with metadata
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'paused', 'completed')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_plans_user ON plans(user_id);
CREATE INDEX idx_plans_type ON plans(type);
CREATE INDEX idx_plans_status ON plans(status, start_date);
```

**Quran Verses:**
```sql
CREATE TABLE quran_verses (
    id SERIAL PRIMARY KEY,
    surah_id INTEGER NOT NULL REFERENCES quran_surahs(id),
    verse_number INTEGER NOT NULL,
    arabic_text TEXT NOT NULL,
    translation_en TEXT,
    difficulty_score DECIMAL(5,2), -- From verse_difficulty.csv
    difficulty_level VARCHAR(10) CHECK (difficulty_level IN ('easy', 'medium', 'hard')),
    average_mistakes DECIMAL(5,2), -- Historical mistake rate
    word_count INTEGER,
    tajweed_rules JSONB, -- Tajweed annotations and rules
    juz_number INTEGER,
    page_number INTEGER, -- For Hafs (604 pages)
    madani_surah_id INTEGER REFERENCES quran_surahs(id), -- For alternate recitations

CREATE INDEX idx_quran_verses_surah ON quran_verses(surah_id);
CREATE INDEX idx_quran_verses_verse ON quran_verses(surah_id, verse_number);
CREATE INDEX idx_quran_verses_difficulty ON quran_verses(difficulty_level);
CREATE INDEX idx_quran_verses_juz ON quran_verses(juz_number);
```

**Quran Surahs:**
```sql
CREATE TABLE quran_surahs (
    id SERIAL PRIMARY KEY,
    surah_number INTEGER UNIQUE NOT NULL,
    name_arabic VARCHAR(100) NOT NULL,
    name_english VARCHAR(100),
    verses_count INTEGER NOT NULL,
    place_of_revelation VARCHAR(50), -- Mecca, Madinah, etc.
    rukus_count INTEGER,
    revelation_order INTEGER,
    makki_surah_id INTEGER REFERENCES quran_surahs(id), -- Alternative Surah recitation

CREATE INDEX idx_quran_surahs_number ON quran_surahs(surah_number);
```

**Difficulty Scores (from research):**
```sql
CREATE TABLE verse_difficulty_scores (
    id SERIAL PRIMARY KEY,
    verse_id INTEGER PRIMARY KEY REFERENCES quran_verses(id),
    average_difficulty DECIMAL(10,2) NOT NULL, -- From research data
    source VARCHAR(50) DEFAULT 'graduation_project', -- Research, community votes
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Ayah Data:**
```sql
CREATE TABLE ayahs (
    id SERIAL PRIMARY KEY,
    ayah_number INTEGER UNIQUE NOT NULL,
    surah_id INTEGER NOT NULL REFERENCES quran_surahs(id),
    verse_count INTEGER NOT NULL,
    verses TEXT, -- List of verse numbers in this Ayah
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_ayahs_number ON ayahs(ayah_number);
```

---

### 2.4 ML Model Pipeline

#### 2.4.1 Training Pipeline

**Data Sources:**
- Historical student performance data from PostgreSQL (progress_records table)
- Public Quran datasets (text, audio, Tajweed annotations)
- Verse difficulty data (verse_difficulty_scores.csv with average_difficulty field)
- Synthetic data augmentation for handling edge cases (missed days, irregular practice patterns)

**Preprocessing:**
```python
# Data cleaning and normalization
import pandas as pd
import numpy as np

# Handle missing values
df = df.fillna({'mistakes_count': 0, 'confidence_level': 5})

# Normalize time measurements
df['minutes_per_verse'] = df['time_spent_minutes'] / df['verses_memorized']

# Encode categorical variables
df['difficulty_encoded'] = df['difficulty_level'].map({'easy': 0, 'medium': 1, 'hard': 2})

# Feature engineering: rolling averages
df['rolling_avg_difficulty'] = df.groupby('user_id')['difficulty_score'].rolling(7, min_periods=1).mean()
df['rolling_avg_confidence'] = df.groupby('user_id')['confidence_level'].rolling(7, min_periods=1).mean()
df['rolling_mistake_rate'] = df.groupby('user_id')['mistakes_count'] / df['verses_memorized'].rolling(7, min_periods=1).mean()
```

**Training:**
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# Load preprocessed data
X = df[['difficulty_score', 'difficulty_encoded', 'rolling_avg_difficulty', 
           'rolling_avg_confidence', 'rolling_mistake_rate', 'time_availability']]
y = df['daily_target_verses']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model 1: Predict daily target (baseline)
rf_target = RandomForestRegressor(n_estimators=100, max_depth=10)
rf_target.fit(X_train, y_train)

# Model 2: Difficulty adaptation (personalization)
rf_difficulty = RandomForestRegressor(n_estimators=50, max_depth=15)
rf_difficulty.fit(X_train, y_train)

# Model 3: Predict mistakes (for revision focus)
rf_mistakes = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1)
rf_mistakes.fit(X_train, y_train)

# Model 4: Decision Support (which verses to assign)
from sklearn.tree import DecisionTreeClassifier
X_cls = df[['difficulty_score', 'time_availability']]
y_cls = df['difficulty_level']
dt_cls = DecisionTreeClassifier(max_depth=10)
dt_cls.fit(X_cls, y_cls)

# Evaluate
print(f"Target Model R2: {r2_score(y_test, rf_target.predict(X_test)):.3f}")
print(f"Difficulty Model R2: {r2_score(y_test, rf_difficulty.predict(X_test)):.3f}")

# Save models
joblib.dump(rf_target, 'models/target_model.pkl')
joblib.dump(rf_difficulty, 'models/difficulty_model.pkl')
joblib.dump(rf_mistakes, 'models/mistake_model.pkl')
joblib.dump(dt_cls, 'models/decision_tree.pkl')
```

#### 2.4.2 Real-Time Inference

**API Endpoint:**
- `POST /api/v1/ml/plan` - Generate personalized plan

**Request Body:**
```json
{
  "user_id": 123,
  "recent_performance": [
    {
      "date": "2025-01-09",
      "ayah_id": 4500,
      "verses_memorized": 5,
      "mistakes": 1,
      "confidence_level": 7,
      "time_minutes": 25
    }
  ],
  "time_available_minutes": 60,
  "current_level": "intermediate",
  "preferences": {
    "focus": "accuracy", -- or "speed", "retention"
    "daily_target_range": [3, 8]
  }
}
```

**Response:**
```json
{
  "plan": {
    "type": "new_memorization",
    "daily_target_verses": 5,
    "verses": {
      "new_memorization": ["2:1", "2:2", "2:3", "2:4", "2:5"],
      "revision": []
    },
    "estimated_time_minutes": 45,
    "confidence": 0.82
  },
  "revision_schedule": {
    "type": "spaced_repetition",
    "algorithm": "SM-2",
    "review_items": ["1:128", "1:129"]  -- From yesterday
    "next_review_date": "2025-01-12"
  },
  "personalized_adjustments": {
    "current_difficulty_adjustment": "+0.1", -- Increase difficulty slightly
    "pace_adjustment": "maintain" -- Keep current pace
    "confidence_adjustment": "boost" -- Encourage user (low confidence)
  }
}
```

**Performance Requirements:**
- Inference latency: <2 seconds per request
- Batch processing: Support 1000+ students simultaneously
- Caching: Redis cache hot plans (most requested) to reduce load
- Model loading: <500ms for cold start, <100ms for cached models

#### 2.4.3 Feedback Loop for Continuous Learning

**Data Collection:**
```python
# Automatic collection from API feedback
from datetime import datetime, timedelta

def collect_feedback_data(user_id, days=30):
    """Collect recent performance and update model"""
    records = ProgressRecord.objects.filter(
        user_id=user_id,
        date__gte=datetime.now() - timedelta(days=days)
    ).order_by('-date')
    
    # Aggregate performance
    avg_difficulty = np.mean([r.difficulty_score for r in records])
    avg_confidence = np.mean([r.confidence_level for r in records])
    mistake_rate = sum(r.mistakes_count for r in records) / sum(r.verses_memorized for r in records)
    
    return {
        'avg_difficulty': avg_difficulty,
        'avg_confidence': avg_confidence,
        'mistake_rate': mistake_rate,
        'total_records': len(records)
    }
```

**Model Update Strategy:**
```python
# Incremental vs. Full Retraining
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load existing model
rf_difficulty = joblib.load('models/difficulty_model.pkl')

# New data from last 30 days
new_data = collect_feedback_data(123, days=30)

# Incremental learning (adaptation)
from sklearn.ensemble import AdaBoostClassifier
incremental_model = AdaBoostClassifier(
    estimator=RandomForestClassifier(n_estimators=50),
    n_estimators=10,
    learning_rate=0.1
)

# Full retraining trigger
if len(new_data['total_records']) > 1000:
    # Retrain monthly
    retrain_full_model()
elif len(new_data['total_records']) > 500:
    # Fine-tune weekly
    fine_tune_model(new_data)
else:
    # Use cached model
    return 'cached'
```

**Learning Rate Adaptation:**
```python
# Adaptive scheduling algorithm (Spaced Repetition with difficulty weights)
class AdaptiveScheduler:
    def __init__(self, user_id):
        self.user_id = user_id
        
    def calculate_next_review(self, last_review_date, performance_history):
        """Calculate next review date based on Spaced Repetition (SM-2)"""
        # SM-2 formula: Review(n) = Review(n-1) * n^(1-n)
        # Where n is the repetition number (1 for first review, 2 for second, etc.)
        
        # Get performance history for verses to review
        verse_performance = self.get_verse_performance(last_review_date)
        
        # Adjust spacing based on performance
        if verse_performance['mistake_rate'] < 0.1:
            n = 2  # Good retention, increase spacing
        elif verse_performance['mistake_rate'] < 0.3:
            n = 3  # Acceptable retention, normal spacing
        else:
            n = 1.5  # Poor retention, decrease spacing
        
        from datetime import datetime, timedelta
        days_to_add = int(n * 7)  # SM-2: 7 * n days
        next_date = last_review_date + timedelta(days=days_to_add)
        
        return next_date
```

---

### 2.5 Persona-Specific Components

#### 2.5.1 Student Portal

**Features:**
- **Daily Plan Display:**
  - Current plan type (new memorization, minor revision, major revision)
  - Verses to memorize today (list with links to Quran)
  - Verses to review (with last reviewed date)
  - Time estimate for each section
  - Progress tracker (verses memorized vs. total Quran)
  - Current streak days

- **Progress Dashboard:**
  - Line chart: verses memorized over time
  - Bar chart: performance metrics (accuracy, confidence, pace)
  - Milestone timeline (Surah completions, Juz completions)
  - Comparison: your progress vs. class average
  - Badges and achievements (7-day streak, 30 verses, Juz 1 complete)

- **Practice Session Recording:**
  - Record practice session with start/end time
  - Count mistakes (tap on verse to mark error)
  - Self-reported confidence level (1-10 slider)
  - Timer for each verse (pause/resume/finish)

- **Milestone Celebrations:**
  - Surah completion popup with confetti animation
  - Digital badge/certificate generation
  - Share achievement via link (parent notification option)
  - Progress percentage display (e.g., "23.5% of Quran completed!")

**UI Components:**
- Plan card with progress indicators
- Interactive Quran reader with Ayah breakdown
- Tajweed highlights (simple rules for beginners)
- Navigation by Surah/Juz/verse number

---

#### 2.5.2 Teacher Dashboard

**Features:**
- **Multi-Student List:**
  - Filterable by progress level (at-risk, on-track, excelling)
  - Sortable by name, progress, last activity date
  - Groupable by class

- **Individual Student Details:**
  - Progress summary (verses memorized, accuracy, streak, pace)
  - Performance trends (improving, declining, stable)
  - Recent activity log (last 7 practice sessions)
  - AI-generated recommendations with explanations

- **Plan Adjustment Interface:**
  - One-click adjustment (reduce/increase daily target by 20%)
  - Manual override with justification
  - View recent performance before adjustment
  - Adjustment history log

- **Performance Analytics:**
  - Scatter plot visualization: pace vs. accuracy for all students
  - Grouping by performance (top 20%, middle 60%, bottom 20%)
  - Export comparison data to CSV/Excel
  - Identify outliers (exceptionally fast/slow learners)
  - Statistical summary: average, median, standard deviation

**Alert System:**
- Automatic "at-risk" flag (declining performance, 0 activity 7 days)
- Priority list sorted by severity and duration
- "Last practice" date indicator for each student
- Bulk alert actions: "Send message", "Adjust plan"

---

#### 2.5.3 Admin Panel (Django Admin)

**Features:**
- **User Management:**
  - User CRUD operations (Create, Read, Update, Delete)
  - Role-based access control (RBAC): student, teacher, parent, admin
  - Bulk operations (import students from CSV, export student data)
  - Activity logs and audit trail

- **Class Management:**
  - Class CRUD operations
  - Teacher assignment (assign Teacher X to Class A, Teacher Y to Class B)
  - Student management (add/remove students to classes)
  - Class statistics (total students, average progress)

- **Program-Wide Analytics Dashboard:**
  - Aggregate metrics across all students
    - Total verses memorized, total students, average progress
    - Retention rates (short-term, long-term)
    - Completion rates (started vs. completed)
  - Time-based comparison: this month vs. last month (growth charts)
  - Export reports in multiple formats (PDF, Excel, CSV)
  - Custom KPI configuration and tracking

- **Report Generation:**
  - Student Progress Report: Individual and class-level performance
  - Class Performance Report: Comparison across teachers and classes
  - Institutional Summary Report: Executive summary with key metrics
  - Custom date range selection (weekly, monthly, quarterly)
  - Report branding (institution logo, colors, header/footer)
  - Batch report generation (generate 10 reports at once)

- **System Configuration:**
  - Django Admin settings: Database configuration, email settings
  - Application logging and error tracking (view error logs)
  - System monitoring: server resources, active users, performance metrics
  - Backup and restore operations

**Scalability Considerations:**
- Pagination for large datasets (1000+ students in analytics)
- Caching layer (Redis) for frequently accessed data (hot user profiles, cached plans)
- Background job queue (Celery) for heavy operations (report generation, email sending)
- Database read replicas for query performance with high query load

---

#### 2.5.4 Parent View

**Features:**
- **Child Progress Overview:**
  - Daily progress summary (verses, streak, confidence)
  - Weekly progress email with trend analysis
  - Progress comparison: child vs. class average (optional, can be hidden)

- **Alert System:**
  - "Falling Behind" alerts when child drops 30% below target
  - Alert shows: how far behind, trend (declining, stable, improving)
  - Parent receives notification via email and/or push notification
  - Suggested actions: "Encourage practice", "Contact teacher", "Adjust plan"

- **Milestone Notifications:**
  - Milestone alerts: "Child completed Surah Al-Baqarah!"
  - Celebration message with digital badge
  - Progress percentage display

- **Parent Resources Section:**
  - "Home Practice Guide" with structured daily schedule
  - Encouragement tips without pressure (avoid blame language)
  - Basic Tajweed guidance for non-expert parents
  - FAQ section answering common parent questions
  - Video tutorials (optional) for parent learning
  - Weekly encouragement emails with quotes from Quran/teachers

**Privacy Controls:**
  - Parent can choose notification frequency (immediate, daily digest, weekly)
  - Child can set minimal involvement mode (only see progress, no notifications)
  - Opt-out options for celebrations
  - Data export request (download child's data upon request)

---

## 3. Deployment Considerations

### 3.1 Scalability

**Horizontal Scaling:**
- **Load Balancer:** Nginx distributing requests across API instances
- **Target:** Support 10,000+ concurrent students with sub-2s response time for plan generation
- **Strategy:**
  - Round-robin for even distribution of requests
  - Health checks with automatic failover
  - Session affinity for user consistency (sticky sessions to same backend instance)
  - Auto-scaling based on CPU/memory usage (monitor metrics, spin up/down instances)

**Database Optimization:**
- **Read Replicas:** 2-3 read-only replicas for complex analytics queries
- **Connection Pooling:** Max 20 concurrent connections per database instance
- **Query Optimization:**
  - Materialized views for complex aggregations
  - EXPLAIN ANALYZE on slow queries
  - Appropriate indexes on user_id, date, and foreign keys
  - Query result caching (Redis) for frequently accessed data

---

### 3.2 Monitoring

**Application Logging:**
```python
# Structured logging (JSON format) with ELK stack
import logging
import json

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
    handlers=[logging.StreamHandler()]
)

# Log levels
logger.info("User 123 requested plan generation")
logger.error("ML model failed to load: model_v1.pkl", extra={"error_code": "MODEL_LOAD_FAILED"})
logger.warning("High memory usage detected", extra={"memory_mb": 2048})
```

**Metrics Collection:**
```python
# Custom metrics for ML model performance
from prometheus_client import Counter, Gauge, Histogram

# Define metrics
api_request_duration = Histogram('api_request_duration_seconds', buckets=[0.1, 0.5, 1.0, 2.0, 5.0])
ml_inference_latency = Gauge('ml_inference_latency_seconds')
plan_generation_success_rate = Counter('plan_generation_success_total')
database_query_duration = Histogram('db_query_duration_ms', buckets=[10, 50, 100, 500, 1000])
user_satisfaction_score = Histogram('user_confidence_level', buckets=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Expose metrics endpoint
from flask import Flask, jsonify
app.route('/metrics', methods=['GET'])
def metrics():
    return jsonify({
        'api_p50': api_request_duration._samples[500],
        'ml_p99': ml_inference_latency._sample(0.99),
        'plan_success_rate': plan_generation_success_rate._value,
        'db_p50': database_query_duration._samples[500]
    })
```

**Alerting:**
```python
# Alert configuration thresholds
ALERT_THRESHOLDS = {
    'api_error_rate': 1.0,  # Alert if error rate > 1%
    'ml_latency_p99': 2.0,  # Alert if P99 > 2 seconds
    'db_p50': 1.0,  # Alert if P50 > 1 second
    'memory_usage': 0.8,  # Alert if memory > 80%
    'disk_usage': 0.85   # Alert if disk > 85%
}

# Alert notification
from flask import Flask
import requests

def check_alerts():
    """Check metrics and send alerts if thresholds exceeded"""
    # Query Prometheus metrics
    response = requests.get('http://prometheus:9090/metrics').json()
    metrics = response.json()
    
    # Check thresholds
    if metrics['api_error_rate'] > ALERT_THRESHOLDS['api_error_rate']:
        send_alert('API error rate exceeded', severity='warning')
    if metrics['ml_latency_p99'] > ALERT_THRESHOLDS['ml_latency_p99']:
        send_alert('ML latency degraded', severity='critical')
```

---

### 3.3 CI/CD Pipeline

**Testing:**
```yaml
# GitHub Actions workflow
name: Test and Build

on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        run: |
          python -m pip install --upgrade pip
          pip install pytest pytest-cov flask-testing
      - name: Run tests
        run: |
          pytest backend/tests/ --cov=backend --cov-report=term-missing
          pytest frontend/tests/ --cov=frontend --cov-report=term-missing
      - name: Upload coverage
        uses: codecov/codecov-action@v2
        with:
          files: ./backend/coverage.xml,./frontend/coverage.xml

  integration-test:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - name: Integration tests
        run: |
          pytest integration/tests/ --cov=integration
      - name: API contract tests
        run: |
          pytest api-contract-tests/
```

**Deployment:**
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]
    paths: ['backend/**', 'frontend/**']
    tags: [production]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker images
        run: |
          docker-compose -f docker-compose.prod.yml build
          docker tag hifz-ai-backend:latest hifz-ai-frontend:latest
      
      - name: Push to registry
        run: |
          docker push ghcr.io/akentar2001/hifz-ai-backend:latest
          docker push ghcr.io/akentar2001/hifz-ai-frontend:latest
      
      - name: Deploy to production
        run: |
          kubectl set image hifz-ai-backend:ghcr.io/akentar2001/hifz-ai-backend:latest
          kubectl rollout restart deployment/hifz-ai-backend
          kubectl set image hifz-ai-frontend:ghcr.io/akentar2001/hifz-ai-frontend:latest
          kubectl rollout restart deployment/hifz-ai-frontend

  staging:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to staging
        run: |
          kubectl set image hifz-ai-backend:ghcr.io/akentar2001/hifz-ai-backend:staging
          kubectl rollout restart deployment/hifz-ai-backend

  rollback:
    on:
      deployment_failed:
        runs-on: ubuntu-latest
        steps:
          - name: Rollback deployment
            run: |
              kubectl rollout undo deployment/hifz-ai-backend
              kubectl scale deployment/hifz-ai-backend --replicas=3
```

---

## 4. Security Considerations

### 4.1 Authentication & Authorization

**Authentication:**
```python
# JWT-based authentication with Django
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

class JWTAuthentication(JWTAuthentication):
    def get_token(self, user):
        tokens = self.get_tokens(user)
        return tokens['access'], tokens['refresh']

# Rate limiting per user/IP
from django.core.cache import cache
from django_ratelimit.decorators import ratelimit

@ratelimit(key='plan_generation', rate='5/hour', method='GET')
class GeneratePlanView(APIView):
    def get(self, request):
        # Rate limit check
        return Response({'message': 'Rate limit exceeded'}, status=429)
```

**Authorization (RBAC):**
```python
# Role-Based Access Control
from rest_framework.permissions import BasePermission, IsAuthenticated

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role in ['teacher', 'admin']

class IsParent(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role in ['parent', 'admin']
```

### 4.2 Data Protection

**Encryption at Rest:**
```sql
-- PostgreSQL Transparent Data Encryption (TDE)
-- Encrypt user PII and progress data at rest
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Column-level encryption for sensitive data
ALTER TABLE users ADD COLUMN email_encrypted BYTEA;
ALTER TABLE users ADD COLUMN personal_data_encrypted BYTEA;
```

**HTTPS/TLS for all communications:**
```nginx
# nginx configuration for HTTPS with Let's Encrypt
server {
    listen 443 ssl http2;
    ssl_certificate /etc/letsencrypt/live/hifz-ai/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/hifz-ai/privkey.pem;
    
    location / {
        /api/v1/plans/generate {
            proxy_pass http://backend:8000;
            proxy_set_header Upgrade $http_upgrade;
        }
    }
}
```

**Input Validation and Sanitization:**
```python
# Validate and sanitize user inputs
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Validate student progress input
class ProgressRecordValidator:
    def validate_verse_count(self, value):
        if value < 0 or value > 50:
            raise ValidationError("Verses must be between 0 and 50")
        return value

# Sanitize all user input to prevent SQL injection
from django.db import connection
from django.utils.safestring import mark_safe

def save_progress_record(user_id, record):
    # Always use parameterized queries
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO progress_records (user_id, record_date, ayah_id, "
            "verses_memorized, verses_reviewed, mistakes_count, "
            "confidence_level, time_spent_minutes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            [user_id, record_date, ayah_id, verses_memorized, 
             verses_reviewed, mistakes_count, confidence_level, time_spent_minutes]
        )
```

### 4.3 Privacy (GDPR/Children's Online Privacy Protection Act)

**Data Minimization:**
- **Minimal Data Collection:** Only collect what's necessary for personalized plans (verses, time, mistakes, confidence)
- **Purpose Limitation:** Use data solely for adaptive scheduling and progress tracking
- **No Unnecessary Data:** Don't collect age, location, phone numbers, or detailed demographics

**Parental Consent for Students under 13:**
```python
# Parental consent model
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    parental_consent = models.BooleanField(default=False)
    
    # Django Admin includes consent checkbox
    # API returns 403 Forbidden for students <13 without consent
```

**Data Export and Deletion:**
- **Right to Access:** Users can request all their data in CSV format
- **Right to Deletion:** Users can request account deletion (GDPR right to be forgotten)
- **Data Retention Policy:** Progress data retained for 1 year after account deletion, then anonymized
- **Anonymization:** Remove PII (email, name, username) before exporting

**Privacy Policy Accessible in UI:**
```html
<div class="privacy-controls">
    <h2>Privacy Settings</h2>
    <h3>Data Export</h3>
    <label>
        <input type="checkbox" name="share_analytics" checked>
        Share anonymized analytics with research community
    </label>
    <button class="btn-download">Download My Data</button>
    
    <h3>Data Deletion</h3>
    <button class="btn-delete">Delete My Account</button>
    <p class="warning">Warning: All your data will be permanently deleted</p>
    
    <h3>Parental Controls</h3>
    <label>
        <select name="parental_consent" id="parental_consent">
            <option value="">Choose...</option>
            <option value="full">Full access</option>
            <option value="partial">View progress only</option>
            <option value="none">No access</option>
        </select>
    </label>
</div>
```

---

## 5. Performance Targets

### 5.1 API Performance

**Latency Targets:**
- **P50 (Plan Generation):** <500ms for 95th percentile of requests
- **P95 (Plan Generation):** <1000ms for 95th percentile of requests
- **Average Response Time:** <200ms across all endpoints

**Throughput Targets:**
- **Concurrent Users:** Support 10,000+ concurrent active users
- **Requests Per Second:** 500+ requests/second per API instance
- **Batch Processing:** Generate plans for 100+ students in <10 seconds

**Availability Targets:**
- **Uptime SLA:** 99.9% (monthly downtime <7.2 hours)
- **Error Rate:** <0.1% (errors per 1,000 requests)
- **Data Consistency:** ACID compliance for all database transactions

### 5.2 ML Performance

**Inference Performance:**
- **Latency:** <2 seconds for plan generation (95th percentile)
- **Accuracy:** >85% accuracy on test dataset for target prediction
- **Personalization Quality:** Student confidence correlation >0.7 with recommended difficulty

**Training Performance:**
- **Training Time:** <4 hours for full model retrain
- **Update Time:** <30 seconds for incremental model updates
- **Data Processing:** Preprocess 10,000 records in <60 seconds

**Adaptation Performance:**
- **Learning Rate:** Model adjusts plan difficulty within 30 seconds of new feedback
- **Adaptation Effectiveness:** 85% of students report plans are appropriate after adaptation

### 5.3 Database Performance

**Query Performance:**
- **P50 (Simple Queries):** <100ms for indexed user lookups
- **P95 (Complex Analytics):** <1000ms for complex aggregation queries
- **Average Response Time:** <300ms for all database queries

**Efficiency Metrics:**
- **Connection Pooling:** Maintain 80% of max connections
- **Index Hit Rate:** >95% index utilization for primary queries
- **Query Cache Hit Rate:** >70% for frequently accessed data (via Redis)

**Capacity Planning:**
- **Concurrent Users:** Support 10,000+ users
- **Storage:** PostgreSQL with connection pooling and read replicas
- **Peak Load:** Handle 5000+ requests/second during peak hours

---

## 6. Technology Summary

| Component | Technology | Justification |
|-----------|-----------|---------------|
| **Backend** | Django (Python) | Mature ecosystem, strong Admin Panel, RBAC |
| **Frontend** | React.js | Component-based, large community, responsive design |
| **Database** | PostgreSQL | ACID compliance, full-text search, JSONB |
| **ML Framework** | Scikit-learn | Spaced Repetition, Decision Support, traditional ML |
| **API Gateway** | Nginx | Load balancing, rate limiting |
| **Message Queue** | Redis | Async communication, caching |
| **Containerization** | Docker | Industry standard deployment |
| **Monitoring** | ELK Stack | Comprehensive logging and metrics |
| **CI/CD** | GitHub Actions | Automated testing and deployment |

---

## 7. Next Steps for Development

### Sprint 1: Foundation (Week 1-2)
1. **Django Setup:**
   - Configure Django project structure
   - Set up Django Admin with user management
   - Configure PostgreSQL connection pooling
   - Implement JWT authentication and RBAC
   - Set up logging and error handling

2. **Database Implementation:**
   - Create all tables with foreign key constraints
   - Implement indexes for query performance
   - Load verse_difficulty.csv into quran_verses table
   - Create stored procedures for common queries

3. **Core ML Integration:**
   - Implement verse difficulty scoring
   - Build preprocessing pipeline
   - Train initial ML models (Random Forest for target prediction, Gradient Boosting for mistakes)
   - Implement Spaced Repetition algorithm (SM-2) for adaptive scheduling
   - Create plan generation API endpoint with all models integrated

### Sprint 2: User Interfaces (Week 3-4)
1. **Student Portal (React):**
   - Daily plan display with Quran verse lookup
   - Progress tracking dashboard with charts
   - Practice session recording
   - Milestone celebrations and badges

2. **Teacher Dashboard (React):**
   - Multi-student list with filtering
   - Individual student details and progress
   - One-click plan adjustment
   - Performance comparison analytics

3. **Admin Panel (Django):**
   - User and class management
   - Program-wide analytics dashboard
   - Report generation (PDF, Excel, CSV)
   - System configuration

### Sprint 3: Advanced ML (Week 5-6)
1. **Advanced Algorithms:**
   - Implement ensemble models (Random Forest + Gradient Boosting)
   - Add decision tree for verse difficulty classification
   - Implement adaptive difficulty adjustment algorithm
   - Integrate spaced repetition with forgetting curves

2. **Real-Time Optimization:**
   - Add Redis caching for hot plans
   - Implement model preloading and warm-up strategies
   - Optimize inference pipeline for sub-2s latency

### Sprint 4: Parent Features (Week 7-8)
1. **Parent View (React):**
   - Child progress overview
   - Alert system for falling behind
   - Milestone notifications
   - Parent resources section

2. **Privacy Controls:**
   - Implement parental consent system
   - Add data export and deletion features
   - Create privacy policy page in UI

### Sprint 5: Testing & Deployment (Week 9-10)
1. **Testing:**
   - Unit tests for all microservices
   - Integration tests for API contracts
   - E2E tests for critical user flows
   - Load testing and stress testing

2. **Deployment:**
   - Set up Docker Compose for all services
   - Configure Nginx load balancer
   - Set up CI/CD pipeline with GitHub Actions
   - Implement health checks and auto-scaling
   - Configure HTTPS with Let's Encrypt
   - Implement backup and restore procedures

---

## Appendix: Key Design Decisions

### A. Technology Stack Changes

**Decision 1: Django instead of Node.js**
- **Change:** Switch backend from Node.js/Express to Django/Django REST Framework
- **Rationale:** Django's ORM (Django ORM) is superior for complex data relationships between users, progress, plans, and Quran data. Django Admin provides out-of-the-box Admin Panel with user management, RBAC, and data export capabilities needed for institutions.
- **Trade-off:** Django has slightly higher learning curve than Node.js, but the productivity gain with built-in Admin Panel and ORM justifies the switch.

**Decision 2: Scikit-learn instead of PyTorch**
- **Change:** Switch ML framework from PyTorch to Scikit-learn
- **Rationale:** The system focuses on **Adaptive Scheduling and Decision Support**, not deep learning. Scikit-learn provides excellent implementations of:
  - Spaced Repetition algorithms (SM-2, SM-5, etc.) needed for revision optimization
  - Random Forest and Gradient Boosting for Decision Support
  - Predictive Analytics for retention and performance forecasting
  - These algorithms are more appropriate than deep learning for adaptive scheduling.
  - Strong community support and extensive documentation.
- **Trade-off:** PyTorch would be overkill. Deep learning provides incremental improvements but is not necessary for the current scope.

### B. Database Schema Enhancements

**Enhancement 1: Ayah and Progress Tables**
- **Change:** Add dedicated tables for Ayah metadata and detailed progress tracking
- **Rationale:** Allows for better granularity in revision scheduling (reviewing by Ayah rather than verse) and provides more detailed progress analytics.
- **Tables:**
  ```sql
  CREATE TABLE ayahs (
      id SERIAL PRIMARY KEY,
      ayah_number INTEGER UNIQUE NOT NULL,
      surah_id INTEGER NOT NULL REFERENCES quran_surahs(id),
      verses TEXT, -- List of verse numbers
      created_at TIMESTAMP DEFAULT NOW()
  );

  CREATE TABLE progress_logs (
      id SERIAL PRIMARY KEY,
      user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
      timestamp TIMESTAMP DEFAULT NOW(),
      event_type VARCHAR(50), -- 'plan_generated', 'plan_adjusted', 'practice_completed', etc.
      event_data JSONB, -- Detailed event information
      created_at TIMESTAMP DEFAULT NOW()
  );
  ```

**Enhancement 2: Difficulty Score Integration**
- **Change:** Add difficulty_score column to quran_verses table with link to verse_difficulty_scores table
- **Rationale:** Incorporates graduation project research (verse_difficulty.csv) which provides empirical difficulty data for each verse based on community performance. This enables more accurate personalized scheduling by considering actual difficulty rather than heuristics.
- **Implementation:**
  ```sql
  ALTER TABLE quran_verses ADD COLUMN difficulty_score DECIMAL(10,2);
  ALTER TABLE quran_verses ADD COLUMN difficulty_source VARCHAR(50);
  CREATE INDEX idx_quran_difficulty ON quran_verses(difficulty_score);
  ```

**Enhancement 3: Weighted Page Strength**
- **Change:** Add page_number column to quran_verses for Hafs (604 pages)
- **Rationale:** Different pages have different lengths and average difficulty. Weighing by page ensures fair distribution of difficulty across the Quran.
- **Implementation:**
  ```sql
  ALTER TABLE quran_verses ADD COLUMN page_number INTEGER;
  UPDATE quran_verses SET page_number = CEIL(verse_number / 7.0);
  ```

### C. ML Algorithm Selection

**Decision: Spaced Repetition Algorithm**
- **Choice:** SM-2 (Simple Mnemonic)
- **Rationale:** Well-established algorithm for memorization with proven effectiveness. Easy to implement in Scikit-learn. Provides predictable and scientifically-based review intervals. More effective than simple schedules for retention.
- **Implementation:** Use `sklearn.scheduling` library for SM-2 with customizable intervals.

**Decision: Decision Support Algorithm**
- **Choice:** Random Forest Classifier
- **Rationale:** Provides interpretable feature importance. Can identify which factors most influence memorization difficulty (time availability, mistake rate, etc.). Good for explaining recommendations to students and teachers.
- **Implementation:** Use `sklearn.ensemble.RandomForestClassifier` with `feature_importances_` attribute for transparency.

**Decision: Ensemble Methods for Target Prediction**
- **Choice:** Random Forest Regressor + Gradient Boosting Regressor
- **Rationale:** Ensemble methods (combining multiple models) often outperform single models. Random Forest provides baseline predictions while Gradient Boosting captures non-linear relationships. Together, they provide robust daily target estimates.
- **Implementation:** Use `sklearn.ensemble.VotingRegressor` or `StackingRegressor` to combine predictions from both models.

---

## 8. Technology Summary

| Component | Technology | Justification |
|-----------|-----------|---------------|
| **Backend** | Django (Python) | Mature ORM, strong Admin Panel, RBAC |
| **Frontend** | React.js | Component-based, large ecosystem |
| **Database** | PostgreSQL | ACID compliance, JSONB, full-text search |
| **ML Framework** | Scikit-learn | Spaced Repetition, Decision Support |
| **API Gateway** | Nginx | Load balancing |
| **Message Queue** | Redis | Async, caching |
| **Containerization** | Docker | Industry standard |
| **Monitoring** | ELK Stack | Logging, metrics, alerts |
| **CI/CD** | GitHub Actions | Testing, deployment |
| **Security** | JWT, RBAC, PostgreSQL TDE, HTTPS/TLS, GDPR | Authentication, data protection, privacy |

---

**Document Version:** 2.0  
**Last Updated:** 2025-01-09  
**Author:** ATLAS (Architect)  
**Project:** HIFZ-AI - Personalized Quran Memorization Using AI