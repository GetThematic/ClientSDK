from unittest.mock import patch, MagicMock

import pytest

from thematic_client_sdk.themes import Themes
from thematic_client_sdk.exceptions import ThematicAPIError


def _response(status_code=200, data=None, text=""):
    response = MagicMock()
    response.status_code = status_code
    response.text = text
    response.json.return_value = {"data": data}
    return response


@patch("thematic_client_sdk.themes.requests.get")
def test_get_draft_returns_the_draft_or_none_when_there_is_none(mock_get):
    themes = Themes("token", "https://api.example.com").organization("org-1")

    mock_get.return_value = _response(data={"id": 41, "version": 3})
    assert themes.get_draft("217") == {"id": 41, "version": 3}
    args, kwargs = mock_get.call_args
    assert (
        args[0]
        == "https://api.example.com/themes/217/versions/draft?organization=org-1"
    )
    assert kwargs["headers"] == {"Authorization": "bearer token"}

    mock_get.return_value = _response(
        400, text='{"status": "error", "message": "No themes found"}'
    )
    assert themes.get_draft("217") is None

    mock_get.return_value = _response(403, text="forbidden")
    with pytest.raises(ThematicAPIError) as exc_info:
        themes.get_draft("217")
    assert exc_info.value.status_code == 403


@patch("thematic_client_sdk.themes.requests.post")
def test_apply_draft_ops_sends_the_version_and_raises_when_the_draft_changed(mock_post):
    themes = Themes("token", "https://api.example.com")
    ops = [{"type": "ReplaceThemes", "args": {"contents": {"themes1": {}}}}]

    mock_post.return_value = _response(data={"draft_id": 41, "version": 4})
    assert themes.apply_draft_ops("217", ops, draft_id=41, version=3) == {
        "draft_id": 41,
        "version": 4,
    }
    args, kwargs = mock_post.call_args
    assert args[0] == "https://api.example.com/themes/217/versions/draft/ops"
    assert kwargs["json"] == {"draft_id": 41, "version": 3, "ops": ops}

    conflict = (
        '{"status": "error", "code": "INVALID_STATE", "draft_id": 41, "version": 5}'
    )
    mock_post.return_value = _response(409, text=conflict)
    with pytest.raises(ThematicAPIError) as exc_info:
        themes.apply_draft_ops("217", ops, draft_id=41, version=3)
    assert (exc_info.value.status_code, exc_info.value.response_text) == (409, conflict)
