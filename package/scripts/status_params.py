# coding=utf8
# Copyright © 2015-2016 Cask Data, Inc.
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

from resource_management import *

# config object that holds the configurations declared in the -config.xml file
config = Script.get_config()

cdap_user = config['configurations']['cdap-env']['cdap_user']
pid_dir = config['configurations']['cdap-env']['cdap_pid_dir']

cdap_auth_pid_file = pid_dir + '/auth-server-' + cdap_user + '.pid'
cdap_master_pid_file = pid_dir + '/master-' + cdap_user + '.pid'
cdap_router_pid_file = pid_dir + '/router-' + cdap_user + '.pid'
cdap_ui_pid_file = pid_dir + '/ui-' + cdap_user + '.pid'
