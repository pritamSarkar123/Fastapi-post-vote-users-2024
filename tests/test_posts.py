from typing import List

import pytest

from app.schemas import post_schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/api/v2/post/")
    posts = res.json()
    posts = list(map(lambda post: post_schemas.PostResponseWithVote(**post), posts))
    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/api/v2/post/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/api/v2/post/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/api/v2/post/99999")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/api/v2/post/{test_posts[0].id}")
    post = post_schemas.PostResponseWithVote(**res.json())
    assert res.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("title 1", "content 1", True),
        ("title 2", "content 2", False),
        ("title 3", "content 3", True),
    ],
)
def test_create_post(
    authorized_client, test_user, title, content, published
):  # here authorized_client and test_user are fixtures and caled once for each test so both are associated with each other, user created in test_user fixture is used to create authorized_client
    res = authorized_client.post(
        "/api/v2/post/",
        json={
            "title": title,
            "content": content,
            "published": published,
        },
    )
    assert res.status_code == 201
    created = res.json()
    post_schemas.PostResponse(**created)
    assert created["content"] == content
    assert created["title"] == title
    assert created["owner_id"] == test_user["id"]
    assert created["published"] is published


def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post(
        "/api/v2/post/",
        json={
            "title": "title 1",
            "content": "content 1",
        },
    )
    assert res.status_code == 201
    created = res.json()
    assert created["published"] is True


def test_unauthorized_user_create_post(client):
    res = client.post(
        "/api/v2/post/",
        json={
            "title": "title 1",
            "content": "content 1",
        },
    )
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/api/v2/post/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f"/api/v2/post/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_not_exist(authorized_client, test_posts):
    res = authorized_client.delete(f"/api/v2/post/99999")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    # storing the already called test_user() fixture value in test_user
    # and the same value is user by authorized_client
    res = authorized_client.delete(f"/api/v2/post/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_posts):
    data = {"title": "updated title", "content": "updated content", "published": True}
    res = authorized_client.put(f"/api/v2/post/{test_posts[0].id}", json=data)
    assert res.status_code == 200
    updated = post_schemas.PostResponse(**res.json())
    assert updated.title == data["title"]
    assert updated.content == data["content"]


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {"title": "updated title", "content": "updated content", "published": True}
    res = authorized_client.put(f"/api/v2/post/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_posts):
    data = {"title": "updated title", "content": "updated content", "published": True}
    res = client.put(f"/api/v2/post/{test_posts[0].id}", json=data)
    assert res.status_code == 401


def test_update_post_not_exist(authorized_client, test_posts):
    data = {"title": "updated title", "content": "updated content", "published": True}
    res = authorized_client.put(f"/api/v2/post/99999", json=data)
    assert res.status_code == 404
