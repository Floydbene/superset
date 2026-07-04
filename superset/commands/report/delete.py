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
from superset import security_manager
from superset.commands.base import BaseBulkDeleteCommand
from superset.commands.report.exceptions import (
    ReportScheduleDeleteFailedError,
    ReportScheduleForbiddenError,
    ReportScheduleNotFoundError,
)
from superset.daos.report import ReportScheduleDAO
from superset.exceptions import SupersetSecurityException


class DeleteReportScheduleCommand(BaseBulkDeleteCommand):
    dao = ReportScheduleDAO
    not_found = ReportScheduleNotFoundError
    delete_failed = ReportScheduleDeleteFailedError

    def _extra_validate(self) -> None:
        for model in self._models:
            try:
                security_manager.raise_for_ownership(model)
            except SupersetSecurityException as ex:
                raise ReportScheduleForbiddenError() from ex
