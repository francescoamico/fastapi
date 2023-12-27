import pytest
from app import schemas, models

@pytest.fixture
def test_vote(authorized_client, test_posts, session, test_user):
    new_vote = models.Vote(user_id=test_user["id"], post_id=test_posts[3].id)
    session.add(new_vote)
    session.commit()

@pytest.mark.parametrize("post_id", [1, 2, 3, 4])
def test_vote_post(authorized_client, test_posts, post_id):
    vote = schemas.Vote(post_id=post_id, dir=1)
    res = authorized_client.post("/votes/", json=vote.model_dump())

    assert res.status_code == 201

def test_vote_twice(authorized_client, test_posts, test_vote):
    vote = schemas.Vote(post_id=test_posts[3].id, dir=1)
    res = authorized_client.post("/votes/", json=vote.model_dump())

    assert res.status_code == 409

def test_delete_vote(authorized_client, test_posts, test_vote):
    vote = schemas.Vote(post_id=test_posts[3].id, dir=0)
    res = authorized_client.post("/votes/", json=vote.model_dump())

    assert res.status_code == 201

def test_delete_vote_not_exists(authorized_client, test_posts):
    vote = schemas.Vote(post_id=test_posts[3].id, dir=0)
    res = authorized_client.post("/votes/", json=vote.model_dump())

    assert res.status_code == 404

@pytest.mark.parametrize("id, dir", [
    (1,0),
    (1,1)
])
def test_unauthorized_vote_post(client, id, dir):
    vote = schemas.Vote(post_id=id, dir=dir)
    res = client.post("/votes/", json=vote.model_dump())

    assert res.status_code == 401

@pytest.mark.parametrize("id, dir", [
    (1,0),
    (1,1)
])
def test_vote_post_not_exists(authorized_client, id, dir):
    vote = schemas.Vote(post_id=id, dir=dir)
    res = authorized_client.post("/votes/", json=vote.model_dump())

    assert res.status_code == 404