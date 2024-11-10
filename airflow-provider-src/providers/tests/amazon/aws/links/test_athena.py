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
from __future__ import annotations

from airflow.providers.amazon.aws.links.athena import AthenaQueryResultsLink

from providers.tests.amazon.aws.links.test_base_aws import BaseAwsLinksTestCase


class TestAthenaQueryResultsLink(BaseAwsLinksTestCase):
    link_class = AthenaQueryResultsLink

    def test_extra_link(self):
        self.assert_extra_link_url(
            expected_url=(
                "https://console.aws.amazon.com/athena/home"
                "?region=eu-west-1#/query-editor/history/00000000-0000-0000-0000-000000000000"
            ),
            region_name="eu-west-1",
            aws_partition="aws",
            query_execution_id="00000000-0000-0000-0000-000000000000",
        )
