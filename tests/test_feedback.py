from unittest.mock import patch, MagicMock

import pytest

from thematic_client_sdk.feedback import Feedback
from thematic_client_sdk.exceptions import ThematicAPIError


def _ok_response(data=None):
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {"data": data if data is not None else {"ok": True}}
    return response


def _error_response(status_code=400, text="bad request"):
    response = MagicMock()
    response.status_code = status_code
    response.text = text
    return response


@patch("thematic_client_sdk.feedback.requests.post")
def test_create_sends_required_field_only(mock_post):
    mock_post.return_value = _ok_response({"id": 1})
    feedback = Feedback("token", "https://api.example.com")

    result = feedback.create("my-feature")

    assert result == {"id": 1}
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert args[0] == "https://api.example.com/feedback"
    assert kwargs["json"] == {"featureId": "my-feature"}
    assert kwargs["headers"] == {"Authorization": "bearer token"}
    assert kwargs["timeout"] == 30


@patch("thematic_client_sdk.feedback.requests.post")
def test_create_includes_optional_fields(mock_post):
    mock_post.return_value = _ok_response()
    feedback = Feedback("token", "https://api.example.com")

    feedback.create(
        "my-feature",
        description="great",
        rating=5,
        data={"foo": "bar"},
        location={"view": "dashboard"},
    )

    _, kwargs = mock_post.call_args
    assert kwargs["json"] == {
        "featureId": "my-feature",
        "description": "great",
        "rating": 5,
        "data": {"foo": "bar"},
        "location": {"view": "dashboard"},
    }


@patch("thematic_client_sdk.feedback.requests.post")
def test_create_omits_none_optional_fields(mock_post):
    mock_post.return_value = _ok_response()
    feedback = Feedback("token", "https://api.example.com")

    feedback.create("my-feature", description="only this", rating=None)

    _, kwargs = mock_post.call_args
    assert kwargs["json"] == {"featureId": "my-feature", "description": "only this"}


@patch("thematic_client_sdk.feedback.requests.post")
def test_create_uses_organization_query_param(mock_post):
    mock_post.return_value = _ok_response()
    feedback = Feedback("token", "https://api.example.com")
    feedback.organization("org-123")

    feedback.create("my-feature")

    args, _ = mock_post.call_args
    assert args[0] == "https://api.example.com/feedback?organization=org-123"


@patch("thematic_client_sdk.feedback.requests.post")
def test_create_raises_on_non_200(mock_post):
    mock_post.return_value = _error_response(500, "boom")
    feedback = Feedback("token", "https://api.example.com")

    with pytest.raises(ThematicAPIError) as exc_info:
        feedback.create("my-feature")

    assert exc_info.value.status_code == 500
    assert exc_info.value.response_text == "boom"
