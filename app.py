
from unittest import result

from flask import Flask, render_template, request
from dataclasses import dataclass

app = Flask(__name__)


# Book data model
@dataclass
class Book:    # Ive define  this class to represent a book in the library system & as i am c/vb.net developer i have used dataclass to define the class in a simple way this is just my habit ;-)
    book_id: str
    title: str
    author: str
    isbn: str
    publication_year: int
    is_available: bool = True



def linear_search(book_list,search_term):
    results=[]
    search_term=search_term.lower()
    for book in book_list:
        if (search_term in book.title.lower() or
            search_term in book.author.lower() or
            search_term in book.isbn.lower()
            ):

            results.append(book)

    return results


# this behaves like in-memory database
books = {}

# Sample data of books
book1 = Book("B001", "Python Programming", "Paul Smith",
             "9781234567890", 2024)

book2 = Book("B002", "Data Structures", "Mark Arnold",
             "9781234567891", 2023)

books[book1.book_id] = book1  #just to handle data in memory
books[book2.book_id] = book2


@app.route("/", methods=["GET", "POST"])
def home():

    message = ""

    if request.method == "POST":

        book_id = request.form.get("book_id", "").strip()
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        isbn = request.form.get("isbn", "").strip()
        year = request.form.get("year", "").strip()
#checking the data integrety 
        if not all([book_id, title, author, isbn, year]):
            message = "Please complete all fields."

        elif book_id in books:
            message = "Error: This Book ID already exists."

        else:
            try:
                publication_year = int(year)

                new_book = Book(
                    book_id,
                    title,
                    author,
                    isbn,
                    publication_year
                )

                books[book_id] = new_book

                message = "Book added successfully!"

            except ValueError: # some times  people may enter twenty instead of 20 or 2020    
                message = "Publication year must be a number."

    return render_template(   #what this application returns
        "index.html",
        books=books.values(),
        message=message
    )


@app.route("/search")
def search_books():

    query = request.args.get("q", "").strip()

    results = linear_search(books.values(), query)

    return render_template(
        "index.html",
        books=books.values(),
        message="",
        search_results=results,
        query=query
    )

@app.route("/search_binary", methods=["GET"])
def binary_search_route():
    print("SEARCH ROUTE aCTIVATED!")
    query = request.args.get("q", "").strip()
    result=None
    print("search term:", query)
    if query:
        result = binary_search(books.values(), query)
    print("Search result:", result)
    return render_template(
        "index.html",
        books=books.values(),
        message="",
        binary_result=result,
        query=query
    )

def binary_search(book_list, target):
    # if i am using binary search i need to sort them befor
    sorted_books= sorted( book_list, key =lambda book:book.title.lower()
    )
    low= 0 
    
    high = len(sorted_books) - 1
    while low<=high:
       mid =(low+high)//2
       middle_title = sorted_books[mid].title.lower()
       if middle_title == target.lower():
           return sorted_books[mid]    
       elif middle_title < target.lower():
           low = mid + 1
       else:
           high = mid - 1
    return None # Book not found
      # return sorted_books[mid] 



def merge_sort_books(books):

    if len(books) <=1:
        return books
    middle = len(books)//2
    left=merge_sort_books( books[:middle])
    right= merge_sort_books(books[middle:])
    return merge_sort_books(left, right )

def merge_books(left,right ):
    sorted_books= []
    j=0 
    i=0
    while i< len(left) and j< len(right):
      if  left[i].title.lower()< right [j].title.lower():
        sorted_books.append(left[i])
        i+=1
    else:
        sorted_books.append(right[j])
        j+=1
    sorted_books= sorted_books + left[i:] + right[j:]
    return sorted_books



if __name__ == "__main__":
    app.run(debug=True)
