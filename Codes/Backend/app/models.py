from app import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    students = db.relationship('Student', backref='user', lazy=True)


class Student(db.Model):
    __tablename__ = "students"
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    __table_args__ = (
    db.CheckConstraint("gender IN ('M', 'F')", name="students_gender_check"),
)

    nationality = db.Column(db.String(50), nullable=False)
    student_phone = db.Column(db.String(15), nullable=True)
    parent_phone = db.Column(db.String(15), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    memorized_parts = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete="SET NULL"), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    recitations = db.relationship("RecitationSession", back_populates="student", cascade="all, delete-orphan")
    plans = db.relationship('StudentPlanInfo', backref='student', lazy=True)


class Surah(db.Model):
    surah_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    no_verses = db.Column(db.Integer, nullable=False)

    verses = db.relationship('Verse', backref='surah', lazy=True)


class Verse(db.Model):
    verse_id = db.Column(db.Integer, primary_key=True)
    surah_id = db.Column(db.Integer, db.ForeignKey('surah.surah_id'), nullable=False)
    begin_verse = db.Column(db.Text, nullable=False)
    order_in_quraan = db.Column(db.Integer, nullable=False)
    reverse_index = db.Column(db.Integer, nullable=False)
    order_in_surah = db.Column(db.Integer, nullable=False)
    page_no = db.Column(db.Integer, nullable=False)
    letters_count = db.Column(db.Integer, nullable=False)
    weight_on_page = db.Column(db.Float, nullable=False)
    verse_difficulty = db.Column(db.Float, nullable=True)

    start_sessions = db.relationship('RecitationSession', foreign_keys='RecitationSession.start_verse_id', backref='start_verse', lazy=True)
    end_sessions = db.relationship('RecitationSession', foreign_keys='RecitationSession.end_verse_id', backref='end_verse', lazy=True)


class RecitationSession(db.Model):
    __tablename__ = "recitation_session"
    session_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    __table_args__ = (
    db.CheckConstraint("type IN ('New_Memorization', 'Minor_Revision', 'Major_Revision')", name="recitation_session_type_check"),
    )
    start_verse_id = db.Column(db.Integer, db.ForeignKey('verse.verse_id'), nullable=False)
    end_verse_id = db.Column(db.Integer, db.ForeignKey('verse.verse_id'), nullable=False)
    rating = db.Column(db.SmallInteger, nullable=True)
    is_accepted = db.Column(db.Boolean, nullable=False)
    pages_count = db.Column(db.Float, nullable=False)
    letters_count = db.Column(db.Integer, nullable=False)
    rl_reward_signal = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    student = db.relationship("Student", back_populates="recitations")


class StudentPlanInfo(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id', ondelete="CASCADE"), primary_key=True)
    memorization_direction = db.Column(db.Boolean, nullable=False)
    last_verse_recited = db.Column(db.Integer, nullable=False)
    revision_direction = db.Column(db.Boolean, nullable=False)
    new_memorization_amount = db.Column(db.Float, nullable=True)
    small_revision_amount = db.Column(db.Float, nullable=True)
    large_revision_amount = db.Column(db.Float, nullable=True)
    memorization_days = db.Column(db.SmallInteger, server_default="0", nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
