"""Tests standard tap features using the built-in SDK tests library."""

from __future__ import annotations

from typing import Any
from urllib.parse import ParseResult

from requests import Response
from singer_sdk.testing import get_standard_tap_tests

from tap_belvo.client import BelvoPaginator
from tap_belvo.tap import TapBelvo

SAMPLE_CONFIG: dict[str, Any] = {}


def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(TapBelvo, config=SAMPLE_CONFIG)
    for test in tests:
        test()


def test_paginator():
    """Validate paginator that uses the page offset."""
    response = Response()
    paginator = BelvoPaginator()

    assert not paginator.finished
    assert paginator.current_value is None

    response._content = (
        b'{"next": "https://sandbox.belvo.com/api/accounts/?page=2&page_size=100"}'
    )
    paginator.advance(response)
    assert not paginator.finished
    assert paginator.current_value == ParseResult(
        scheme="https",
        netloc="sandbox.belvo.com",
        path="/api/accounts/",
        params="",
        query="page=2&page_size=100",
        fragment="",
    )
    assert paginator.count == 1

    response._content = b'{"next": null}'
    paginator.advance(response)
    assert paginator.finished
    assert paginator.count == 2  # noqa: PLR2004
