from database import LibraryReport, ReaderService, BookService, StructuredDataReturn, LibraryService
from init_db import Book, Reader, Loan

def get_overdue_books():
   books = LibraryReport.get_overdue_books()
   for book in books:
      print(book)

def get_loaned_books():
   try:
      reader_id = int(input("Type id reader"))
      reader = LibraryReport.get_currently_loaned_books(reader_id)
      print("Get loaned book successfully")
      for red in reader:
         print(red)
      return reader_id
   except ValueError:
      print("Reader not found")

def check_returned_book():
   try:
      book_id = int(input("Type id book: "))
      loan = LibraryService.book_return(book_id)
      print("Book returned successfully")
      return loan
   except ValueError:
      print("No active loan found for this book")

def to_lend():
   try:
      book_id = int(input("Type id book: "))
      reader_id = int(input("Type id reader: "))
      #check_book = LibraryService.get_book(book_id)
      #check_reader = LibraryService.get_reader(reader_id)
      loan = LibraryService.loan(book_id, reader_id)
      return loan
   except ValueError:
      print("Book is already loaned")

def sub_choice_one_sub_four():
   print("""
=== Loans Menu ==========
|   Choose:             |
|1. To lend             |
|2. Check returned book |
|3. Get loaned books    |
|4. Get overdue books   |
|5. Back                | 
|-----------------------|
   """)
   choice = int(input("Type your choice: "))
   return choice

def sub_choice_one(choice:int):
   if choice == 1:
      title = input("Type book'title: ")
      author = input("Type book's author: ")
      new_book = BookService.register(title, author)
      print("Book registered successfully")
      return new_book
    
   elif choice == 2:
      book_id = int(input("Type book id: "))
      which = input("Update name or author? Type N or A or both: ")
      if which == 'N':
          book_title = input("Type title book: ")
          ch = BookService.update(book_id, book_title)
          print("Title updated successfully")
          return ch
      elif which == 'A':
         book_author = input("Type autor book: ")
         ch = BookService.update(book_id, book_author)
         print("Author updated successfully")
         return ch
      elif which == 'both':
         book_title = input("Type title book: ")
         book_author = input("Type autor book: ")
         ch = BookService.update(book_id, book_title, book_author)
         print("Book updated successfully")
         return ch
      else:
          false = "Error, type N or A or both"
          return false
      
   elif choice == 3:
      book_id = int(input("Type book id: "))
      book_deleted = BookService.delete(book_id)
      print("Book deleted")
   
   elif choice == 4:
      all_books = StructuredDataReturn.return_all_books()
      for book in all_books:
         print(book)
      print("All book returned successfully")

   elif choice == 5:
      choice = sub_choice_one_sub_four()
      if choice == 1:
         lend = to_lend()
      elif choice == 2:
         loaned = check_returned_book()
      elif choice == 3:
         get_loaned_book = get_loaned_books()
      elif choice == 4:
         gt_ovrdue = get_overdue_books()
      elif choice == 5:
         menu()

   elif choice == 6:
      menu()

def choose_one():
    print("""
=== Library Menu ===
|   Choose:           |
|1. Register book     |
|2. Update book       |
|3. Delete book       |
|4. Return all book   |
|5. Loans             |
|6. Back              |
|---------------------|
   """)
    choice = int(input("Type your choice: "))
    return choice
#=======================================================
#=======================================================
#=======================================================
def sub_choice_two(choice:int):
   if choice == 1:
      name = input("Type name reader: ")
      new_reader = ReaderService.register(name)
      print("Reader registered successfully")
      return new_reader
   
   elif choice == 2:
       try:
           reader_id = int(input("Type id reader: "))
       except ValueError:
           print("Type a valid number")
           return

       reader_name = input("Type name reader: ")

       if not LibraryService.reader_exists(reader_id):
           print("Reader not found")
           return

       if LibraryService.reader_name_exists(reader_name):
           print("Reader name already exists")
           return

       reader_updated = ReaderService.update(reader_id, reader_name)
       return reader_updated
   
   elif choice == 3:
      try:
         reader_id = int(input("Type id reader: "))
         ReaderService.delete(reader_id)
         print("Reader deleted")
      except ValueError:
         print("Reader not found")
   
   elif choice == 4:
      try:
         reader_id = int(input("Type id reader: "))
         reader = LibraryService.get_reader(reader_id)
         print(reader.readers_name)
      
      except ValueError:
         print("Type correct reader id")
   
   elif choice == 5:
      readers = StructuredDataReturn.return_all_readers()
      for reader in readers:
         print(reader)


def choose_two():
   print("""
=== Library Menu ===
|   Choose:           |
|1. Register reader   |
|2. Update reader     |
|3. Delete reader     |
|4. Get reader        |
|5. Return all readers|
|6. Back              |
|---------------------| 
   """)
   choice = int(input("Type your choice: "))
   return choice

def menu():
    print("""
=== Library Menu ===
|   Welcome        |
|   Choose:        |
|1. Manage books   |
|2. Manage readers |
|------------------|
""")
    choice = int(input("Type your choice: "))
    return choice


while(1):
   choice = menu()
   if choice == 1:
      print("You choose to manage books")
      book_choice = choose_one()
      sub_book_choice = sub_choice_one(book_choice)
   
   elif choice == 2:
      print("You choose to manage readers")
      reader_choice = choose_two()
      sub_reader_choice = sub_choice_two(reader_choice)

   else:
       print("Invalid choice, type a number")
       