# package specific package should present here
# package and subpackage will get this
# if subpackage have another conftest.py then the subpackage and its sub pagkage will have access to that file, not the current outer package
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import get_db
from app.main import app
from app.models import Base, Post
from app.utils.oauth2 import create_access_token

# from alembic import command

# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:root@localhost:5433/fastapi_test"

####################### ---->>
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


## **** in function scoped fixtures, they are called once for each test

####################### << ---- one timer fixture not needed


# @pytest.fixture
# def client():
#     Base.metadata.create_all(bind=engine)
#     yield TestClient(app)
#     Base.metadata.drop_all(bind=engine)


# @pytest.fixture
# def client():
#     command.upgrade("head")
#     yield TestClient(app)
#     command.downgrade("base")
##<- little slower then sqlalchemy and different db making complex, alembic based


# @pytest.fixture
# def client():
#     Base.metadata.drop_all(bind=engine)  # clear before the next test runs
#     # for this we can check for what reason in db the test fails
#     # it does not clears up until the next test starts
#     # best for -x mode [stop at initial failure]
#     Base.metadata.create_all(bind=engine)
#     yield TestClient(app)


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user2(client):
    user_data = {"email": "j@j2.com", "password": "password"}
    res = client.post("/api/v2/user/create/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {"email": "j@j.com", "password": "password"}
    res = client.post("/api/v2/user/create/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}",
    }
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user["id"],
        },
        {"title": "2nd title", "content": "2nd content", "owner_id": test_user["id"]},
        {"title": "3rd title", "content": "3rd content", "owner_id": test_user["id"]},
        {"title": "4th title", "content": "4th content", "owner_id": test_user2["id"]},
        {"title": "5th title", "content": "5th content", "owner_id": test_user2["id"]},
    ]

    def create_post(params):
        return Post(**params)

    post_map = map(create_post, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(Post).all()

    return posts
