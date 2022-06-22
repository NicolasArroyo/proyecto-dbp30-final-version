from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from models import Account, Book, Author

ELEMENTS_PER_PAGE = 5


def paginate_elements(request, selection, is_descendent):
    if is_descendent:
        start = len(selection) - ELEMENTS_PER_PAGE
        end = len(selection)
    else:
        page = request.args.get('page', 1, type=int)

        start = (page - 1) * ELEMENTS_PER_PAGE
        end = start + ELEMENTS_PER_PAGE

    elements = [element.format() for element in selection]
    current_elements = elements[start: end]

    return current_elements


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorizations, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS, POST, PATCH, DELETE')
        return response

    # ACCOUNTS ENDPOINTS

    @app.route('/accounts', methods=['GET'])
    def get_accounts():
        selection = Account.query.order_by('id').all()
        accounts = paginate_elements(request, selection, False)

        if len(accounts) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'accounts': accounts,
            'total_accounts': len(selection)
        })

    @app.route('/accounts', methods=['POST'])
    def post_account():
        body = request.get_json()
        first_name = body.get('first_name', None)
        last_name = body.get('last_name', None)
        username = body.get('username', None)
        password = body.get('password', None)
        number_of_sanctions = body.get('number_of_sanctions', None)
        is_active = body.get('is_active', None)
        email = body.get('email', None)
        is_admin = body.get('is_admin', None)
        search = body.get('search', None)

        if search:
            selection = Account.query.order_by('id').filter(Account.username.like('%{}%'.format(search))).all()

            accounts = paginate_elements(request, selection, False)
            return jsonify({
                'success': True,
                'accounts': accounts,
                'total_accounts': len(selection)
            })

        try:
            account = Account(first_name=first_name, last_name=last_name, username=username, password=password,
                              number_of_sanctions=number_of_sanctions, is_active=is_active, email=email,
                              is_admin=is_admin)

            new_account_id = account.post()

            selection = Account.query.order_by('id').all()
            accounts = paginate_elements(request, selection, True)

            return jsonify({
                'success': True,
                'created': new_account_id,
                'accounts': accounts,
                'total_accounts': len(selection)
            })

        except Exception as e:
            print(e)
            abort(500)

    @app.route('/accounts', methods=['PATCH'])
    def patch_account(account_id):
        error_404 = False
        try:
            account = Account.query.filter(Account.id == account_id).one_or_none()
            if account is None:
                error_404 = True
                abort(404)

            body = request.get_json()

            if 'first_name' in body:
                account.first_name = body.get('first_name')

            if 'last_name' in body:
                account.last_name = body.get('last_name')

            if 'username' in body:
                account.username = body.get('username')

            if 'password' in body:
                account.password = body.get('password')

            if 'number_of_sanctions' in body:
                account.number_of_sanctions = body.get('number_of_sanctions')

            if 'is_active' in body:
                account.is_active = body.get('is_active')

            if 'email' in body:
                account.email = body.get('email')

            if 'is_admin' in body:
                account.completed = body.get('is_admin')

            account.patch()

            return jsonify({
                'success': True,
                'id': account_id,
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/accounts', methods=['DELETE'])
    def delete_account(account_id):
        error_404 = False
        try:
            account = Account.query.filter(Account.id == account_id).one_or_none()
            if account is None:
                error_404 = True
                abort(404)

            account.delete()

            selection = Account.query.order_by('id').all()
            accounts = paginate_elements(request, selection, False)

            return jsonify({
                'success': True,
                'deleted': account_id,
                'accounts': accounts,
                'total_accounts': len(selection)
            })
        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    # BOOKS ENDPOINTS

    @app.route('/books', methods=['GET'])
    def get_books():
        selection = Book.query.order_by('id').all()
        books = paginate_elements(request, selection, False)

        if len(books) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'books': books,
            'total_books': len(selection)
        })

    @app.route('/books', methods=['POST'])
    def post_book():
        body = request.get_json()
        ISBN = body.get('ISBN', None)
        title = body.get('title', None)
        subject = body.get('subject', None)
        language = body.get('language', None)
        number_of_pages = body.get('number_of_pages', None)
        publication_date = body.get('publication_date', None)
        publisher = body.get('publisher', None)
        price = body.get('price', None)
        due_date = body.get('due_date', None)
        borrowed_date = body.get('borrowed_date', None)
        search = body.get('search', None)

        if search:
            selection = Book.query.order_by('id').filter(Book.title.like('%{}%'.format(search))).all()

            books = paginate_elements(request, selection, False)
            return jsonify({
                'success': True,
                'books': books,
                'total_books': len(selection)
            })

        try:
            book = Book(ISBN=ISBN, title=title, subject=subject, language=language, number_of_pages=number_of_pages,
                        publication_date=publication_date, publisher=publisher, price=price, due_date=due_date,
                        borrowed_date=borrowed_date)

            new_book_id = book.post()

            selection = Book.query.order_by('id').all()
            books = paginate_elements(request, selection, True)

            return jsonify({
                'success': True,
                'created': new_book_id,
                'books': books,
                'total_books': len(selection)
            })

        except Exception as e:
            print(e)
            abort(500)

    @app.route('/books', methods=['PATCH'])
    def patch_book(book_id):
        error_404 = False
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()
            if book is None:
                error_404 = True
                abort(404)

            body = request.get_json()

            if 'ISBN' in body:
                book.ISBN = body.get('ISBN')

            if 'title' in body:
                book.title = body.get('title')

            if 'subject' in body:
                book.subject = body.get('subject')

            if 'language' in body:
                book.language = body.get('language')

            if 'number_of_pages' in body:
                book.number_of_pages = body.get('number_of_pages')

            if 'publication_date' in body:
                book.publication_date = body.get('publication_date')

            if 'publisher' in body:
                book.publisher = body.get('publisher')

            if 'price' in body:
                book.price = body.get('price')

            if 'due_date' in body:
                book.due_date = body.get('due_date')

            if 'borrowed_date' in body:
                book.borrowed_date = body.get('borrowed_date')

            book.patch()

            return jsonify({
                'success': True,
                'id': book_id,
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/books', methods=['DELETE'])
    def delete_book(book_id):
        error_404 = False
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()
            if book is None:
                error_404 = True
                abort(404)

            book.delete()

            selection = Book.query.order_by('id').all()
            books = paginate_elements(request, selection, False)

            return jsonify({
                'success': True,
                'deleted': author_id,
                'books': books,
                'total_books': len(selection)
            })
        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    # AUTHORS ENDPOINTS

    @app.route('/authors', methods=['GET'])
    def get_authors():
        selection = Author.query.order_by('id').all()
        authors = paginate_elements(request, selection, False)

        if len(authors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'authors': authors,
            'total_authors': len(selection)
        })

    @app.route('/authors', methods=['POST'])
    def post_author():
        body = request.get_json()
        name = body.get('name', None)
        dob = body.get('dob', None)
        search = body.get('search', None)

        if search:
            selection = Author.query.order_by('id').filter(Author.name.like('%{}%'.format(search))).all()

            authors = paginate_elements(request, selection, False)
            return jsonify({
                'success': True,
                'authors': authors,
                'total_authors': len(selection)
            })

        try:
            author = Author(name=name, dob=dob)

            new_author_id = author.post()

            selection = Author.query.order_by('id').all()
            authors = paginate_elements(request, selection, True)

            return jsonify({
                'success': True,
                'created': new_author_id,
                'author': author,
                'total_authors': len(selection)
            })

        except Exception as e:
            print(e)
            abort(500)

    @app.route('/authors', methods=['PATCH'])
    def patch_author(author_id):
        error_404 = False
        try:
            author = Author.query.filter(Author.id == author_id).one_or_none()
            if author is None:
                error_404 = True
                abort(404)

            body = request.get_json()

            if 'name' in body:
                author.name = body.get('name')

            if 'dob' in body:
                author.dob = body.get('dob')

            author.patch()

            return jsonify({
                'success': True,
                'id': author_id,
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/authors', methods=['DELETE'])
    def delete_author(author_id):
        error_404 = False
        try:
            author = Author.query.filter(Author.id == author_id).one_or_none()
            if author is None:
                error_404 = True
                abort(404)

            books_to_delete = Book.query.filter(Book.author_id == author_id).all()
            for book_to_delete in books_to_delete:
                book_to_delete.delete()

            author.delete()

            selection = Author.query.order_by('id').all()
            authors = paginate_elements(request, selection, False)

            return jsonify({
                'success': True,
                'deleted': author_id,
                'authors': authors,
                'total_authors': len(selection)
            })
        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    # ERROR HANDLING

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'code': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'code': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'code': 500,
            'message': 'internal server error'
        }), 500

    return app
