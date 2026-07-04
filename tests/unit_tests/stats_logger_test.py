# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import logging
from unittest.mock import MagicMock

import pytest

from superset.stats_logger import BaseStatsLogger, DummyStatsLogger, StatsdStatsLogger


def _has_statsd() -> bool:
    try:
        import statsd  # noqa: F401

        return True
    except ModuleNotFoundError:
        return False


def test_base_stats_logger_key_with_prefix():
    logger = BaseStatsLogger(prefix="myapp")
    assert logger.key(".requests") == "myapp.requests"


def test_base_stats_logger_key_without_prefix():
    logger = BaseStatsLogger(prefix="")
    assert logger.key("requests") == "requests"


def test_base_stats_logger_default_prefix():
    logger = BaseStatsLogger()
    assert logger.prefix == "superset"
    assert logger.key(".count") == "superset.count"


def test_base_stats_logger_incr_raises():
    logger = BaseStatsLogger()
    with pytest.raises(NotImplementedError):
        logger.incr("key")


def test_base_stats_logger_decr_raises():
    logger = BaseStatsLogger()
    with pytest.raises(NotImplementedError):
        logger.decr("key")


def test_base_stats_logger_timing_raises():
    logger = BaseStatsLogger()
    with pytest.raises(NotImplementedError):
        logger.timing("key", 1.0)


def test_base_stats_logger_gauge_raises():
    logger = BaseStatsLogger()
    with pytest.raises(NotImplementedError):
        logger.gauge("key", 1.0)


def test_dummy_stats_logger_incr(caplog: pytest.LogCaptureFixture):
    logger = DummyStatsLogger()
    with caplog.at_level(logging.DEBUG):
        logger.incr("test_key")
    assert "test_key" in caplog.text


def test_dummy_stats_logger_decr(caplog: pytest.LogCaptureFixture):
    logger = DummyStatsLogger()
    with caplog.at_level(logging.DEBUG):
        logger.decr("test_key")
    assert "test_key" in caplog.text


def test_dummy_stats_logger_timing(caplog: pytest.LogCaptureFixture):
    logger = DummyStatsLogger()
    with caplog.at_level(logging.DEBUG):
        logger.timing("test_key", 42.5)
    assert "test_key" in caplog.text
    assert "42.5" in caplog.text


def test_dummy_stats_logger_gauge(caplog: pytest.LogCaptureFixture):
    logger = DummyStatsLogger()
    with caplog.at_level(logging.DEBUG):
        logger.gauge("test_key", 99.0)
    assert "test_key" in caplog.text


def test_statsd_stats_logger_fallback_raises_without_statsd():
    try:
        import statsd  # noqa: F401

        pytest.skip("statsd is installed; fallback path not exercised")
    except ModuleNotFoundError:
        pass

    with pytest.raises(ModuleNotFoundError):
        StatsdStatsLogger(statsd_client=MagicMock())


@pytest.mark.skipif(
    not _has_statsd(),
    reason="statsd package not installed",
)
def test_statsd_stats_logger_with_client():
    mock_client = MagicMock()
    logger = StatsdStatsLogger(statsd_client=mock_client)
    logger.incr("key")
    mock_client.incr.assert_called_once_with("key")


@pytest.mark.skipif(
    not _has_statsd(),
    reason="statsd package not installed",
)
def test_statsd_stats_logger_decr_with_client():
    mock_client = MagicMock()
    logger = StatsdStatsLogger(statsd_client=mock_client)
    logger.decr("key")
    mock_client.decr.assert_called_once_with("key")


@pytest.mark.skipif(
    not _has_statsd(),
    reason="statsd package not installed",
)
def test_statsd_stats_logger_timing_with_client():
    mock_client = MagicMock()
    logger = StatsdStatsLogger(statsd_client=mock_client)
    logger.timing("key", 3.14)
    mock_client.timing.assert_called_once_with("key", 3.14)


@pytest.mark.skipif(
    not _has_statsd(),
    reason="statsd package not installed",
)
def test_statsd_stats_logger_gauge_with_client():
    mock_client = MagicMock()
    logger = StatsdStatsLogger(statsd_client=mock_client)
    logger.gauge("key", 100.0)
    mock_client.gauge.assert_called_once_with("key", 100.0)
