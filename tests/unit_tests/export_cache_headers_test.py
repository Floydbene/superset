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

# pylint: disable=invalid-name, import-outside-toplevel, unused-argument

"""
Tests verifying that export download endpoints set Cache-Control: no-store
rather than inheriting the application-wide SEND_FILE_MAX_AGE_DEFAULT (1 year).
"""

from io import BytesIO
from typing import Any
from unittest.mock import MagicMock
from zipfile import is_zipfile

import pytest
from pytest_mock import MockerFixture

# ---------------------------------------------------------------------------
# Chart export
# ---------------------------------------------------------------------------


def test_chart_export_has_no_store_cache_header(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """Export chart response must include Cache-Control: no-store."""
    mocked_export_result = [
        ("metadata.yaml", lambda: "version: 1.0.0\ntype: Slice\n"),
        ("charts/example.yaml", lambda: "<CHART CONTENTS>"),
    ]

    ExportChartsCommand = mocker.patch(  # noqa: N806
        "superset.charts.api.ExportChartsCommand"
    )
    ExportChartsCommand().run.return_value = mocked_export_result[:]

    response = client.get("/api/v1/chart/export/?q=[1]")
    assert response.status_code == 200
    assert response.headers["Cache-Control"] == "no-store"


def test_chart_export_response_is_valid_zip_attachment(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """Export chart response must be a ZIP attachment with correct headers."""
    mocked_export_result = [
        ("metadata.yaml", lambda: "version: 1.0.0\ntype: Slice\n"),
        ("charts/example.yaml", lambda: "<CHART CONTENTS>"),
    ]

    ExportChartsCommand = mocker.patch(  # noqa: N806
        "superset.charts.api.ExportChartsCommand"
    )
    ExportChartsCommand().run.return_value = mocked_export_result[:]

    response = client.get("/api/v1/chart/export/?q=[1]")
    assert response.status_code == 200
    assert response.content_type == "application/zip"
    assert "attachment" in response.headers.get("Content-Disposition", "")
    assert is_zipfile(BytesIO(response.data))
    assert response.headers["Cache-Control"] == "no-store"


def test_chart_export_cache_header_with_token_param(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """Cache-Control: no-store must be present even with a download token."""
    mocked_export_result = [
        ("metadata.yaml", lambda: "version: 1.0.0\ntype: Slice\n"),
        ("charts/example.yaml", lambda: "<CHART CONTENTS>"),
    ]

    ExportChartsCommand = mocker.patch(  # noqa: N806
        "superset.charts.api.ExportChartsCommand"
    )
    ExportChartsCommand().run.return_value = mocked_export_result[:]

    response = client.get("/api/v1/chart/export/?q=[1]&token=abc123")
    assert response.status_code == 200
    assert response.headers["Cache-Control"] == "no-store"


def test_chart_export_does_not_contain_max_age(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """Export must not have max-age in Cache-Control (no long-lived caching)."""
    mocked_export_result = [
        ("metadata.yaml", lambda: "version: 1.0.0\ntype: Slice\n"),
        ("charts/example.yaml", lambda: "<CHART CONTENTS>"),
    ]

    ExportChartsCommand = mocker.patch(  # noqa: N806
        "superset.charts.api.ExportChartsCommand"
    )
    ExportChartsCommand().run.return_value = mocked_export_result[:]

    response = client.get("/api/v1/chart/export/?q=[1]")
    assert response.status_code == 200
    cache_control = response.headers["Cache-Control"]
    assert "max-age" not in cache_control


# ---------------------------------------------------------------------------
# Dashboard export
# ---------------------------------------------------------------------------


def test_dashboard_export_has_no_store_cache_header(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """Export dashboard response must include Cache-Control: no-store."""
    mocked_export_result = [
        ("metadata.yaml", lambda: "version: 1.0.0\ntype: Dashboard\n"),
        ("dashboards/example.yaml", lambda: "<DASHBOARD CONTENTS>"),
    ]

    ExportDashboardsCommand = mocker.patch(  # noqa: N806
        "superset.dashboards.api.ExportDashboardsCommand"
    )
    ExportDashboardsCommand().run.return_value = mocked_export_result[:]

    response = client.get("/api/v1/dashboard/export/?q=[1]")
    assert response.status_code == 200
    assert response.headers["Cache-Control"] == "no-store"


def test_dashboard_export_response_is_valid_zip_attachment(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """Export dashboard must return a ZIP with correct content headers."""
    mocked_export_result = [
        ("metadata.yaml", lambda: "version: 1.0.0\ntype: Dashboard\n"),
        ("dashboards/example.yaml", lambda: "<DASHBOARD CONTENTS>"),
    ]

    ExportDashboardsCommand = mocker.patch(  # noqa: N806
        "superset.dashboards.api.ExportDashboardsCommand"
    )
    ExportDashboardsCommand().run.return_value = mocked_export_result[:]

    response = client.get("/api/v1/dashboard/export/?q=[1]")
    assert response.status_code == 200
    assert response.content_type == "application/zip"
    assert "attachment" in response.headers.get("Content-Disposition", "")
    assert is_zipfile(BytesIO(response.data))
    assert response.headers["Cache-Control"] == "no-store"


def test_dashboard_export_cache_header_with_token_param(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """Cache-Control: no-store must be present with a download token."""
    mocked_export_result = [
        ("metadata.yaml", lambda: "version: 1.0.0\ntype: Dashboard\n"),
        ("dashboards/example.yaml", lambda: "<DASHBOARD CONTENTS>"),
    ]

    ExportDashboardsCommand = mocker.patch(  # noqa: N806
        "superset.dashboards.api.ExportDashboardsCommand"
    )
    ExportDashboardsCommand().run.return_value = mocked_export_result[:]

    response = client.get("/api/v1/dashboard/export/?q=[1]&token=xyz789")
    assert response.status_code == 200
    assert response.headers["Cache-Control"] == "no-store"


def test_dashboard_export_does_not_contain_max_age(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """Dashboard export must not have max-age in Cache-Control."""
    mocked_export_result = [
        ("metadata.yaml", lambda: "version: 1.0.0\ntype: Dashboard\n"),
        ("dashboards/example.yaml", lambda: "<DASHBOARD CONTENTS>"),
    ]

    ExportDashboardsCommand = mocker.patch(  # noqa: N806
        "superset.dashboards.api.ExportDashboardsCommand"
    )
    ExportDashboardsCommand().run.return_value = mocked_export_result[:]

    response = client.get("/api/v1/dashboard/export/?q=[1]")
    assert response.status_code == 200
    cache_control = response.headers["Cache-Control"]
    assert "max-age" not in cache_control


# ---------------------------------------------------------------------------
# Dashboard export_as_example
# ---------------------------------------------------------------------------


def test_dashboard_export_as_example_has_no_store_cache_header(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """export_as_example response must include Cache-Control: no-store."""
    ExportExampleCommand = mocker.patch(  # noqa: N806
        "superset.dashboards.api.ExportExampleCommand"
    )
    ExportExampleCommand().run.return_value = [
        ("metadata.yaml", lambda: "version: 1.0.0\n"),
    ]

    # Mock the datamodel.get to return a dashboard object with a slug
    mock_dashboard = MagicMock()
    mock_dashboard.slug = "test-dashboard"
    mocker.patch(
        "superset.dashboards.api.DashboardRestApi.datamodel"
    ).get.return_value = mock_dashboard

    response = client.get("/api/v1/dashboard/1/export_as_example/")
    assert response.status_code == 200
    assert response.headers["Cache-Control"] == "no-store"


def test_dashboard_export_as_example_response_is_valid_zip(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """export_as_example must return a ZIP attachment with no caching."""
    ExportExampleCommand = mocker.patch(  # noqa: N806
        "superset.dashboards.api.ExportExampleCommand"
    )
    ExportExampleCommand().run.return_value = [
        ("metadata.yaml", lambda: "version: 1.0.0\n"),
        ("dashboards/test.yaml", lambda: "<DASHBOARD>"),
    ]

    mock_dashboard = MagicMock()
    mock_dashboard.slug = "my-slug"
    mocker.patch(
        "superset.dashboards.api.DashboardRestApi.datamodel"
    ).get.return_value = mock_dashboard

    response = client.get("/api/v1/dashboard/1/export_as_example/")
    assert response.status_code == 200
    assert response.content_type == "application/zip"
    assert "attachment" in response.headers.get("Content-Disposition", "")
    assert "my-slug_example.zip" in response.headers.get("Content-Disposition", "")
    assert is_zipfile(BytesIO(response.data))
    assert response.headers["Cache-Control"] == "no-store"


def test_dashboard_export_as_example_cache_header_with_token(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """export_as_example must set no-store even when token query param is present."""
    ExportExampleCommand = mocker.patch(  # noqa: N806
        "superset.dashboards.api.ExportExampleCommand"
    )
    ExportExampleCommand().run.return_value = [
        ("metadata.yaml", lambda: "version: 1.0.0\n"),
    ]

    mock_dashboard = MagicMock()
    mock_dashboard.slug = "dash"
    mocker.patch(
        "superset.dashboards.api.DashboardRestApi.datamodel"
    ).get.return_value = mock_dashboard

    response = client.get("/api/v1/dashboard/1/export_as_example/?token=tok123")
    assert response.status_code == 200
    assert response.headers["Cache-Control"] == "no-store"


# ---------------------------------------------------------------------------
# Dataset export
# ---------------------------------------------------------------------------


def test_dataset_export_has_no_store_cache_header(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """Export dataset response must include Cache-Control: no-store."""
    mocked_export_result = [
        ("metadata.yaml", lambda: "version: 1.0.0\ntype: SqlaTable\n"),
        ("datasets/example.yaml", lambda: "<DATASET CONTENTS>"),
    ]

    ExportDatasetsCommand = mocker.patch(  # noqa: N806
        "superset.datasets.api.ExportDatasetsCommand"
    )
    ExportDatasetsCommand().run.return_value = mocked_export_result[:]

    response = client.get("/api/v1/dataset/export/?q=[1]")
    assert response.status_code == 200
    assert response.headers["Cache-Control"] == "no-store"


def test_dataset_export_response_is_valid_zip_attachment(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """Export dataset must return a ZIP with correct content headers."""
    mocked_export_result = [
        ("metadata.yaml", lambda: "version: 1.0.0\ntype: SqlaTable\n"),
        ("datasets/example.yaml", lambda: "<DATASET CONTENTS>"),
    ]

    ExportDatasetsCommand = mocker.patch(  # noqa: N806
        "superset.datasets.api.ExportDatasetsCommand"
    )
    ExportDatasetsCommand().run.return_value = mocked_export_result[:]

    response = client.get("/api/v1/dataset/export/?q=[1]")
    assert response.status_code == 200
    assert response.content_type == "application/zip"
    assert "attachment" in response.headers.get("Content-Disposition", "")
    assert is_zipfile(BytesIO(response.data))
    assert response.headers["Cache-Control"] == "no-store"


def test_dataset_export_cache_header_with_token_param(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """Cache-Control: no-store must be present with a download token."""
    mocked_export_result = [
        ("metadata.yaml", lambda: "version: 1.0.0\ntype: SqlaTable\n"),
        ("datasets/example.yaml", lambda: "<DATASET CONTENTS>"),
    ]

    ExportDatasetsCommand = mocker.patch(  # noqa: N806
        "superset.datasets.api.ExportDatasetsCommand"
    )
    ExportDatasetsCommand().run.return_value = mocked_export_result[:]

    response = client.get("/api/v1/dataset/export/?q=[1]&token=ds_token_42")
    assert response.status_code == 200
    assert response.headers["Cache-Control"] == "no-store"


def test_dataset_export_does_not_contain_max_age(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """Dataset export must not have max-age in Cache-Control."""
    mocked_export_result = [
        ("metadata.yaml", lambda: "version: 1.0.0\ntype: SqlaTable\n"),
        ("datasets/example.yaml", lambda: "<DATASET CONTENTS>"),
    ]

    ExportDatasetsCommand = mocker.patch(  # noqa: N806
        "superset.datasets.api.ExportDatasetsCommand"
    )
    ExportDatasetsCommand().run.return_value = mocked_export_result[:]

    response = client.get("/api/v1/dataset/export/?q=[1]")
    assert response.status_code == 200
    cache_control = response.headers["Cache-Control"]
    assert "max-age" not in cache_control


# ---------------------------------------------------------------------------
# Assets export (importexport)
# ---------------------------------------------------------------------------


def test_assets_export_has_no_store_cache_header(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """Export assets response must include Cache-Control: no-store."""
    mocked_export_result = [
        ("metadata.yaml", lambda: "version: 1.0.0\ntype: assets\n"),
        ("databases/example.yaml", lambda: "<DATABASE CONTENTS>"),
    ]

    ExportAssetsCommand = mocker.patch(  # noqa: N806
        "superset.importexport.api.ExportAssetsCommand"
    )
    ExportAssetsCommand().run.return_value = mocked_export_result[:]

    response = client.get("/api/v1/assets/export/")
    assert response.status_code == 200
    assert response.headers["Cache-Control"] == "no-store"


def test_assets_export_response_is_valid_zip_attachment(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """Export assets must return a ZIP with correct content headers."""
    mocked_export_result = [
        ("metadata.yaml", lambda: "version: 1.0.0\ntype: assets\n"),
        ("databases/example.yaml", lambda: "<DATABASE CONTENTS>"),
    ]

    ExportAssetsCommand = mocker.patch(  # noqa: N806
        "superset.importexport.api.ExportAssetsCommand"
    )
    ExportAssetsCommand().run.return_value = mocked_export_result[:]

    response = client.get("/api/v1/assets/export/")
    assert response.status_code == 200
    assert response.content_type == "application/zip"
    assert "attachment" in response.headers.get("Content-Disposition", "")
    assert is_zipfile(BytesIO(response.data))
    assert response.headers["Cache-Control"] == "no-store"


def test_assets_export_does_not_contain_max_age(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """Assets export must not have max-age in Cache-Control."""
    mocked_export_result = [
        ("metadata.yaml", lambda: "version: 1.0.0\ntype: assets\n"),
        ("databases/example.yaml", lambda: "<DATABASE CONTENTS>"),
    ]

    ExportAssetsCommand = mocker.patch(  # noqa: N806
        "superset.importexport.api.ExportAssetsCommand"
    )
    ExportAssetsCommand().run.return_value = mocked_export_result[:]

    response = client.get("/api/v1/assets/export/")
    assert response.status_code == 200
    cache_control = response.headers["Cache-Control"]
    assert "max-age" not in cache_control


# ---------------------------------------------------------------------------
# Cross-cutting: verify SEND_FILE_MAX_AGE_DEFAULT is overridden
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "app",
    [{"SEND_FILE_MAX_AGE_DEFAULT": 31536000}],
    indirect=True,
)
def test_chart_export_overrides_send_file_max_age_default(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """Even with SEND_FILE_MAX_AGE_DEFAULT=1year, export must use no-store."""
    mocked_export_result = [
        ("metadata.yaml", lambda: "version: 1.0.0\ntype: Slice\n"),
        ("charts/example.yaml", lambda: "<CHART CONTENTS>"),
    ]

    ExportChartsCommand = mocker.patch(  # noqa: N806
        "superset.charts.api.ExportChartsCommand"
    )
    ExportChartsCommand().run.return_value = mocked_export_result[:]

    response = client.get("/api/v1/chart/export/?q=[1]")
    assert response.status_code == 200
    assert response.headers["Cache-Control"] == "no-store"
    assert "31536000" not in response.headers.get("Cache-Control", "")


@pytest.mark.parametrize(
    "app",
    [{"SEND_FILE_MAX_AGE_DEFAULT": 31536000}],
    indirect=True,
)
def test_dashboard_export_overrides_send_file_max_age_default(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """Even with SEND_FILE_MAX_AGE_DEFAULT=1year, export must use no-store."""
    mocked_export_result = [
        ("metadata.yaml", lambda: "version: 1.0.0\ntype: Dashboard\n"),
        ("dashboards/example.yaml", lambda: "<DASHBOARD CONTENTS>"),
    ]

    ExportDashboardsCommand = mocker.patch(  # noqa: N806
        "superset.dashboards.api.ExportDashboardsCommand"
    )
    ExportDashboardsCommand().run.return_value = mocked_export_result[:]

    response = client.get("/api/v1/dashboard/export/?q=[1]")
    assert response.status_code == 200
    assert response.headers["Cache-Control"] == "no-store"
    assert "31536000" not in response.headers.get("Cache-Control", "")


@pytest.mark.parametrize(
    "app",
    [{"SEND_FILE_MAX_AGE_DEFAULT": 31536000}],
    indirect=True,
)
def test_dataset_export_overrides_send_file_max_age_default(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """Even with SEND_FILE_MAX_AGE_DEFAULT=1year, export must use no-store."""
    mocked_export_result = [
        ("metadata.yaml", lambda: "version: 1.0.0\ntype: SqlaTable\n"),
        ("datasets/example.yaml", lambda: "<DATASET CONTENTS>"),
    ]

    ExportDatasetsCommand = mocker.patch(  # noqa: N806
        "superset.datasets.api.ExportDatasetsCommand"
    )
    ExportDatasetsCommand().run.return_value = mocked_export_result[:]

    response = client.get("/api/v1/dataset/export/?q=[1]")
    assert response.status_code == 200
    assert response.headers["Cache-Control"] == "no-store"
    assert "31536000" not in response.headers.get("Cache-Control", "")


@pytest.mark.parametrize(
    "app",
    [{"SEND_FILE_MAX_AGE_DEFAULT": 31536000}],
    indirect=True,
)
def test_assets_export_overrides_send_file_max_age_default(
    mocker: MockerFixture,
    client: Any,
    full_api_access: None,
) -> None:
    """Even with SEND_FILE_MAX_AGE_DEFAULT=1year, export must use no-store."""
    mocked_export_result = [
        ("metadata.yaml", lambda: "version: 1.0.0\ntype: assets\n"),
        ("databases/example.yaml", lambda: "<DATABASE CONTENTS>"),
    ]

    ExportAssetsCommand = mocker.patch(  # noqa: N806
        "superset.importexport.api.ExportAssetsCommand"
    )
    ExportAssetsCommand().run.return_value = mocked_export_result[:]

    response = client.get("/api/v1/assets/export/")
    assert response.status_code == 200
    assert response.headers["Cache-Control"] == "no-store"
    assert "31536000" not in response.headers.get("Cache-Control", "")
