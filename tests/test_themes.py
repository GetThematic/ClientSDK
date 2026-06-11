from unittest.mock import patch, MagicMock

import pytest

from thematic_client_sdk.themes import Themes
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


@patch("thematic_client_sdk.themes.requests.post")
def test_backfill_mapped_phrases_sends_all_options(mock_post):
    mock_post.return_value = _ok_response({})
    themes = Themes("token", "https://api.example.com")

    result = themes.backfill_mapped_phrases(
        "L12",
        rql_filter="(date=ge=2026-05-01;date=le=2026-05-31)",
        completion_callback="workflow://wf-1/run-1",
    )

    assert result == {}
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert args[0] == "https://api.example.com/themes/L12/backfill-mapped-phrases"
    assert kwargs["json"] == {
        "filter": "(date=ge=2026-05-01;date=le=2026-05-31)",
        "completionCallback": "workflow://wf-1/run-1",
    }
    assert kwargs["headers"] == {"Authorization": "bearer token"}
    assert kwargs["timeout"] == 30


@patch("thematic_client_sdk.themes.requests.post")
def test_backfill_mapped_phrases_defaults_to_empty_body(mock_post):
    mock_post.return_value = _ok_response({})
    themes = Themes("token", "https://api.example.com")

    themes.backfill_mapped_phrases("57")

    _, kwargs = mock_post.call_args
    assert kwargs["json"] == {}


@patch("thematic_client_sdk.themes.requests.post")
def test_backfill_mapped_phrases_raises_on_error(mock_post):
    mock_post.return_value = _error_response(status_code=400, text="draft exists")
    themes = Themes("token", "https://api.example.com")

    with pytest.raises(ThematicAPIError) as excinfo:
        themes.backfill_mapped_phrases("57")

    assert excinfo.value.status_code == 400
    assert "draft exists" in str(excinfo.value)
