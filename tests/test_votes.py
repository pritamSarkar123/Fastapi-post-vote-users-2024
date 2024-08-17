import pytest

from app import models


@pytest.fixture
def test_vote(test_posts, session, test_user, test_user2):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts, test_user2):
    res = authorized_client.post(
        f"/api/v2/vote/",
        json={"post_id": test_posts[3].id, "vote_dir": 1},
    )

    assert res.status_code == 201


def test_vote_on_self_post(authorized_client, test_posts):
    res = authorized_client.post(
        f"/api/v2/vote/",
        json={"post_id": test_posts[0].id, "vote_dir": 1},
    )

    assert res.status_code == 409


def test_vote_twice_post(authorized_client, test_posts, test_user2, test_vote):
    res = authorized_client.post(
        f"/api/v2/vote/",
        json={"post_id": test_posts[3].id, "vote_dir": 1},
    )

    assert res.status_code == 409


def test_unauthorized_user_vote(client, test_posts):
    res = client.post(
        f"/api/v2/vote/",
        json={"post_id": test_posts[3].id, "vote_dir": 1},
    )

    assert res.status_code == 401


def test_down_vote(authorized_client, test_posts, test_user2, test_vote):
    res = authorized_client.post(
        f"/api/v2/vote/",
        json={"post_id": test_posts[3].id, "vote_dir": 0},
    )

    assert res.status_code == 201


def test_down_vote_not_exists(
    authorized_client, test_posts, test_user2
):  # vote not created
    res = authorized_client.post(
        f"/api/v2/vote/",
        json={"post_id": test_posts[3].id, "vote_dir": 0},
    )

    assert res.status_code == 404


def test_vote_post_not_exist(authorized_client, test_posts):
    res = authorized_client.post(
        f"/api/v2/vote/",
        json={"post_id": 9999, "vote_dir": 1},
    )

    assert res.status_code == 404
