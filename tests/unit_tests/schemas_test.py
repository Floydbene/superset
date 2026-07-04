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

from superset.errors import SupersetErrorType
from superset.schemas import error_payload_content


def test_error_payload_content_structure():
    schema = error_payload_content["application/json"]["schema"]
    assert schema["type"] == "object"
    assert "errors" in schema["properties"]
    assert "message" in schema["properties"]


def test_error_payload_errors_array():
    errors_prop = error_payload_content["application/json"]["schema"]["properties"][
        "errors"
    ]
    assert errors_prop["type"] == "array"
    item_props = errors_prop["items"]["properties"]
    assert "message" in item_props
    assert "error_type" in item_props
    assert "level" in item_props
    assert "extra" in item_props


def test_error_payload_error_type_enum():
    error_type_enum = error_payload_content["application/json"]["schema"]["properties"][
        "errors"
    ]["items"]["properties"]["error_type"]["enum"]
    assert "GENERIC_DB_ENGINE_ERROR" in error_type_enum
    assert "FRONTEND_CSRF_ERROR" in error_type_enum
    assert len(error_type_enum) == len(SupersetErrorType)


def test_error_payload_level_enum():
    level_enum = error_payload_content["application/json"]["schema"]["properties"][
        "errors"
    ]["items"]["properties"]["level"]["enum"]
    assert level_enum == ["info", "warning", "error"]
