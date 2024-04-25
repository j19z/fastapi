import pytest
from app import models

@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    data = {
        "post_id":test_posts[3].id,
        "dir": True
        }
    res = authorized_client.post('/vote/', json=data)
    assert res.status_code == 201


def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post('/vote/', json={"post_id":test_posts[3].id, "dir": True})
    assert res.status_code == 409
    
    
def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post('/vote/', json={"post_id":test_posts[3].id, "dir": False})
    assert res.status_code == 201


def test_delete_vote_non_exist(authorized_client, test_posts):
    # res = authorized_client.post('/vote/', json={"post_id":'88888888', "dir": False})
    res = authorized_client.post('/vote/', json={"post_id":test_posts[3].id, "dir": False})
    assert res.status_code == 404
    
    
def test_vote_non_exist(authorized_client, test_posts):
    # res = authorized_client.post('/vote/', json={"post_id":'88888888', "dir": False})
    res = authorized_client.post('/vote/', json={"post_id":88888888, "dir": True})
    assert res.status_code == 404
    
    
def test_vote_unauthorized_user(client, test_posts):
    # res = authorized_client.post('/vote/', json={"post_id":'88888888', "dir": False})
    res = client.post('/vote/', json={"post_id":test_posts[3].id, "dir": True})
    assert res.status_code == 401