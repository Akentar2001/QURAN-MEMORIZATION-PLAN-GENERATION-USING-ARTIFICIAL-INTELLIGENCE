from app import db

class users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    students = db.relationship('students', backref='users', lazy=True)


class students(db.Model):
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete="SET NULL"), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    recitations = db.relationship("recitation_session", back_populates="student", cascade="all, delete-orphan")
    plans = db.relationship('students_plans_info', backref='students', lazy=True)


class surahs(db.Model):
    surah_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    no_verses = db.Column(db.Integer, nullable=False)

    verses = db.relationship('verses', backref='surahs', lazy=True)


class verses(db.Model):
    verse_id = db.Column(db.Integer, primary_key=True)
    surah_id = db.Column(db.Integer, db.ForeignKey('surahs.surah_id'), nullable=False)
    begin_verse = db.Column(db.Text, nullable=False)
    order_in_quraan = db.Column(db.Integer, nullable=False)
    reverse_index = db.Column(db.Integer, nullable=False)
    order_in_surah = db.Column(db.Integer, nullable=False)
    page_no = db.Column(db.Integer, nullable=False)
    letters_count = db.Column(db.Integer, nullable=False)
    weight_on_page = db.Column(db.Float, nullable=False)
    verse_difficulty = db.Column(db.Float, nullable=True)

    start_sessions = db.relationship('recitation_session', foreign_keys='recitation_session.start_verse_id', backref='start_verse', lazy=True)
    end_sessions = db.relationship('recitation_session', foreign_keys='recitation_session.end_verse_id', backref='end_verse', lazy=True)


class recitation_session(db.Model):
    __tablename__ = "recitation_session"
    session_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    __table_args__ = (
    db.CheckConstraint("type IN ('New_Memorization', 'Minor_Revision', 'Major_Revision')", name="recitation_session_type_check"),
    )
    start_verse_id = db.Column(db.Integer, db.ForeignKey('verses.verse_id'), nullable=False)
    end_verse_id = db.Column(db.Integer, db.ForeignKey('verses.verse_id'), nullable=False)
    rating = db.Column(db.SmallInteger, nullable=True)
    is_accepted = db.Column(db.Boolean, nullable=True)
    pages_count = db.Column(db.Float, nullable=True)
    letters_count = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    student = db.relationship("students", back_populates="recitations")


class students_plans_info(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id', ondelete="CASCADE"), primary_key=True)
    
    memorized_parts = db.Column(db.Float, nullable=True)
    overall_rating = db.Column(db.Float, nullable=True)
    memorization_days = db.Column(db.SmallInteger, server_default="5", nullable=False)

    new_memorization_letters_amount = db.Column(db.Integer, nullable=True)
    new_memorization_pages_amount = db.Column(db.Float, nullable=True)
    memorization_direction = db.Column(db.Boolean, nullable=False)
    last_verse_recited_new_memorization = db.Column(db.Integer, nullable=False)
    overall_rating_new_memorization = db.Column(db.Float, nullable=True)

    small_revision_letters_amount = db.Column(db.Integer, nullable=True)
    small_revision_pages_amount = db.Column(db.Float, nullable=True)
    overall_rating_small_revision = db.Column(db.Float, nullable=True)

    large_revision_letters_amount = db.Column(db.Integer, nullable=True)
    large_revision_pages_amount = db.Column(db.Float, nullable=True)
    revision_direction = db.Column(db.Boolean, nullable=False)
    last_verse_recited_large_revision = db.Column(db.Integer, nullable=True)
    overall_rating_large_revision = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    rl_last_action = db.Column(db.Float, nullable=True)
