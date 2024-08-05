from flask import Blueprint, render_template, url_for, flash, session, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegistrationForm, BookForm, CommentForm
from app.models import Users, Book, Comment
import logging
from main import db

app_bp = Blueprint('app_bp', __name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app_bp.route('/')
def home():
    messages = ["Welcome to the Book Review App!", "Enjoy your stay!"]
    return render_template('home.html', messages=messages)

@app_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Login successful', 'success')
            return redirect(url_for('app_bp.home'))
        else:
            flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html', form=form)

@app_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data, method='pbkdf2:sha256', salt_length=8
        )
        new_user = Users(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful', 'success')
        return redirect(url_for('app_bp.login'))
    return render_template('register.html', form=form)

@app_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('app_bp.home'))

@app_bp.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        amazon_link = (
            f"https://www.amazon.com/s?tag=faketag&k="
            f"{form.name.data.replace(' ', '+')}"
        )
        new_book = Book(
            name=form.name.data,
            author=form.author.data,
            details=form.details.data,
            price=form.price.data,
            image_link=form.image_link.data,
            amazon_link=amazon_link
        )
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully', 'success')
        return redirect(url_for('app_bp.search'))
    return render_template('add_book.html', form=form)

@app_bp.route('/search', methods=['GET', 'POST'])
def search():
    search_query = ""
    books = []

    if request.method == 'POST':
        search_query = request.form.get('search', '')
        if search_query:
            books = Book.query.filter(Book.name.contains(search_query)).all()
    return render_template(
        'search.html', books=books, search_query=search_query
    )

@app_bp.route('/delete_book', methods=['GET', 'POST'])
def delete_book():
    search_query = ""
    books = []

    if request.method == 'POST':
        search_query = request.form.get('search', '')
        if search_query:
            books = Book.query.filter(Book.name.contains(search_query)).all()

    return render_template(
        'delete_book.html', books=books, search_query=search_query
    )

@app_bp.route('/delete_book/<int:book_id>', methods=['GET', 'POST'])
def confirm_delete(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        try:
            # Delete associated comments
            Comment.query.filter_by(book_id=book.id).delete()
            db.session.delete(book)
            db.session.commit()
            flash(f'Book "{book.name}" deleted successfully', 'success')
            return redirect(url_for('app_bp.delete_book'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error deleting book: {e}')
            flash(
                f'An error occurred while trying to delete the book: {str(e)}',
                'danger'
            )

    return render_template('confirm_delete.html', book=book)

@app_bp.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(content=form.content.data, book_id=book.id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added successfully', 'success')
    return render_template('book_details.html', book=book, form=form)

@app_bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# from flask import Blueprint, render_template, url_for, flash, session, request, redirect
# from werkzeug.security import generate_password_hash, check_password_hash
# from app.forms import LoginForm, RegistrationForm, BookForm, CommentForm
# import logging
# from app import db

# app_bp = Blueprint('app_bp', __name__)

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# @app_bp.route('/')
# def home():
#     messages = ["Welcome to the Book Review App!", "Enjoy your stay!"]
#     return render_template('home.html', messages=messages)

# @app_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     from app.models import Users  # type: ignore # Local import to avoid circular dependency
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(email=form.email.data).first()
#         if user and check_password_hash(user.password, form.password.data):
#             session['user_id'] = user.id
#             flash('Login successful', 'success')
#             return redirect(url_for('app_bp.home'))
#         else:
#             flash('Login failed. Check your credentials.', 'danger')
#     return render_template('login.html', form=form)

# @app_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     from app.models import Users  # type: ignore # Local import to avoid circular dependency
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
#         new_user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         flash('Registration successful', 'success')
#         return redirect(url_for('app_bp.login'))
#     return render_template('register.html', form=form)

# @app_bp.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     flash('You have been logged out', 'info')
#     return redirect(url_for('app_bp.home'))

# @app_bp.route('/add_book', methods=['GET', 'POST'])
# def add_book():
#     from app.models import Book  # type: ignore # Local import to avoid circular dependency
#     form = BookForm()
#     if form.validate_on_submit():
#         amazon_link = f"https://www.amazon.com/s?tag=faketag&k={form.name.data.replace(' ', '+')}"
#         new_book = Book(
#             name=form.name.data,
#             author=form.author.data,
#             details=form.details.data,
#             price=form.price.data,
#             image_link=form.image_link.data,
#             amazon_link=amazon_link
#         )
#         db.session.add(new_book)
#         db.session.commit()
#         flash('Book added successfully', 'success')
#         return redirect(url_for('app_bp.search'))
#     return render_template('add_book.html', form=form)

# @app_bp.route('/search', methods=['GET', 'POST'])
# def search():
#     from app.models import Book  # type: ignore # Local import to avoid circular dependency
#     search_query = ""
#     books = []

#     if request.method == 'POST':
#         search_query = request.form.get('search', '')
#         if search_query:
#             books = Book.query.filter(Book.name.contains(search_query)).all()
#     return render_template('search.html', books=books, search_query=search_query)

# @app_bp.route('/delete_book', methods=['GET', 'POST'])
# def delete_book():
#     from app.models import Book  # type: ignore # Local import to avoid circular dependency
#     search_query = ""
#     books = []

#     if request.method == 'POST':
#         search_query = request.form.get('search', '')
#         if search_query:
#             books = Book.query.filter(Book.name.contains(search_query)).all()

#     return render_template('delete_book.html', books=books, search_query=search_query)

# @app_bp.route('/delete_book/<int:book_id>', methods=['GET', 'POST'])
# def confirm_delete(book_id):
#     from app.models import Book, Comment  # type: ignore # Local import to avoid circular dependency
#     book = Book.query.get_or_404(book_id)

#     if request.method == 'POST':
#         try:
#             # Delete associated comments
#             Comment.query.filter_by(book_id=book.id).delete()
#             db.session.delete(book)
#             db.session.commit()
#             flash(f'Book "{book.name}" deleted successfully', 'success')
#             return redirect(url_for('app_bp.delete_book'))
#         except Exception as e:
#             db.session.rollback()
#             logger.error(f'Error deleting book: {e}')
#             flash(f'An error occurred while trying to delete the book: {str(e)}', 'danger')

#     return render_template('confirm_delete.html', book=book)

# @app_bp.route('/book/<int:book_id>', methods=['GET', 'POST'])
# def book_details(book_id):
#     from app.models import Book, Comment  # type: ignore # Local import to avoid circular dependency
#     book = Book.query.get_or_404(book_id)
#     form = CommentForm()
#     if form.validate_on_submit():
#         new_comment = Comment(content=form.content.data, book_id=book.id)
#         db.session.add(new_comment)
#         db.session.commit()
#         flash('Comment added successfully', 'success')
#     return render_template('book_details.html', book=book, form=form)

# @app_bp.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404



# if __name__ == '__main__':
#    port = int(os.environ.get('PORT', 5000))
#    app.run(host='127.0.0.1', port=5000, debug=True)

