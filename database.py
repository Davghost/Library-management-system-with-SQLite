from init_db import Reader, Book, Loan, engine, BaseService
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta

Session = sessionmaker(bind=engine)

class ReaderService(BaseService):
   @staticmethod
   def register(readers_name:str):
      session = Session()
      try:
         reader = Reader(readers_name=readers_name)
         return ReaderService.create(session, reader)
      finally:
         #print("reader added successfully")
         session.close()

   @staticmethod
   def update(reader_id:int, reader_name:str):
      session = Session()
      try:
         reader = session.get(Reader, reader_id)
         if not reader:
            raise ValueError("Reader not found")
         
         reader.readers_name = reader_name
         BaseService.update(session)
         return reader
      finally:
         session.close()

   @staticmethod
   def delete(reader_id:int):
      session = Session()
      try:
         reader = session.get(Reader, reader_id)
         if reader is None:
            raise ValueError("Reader not found")
         
         BaseService.delete(session, reader)
      finally:
         session.close()

class BookService(BaseService):
   @staticmethod
   def register(title:str, author:str):
      session = Session()
      try:
         book = Book(title=title, author=author)
         return BookService.create(session, book)
      finally:
         #print("book added successfully")
         session.close()
   
   @staticmethod
   def update(book_id:int, book_title:str | None=None, book_author:str | None=None):
      session = Session()
      try:
         book = session.get(Book, book_id)
         if not book:
            raise ValueError("Book not found")
         
         if book_title is not None:
            book.title = book_title

         if book_author is not None:
            book.author = book_author

         BaseService.update(session)
         return book
      finally:
         session.close()

   @staticmethod
   def delete(book_id:int):
      session = Session()
      try:
         book = session.get(Book, book_id)
         if book is None:
            raise ValueError("Book not found")
         
         BaseService.delete(session, book)
      finally:
         session.close()
      
class StructuredDataReturn():
   @staticmethod
   def return_all_readers():
      with Session(engine) as session:
         readers = session.query(Reader).all()

         return [
            {
               "id": reader.id,
               "name": reader.readers_name,
            }
            for reader in readers
         ]
   
   @staticmethod
   def return_all_books():
      with Session(engine) as session:
         books = session.query(Book).all()
         return [
             {
                 "id": book.id,
                 "title": book.title,
                 "author": book.author
             }
             for book in books
         ]

class LibraryService():
   @staticmethod
   def loan(book_id:int, reader_id:int):
      session = Session()
      try:
         reader = session.get(Reader, reader_id)
         
         if reader is None:
            raise ValueError("Reader not found")
         
         free = BaseService.check_free_loan(session, book_id)
         if not free:
            raise ValueError("Book is already loaned")

         loan = Loan(
            book_id = book_id,
            reader_id = reader_id,
            loan_date = date.today(),
            return_date = None
         )

         BaseService.create(session, loan)
         return loan
               
      finally:
         session.close()

   @staticmethod
   def book_return(book_id:int):
      session = Session()
      try:
         loan = session.query(Loan).filter(
            Loan.book_id == book_id,
            Loan.return_date == None
         ).first()

         if loan is None:
            raise ValueError("No active loan found for this book")
         
         loan.return_date = date.today()
         BaseService.update(session)

         return loan
      
      finally:
         session.close()

class LibraryReport(BaseService):
   @staticmethod
   def get_currently_loaned_books(reader_id:int):
      session = Session()
      try:
         if not session.get(Reader,reader_id):
            raise ValueError("Reader not found")

         loans = session.query(Loan).filter(
            Loan.reader_id == reader_id,
            Loan.return_date == None
         ).all()

         return [
            {
               "id": loan.book.id,
               "title": loan.book.title,
               "author": loan.book.author,
               "loan_date": loan.loan_date
            }
            for loan in loans
         ]
      finally:
         session.close()
   
   @staticmethod
   def get_overdue_books():
      session = Session()
      try:
         overdue_threshold = date.today() - timedelta(days=30)

         loans = session.query(Loan).filter(
            Loan.loan_date >= overdue_threshold,
            Loan.return_date == None
         ).all()

         if not loans:
            raise ValueError("There are no overdue books")

         return [
            {
               "id": loan.book.id,
               "title": loan.book.title,
               "reader_name": loan.reader.readers_name
            }
            for loan in loans
         ]
      finally:
         session.close()
