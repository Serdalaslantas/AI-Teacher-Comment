# main.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./school.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Models
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    grades = relationship("Grade", back_populates="student")


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject = Column(String)
    grade = Column(Integer)
    student = relationship("Student", back_populates="grades")


class SampleComment(Base):
    __tablename__ = "sample_comments"
    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String)


Base.metadata.create_all(bind=engine)


# Pydantic models
class StudentCreate(BaseModel):
    name: str


class GradeCreate(BaseModel):
    subject: str
    grade: int


class SampleCommentCreate(BaseModel):
    comment: str


class StudentOut(StudentCreate):
    id: int
    grades: list[GradeCreate]


# FastAPI app
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/students/", response_model=StudentOut)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.post("/students/{student_id}/grades/")
def add_grade(student_id: int, grade: GradeCreate, db: Session = Depends(get_db)):
    db_grade = Grade(**grade.dict(), student_id=student_id)
    db.add(db_grade)
    db.commit()
    return {"message": "Grade added successfully"}


@app.get("/students/", response_model=list[StudentOut])
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students


@app.post("/sample-comment/")
def save_sample_comment(comment: SampleCommentCreate, db: Session = Depends(get_db)):
    db.query(SampleComment).delete()
    new_comment = SampleComment(**comment.dict())
    db.add(new_comment)
    db.commit()
    return {"message": "Sample comment saved successfully"}


@app.get("/sample-comment/", response_model=SampleCommentCreate)
def get_sample_comment(db: Session = Depends(get_db)):
    comment = db.query(SampleComment).order_by(SampleComment.id.desc()).first()
    return comment or {"comment": ""}


# Updated generate_comment endpoint
@app.post("/generate-comment/{student_id}")
def generate_comment(student_id: int, db: Session = Depends(get_db)):
    # Get student data
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Get sample comment
    sample_comment = db.query(SampleComment).order_by(SampleComment.id.desc()).first()

    # Prepare grades text
    grades_text = "\n".join([f"{grade.subject}: {grade.grade}" for grade in student.grades])

    # Generate prompt
    prompt = f"""Generate a student progress report using this format:
    {sample_comment.comment if sample_comment else ''}

    Student: {student.name}
    Grades:
    {grades_text}
    Report:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "You are a helpful teacher's assistant generating student progress reports."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )

        return {
            "student_id": student_id,
            "comment": response.choices[0].message.content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))