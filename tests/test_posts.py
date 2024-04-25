import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts/')
    def validate(post):
        return schemas.PostOut(**post)
    
    post_map = map(validate, res.json())
    post_list = list(post_map)
    # Sort post_list by id in ascending order
    post_list = sorted(post_list, key=lambda post: post.Post.id)

    # Check agains Schemas (PostOut) 
    for i in range(len(post_list)):
        assert  post_list[i].Post.id == test_posts[i].id  
    
    # Check we are passing the same lenght of posts
    assert len(res.json()) == len(test_posts)
    
    # Check Status Code
    assert res.status_code == 200
   

# Checking for 401, note this function is not using authorized_client as param
def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get('/posts/')
    assert res.status_code == 401
    

# Checking for 401, note this function is not using authorized_client as param
def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401
    

# For this test we do get a authorized_client, create the posts with test_posts and try a post that does not exist
def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get('/posts/88888888')
    assert res.status_code == 404
    
    
def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')
    
    # this below converts json to a pydantic model in this case a PostOut Schema this is an example of the output:
    # ****Post*****=ForPostOut(id=1, title='First Title', content='First Content', created_at=datetime.datetime(2024, 4, 24, 
    # 15, 42, 48, 957365, tzinfo=TzInfo(-04:00)), user=UserOut(id=1, email='test_user_email@gmail.com', 
    # created_at=datetime.datetime(2024, 4, 24, 15, 42, 48, 747968, tzinfo=TzInfo(-04:00)))) votes=0
    post = schemas.PostOut(**res.json())
    # ****Post*****
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title
    assert res.status_code == 200


@pytest.mark.parametrize('title, content, published',[
    ('awsome new title', 'awsome new content', True),
    ('favorite pizza', 'i love peperoni', False),
    ('tallest skyscrapers', 'wahoo', True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post('/posts/', json={'title':title, 'content':content, 'published':published})
    created_post = schemas.Post(**res.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user['id']
    assert res.status_code == 201
    

# Checking if published is set to True by default as et on the schema (PostBase)
def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post('/posts/', json={'title':'Any Title', 'content':'Any Content'})
    created_post = schemas.Post(**res.json())
    assert created_post.title == 'Any Title'
    assert created_post.content == 'Any Content'
    assert created_post.published is True
    assert created_post.user_id == test_user['id']
    assert res.status_code == 201
    
def test_unauthorized_user_create_posts(client, test_user, test_posts):
    res = client.post('/posts/', json={'title':'Any Title', 'content':'Any Content'})
    assert res.status_code == 401


def test_unauthorized_user_delete_posts(client, test_user, test_posts):
    res = client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401
    
    
def test_delete_post_success(authorized_client,test_user, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 204
    
def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete('/posts/88888888')
    assert res.status_code == 404
    
def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[3].id}')
    assert res.status_code == 403
    
def test_update_post(authorized_client, test_user, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[0].id
    }
    res = authorized_client.put(f'/posts/{test_posts[0].id}', json=data)
    updated_post = schemas.Post(**res.json())
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert res.status_code == 200
   
    
def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[3].id
    }
    
    res = authorized_client.put(f'/posts/{test_posts[3].id}', json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_posts(client, test_user, test_posts):
    res = client.put(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401 

def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[3].id
    }
    res = authorized_client.put('/posts/88888888', json=data)
    assert res.status_code == 404
    
