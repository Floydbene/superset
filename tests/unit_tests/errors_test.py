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

from superset.errors import (
    ERROR_TYPES_TO_ISSUE_CODES_MAPPING,
    ErrorLevel,
    ISSUE_CODES,
    SupersetError,
    SupersetErrorType,
)


def test_superset_error_type_values():
    assert SupersetErrorType.FRONTEND_CSRF_ERROR == "FRONTEND_CSRF_ERROR"
    assert SupersetErrorType.GENERIC_DB_ENGINE_ERROR == "GENERIC_DB_ENGINE_ERROR"
    assert SupersetErrorType.SYNTAX_ERROR == "SYNTAX_ERROR"
    assert SupersetErrorType.GENERIC_BACKEND_ERROR == "GENERIC_BACKEND_ERROR"


def test_superset_error_type_is_str():
    assert isinstance(SupersetErrorType.FRONTEND_CSRF_ERROR, str)


def test_error_level_values():
    assert ErrorLevel.INFO == "info"
    assert ErrorLevel.WARNING == "warning"
    assert ErrorLevel.ERROR == "error"


def test_superset_error_basic():
    error = SupersetError(
        message="Test error",
        error_type=SupersetErrorType.FRONTEND_CSRF_ERROR,
        level=ErrorLevel.ERROR,
    )
    assert error.message == "Test error"
    assert error.error_type == SupersetErrorType.FRONTEND_CSRF_ERROR
    assert error.level == ErrorLevel.ERROR
    assert error.extra is None


def test_superset_error_with_extra():
    extra = {"key": "value"}
    error = SupersetError(
        message="Test error",
        error_type=SupersetErrorType.FRONTEND_CSRF_ERROR,
        level=ErrorLevel.WARNING,
        extra=extra,
    )
    assert error.extra is not None
    assert error.extra["key"] == "value"


def test_superset_error_post_init_adds_issue_codes():
    error = SupersetError(
        message="DB error",
        error_type=SupersetErrorType.GENERIC_DB_ENGINE_ERROR,
        level=ErrorLevel.ERROR,
    )
    assert error.extra is not None
    assert "issue_codes" in error.extra
    issue_codes = error.extra["issue_codes"]
    assert len(issue_codes) == 1
    assert issue_codes[0]["code"] == 1002


def test_superset_error_post_init_preserves_existing_extra():
    error = SupersetError(
        message="DB error",
        error_type=SupersetErrorType.GENERIC_DB_ENGINE_ERROR,
        level=ErrorLevel.ERROR,
        extra={"existing_key": "existing_value"},
    )
    assert error.extra is not None
    assert error.extra["existing_key"] == "existing_value"
    assert "issue_codes" in error.extra


def test_superset_error_post_init_no_issue_codes_for_unmapped_type():
    error = SupersetError(
        message="CSRF error",
        error_type=SupersetErrorType.FRONTEND_CSRF_ERROR,
        level=ErrorLevel.ERROR,
    )
    assert error.extra is None


def test_superset_error_post_init_multiple_issue_codes():
    error = SupersetError(
        message="Timeout",
        error_type=SupersetErrorType.BACKEND_TIMEOUT_ERROR,
        level=ErrorLevel.ERROR,
    )
    assert error.extra is not None
    issue_codes = error.extra["issue_codes"]
    assert len(issue_codes) == 2
    codes = [ic["code"] for ic in issue_codes]
    assert 1000 in codes
    assert 1001 in codes


def test_superset_error_to_dict_basic():
    error = SupersetError(
        message="Test",
        error_type=SupersetErrorType.FRONTEND_CSRF_ERROR,
        level=ErrorLevel.INFO,
    )
    d = error.to_dict()
    assert d["message"] == "Test"
    assert d["error_type"] == "FRONTEND_CSRF_ERROR"
    assert "extra" not in d


def test_superset_error_to_dict_with_extra():
    error = SupersetError(
        message="Test",
        error_type=SupersetErrorType.GENERIC_DB_ENGINE_ERROR,
        level=ErrorLevel.ERROR,
        extra={"detail": "some detail"},
    )
    d = error.to_dict()
    assert "extra" in d
    assert d["extra"]["detail"] == "some detail"
    assert "issue_codes" in d["extra"]


def test_issue_codes_are_complete():
    for error_type, codes in ERROR_TYPES_TO_ISSUE_CODES_MAPPING.items():
        for code in codes:
            assert code in ISSUE_CODES, (
                f"Issue code {code} referenced by {error_type} not in ISSUE_CODES"
            )


def test_error_types_to_issue_codes_mapping_keys_are_valid():
    for error_type in ERROR_TYPES_TO_ISSUE_CODES_MAPPING:
        assert isinstance(error_type, SupersetErrorType)
