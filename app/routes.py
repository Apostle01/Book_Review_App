from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegistrationForm, BookForm, CommentForm
from app.models import Users, Book, Comment
from app import db, login_manager

app_bp = Blueprint('app_bp', __name__)

@app_bp.before_app_first_request
def create_tables():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app_bp.route('/')
def home():
    messages = ["Welcome to the Book Review App!", "Enjoy your stay!"]
    books = Book.query.all()
    return render_template('home.html', messages=messages, books=books)

@app_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('app_bp.home'))
        else:
            flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html', form=form)

@app_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
        new_user = Users(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful', 'success')
        return redirect(url_for('app_bp.login'))
    return render_template('register.html', form=form)

@app_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('app_bp.home'))

@app_bp.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        amazon_link = f"https://www.amazon.com/s?tag=faketag&k={form.name.data.replace(' ', '+')}"
        new_book = Book(name=form.name.data, author=form.author.data, details=form.details.data, price=form.price.data, image_link=form.image_link.data, amazon_link=amazon_link)
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
    return render_template('search.html', books=books, search_query=search_query)

@app_bp.route('/delete_book', methods=['GET', 'POST'])
@login_required
def delete_book():
    search_query = ""
    books = []

    if request.method == 'POST':
        search_query = request.form.get('search', '')
        if search_query:
            books = Book.query.filter(Book.name.contains(search_query)).all()
    return render_template('delete_book.html', books=books, search_query=search_query)

@app_bp.route('/delete_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def confirm_delete(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        try:
            Comment.query.filter_by(book_id=book.id).delete()
            db.session.delete(book)
            db.session.commit()
            flash(f'Book "{book.name}" deleted successfully', 'success')
            return redirect(url_for('app_bp.delete_book'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while trying to delete the book: {str(e)}', 'danger')

    return render_template('confirm_delete.html', book=book)

@app_bp.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(content=formcontent.data, book_id=book.id, user_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added successfully', 'success')
    return render_template('book_details.html', book=book, form=form)

@app_bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
