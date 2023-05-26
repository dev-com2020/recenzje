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

@app.route('/get-book-row/<int:id>', methods=['GET'])
def get_book_row(id):
    book = Book.query.get(id)
    author = Author.query.get(book.author_id)

    response = f'''
    <tr>
    <td>{book.title}</td>
    <td>{author.name}</td>
    <td>
    <button class="btn btn-primary"
    hx-get="/get-edit-form/{id}">Edytuj</button>
    </td>
    </tr>
    '''
    return response

@app.route('/get-edit-form/<int:id>', methods=['GET'])
def get_edit_form(id):
    book = Book.query.get(id)
    author = Author.query.get(book.author_id)

    response = f'''
    <tr>
    <td>{book.title}</td>
    <td>{author.name}</td>
    <td>
    <button class="btn btn-primary"
    hx-get="/get-book-row/{id}">Edytuj</button>
    </td>
    <button class="btn btn-primary" hx-put='/update{id} hx-include='closets tr'>
    Zapisz</button>
    </tr>
    '''
    return response

@app.route('/submit', methods=['POST'])
def submit():
    global_book_object = Book()
    title = request.form['title']
    author_name = request.form['author']

    author_exist = db.session.query(Author).filter(Author.name == author_name).first()
    if author_exist:
        author_id = author_exist.author_id
        book = Book(author_id=author_id, title=title)
        db.session.add(book)
        db.session.commit()
        global_book_object = book
    else:
        author = Author(name=author_name)
        db.session.add(author)
        db.session.commit()

        book = Book(author_id=author.author_id, title=title)
        db.session.add(book)
        db.session.commit()
        global_book_object = book

    response = f'''
    <tr>
    <td>{title}</td>
    <td>{author_name}</td>
    <td>
    <button class="btn btn-primary"
    hx-get="/get-edit-form/{global_book_object.book_id}">Edytuj</button>
    </td>
    </tr>
    '''
    return response

@app.route("/update/<int:id>", methods=['PUT'])
def update_book(id):
    db.session.query(Book).filter(Book.book_id == id).update({"title": request.form["title"]})
    db.session.commit()

    title = request.form["title"]
    book = Book.query.get(id)
    author = Author.query.get(book.author_id)

    response = f'''
    <tr>
    <td>{title}</td>
    <td>{author.name}</td>
    <td>
    <button class="btn btn-primary"
    hx-get="/get-edit-form/{id}">Edytuj</button>
    </td>
    </tr>
    '''
    return response