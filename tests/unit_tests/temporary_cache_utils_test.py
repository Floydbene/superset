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

from superset.temporary_cache.utils import cache_key, SEPARATOR


def test_cache_key_single_arg():
    assert cache_key("abc") == "abc"


def test_cache_key_multiple_args():
    assert cache_key("a", "b", "c") == "a;b;c"


def test_cache_key_numeric_args():
    assert cache_key(1, 2, 3) == "1;2;3"


def test_cache_key_mixed_types():
    assert cache_key("dashboard", 42, True) == "dashboard;42;True"


def test_cache_key_empty():
    assert cache_key() == ""


def test_separator_value():
    assert SEPARATOR == ";"
