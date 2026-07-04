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

from superset.constants import (
    CACHE_DISABLED_TIMEOUT,
    CacheRegion,
    EXTRA_FORM_DATA_APPEND_KEYS,
    EXTRA_FORM_DATA_OVERRIDE_KEYS,
    EXTRA_FORM_DATA_OVERRIDE_REGULAR_MAPPINGS,
    InstantTimeComparison,
    MODEL_API_RW_METHOD_PERMISSION_MAP,
    MODEL_VIEW_RW_METHOD_PERMISSION_MAP,
    NO_TIME_RANGE,
    NULL_STRING,
    PandasAxis,
    PandasPostprocessingCompare,
    PASSWORD_MASK,
    RouteMethod,
    TimeGrain,
)


def test_null_string():
    assert NULL_STRING == "<NULL>"


def test_password_mask():
    assert PASSWORD_MASK == "X" * 10


def test_no_time_range():
    assert NO_TIME_RANGE == "No filter"


def test_cache_disabled_timeout():
    assert CACHE_DISABLED_TIMEOUT == -1


def test_instant_time_comparison_values():
    assert InstantTimeComparison.INHERITED == "r"
    assert InstantTimeComparison.YEAR == "y"
    assert InstantTimeComparison.MONTH == "m"
    assert InstantTimeComparison.WEEK == "w"


def test_route_method_api_set():
    assert RouteMethod.API_CREATE in RouteMethod.API_SET
    assert RouteMethod.API_DELETE in RouteMethod.API_SET
    assert RouteMethod.API_GET in RouteMethod.API_SET
    assert RouteMethod.API_READ in RouteMethod.API_SET
    assert RouteMethod.API_UPDATE in RouteMethod.API_SET


def test_route_method_crud_set():
    assert RouteMethod.ADD in RouteMethod.CRUD_SET
    assert RouteMethod.LIST in RouteMethod.CRUD_SET
    assert RouteMethod.EDIT in RouteMethod.CRUD_SET
    assert RouteMethod.DELETE in RouteMethod.CRUD_SET


def test_route_method_rest_model_view_crud_set():
    assert RouteMethod.GET in RouteMethod.REST_MODEL_VIEW_CRUD_SET
    assert RouteMethod.GET_LIST in RouteMethod.REST_MODEL_VIEW_CRUD_SET
    assert RouteMethod.POST in RouteMethod.REST_MODEL_VIEW_CRUD_SET
    assert RouteMethod.PUT in RouteMethod.REST_MODEL_VIEW_CRUD_SET


def test_model_view_rw_permission_map_read_methods():
    read_methods = [
        k for k, v in MODEL_VIEW_RW_METHOD_PERMISSION_MAP.items() if v == "read"
    ]
    assert "list" in read_methods
    assert "show" in read_methods
    assert "api_get" in read_methods


def test_model_view_rw_permission_map_write_methods():
    write_methods = [
        k for k, v in MODEL_VIEW_RW_METHOD_PERMISSION_MAP.items() if v == "write"
    ]
    assert "add" in write_methods
    assert "edit" in write_methods
    assert "delete" in write_methods


def test_model_api_rw_permission_map_operations():
    assert MODEL_API_RW_METHOD_PERMISSION_MAP["get"] == "read"
    assert MODEL_API_RW_METHOD_PERMISSION_MAP["get_list"] == "read"
    assert MODEL_API_RW_METHOD_PERMISSION_MAP["post"] == "write"
    assert MODEL_API_RW_METHOD_PERMISSION_MAP["put"] == "write"
    assert MODEL_API_RW_METHOD_PERMISSION_MAP["delete"] == "write"


def test_extra_form_data_append_keys():
    assert "adhoc_filters" in EXTRA_FORM_DATA_APPEND_KEYS
    assert "filters" in EXTRA_FORM_DATA_APPEND_KEYS
    assert "interactive_groupby" in EXTRA_FORM_DATA_APPEND_KEYS


def test_extra_form_data_override_regular_mappings():
    assert "granularity_sqla" in EXTRA_FORM_DATA_OVERRIDE_REGULAR_MAPPINGS
    assert (
        EXTRA_FORM_DATA_OVERRIDE_REGULAR_MAPPINGS["granularity_sqla"] == "granularity"
    )


def test_extra_form_data_override_keys_include_both_sources():
    assert "granularity" in EXTRA_FORM_DATA_OVERRIDE_KEYS
    assert "relative_start" in EXTRA_FORM_DATA_OVERRIDE_KEYS
    assert "relative_end" in EXTRA_FORM_DATA_OVERRIDE_KEYS


def test_time_grain_values():
    assert TimeGrain.SECOND == "PT1S"
    assert TimeGrain.MINUTE == "PT1M"
    assert TimeGrain.HOUR == "PT1H"
    assert TimeGrain.DAY == "P1D"
    assert TimeGrain.WEEK == "P1W"
    assert TimeGrain.MONTH == "P1M"
    assert TimeGrain.QUARTER == "P3M"
    assert TimeGrain.YEAR == "P1Y"


def test_pandas_axis_values():
    assert PandasAxis.ROW == 0
    assert PandasAxis.COLUMN == 1


def test_pandas_postprocessing_compare_values():
    assert PandasPostprocessingCompare.DIFF == "difference"
    assert PandasPostprocessingCompare.PCT == "percentage"
    assert PandasPostprocessingCompare.RAT == "ratio"


def test_cache_region_values():
    assert CacheRegion.DEFAULT == "default"
    assert CacheRegion.DATA == "data"
    assert CacheRegion.THUMBNAIL == "thumbnail"
