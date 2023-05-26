from flask import render_template, request, jsonify

from app import app, db
from app.models import Book, Author

data = [{
    "title": "Lord of the Rings",
    "author": "Tolkien"
},
    {
        "title": "Miś Uszatek",
        "author": "nieznany"
    }]


@app.route('/', methods=['GET'])
def home():
    books = db.session.query(Book).all()
    book_list = []

    for book in books:
        author = Author.query.get(book.author_id)
        book_object = {'id': book.book_id, "title": book.title, "author": author.name}
        book_list.append(book_object)
    return render_template("index.html", books=book_list)
