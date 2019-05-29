# coding=utf8
# Copyright © 2015-2017 Cask Data, Inc.
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

import ambari_helpers as helpers
from resource_management import *


class Master(Script):
    def install(self, env):
        print('Install the CDAP Master')
        import params
        # Add repository file
        helpers.add_repo(
            params.files_dir + params.repo_file,
            params.os_repo_dir
        )
        # Install any global packages
        self.install_packages(env)
        # Workaround for CDAP-3961
        helpers.package('cdap-hbase-compat-1.1')
        # Install package
        helpers.package('cdap-master')
        self.configure(env)

    def start(self, env, upgrade_type=None):
        print('Start the CDAP Master')
        import params
        import status_params
        env.set_params(params)
        self.configure(env)
        helpers.create_hdfs_dir(params.hdfs_namespace, params.cdap_hdfs_user, 775)
        # Create user's HDFS home
        helpers.create_hdfs_dir('/user/' + params.cdap_user, params.cdap_user, 775)
        if params.cdap_hdfs_user != params.cdap_user:
            helpers.create_hdfs_dir('/user/' + params.cdap_hdfs_user, params.cdap_hdfs_user, 775)

        # Hack to work around CDAP-1967
        self.remove_jackson(env)
        daemon_cmd = format('/opt/cdap/master/bin/cdap master start')
        no_op_test = format('ls {status_params.cdap_master_pid_file} >/dev/null 2>&1 && ps -p $(<{status_params.cdap_master_pid_file}) >/dev/null 2>&1')
        Execute(
            daemon_cmd,
            user=params.cdap_user,
            not_if=no_op_test
        )

    def stop(self, env, upgrade_type=None):
        print('Stop the CDAP Master')
        import status_params
        daemon_cmd = format('service cdap-master stop')
        no_op_test = format('ls {status_params.cdap_master_pid_file} >/dev/null 2>&1 && ps -p $(<{status_params.cdap_master_pid_file}) >/dev/null 2>&1')
        Execute(
            daemon_cmd,
            only_if=no_op_test
        )

    def status(self, env):
        import status_params
        check_process_status(status_params.cdap_master_pid_file)

    def configure(self, env):
        print('Configure the CDAP Master')
        import params
        env.set_params(params)
        helpers.cdap_config('master')

    def upgrade(self, env):
        self.run_class(
            env,
            classname='io.cdap.cdap.data.tools.UpgradeTool',
            label='CDAP Upgrade Tool',
            arguments='upgrade force'
        )

    def upgrade_hbase(self, env):
        self.run_class(
            env,
            classname='io.cdap.cdap.data.tools.UpgradeTool',
            label='CDAP HBase Coprocessor Upgrade Tool',
            arguments='upgrade_hbase force'
        )

    def postupgrade(self, env):
        self.run_class(
            env,
            classname='io.cdap.cdap.data.tools.flow.FlowQueuePendingCorrector',
            label='CDAP Post-Upgrade Tool'
        )

    def queue_debugger(self, env):
        self.run_class(
            env,
            classname='io.cdap.cdap.data.tools.SimpleHBaseQueueDebugger',
            label='CDAP Queue Debugger Tool'
        )

    def jobqueue_debugger(self, env):
        self.run_class(
            env,
            classname='io.cdap.cdap.data.tools.JobQueueDebugger',
            label='CDAP Job Queue Debugger Tool'
        )

    def run_class(self, env, classname, label=None, arguments=''):
        if label is None:
            label = classname
        print('Running: ' + label)
        import params
        cmd = format("/opt/cdap/master/bin/cdap run %s %s" % (classname, arguments))
        Execute(
            cmd,
            user=params.cdap_user
        )

    def remove_jackson(self, env):
        jackson_check = format('ls -1 /opt/cdap/master/lib/org.codehaus.jackson* 2>/dev/null')
        Execute(
            'rm -f /opt/cdap/master/lib/org.codehaus.jackson.jackson-*',
            not_if=jackson_check
        )

if __name__ == "__main__":
    Master().execute()
