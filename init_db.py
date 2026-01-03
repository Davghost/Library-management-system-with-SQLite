from sqlalchemy import create_engine, Column, Integer, UnicodeText, Unicode, ForeignKey, Date
from datetime import date
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.exc import SQLAlchemyError
import os

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(basedir, 'library.db')}"
engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
   pass

class BaseService:

   @staticmethod
   def create(session, instance):
      try:
         session.add(instance)
         session.commit()
         session.refresh(instance)
         return instance
      except SQLAlchemyError:
         session.rollback()
         raise
   
   @staticmethod
   def update(session):
      try:
         session.commit()
      except SQLAlchemyError:
         session.rollback()
         raise
   
   @staticmethod
   def delete(session, instance):
      try:
         session.delete(instance)
         session.commit()
      except SQLAlchemyError:
         session.rollback()
         raise

   @staticmethod
   def check_free_loan(session, book_id) -> bool:
        loan = session.query(Loan).filter(
            Loan.book_id == book_id,
            Loan.return_date == None
        ).first()
        
        return loan is None
   
class Book(Base):
   __tablename__ = "book"
   id = Column(Integer, primary_key=True)
   title = Column(UnicodeText, unique=True, nullable=False)
   author = Column(Unicode(64), unique=False, nullable=False)

class Reader(Base):
   __tablename__ = "reader"
   id = Column(Integer, primary_key=True)
   readers_name = Column(Unicode(64), unique=True, nullable=False)

class Loan(Base):
   __tablename__ = "loan"
   id = Column(Integer, primary_key=True)
   book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
   reader_id = Column(Integer, ForeignKey("reader.id"), nullable=False)
   loan_date = Column(Date, default=date.today, nullable=False)
   return_date = Column(Date, nullable=True)

   book = relationship("Book")
   reader = relationship("Reader")

Base.metadata.create_all(engine)