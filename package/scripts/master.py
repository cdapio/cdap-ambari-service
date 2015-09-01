import sys
import ambari_helpers as helpers
from resource_management import *

class Master(Script):
  def install(self, env):
    print 'Install the CDAP Master'
    import params
    # Add repository file
    helpers.add_repo(params.files_dir + params.repo_file, params.os_repo_dir)
    # Install any global packages
    self.install_packages(env)
    # Install package
    helpers.package('cdap-master')
    self.configure(env)

  def start(self, env):
    print 'Start the CDAP Master'
    import params
    import status_params
    env.set_params(params)
    self.configure(env)
    helpers.create_hdfs_dir(params.hdfs_namespace, params.hdfs_user, 755)
    # Hack to work around CDAP-1967
    self.remove_jackson(env)
    daemon_cmd = format('/opt/cdap/master/bin/svc-master start')
    no_op_test = format('ls {status_params.cdap_master_pid_file} >/dev/null 2>&1 && ps -p $(<{status_params.cdap_master_pid_file}) >/dev/null 2>&1')
    Execute( daemon_cmd,
             user=params.cdap_user,
             not_if=no_op_test
    )

  def stop(self, env):
    print 'Stop the CDAP Master'
    import params
    self.configure(env)
    Execute('service cdap-master stop')

  def status(self, env):
    import status_params
    check_process_status(status_params.cdap_master_pid_file)

  def configure(self, env):
    print 'Configure the CDAP Master'
    import params
    env.set_params(params)
    helpers.cdap_config('master')

  def remove_jackson(self, env):
    jackson_check = format('ls -1 /opt/cdap/master/lib/org.codehaus.jackson* 2>/dev/null')
    Execute( 'rm -f /opt/cdap/master/lib/org.codehaus.jackson.jackson-*',
             not_if=jackson_check
    )

if __name__ == "__main__":
  Master().execute()
