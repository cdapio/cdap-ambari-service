# coding=utf8
# Copyright © 2016-2017 Cask Data, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

import logging

from resource_management import *

RESULT_STATE_OK = 'OK'
RESULT_STATE_CRITICAL = 'CRITICAL'
RESULT_STATE_UNKNOWN = 'UNKNOWN'

LOGGER_EXCEPTION_MESSAGE = "[Alert] CDAP UI Health on {0} fails:"
logger = logging.getLogger('ambari_alerts')


def execute(configurations={}, parameters={}, host_name=None):
    if configurations is None:
        return (RESULT_STATE_UNKNOWN, ['There were no configurations supplied to the script.'])
    try:
        check_cmd = format('service cdap-ui status')
        Execute(check_cmd, timeout=5)
        return(RESULT_STATE_OK, ['UI OK - CDAP UI is running'])
    except:
        return(RESULT_STATE_CRITICAL, [LOGGER_EXCEPTION_MESSAGE])
