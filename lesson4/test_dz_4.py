from lesson4.dz_4 import User, Post, engine
from typing import Sequence
from sqlalchemy.orm import Session
from sqlalchemy import func, select


def get_users(
        session: Session,
) -> Sequence[User]:
    stmt = (
        select(User)
    )
    users = session.scalars(stmt).all()
    return users


def get_user_id_by_email(
        session: Session,
        user_email: str,
) -> dict | None:
    stmt = select(User.id, User.username, User.email).where(
        func.lower(User.email) == user_email)
    user = session.scalar(stmt)
    return user


def get_post_title_by_text(
        session: Session,
        post_text: str,
) -> str | None:
    stmt = select(Post.title).where(
        func.lower(Post.text) == post_text)
    post = session.scalar(stmt)
    return post


def test_get_all_users():
    with Session(engine) as session:
        all_users = get_users(session)
        # print(all_users)
        assert len(all_users) == 3


def test_get_user_id_by_email():
    with Session(engine) as session:
        user_id = get_user_id_by_email(session, '22email@yandex.ru')
        assert user_id == 2


def test_get_post_title_by_text():
    with Session(engine) as session:
        post_title = get_post_title_by_text(session, 'good_content')
        assert post_title == 'about_life'
