import datetime
from flask import Blueprint, render_template, request, redirect, Flask
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from sqlalchemy.orm import (
    # sessionmaker,
    relationship,
    DeclarativeBase,
    Session, sessionmaker,
)
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Table,
    ForeignKey,
    create_engine,
    # select, exists, Exists, except_all, except_, text
)


class Base(DeclarativeBase):
    pass


engine = create_engine('sqlite:///my_blog.db')


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False, unique=True)
    login = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=True, unique=True)
    password = Column(String, nullable=False)

    posts = relationship("Post", back_populates="user")

    def is_active(self):
        return True

    def __str__(self):
        return (
            f"{self.__class__.__name__}(user_id={self.user_id}, "
            f"username={self.username!r}, email={self.email!r})")


tags_posts_table = Table(
    'tags_posts',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
)


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    user_email = Column(Integer, ForeignKey('users.email'))

    user = relationship("User", back_populates="posts")
    tags = relationship("Tag", secondary=tags_posts_table, back_populates="posts")

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Post id: {self.id}, created_at: {self.created_date}, title : {self.title}, " \
               f"text: {self.text}, user_email: {self.user_email}"


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    tag_name = Column(String, nullable=False)

    posts = relationship("Post", secondary=tags_posts_table, back_populates="tags")

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"<Tag: {self.tag_name}>"


def create_user(
        session: Session,
        username: str,
        login: str,
        email: str,
        password: str
) -> User | None:
    user = User(
        username=username,
        login=login,
        email=email,
        password=password
    )
    session.add(user)
    print(f'Add user {user}')
    session.commit()
    return user


def create_post(
        session: Session,
        user_email: str,
        title: str,
        text: str
) -> Post:
    post = Post(
        user_email=user_email,
        title=title,
        text=text
    )
    session.add(post)
    session.commit()
    print(post)
    return post


def create_tag(
        session: Session,
        tag_name: str
) -> Tag:
    tag = Tag(
        tag_name=tag_name
    )
    session.add(tag)
    session.commit()
    return tag


def get_user_by_id(
        session: Session,
        user_id: int,
) -> User | None:
    user = session.get(User, user_id)
    return user


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
registration_app = Blueprint('registration_app', __name__)
add_film_app = Blueprint('add_film_app', __name__)
film_app = Blueprint('film_app', __name__)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


@registration_app.route('/', methods=['GET'], endpoint='registration')
def register():
    return render_template('registration.html')


@registration_app.route('/', methods=['POST'], endpoint='registration_post')
def register_post():
    data = request.form
    username = data.get('username')
    login = data.get('login')
    email = data.get('email')
    password = data.get('password')
    try:
        create_user(username, login, email, password)
    except BaseException as error:
        return render_template('registration.html', error='login занят')
    return redirect('success-reg', code=302)


@registration_app.route('/success-reg', methods=['GET'], endpoint='success-reg')
def register_success():
    return render_template('success_reg.html')


@login_manager.user_loader
def load_user(user_id):
    # return get_user_by_id(session, user_id=user_id)
    return session.query(User).get(user_id)


@app.route('/')
def home():
    auth_user = current_user.is_authenticated
    posts = session.query(Post).order_by(Post.id.desc())[0:4]
    return render_template('index.html', auth_user=auth_user, posts=posts)


@app.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login/', methods=['POST'])
def login_post():
    data = request.form
    login = data.get('login')
    password = data.get('password')
    user = session.query(User).filter(User.login == login).first()
    print(user)
    user = session.query(User).filter_by(login=login, password=password).first()
    if user:
        login_user(user)
        # login_user(User(user_id=1, username='bob1', login='bob1', email='11email@yandex.ru', password='bob12345'))
        return redirect('/')
    else:
        error = 'Неверный логин или пароль'
        return render_template('login.html', error=error)


@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'GET':
        auth_user = current_user.is_authenticated
        return render_template('logout.html', auth_user=auth_user)
    elif request.method == 'POST':
        logout_user()
        return redirect('/')


@add_film_app.route('/', endpoint='add-film')
@login_required
def page_view():
    auth_user = current_user.is_authenticated
    return render_template('add_film.html', auth_user=auth_user)


@add_film_app.route('/', methods=['POST'], endpoint='/form-add-film')
@login_required
def form_data():
    r = request.form
    film_title = r.get('film_title')
    film_text = r.get('film_text')
    create_post(film_title, film_text, current_user.username)
    return redirect('/')


@film_app.route('/', endpoint='films')
def page_view():
    auth_user = current_user.is_authenticated
    posts = session.query(Post).order_by(Post.id.desc())
    return render_template('post_page.html', auth_user=auth_user, posts=posts)


@film_app.route('/<int:post_id>', endpoint='film_view')
def film_view(post_id):
    auth_user = current_user.is_authenticated
    post = session.query(Post).filter_by(id=post_id).first()
    return render_template('post-template.html', auth_user=auth_user, post_id=id, post=post)


app.register_blueprint(add_film_app, url_prefix='/add-film')
app.register_blueprint(film_app, url_prefix='/films')
app.register_blueprint(registration_app, url_prefix='/registration')


def create_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    create_user(session=session, username='bob1', login='bob1', email='11email@yandex.ru', password='bob12345')

    create_post(session=session, user_email='new_1_email@yandex.ru', title='about_life', text='good_content')
    create_post(session=session, user_email='new_2_email@yandex.ru', title='about_weather', text='good_content_2')

    create_tag(session=session, tag_name='sience')
    create_tag(session=session, tag_name='snowboard')
    create_tag(session=session, tag_name='politics')


if __name__ == '__main__':
    create_database()
    app.run('127.0.0.1', port=5000, debug=True)
