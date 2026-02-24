import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.mark.api
def test_get_users():
    response = requests.get(f"{BASE_URL}/users")

    assert response.status_code == 200

    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 10
    assert body[0]["id"] == 1

@pytest.mark.api
def test_create_post():
    payload = {
        "title": "hello",
        "body": "world",
        "userId": 1
    }

    response = requests.post(f"{BASE_URL}/posts", json=payload)

    assert response.status_code == 201

    body = response.json()
    assert body["title"] == "hello"
    assert body["userId"] == 1


@pytest.mark.api
def test_get_users_with_client():
    from api.api_client import APIClient

    client = APIClient(base_url=BASE_URL)
    response = client.get("/users")

    assert response.status_code == 200
    assert len(response.json()) == 10

@pytest.mark.api
def test_get_posts(api_client):
    response = api_client.get(f"{api_client.base_url}/posts")

    assert response.status_code == 200, f"status={response.status_code}, body={response.text}"

    data = response.json()
    assert "posts" in data, f"Expected 'posts' key. Got: {data.keys()}"
    assert isinstance(data["posts"], list)
    assert len(data["posts"]) > 0


@pytest.mark.api
def test_get_posts(api_client):
    response = api_client.get(f"{api_client.base_url}/posts")

    assert response.status_code == 200, f"Unexpected status={response.status_code}, body={response.text}"

    data = response.json()

    # DummyJSON format: {"posts":[...], "total":..., "skip":..., "limit":...}
    if isinstance(data, dict) and "posts" in data:
        assert isinstance(data["posts"], list)
        assert len(data["posts"]) > 0
        assert "total" in data

    # JsonPlaceholder format: [...]
    elif isinstance(data, list):
        assert len(data) > 0

    else:
        pytest.fail(f"Unexpected response shape: {type(data)} -> {data}")


@pytest.mark.api
def test_api_invalid_user(api_client):
    response = api_client.get(f"{api_client.base_url}/users/9999")

    assert response.status_code == 404, f"status={response.status_code}, body={response.text}"

@pytest.mark.api
@pytest.mark.parametrize("user_id", [1, 2, 3, 4])
def test_get_single_user(api_client, user_id):
    response = api_client.get(f"{api_client.base_url}/users/{user_id}")

    assert response.status_code == 200, f"status={response.status_code}, body={response.text}"

    data = response.json()
    assert data["id"] == user_id
    assert "username" in data
    assert "email" in data