from flask_sqlalchemy import SQLAlchemy

# postgresql://postgres:1234@localhost:5432/proyecto_dbp30_final_version
database_name = 'proyecto_dbp30_final_version'
database_path = 'postgresql://{}:{}@{}:{}/{}'.format('postgres', '1234', 'localhost', '5432', database_name)
db = SQLAlchemy()


def setup_db(app, database=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    number_of_sanctions = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    email = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    books = db.relationship('Book', backref='account')

    def post(self):
        try:
            db.session.add(self)
            db.session.commit()
            created_id = self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()

        return created_id

    def patch(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def format(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'password': self.password,
            'number_of_sanctions': self.number_of_sanctions,
            'is_active': self.is_active,
            'email': self.email,
            'is_admin': self.is_admin
        }


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    ISBN = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    language = db.Column(db.String, nullable=False)
    number_of_pages = db.Column(db.Integer, nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    publisher = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    due_date = db.Column(db.Date)
    borrowed_date = db.Column(db.Date)

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)

    def post(self):
        try:
            db.session.add(self)
            db.session.commit()
            created_id = self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()

        return created_id

    def patch(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def format(self):
        return {
            'id': self.id,
            'ISBN': self.ISBN,
            'title': self.title,
            'subject': self.subject,
            'language': self.language,
            'number_of_pages': self.number_of_pages,
            'publication_date': self.publication_date,
            'publisher': self.publisher,
            'price': self.price,
            'due_date': self.due_date,
            'borrowed_date': self.borrowed_date
        }


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)

    books = db.relationship('Book', backref='author')

    def post(self):
        try:
            db.session.add(self)
            db.session.commit()
            created_id = self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()

        return created_id

    def patch(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'dob': self.dob
        }
