from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app import models
from app.config import settings
from app.database import Base, get_db
from app.main import app
from app.oauth2 import create_access_token

# Note: All The fixtures that you define om conftest.py will be shared among all tests in your test suite, no need to import it. 

# **START** Inititate a Testing DB
#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# The @pytest.fixture(scope='module') lets me keep this fixure for all the module, thismeans it will not start over for each function
# by default this is set as scope='function', the problem with leaving it with function ist hat it will drop all tables 
# for each function on the test module. The problem with using this scope='module' is that one function testing will
# depend of other fucntions testing, and this is not righ, each testing should be independent. So we keep the default.
@pytest.fixture()
def session():
    # This way to catch errors and see what was saved on the DB (use the -x flag on pytest command)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # Example Using Alembic
    # from alembic import command
    # command.upgrade('head')
    # yield TestClient(app)
    # command.downgrade('base')
    
    # This is one way to do it
    # # Create the tables before the test
    # Base.metadata.create_all(bind=engine)
    # # Test
    # yield TestClient(app)
    # # Delete the tables after testing has ended
    # Base.metadata.drop_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
# **END** Inititate a Testing DB


@pytest.fixture
def test_user(client):
    user_data = {'email': 'test_user_email@gmail.com', 'password': 'password123'}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

# Create a second user to test 'test_delete_other_user_post'
@pytest.fixture
def test_user2(client):
    user_data = {'email': 'test_user_email2@gmail.com', 'password': 'password123'}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user



@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token}'
    }
    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    
    # #This is one way to do this
    # session.add_all([models.Post(title='First Title',content='First Content', user_id=test_user['id'])],
    #                [models.Post(title='Second Title',content='Second Content', user_id=test_user['id'])],
    #                [models.Post(title='Third Title',content='Third Content', user_id=test_user['id'])])
    
    # session.commit()
    # posts = session.query(models.Post).all()
    
    # return posts
    
    # This is the second way (better... well not sure if its better but it helps understand how to go from a dict to models)
    
    posts_data = [{
        'title': 'First Title',
        'content': 'First Content',
        'user_id': test_user['id']
    },{
        'title': 'Second Title',
        'content': 'Second Content',
        'user_id': test_user['id']
    },{
        'title': 'Third Title',
        'content': 'Third Content',
        'user_id': test_user['id']
    },{
        'title': 'Fourth Title',
        'content': 'Fourth Content',
        'user_id': test_user2['id']
    }]
    
    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, posts_data)
    post = list(post_map)
    session.add_all(post)
    session.commit()
    posts = session.query(models.Post).order_by(models.Post.id).all()
    return posts