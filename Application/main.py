#Exemple
class Author:
    def __init__(self, name):
        self.name = name
        self.books = []

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

author1 = Author("J.K. Rowling")
book1 = Book("Harry Potter", author1)
author1.books.append(book1)
