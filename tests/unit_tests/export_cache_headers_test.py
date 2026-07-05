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

from typing import Any

from pytest_mock import MockerFixture


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
