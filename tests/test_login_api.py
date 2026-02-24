import pytest

@pytest.mark.api
def test_login_api_success():
    from api.auth_api import AuthAPI

    api = AuthAPI()
    response = api.login("emilys", "emilyspass")

    print("Status:", response.status_code)
    print("Body:", response.text)

    data = response.json()
    assert response.status_code == 200
    assert "accessToken" in data
    assert "refreshToken" in data

