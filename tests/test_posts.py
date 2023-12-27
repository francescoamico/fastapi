import pytest
from app import schemas

def test_get_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    posts = list(map(lambda post:schemas.PostOut(**post), res.json()))
    assert len(posts) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_get_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

@pytest.mark.parametrize("id, title, content", [
    (1, "1st title", "1st content"),
    (2, "2nd title", "2nd content"),
    (3, "3rd title", "3rd content")
])
def test_get_post(authorized_client, test_posts, id, title, content):
    res = authorized_client.get(f"/posts/{id}")
    
    post = schemas.PostOut(**res.json()).Post
    assert post.id == id
    assert post.title == title
    assert post.content == content
    assert res.status_code == 200

@pytest.mark.parametrize("id", [1, 2, 3])
def test_unauthorized_get_post(client, test_posts, id):
    res = client.get(f"/posts/{id}")
    assert res.status_code == 401

@pytest.mark.parametrize("id", [1, 10, 100, 1000, 1000000, 10000000])
def test_get_post_not_exists(authorized_client, id):
    res = authorized_client.get(f"/posts/{id}")
    assert res.status_code == 404

@pytest.mark.parametrize("title, content, published", [
    ("1st title", "1st content", True),
    ("2nd title", "2nd content", True),
    ("3rd title", "3rd content", False)
])
def test_create_post(authorized_client, test_user, title, content, published):
    post = schemas.PostCreate(title=title, content=content, published=published)
    res = authorized_client.post("/posts/", json=post.model_dump())

    new_post = schemas.Post(**res.json())
    assert new_post.title == title
    assert new_post.content == content
    assert new_post.published == published
    assert new_post.owner.id == test_user["id"]
    assert res.status_code == 201

def test_create_post_default_published_true(authorized_client, test_user):
    post = schemas.PostCreate(title="anytitle", content="anycontent")
    res = authorized_client.post("/posts/", json=post.model_dump())

    new_post = schemas.Post(**res.json())
    assert new_post.title == post.title
    assert new_post.content == post.content
    assert new_post.published == True
    assert new_post.owner.id == test_user["id"]
    assert res.status_code == 201

def test_unauthorized_create_post(client):
    post = schemas.PostCreate(title="anytitle", content="anycontent")
    res = client.post("/posts/", json=post.model_dump())
    assert res.status_code == 401

@pytest.mark.parametrize("id", [1, 2, 3])
def test_delete_post(authorized_client, test_posts, id):
    res = authorized_client.delete(f"/posts/{id}")
    assert res.status_code == 204

@pytest.mark.parametrize("id", [1, 10, 100, 1000, 1000000, 10000000])
def test_unauthorized_delete_post(client, id):
    res = client.delete(f"/posts/{id}")
    assert res.status_code == 401

@pytest.mark.parametrize("id", [1, 10, 100, 1000, 1000000, 10000000])
def test_delete_post_not_exists(authorized_client, id):
    res = authorized_client.delete(f"/posts/{id}")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_posts):
    post = schemas.PostCreate(title="1st title updated", content="1st content updated")
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=post.model_dump())

    new_post = schemas.Post(**res.json())
    assert new_post.title == post.title
    assert new_post.content == post.content
    assert res.status_code == 200

@pytest.mark.parametrize("id", [1, 10, 100, 1000, 1000000, 10000000])
def test_unauthorized_update_post(client, id):
    post = schemas.PostCreate(title="anycontent", content="anycontent")
    res = client.put(f"/posts/{id}", json=post.model_dump())

    assert res.status_code == 401

@pytest.mark.parametrize("id", [1, 10, 100, 1000, 1000000, 10000000])
def test_update_post_not_exists(authorized_client, id):
    post = schemas.PostCreate(title="anycontent", content="anycontent")
    res = authorized_client.put(f"/posts/{id}", json=post.model_dump())

    assert res.status_code == 404

def test_update_other_user_post(authorized_client, test_posts):
    post = schemas.PostCreate(title="1st title updated", content="1st content updated")
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=post.model_dump())
    
    assert res.status_code == 403 