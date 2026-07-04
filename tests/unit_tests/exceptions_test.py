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

from collections import defaultdict

from marshmallow import ValidationError

from superset.errors import ErrorLevel, SupersetError, SupersetErrorType
from superset.exceptions import (
    CertificateException,
    InvalidPayloadFormatError,
    InvalidPayloadSchemaError,
    OAuth2Error,
    OAuth2RedirectError,
    OAuth2TokenRefreshError,
    SupersetDisallowedSQLFunctionException,
    SupersetDisallowedSQLTableException,
    SupersetDMLNotAllowedException,
    SupersetErrorException,
    SupersetErrorFromParamsException,
    SupersetErrorsException,
    SupersetException,
    SupersetGenericDBErrorException,
    SupersetGenericErrorException,
    SupersetInvalidCTASException,
    SupersetInvalidCVASException,
    SupersetMarshmallowValidationError,
    SupersetParseError,
    SupersetResultsBackendNotConfigureException,
    SupersetSecurityException,
    SupersetSyntaxErrorException,
    SupersetTimeoutException,
)


def test_superset_exception_default():
    exc = SupersetException()
    assert exc.status == 500
    assert str(exc) == ""
    assert exc.exception is None
    assert exc.error_type is None


def test_superset_exception_with_message():
    exc = SupersetException("Something went wrong")
    assert exc.message == "Something went wrong"
    assert str(exc) == "Something went wrong"


def test_superset_exception_with_nested_exception():
    inner = ValueError("inner error")
    exc = SupersetException("outer", exception=inner)
    assert exc.exception is inner


def test_superset_exception_with_error_type():
    exc = SupersetException("msg", error_type=SupersetErrorType.GENERIC_BACKEND_ERROR)
    assert exc.error_type == SupersetErrorType.GENERIC_BACKEND_ERROR


def test_superset_exception_to_dict():
    exc = SupersetException("test message")
    d = exc.to_dict()
    assert d["message"] == "test message"


def test_superset_exception_to_dict_with_error_type():
    exc = SupersetException("msg", error_type=SupersetErrorType.GENERIC_BACKEND_ERROR)
    d = exc.to_dict()
    assert d["error_type"] == SupersetErrorType.GENERIC_BACKEND_ERROR


def test_superset_error_exception():
    error = SupersetError(
        message="error msg",
        error_type=SupersetErrorType.GENERIC_DB_ENGINE_ERROR,
        level=ErrorLevel.ERROR,
    )
    exc = SupersetErrorException(error)
    assert exc.error is error
    assert exc.status == 500
    assert str(exc) == "error msg"


def test_superset_error_exception_custom_status():
    error = SupersetError(
        message="not found",
        error_type=SupersetErrorType.OBJECT_DOES_NOT_EXIST_ERROR,
        level=ErrorLevel.ERROR,
    )
    exc = SupersetErrorException(error, status=404)
    assert exc.status == 404


def test_superset_error_exception_to_dict():
    error = SupersetError(
        message="err",
        error_type=SupersetErrorType.FRONTEND_CSRF_ERROR,
        level=ErrorLevel.ERROR,
    )
    exc = SupersetErrorException(error)
    d = exc.to_dict()
    assert d["message"] == "err"
    assert d["error_type"] == "FRONTEND_CSRF_ERROR"


def test_superset_generic_error_exception():
    exc = SupersetGenericErrorException("generic error")
    assert exc.error.error_type == SupersetErrorType.GENERIC_BACKEND_ERROR
    assert exc.error.level == ErrorLevel.ERROR
    assert str(exc) == "generic error"


def test_superset_generic_error_exception_custom_status():
    exc = SupersetGenericErrorException("error", status=503)
    assert exc.status == 503


def test_superset_error_from_params_exception():
    exc = SupersetErrorFromParamsException(
        error_type=SupersetErrorType.SYNTAX_ERROR,
        message="syntax issue",
        level=ErrorLevel.WARNING,
        extra={"hint": "check SQL"},
    )
    assert exc.error.error_type == SupersetErrorType.SYNTAX_ERROR
    assert exc.error.message == "syntax issue"
    assert exc.error.level == ErrorLevel.WARNING


def test_superset_errors_exception():
    errors = [
        SupersetError(
            message="e1",
            error_type=SupersetErrorType.SYNTAX_ERROR,
            level=ErrorLevel.ERROR,
        ),
        SupersetError(
            message="e2",
            error_type=SupersetErrorType.GENERIC_DB_ENGINE_ERROR,
            level=ErrorLevel.ERROR,
        ),
    ]
    exc = SupersetErrorsException(errors)
    assert exc.errors == errors
    assert exc.status == 500


def test_superset_errors_exception_custom_status():
    exc = SupersetErrorsException([], status=422)
    assert exc.status == 422


def test_superset_syntax_error_exception():
    errors = [
        SupersetError(
            message="syntax",
            error_type=SupersetErrorType.SYNTAX_ERROR,
            level=ErrorLevel.ERROR,
        )
    ]
    exc = SupersetSyntaxErrorException(errors)
    assert exc.status == 422


def test_superset_timeout_exception():
    exc = SupersetTimeoutException(
        error_type=SupersetErrorType.BACKEND_TIMEOUT_ERROR,
        message="timed out",
        level=ErrorLevel.ERROR,
    )
    assert exc.status == 408


def test_superset_generic_db_error_exception():
    exc = SupersetGenericDBErrorException("db error")
    assert exc.status == 400
    assert exc.error.error_type == SupersetErrorType.GENERIC_DB_ENGINE_ERROR


def test_superset_generic_db_error_exception_with_extra():
    exc = SupersetGenericDBErrorException("db error", extra={"sql": "SELECT 1"})
    assert exc.error.extra is not None


def test_superset_security_exception():
    error = SupersetError(
        message="access denied",
        error_type=SupersetErrorType.TABLE_SECURITY_ACCESS_ERROR,
        level=ErrorLevel.ERROR,
    )
    exc = SupersetSecurityException(error, payload={"dashboard_id": 1})
    assert exc.status == 403
    assert exc.payload == {"dashboard_id": 1}


def test_certificate_exception():
    exc = CertificateException()
    assert exc.status == 500


def test_invalid_payload_format_error():
    exc = InvalidPayloadFormatError()
    assert exc.status == 400
    assert exc.error.error_type == SupersetErrorType.INVALID_PAYLOAD_FORMAT_ERROR


def test_invalid_payload_format_error_custom_message():
    exc = InvalidPayloadFormatError("Custom format error")
    assert exc.error.message == "Custom format error"


def test_invalid_payload_schema_error():
    validation_err = ValidationError({"field": ["required"]})
    exc = InvalidPayloadSchemaError(validation_err)
    assert exc.status == 422
    assert exc.error.error_type == SupersetErrorType.INVALID_PAYLOAD_SCHEMA_ERROR
    assert exc.error.extra is not None
    assert "messages" in exc.error.extra


def test_invalid_payload_schema_error_with_defaultdict():
    messages = {"field": defaultdict(list, {"nested": ["error"]})}
    validation_err = ValidationError(messages)
    exc = InvalidPayloadSchemaError(validation_err)
    assert isinstance(exc.error.extra["messages"]["field"], dict)


def test_superset_marshmallow_validation_error():
    validation_err = ValidationError({"name": ["Missing field"]})
    exc = SupersetMarshmallowValidationError(validation_err, payload={"data": "test"})
    assert exc.status == 422
    assert exc.error.error_type == SupersetErrorType.MARSHMALLOW_ERROR
    assert exc.error.extra["payload"] == {"data": "test"}


def test_superset_parse_error_default_message():
    exc = SupersetParseError(sql="SELECT * FORM table")
    assert exc.status == 422
    assert exc.error.error_type == SupersetErrorType.INVALID_SQL_ERROR
    assert exc.error.extra["sql"] == "SELECT * FORM table"


def test_superset_parse_error_with_highlight_and_position():
    exc = SupersetParseError(
        sql="SELECT * FORM t",
        engine="postgresql",
        highlight="FORM",
        line=1,
        column=10,
    )
    assert "FORM" in str(exc)
    assert exc.error.extra["engine"] == "postgresql"
    assert exc.error.extra["line"] == 1
    assert exc.error.extra["column"] == 10


def test_superset_parse_error_custom_message():
    exc = SupersetParseError(sql="bad sql", message="Custom parse error")
    assert str(exc) == "Custom parse error"


def test_oauth2_redirect_error():
    exc = OAuth2RedirectError(
        url="https://auth.example.com",
        tab_id="tab-123",
        redirect_uri="https://superset.example.com/callback",
    )
    assert exc.status == 403
    assert exc.error.error_type == SupersetErrorType.OAUTH2_REDIRECT
    assert exc.error.extra["url"] == "https://auth.example.com"
    assert exc.error.extra["tab_id"] == "tab-123"


def test_oauth2_token_refresh_error():
    exc = OAuth2TokenRefreshError("Token expired")
    assert exc.error.error_type == SupersetErrorType.OAUTH2_REDIRECT
    assert exc.error.extra["error"] == "Token expired"
    assert isinstance(exc, OAuth2RedirectError)


def test_oauth2_error():
    exc = OAuth2Error("something broke")
    assert exc.error.error_type == SupersetErrorType.OAUTH2_REDIRECT_ERROR
    assert exc.error.extra["error"] == "something broke"


def test_superset_disallowed_sql_function():
    exc = SupersetDisallowedSQLFunctionException({"SLEEP", "BENCHMARK"})
    assert exc.error.error_type == SupersetErrorType.SYNTAX_ERROR


def test_superset_disallowed_sql_table():
    exc = SupersetDisallowedSQLTableException({"pg_catalog", "information_schema"})
    assert exc.error.error_type == SupersetErrorType.SYNTAX_ERROR


def test_superset_dml_not_allowed():
    exc = SupersetDMLNotAllowedException()
    assert exc.error.error_type == SupersetErrorType.DML_NOT_ALLOWED_ERROR


def test_superset_invalid_ctas():
    exc = SupersetInvalidCTASException()
    assert exc.error.error_type == SupersetErrorType.INVALID_CTAS_QUERY_ERROR


def test_superset_invalid_cvas():
    exc = SupersetInvalidCVASException()
    assert exc.error.error_type == SupersetErrorType.INVALID_CVAS_QUERY_ERROR


def test_superset_results_backend_not_configured():
    exc = SupersetResultsBackendNotConfigureException()
    assert (
        exc.error.error_type == SupersetErrorType.RESULTS_BACKEND_NOT_CONFIGURED_ERROR
    )


def test_all_exceptions_are_catchable_as_superset_exception():
    error = SupersetError(
        message="e",
        error_type=SupersetErrorType.GENERIC_BACKEND_ERROR,
        level=ErrorLevel.ERROR,
    )
    exception_instances = [
        SupersetException("test"),
        SupersetErrorException(error),
        SupersetGenericErrorException("test"),
        SupersetGenericDBErrorException("test"),
        SupersetSecurityException(error),
    ]
    for exc in exception_instances:
        assert isinstance(exc, SupersetException)
