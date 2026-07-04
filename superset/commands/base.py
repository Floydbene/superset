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
from abc import ABC, abstractmethod
from functools import partial
from typing import Any, Optional

from flask_appbuilder import Model
from flask_appbuilder.security.sqla.models import User

from superset.commands.utils import compute_owner_list, populate_owner_list

logger = logging.getLogger(__name__)


class BaseCommand(ABC):
    """
    Base class for all Command like Superset Logic objects
    """

    @abstractmethod
    def run(self) -> Any:
        """
        Run executes the command. Can raise command exceptions
        :raises: CommandException
        """

    @abstractmethod
    def validate(self) -> None:
        """
        Validate is normally called by run to validate data.
        Will raise exception if validation fails
        :raises: CommandException
        """


class BaseBulkDeleteCommand(BaseCommand):
    """Shared base for commands that delete one or more models by ID.

    Subclasses set class-level attributes and optionally override
    ``_extra_validate`` to add domain-specific checks (e.g. ownership,
    associated reports).

    Required class attributes::

        dao            – the DAO class used to look up and delete models
        not_found      – exception class raised when IDs are missing
        delete_failed  – exception class used as the ``@transaction`` reraise
    """

    from superset.commands.exceptions import CommandException
    from superset.daos.base import BaseDAO

    dao: type[BaseDAO[Model]]
    not_found: type[CommandException]
    delete_failed: type[CommandException]

    def __init__(self, model_ids: list[int]) -> None:
        self._model_ids = model_ids
        self._models: list[Model] = []

    def run(self) -> None:
        from superset.utils.decorators import on_error, transaction

        @transaction(on_error=partial(on_error, reraise=self.delete_failed))
        def _run(cmd: "BaseBulkDeleteCommand") -> None:
            cmd.validate()
            cmd.dao.delete(cmd._models)

        _run(self)

    def validate(self) -> None:
        self._models = self.dao.find_by_ids(self._model_ids)
        if not self._models or len(self._models) != len(self._model_ids):
            raise self.not_found()
        self._extra_validate()

    def _extra_validate(self) -> None:
        """Override in subclasses for additional validation (ownership, etc.)."""


class CreateMixin:  # pylint: disable=too-few-public-methods
    @staticmethod
    def populate_owners(owner_ids: Optional[list[int]] = None) -> list[User]:
        """
        Populate list of owners, defaulting to the current user if `owner_ids` is
        undefined or empty. If current user is missing in `owner_ids`, current user
        is added unless belonging to the Admin role.

        :param owner_ids: list of owners by id's
        :raises OwnersNotFoundValidationError: if at least one owner can't be resolved
        :returns: Final list of owners
        """
        return populate_owner_list(owner_ids, default_to_user=True)


class UpdateMixin:
    @staticmethod
    def populate_owners(owner_ids: Optional[list[int]] = None) -> list[User]:
        """
        Populate list of owners. If current user is missing in `owner_ids`, current user
        is added unless belonging to the Admin role.

        :param owner_ids: list of owners by id's
        :raises OwnersNotFoundValidationError: if at least one owner can't be resolved
        :returns: Final list of owners
        """
        return populate_owner_list(owner_ids, default_to_user=False)

    @staticmethod
    def compute_owners(
        current_owners: Optional[list[User]],
        new_owners: Optional[list[int]],
    ) -> list[User]:
        """
        Handle list of owners for update events.

        :param current_owners: list of current owners
        :param new_owners: list of new owners specified in the update payload
        :returns: Final list of owners
        """
        return compute_owner_list(current_owners, new_owners)
