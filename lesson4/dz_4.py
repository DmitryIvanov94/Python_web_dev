import datetime
from sqlalchemy.orm import (
    # sessionmaker,
    relationship,
    DeclarativeBase,
    Session,
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

    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False, unique=True)
    email = Column(String, nullable=True, unique=True)

    posts = relationship("Post", back_populates="user")

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
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
        email: str | None = None
) -> User:
    user = User(
        username=username,
        email=email
    )
    session.add(user)
    session.commit()
    print(user)
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


def create_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        users_list = {'bob1': '11email@yandex.ru', 'bob2': '22email@yandex.ru', 'bob3': '33email@yandex.ru'}
        for key, value in users_list.items():
            create_user(session=session, username=key, email=value)

        create_post(session=session, user_email='new_1_email@yandex.ru', title='about_life', text='good_content')
        create_post(session=session, user_email='new_2_email@yandex.ru', title='about_weather', text='good_content_2')

        create_tag(session=session, tag_name='sience')
        create_tag(session=session, tag_name='snowboard')
        create_tag(session=session, tag_name='politics')

        session.commit()


if __name__ == "__main__":
    create_database()
